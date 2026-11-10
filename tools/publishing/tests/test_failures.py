"""Isolated publishing failure contracts; no live services or routes."""
import hashlib, json, os, pathlib, shutil, subprocess, tempfile, unittest
SOURCE = pathlib.Path(__file__).resolve().parents[1]

class FailureContracts(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='publishing-regression-')
        self.addCleanup(self.temp.cleanup)
        self.base = pathlib.Path(self.temp.name)
        self.lib = self.base / 'lib'
        shutil.copytree(SOURCE, self.lib)
        self.root = self.base / 'store'
        self.records = self.root / 'state/previews'
        for directory in ['state/previews', 'staging', 'public', 'launches']:
            (self.root / directory).mkdir(parents=True)
        self.work = self.base / 'work'
        self.work.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.work)], check=True)
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        self.log = self.base / 'calls'
        mocks = {'hostname': 'echo "${MOCK_HOST:-home-lab}"', 'id': 'echo coder', 'tailscale': 'if [[ $1 == status ]]; then echo \'{"Self":{"DNSName":"mock.example.ts.net."}}\'; else echo \'{}\'; fi', 'ss': 'exit 0', 'sudo': 'echo sudo >> "$MOCK_LOG"; exit "${MOCK_SUDO_EXIT:-0}"', 'systemctl': 'echo systemctl "$@" >> "$MOCK_LOG"; if [[ $2 == is-active ]]; then exit 1; fi; if [[ $2 == start ]]; then exit "${MOCK_START_EXIT:-0}"; fi; exit 0', 'curl': 'exit "${MOCK_CURL_EXIT:-22}"', 'python3': 'case "$1" in */preview-check.py) exit "${MOCK_READY_EXIT:-0}";; */service-files.py) exit 0;; esac\nexec /usr/bin/python3 "$@"'}
        for name, body in mocks.items():
            path = self.bin / name
            path.write_text('#!/bin/bash\n' + body + '\n')
            path.chmod(493)
        self.env = dict(os.environ, HOME=str(self.base / 'home'), LAB_PUBLISH_ROOT=str(self.root), PATH=str(self.bin) + ':' + os.environ['PATH'], MOCK_LOG=str(self.log))

    def identifier(self, service='docs'):
        return hashlib.sha256((str(self.work) + '\x00' + service).encode()).hexdigest()[:20]

    def record(self, service='docs', **values):
        data = dict(id=self.identifier(service), unit='mock.service', external_port=8400, internal_port=20000, status='ready', health_path='/', host='mock.example.ts.net', url='https://mock.example.ts.net:8400/')
        data.update(values)
        path = self.records / (self.identifier(service) + '.json')
        path.write_text(json.dumps(data))
        return path

    def launch(self, service='docs', **env):
        return subprocess.run(['bash', str(self.lib / 'start-preview.sh'), str(self.work), service, '--', '/bin/true'], env=dict(self.env, **env), capture_output=True, text=True, timeout=110)

    def assert_registry_refused(self, result, before):
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual({p.name: p.read_bytes() for p in self.records.iterdir()}, before)
        self.assertFalse(self.log.exists(), 'must refuse before systemctl or sudo')
        self.assertIn('registry is invalid', result.stderr)

    def test_privilege_denial_clears_previously_ready_state(self):
        path = self.record()
        result = self.launch(MOCK_SUDO_EXIT='1')
        self.assertNotEqual(result.returncode, 0)
        data = json.loads(path.read_text())
        self.assertEqual(data['status'], 'publication-pending')
        self.assertIn('route', data['last_error'])
        self.assertEqual(data['external_port'], 8400)

    def test_failed_https_clears_previously_ready_state(self):
        path = self.record()
        result = self.launch()
        self.assertNotEqual(result.returncode, 0)
        data = json.loads(path.read_text())
        self.assertEqual(data['status'], 'publication-pending')
        self.assertIn('HTTPS', data['last_error'])

    def test_failed_local_readiness_clears_previously_ready_state(self):
        path = self.record()
        result = self.launch(MOCK_READY_EXIT='1')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(path.read_text())['status'], 'failed')

    def test_failed_service_start_clears_previously_ready_state(self):
        path = self.record()
        result = self.launch(MOCK_START_EXIT='1')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(path.read_text())['status'], 'failed')

    def test_malformed_json_refuses_new_allocation_and_reuse(self):
        for service in ['new', 'docs']:
            with self.subTest(service=service):
                self.record(status='retired' if service == 'new' else 'ready')
                (self.records / 'broken.json').write_text('{broken')
                before = {p.name: p.read_bytes() for p in self.records.iterdir()}
                self.assert_registry_refused(self.launch(service), before)

    def test_invalid_schema_refuses_allocation(self):
        cases = [[], {}, dict(status='retired', external_port='8400', internal_port=20000), dict(status='retired', external_port=8400, internal_port=29999.5), dict(status='unknown', external_port=8400, internal_port=20000), dict(status='retired', external_port=10000, internal_port=20000)]
        for value in cases:
            with self.subTest(value=value):
                (self.records / 'invalid.json').write_text(json.dumps(value))
                before = {p.name: p.read_bytes() for p in self.records.iterdir()}
                self.assert_registry_refused(self.launch('new'), before)

    def test_duplicate_https_and_active_internal_reservations_refuse_allocation(self):
        for external, internal in [(8400, 20001), (8401, 20000)]:
            with self.subTest(external=external, internal=internal):
                self.record()
                self.record('other', external_port=external, internal_port=internal)
                before = {p.name: p.read_bytes() for p in self.records.iterdir()}
                self.assert_registry_refused(self.launch('new'), before)

    def test_retired_internal_port_reuse_is_permitted_without_https_reuse(self):
        self.record(status='retired')
        result = self.launch('new', MOCK_CURL_EXIT='0')
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((self.records / (self.identifier('new') + '.json')).read_text())
        self.assertEqual(data['external_port'], 8401)
        self.assertEqual(data['internal_port'], 20000)

    def test_full_retired_range_refuses_without_changing_reservations(self):
        for port in range(8400, 10000):
            (self.records / f'{port}.json').write_text(json.dumps(dict(status='retired', external_port=port, internal_port=20000)))
        before = {p.name: p.read_bytes() for p in self.records.iterdir()}
        result = self.launch('new')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('range exhausted', result.stderr)
        self.assertEqual({p.name: p.read_bytes() for p in self.records.iterdir()}, before)
        self.assertFalse(self.log.exists())

    def report_args(self):
        source = self.base / 'report'
        source.mkdir(exist_ok=True)
        (source / 'index.html').write_text('test report')
        return ['bash', str(self.lib / 'publish-report.sh'), '--source', str(source), '--project', 'audit', '--name', 'check', '--title', 'Audit']

    def test_failed_report_verification_preserves_pending_bundle(self):
        result = subprocess.run(self.report_args(), env=self.env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        db = json.loads((self.root / 'state/reports.json').read_text())
        self.assertEqual(db[data['id']]['delivery'], 'pending')
        self.assertTrue((self.root / 'public/_releases' / data['id'] / data['revision'] / 'index.html').is_file())

    def test_wrong_response_body_keeps_report_pending(self):
        result = subprocess.run(self.report_args(), env=dict(self.env, MOCK_CURL_EXIT='0'), capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        db = json.loads((self.root / 'state/reports.json').read_text())
        self.assertEqual(db[data['id']]['delivery'], 'pending')

    def test_concurrent_report_writers_preserve_losing_draft(self):
        args = self.report_args()
        initial = subprocess.run(args, env=self.env, capture_output=True, text=True)
        data = json.loads(initial.stdout)
        args += ['--id', data['id'], '--expected-revision', data['revision']]
        writers = [subprocess.Popen(args, env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(2)]
        output = [p.communicate(timeout=15) for p in writers]
        self.assertEqual(sum(('Revision conflict' in stderr for _, stderr in output)), 1)
        self.assertEqual(sum(('Content saved' in stderr for _, stderr in output)), 1)
        self.assertEqual(sum((p.is_dir() for p in (self.root / 'staging').iterdir())), 1)

    def test_wrong_host_refuses_before_creating_state(self):
        destination = self.base / 'wrong-host-store'
        result = subprocess.run(['bash', str(self.lib / 'publish-report.sh')], env=dict(self.env, MOCK_HOST='macbook', LAB_PUBLISH_ROOT=str(destination)), capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(destination.exists())
        self.assertFalse(self.log.exists())
if __name__ == '__main__':
    unittest.main(verbosity=2)
