import contextlib
import importlib.util
from http.client import HTTPConnection
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parents[1]


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


reports = module('reports', 'report-files.py')
server = module('server', 'report-server.py')


class Publishing(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'store'
        for path in ['state/previews', 'staging', 'public', 'launches']:
            (self.root / path).mkdir(parents=True)
        self.source = Path(self.temp.name) / 'source'
        self.source.mkdir()
        (self.source / 'index.html').write_text('<h1>First</h1><img src="image.txt">')
        (self.source / 'image.txt').write_text('first-image')

    def tearDown(self):
        self.temp.cleanup()

    def publish(self, expected='new', report_id=None):
        return reports.publish(self.root, self.source, 'stack-effect', 'graph-review', '<Graph review>', expected, report_id)

    @contextlib.contextmanager
    def serving(self):
        from functools import partial
        http = server.ThreadingHTTPServer(('127.0.0.1', 0), partial(server.Handler, root=self.root))
        thread = threading.Thread(target=http.serve_forever, daemon=True)
        thread.start()
        try:
            yield f'http://127.0.0.1:{http.server_port}'
        finally:
            http.shutdown()
            http.server_close()
            thread.join()

    def test_revision_preserves_canonical_link_and_old_companion_files(self):
        first = self.publish()
        with self.serving() as base:
            with urllib.request.urlopen(base + first['path']) as response:
                old_url = response.url
                self.assertIn(b'First', response.read())
            (self.source / 'index.html').write_text('<h1>Second</h1><img src="image.txt">')
            (self.source / 'image.txt').write_text('second-image')
            second = self.publish(first['revision'], first['id'])
            self.assertEqual(first['path'], second['path'])
            self.assertEqual(first['created'], second['created'])
            with urllib.request.urlopen(base + first['path']) as response:
                self.assertIn(b'Second', response.read())
            with urllib.request.urlopen(old_url.rsplit('/', 1)[0] + '/image.txt') as response:
                self.assertEqual(response.read(), b'first-image')

    def test_nested_directory_indexes_preserve_links_without_listing_directories(self):
        (self.source / 'index.html').write_text('<a href="details/">Details</a>')
        details = self.source / 'details'
        details.mkdir()
        (details / 'index.html').write_text('<h1>Details</h1><img src="image.txt">')
        (details / 'image.txt').write_text('nested-image')
        (self.source / 'empty').mkdir()
        report = self.publish()
        with self.serving() as base:
            with urllib.request.urlopen(base + report['path']) as response:
                release = response.url.rsplit('/', 1)[0]
                self.assertIn(b'href="details/"', response.read())
            for method in ['GET', 'HEAD']:
                for suffix in ['/details/', '/details?view=full']:
                    with self.subTest(method=method, suffix=suffix):
                        url = urlsplit(release + suffix)
                        target = url.path + ('?' + url.query if url.query else '')
                        with contextlib.closing(HTTPConnection(url.netloc)) as connection:
                            connection.request(method, target)
                            response = connection.getresponse()
                            if '?' in suffix:
                                self.assertEqual(response.status, 301)
                                location = response.getheader('Location')
                                self.assertEqual(location, url.path + '/?view=full')
                                self.assertEqual(response.read(), b'')
                                # Send HEAD explicitly after the redirect. Older urllib
                                # versions follow it with GET, which changes the assertion.
                                connection.request(method, location)
                                response = connection.getresponse()
                            self.assertEqual(response.status, 200)
                            self.assertEqual(response.read(), b'' if method == 'HEAD' else (details / 'index.html').read_bytes())
                for suffix in ['/empty/', '/empty', '/%2e%2e/%2e%2e/%2e%2e/state/reports.json']:
                    with self.subTest(method=method, denied=suffix):
                        with self.assertRaises(urllib.error.HTTPError) as error:
                            urllib.request.urlopen(urllib.request.Request(release + suffix, method=method))
                        self.assertEqual(error.exception.code, 404)
            with urllib.request.urlopen(release + '/details/image.txt') as response:
                self.assertEqual(response.read(), b'nested-image')

    def test_stale_author_keeps_draft_without_overwriting_published_report(self):
        first = self.publish()
        second = self.publish(first['revision'], first['id'])
        (self.source / 'index.html').write_text('losing draft')
        with self.assertRaisesRegex(ValueError, 'Draft preserved'):
            self.publish(first['revision'], first['id'])
        db = json.loads((self.root / 'state/reports.json').read_text())
        self.assertEqual(db[first['id']]['revision'], second['revision'])
        self.assertTrue(any((p / 'index.html').read_text() == 'losing draft' for p in (self.root / 'staging').iterdir()))

    def test_index_escapes_titles_and_does_not_expose_private_files(self):
        report = self.publish()
        (self.root / 'state/secret').write_text('secret')
        with self.serving() as base:
            with urllib.request.urlopen(base + '/reports/') as response:
                text = response.read().decode()
                self.assertIn('&lt;Graph review&gt;', text)
                self.assertIn('stack-effect', text)
                self.assertIn('id="project"', text)
            for path in ['/reports/state/secret', '/reports/_releases/../../state/secret', '/reports/_releases/%252e%252e/%252e%252e/state/secret']:
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(base + path)
                self.assertEqual(error.exception.code, 404)

    def test_symlink_rejected_and_explicit_deletion_removes_report_bundles(self):
        (self.source / 'escape').symlink_to('/etc/passwd')
        with self.assertRaisesRegex(ValueError, 'Unsupported'):
            self.publish()
        (self.source / 'escape').unlink()
        report = self.publish()
        reports.delete(self.root, report['id'])
        self.assertFalse((self.root / 'public/_releases' / report['id']).exists())
        self.assertEqual(json.loads((self.root / 'state/reports.json').read_text()), {})

    def test_allocation_skips_all_records_and_never_reuses_retired_urls(self):
        home = Path(self.temp.name) / 'home'; home.mkdir()
        worktree = Path(self.temp.name) / 'worktree'; worktree.mkdir()
        subprocess.run(['git', 'init', '-q', str(worktree)], check=True)
        mocks = Path(self.temp.name) / 'bin'; mocks.mkdir()
        mock_commands = {
            'hostname': 'echo home-lab', 'id': 'echo coder',
            'tailscale': 'if [ "$1" = status ]; then echo \'{"Self":{"DNSName":"home-lab.example.ts.net."}}\'; else echo \'{}\'; fi',
            'ss': 'exit 0', 'systemctl': 'if [ "$3" = is-active ] || [ "$2" = is-active ]; then exit 1; fi; exit 0',
        }
        for name, body in mock_commands.items():
            file = mocks / name; file.write_text('#!/bin/bash\n' + body + '\n'); file.chmod(0o755)
        # Include a later false record to catch jq -e's last-value semantics.
        records = self.root / 'state/previews'
        (records / 'a.json').write_text(json.dumps(dict(external_port=8400, internal_port=20000, status='retired')))
        (records / 'z.json').write_text(json.dumps(dict(external_port=8401, internal_port=20001, status='ready')))
        env = dict(os.environ, HOME=str(home), LAB_PUBLISH_ROOT=str(self.root), PATH=str(mocks)+':'+os.environ['PATH'])
        result = subprocess.run(['bash', str(HERE/'start-preview.sh'), str(worktree), 'docs', '--', '/bin/true', '-m', 'fixture'], env=env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        created = [json.loads(p.read_text()) for p in records.glob('*.json') if p.name not in ['a.json','z.json']]
        self.assertEqual(len(created), 1, result.stderr)
        self.assertEqual(created[0]['external_port'], 8402)
        self.assertEqual(created[0]['internal_port'], 20000)
        self.assertEqual(created[0]['argv'][-2:], ['-m', 'fixture'])
        self.assertIn('not ready', result.stderr)

    def test_missing_worktree_fails_without_fallback(self):
        record = self.root / 'missing.json'
        record.write_text(json.dumps(dict(status='allocated', worktree=str(self.root/'absent'))))
        result = subprocess.run([sys.executable, str(HERE/'preview-runner.py'), str(record)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('missing', result.stderr)

    def test_repeated_launch_failures_have_a_finite_budget(self):
        record = self.root / 'runner.json'
        record.write_text(json.dumps(dict(status='allocated', worktree=str(self.source), internal_port=23456, host='home-lab.example.ts.net', argv=['/bin/false'])))
        result = subprocess.run([sys.executable, str(HERE/'preview-runner.py'), str(record)], capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout.count('Preview exited'), 4)


if __name__ == '__main__':
    unittest.main()
