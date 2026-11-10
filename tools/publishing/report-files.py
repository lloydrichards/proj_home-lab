"""Prepare immutable report bundles and commit one optimistic metadata update."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import sys
import uuid
from zoneinfo import ZoneInfo


def identifier(value):
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,119}", value):
        raise ValueError("Use a lowercase identifier of at most 120 characters")
    return value


def atomic_json(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    with temporary.open('rb') as stream:
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def publish(root, source, project, name, title, expected, report_id=None, summary='', draft=False):
    identifier(project)
    identifier(name)
    source = Path(source).resolve(strict=True)
    if not (source / 'index.html').is_file():
        raise ValueError('The source directory needs index.html')
    if root.resolve().is_relative_to(source):
        raise ValueError('The source must not contain the publishing store')
    now = dt.datetime.now(ZoneInfo('Europe/Zurich'))
    report_id = identifier(report_id or f'{now:%y%m%d}_{project}_{name}')
    db_path = root / 'state/reports.json'
    db = json.loads(db_path.read_text()) if db_path.exists() else {}
    current = db.get(report_id)
    if not current and report_id != f'{now:%y%m%d}_{project}_{name}':
        raise ValueError('New report ids must match the publication date, project, and name')
    revision = uuid.uuid4().hex
    staging = root / 'staging' / revision
    # Copy the draft before checking its revision so a conflict cannot discard it.
    for path in source.rglob('*'):
        if path.is_symlink() or not (path.is_dir() or path.is_file()):
            raise ValueError(f'Unsupported file in report: {path.relative_to(source)}')
    shutil.copytree(source, staging)
    if (current and current['revision'] != expected) or (not current and expected != 'new'):
        raise ValueError(f'Revision conflict. Draft preserved at {staging}')
    if current and current['project'] != project:
        raise ValueError(f'Project mismatch. Draft preserved at {staging}')
    release = root / 'public/_releases' / report_id / revision
    release.parent.mkdir(parents=True, exist_ok=True)
    os.replace(staging, release)
    record = dict(id=report_id, project=project, title=title, summary=summary,
                  draft=draft, revision=revision, delivery='pending', updated=now.isoformat(),
                  created=current['created'] if current else now.isoformat(),
                  path=f'/reports/{report_id}/')
    db[report_id] = record
    atomic_json(db_path, db)
    return record


def delete(root, report_id):
    identifier(report_id)
    db_path = root / 'state/reports.json'
    db = json.loads(db_path.read_text()) if db_path.exists() else {}
    if report_id not in db:
        raise ValueError('Unknown report')
    del db[report_id]
    atomic_json(db_path, db)
    shutil.rmtree(root / 'public/_releases' / report_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=['publish', 'delete'])
    parser.add_argument('root', type=Path)
    parser.add_argument('--id')
    parser.add_argument('--source')
    parser.add_argument('--project')
    parser.add_argument('--name')
    parser.add_argument('--title')
    parser.add_argument('--summary', default='')
    parser.add_argument('--draft', action='store_true')
    parser.add_argument('--expected-revision', default='new')
    args = parser.parse_args()
    try:
        if args.operation == 'delete':
            if not args.id:
                parser.error('Deletion requires --id')
            delete(args.root, args.id)
            print('Deleted report', args.id)
        else:
            if not all([args.source, args.project, args.name, args.title]):
                parser.error('Publishing requires --source, --project, --name, and --title')
            result = publish(args.root, args.source, args.project, args.name, args.title,
                             args.expected_revision, args.id, args.summary, args.draft)
            print(json.dumps(result))
            print('Content saved. Verify the canonical Tailscale URL before sharing.', file=sys.stderr)
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
