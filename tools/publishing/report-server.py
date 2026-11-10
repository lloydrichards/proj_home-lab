"""Read-only report index and canonical links to immutable bundles."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from html import escape
import json
from pathlib import Path
import sys
from urllib.parse import quote, unquote, urlsplit


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, root, **kwargs):
        self.root = root
        super().__init__(*args, directory=str(root / 'public'), **kwargs)

    def do_GET(self):
        self.respond(False)

    def do_HEAD(self):
        self.respond(True)

    def respond(self, head):
        path = unquote(urlsplit(self.path).path)
        if path == '/reports' or path.startswith('/reports/'):
            path = path[len('/reports'):]
        path = path or '/'
        db_path = self.root / 'state/reports.json'
        db = json.loads(db_path.read_text()) if db_path.exists() else {}
        if path == '/':
            rows = []
            for report in sorted(db.values(), key=lambda x: x['updated'], reverse=True):
                text = ' '.join([report['title'], report['project'], report['summary']]).lower()
                rows.append(f'<li data-project="{escape(report["project"], quote=True)}" data-search="{escape(text, quote=True)}"><a href="{report["path"]}">{escape(report["title"])}</a> '
                            f'<span>{escape(report["project"])} · {escape(report["updated"])}{ " · Draft" if report["draft"] else ""}</span><p>{escape(report["summary"])}</p></li>')
            options = ''.join(f'<option>{escape(x)}</option>' for x in sorted({r['project'] for r in db.values()}))
            page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Home-lab reports</title>
<style>:root{color-scheme:light dark}body{font:1rem/1.6 system-ui;max-width:60rem;margin:auto;padding:1.5rem}input,select{font:inherit;max-width:100%;padding:.5rem}li{margin-block:1.5rem}span{display:block;font-size:.85rem}a{overflow-wrap:anywhere}</style>
<main><h1>Reports</h1><p>Development reports, retained until explicitly deleted.</p><label for="search">Search titles, projects, and summaries</label><br><input id="search" type="search"><p><label for="project">Project</label> <select id="project"><option value="">All projects</option>''' + options + '</select></p><p id="count" role="status"></p><ul>' + ''.join(rows) + '''</ul></main><script>
const search=document.querySelector('#search'),project=document.querySelector('#project');
function filter(){let count=0;for(const row of document.querySelectorAll('li')){row.hidden=!(row.dataset.search.includes(search.value.toLowerCase())&&(!project.value||row.dataset.project===project.value));if(!row.hidden)count++}document.querySelector('#count').textContent=count+' reports'}search.addEventListener('input',filter);project.addEventListener('change',filter);filter();</script></html>'''
            data = page.encode()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            if not head:
                self.wfile.write(data)
            return
        report_id = path.strip('/')
        if report_id in db:
            record = db[report_id]
            self.send_response(307)
            self.send_header('Location', f'/reports/_releases/{report_id}/{record["revision"]}/index.html')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            return
        if not path.startswith('/_releases/'):
            self.send_error(404)
            return
        target = (self.root / 'public' / path.lstrip('/')).resolve()
        releases = (self.root / 'public/_releases').resolve()
        if not target.is_relative_to(releases):
            self.send_error(404)
            return
        if target.is_dir():
            index = next((candidate.resolve() for name in ('index.html', 'index.htm')
                          if (candidate := target / name).is_file()), None)
            if index is None or not index.is_relative_to(releases):
                self.send_error(404)
                return
            if not path.endswith('/'):
                query = urlsplit(self.path).query
                location = '/reports' + quote(path, safe="/") + '/'
                if query:
                    location += '?' + query
                self.send_response(301)
                self.send_header('Location', location)
                self.send_header('Content-Length', '0')
                self.end_headers()
                return
        elif not target.is_file():
            self.send_error(404)
            return
        self.path = quote(path, safe="/")
        if head:
            super().do_HEAD()
        else:
            super().do_GET()

    def list_directory(self, path):
        self.send_error(404)
        return None


if __name__ == '__main__':
    root = Path(sys.argv[1]).resolve()
    ThreadingHTTPServer(('127.0.0.1', int(sys.argv[2]) if len(sys.argv) > 2 else 8379), partial(Handler, root=root)).serve_forever()
