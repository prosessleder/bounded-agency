#!/usr/bin/env python3
"""Export the selected bibliography and run the pinned upstream RefChecker.

Network access is required. Default runs disable LLMs and paid web search.
Exit 2 means incomplete/failed execution; --strict also exits 1 on findings.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REVISION = 'b5792c5b28edda686cc078a173bc49fe8c0a7d4f'


def export_bibliography(source: str) -> tuple[str, list[dict]]:
    """Parse this project's numbered author/year/title Markdown convention.

    Reject unknown layouts rather than silently omitting metadata. Retain each
    original citation in the audit input alongside the derived verification fields.
    """
    matches = re.findall(r'^\[(\d+)\]\s+(.+?)(?=\n\n\[\d+\]|\Z)', source, re.M | re.S)
    if not matches or [int(n) for n, _ in matches] != list(range(1, len(matches) + 1)):
        raise ValueError('Expected consecutive bibliography numbers starting at 1')
    entries, blocks = [], []
    for number, raw in matches:
        raw = ' '.join(raw.split())
        prefix = re.match(r'(.+?)\. (\d{4}(?:, updated \d{4})?|Undated)\. (.+)', raw)
        if not prefix:
            raise ValueError(f'Cannot parse author/year for reference [{number}]')
        names, date, rest = prefix.groups()
        names = re.sub(r', eds?\.?$', '', names)
        title_match = re.match(r'“(.+?)”|\*([^*]+)\*', rest)
        if not title_match:
            raise ValueError(f'Cannot parse title for reference [{number}]')
        title = (title_match.group(1) or title_match.group(2)).rstrip('.')
        authors = re.split(r',\s+(?:and\s+)?|\s+and\s+', names)
        urls = re.findall(r'\]\((https://[^\s)]+)\)', raw)
        if not urls:
            raise ValueError(f'Missing primary URL for reference [{number}]')
        fields = {'title': title, 'author': ' and '.join(authors), 'url': urls[0]}
        # Organization names use BibTeX's literal-author convention.
        if names in {'Open Policy Agent project', 'Inferal'}:
            fields['author'] = '{' + names + '}'
        if date != 'Undated':
            fields['year'] = date[:4]
        doi = next((url.removeprefix('https://doi.org/') for url in urls
                    if url.startswith('https://doi.org/')), None)
        if doi:
            fields['doi'] = doi
        arxiv = re.search(r'arXiv:(\d{4}\.\d{4,5}(?:v\d+)?)', raw)
        if arxiv:
            fields.update(eprint=arxiv.group(1), archivePrefix='arXiv')
        journal = re.search(r'\*([^*]+)\*', rest[title_match.end():])
        if journal:
            fields['journal'] = journal.group(1)
        for key, value in fields.items():
            if key != 'author' and any(c in value for c in '{}\\'):
                raise ValueError(f'Unsupported BibTeX characters in [{number}] {key}')
        blocks.append('@misc{ref' + number + ',\n' + ',\n'.join(
            '  ' + key + ' = {' + value + '}' for key, value in fields.items()) + '\n}')
        entries.append({'number': int(number), 'key': 'ref' + number,
                        'original': raw, 'authors': authors, 'fields': fields})
    return '\n\n'.join(blocks) + '\n', entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--python', type=Path, default=ROOT / '.venv-refchecker/bin/python',
                        help='Python environment containing the pinned requirements')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'output/refchecker')
    parser.add_argument('--strict', action='store_true', help='Fail on errors, warnings, or unverified references')
    parser.add_argument('--llm-provider', choices=['openai', 'anthropic', 'google', 'azure'],
                        help='Opt into LLM extraction/search and associated API charges')
    parser.add_argument('--export-only', action='store_true', help='Export inputs without network or dependencies')
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    try:
        source_bytes = {name: (ROOT / name).read_bytes() for name in ['paper.md', 'references.md']}
        source_hashes = {name: sha256(data).hexdigest() for name, data in source_bytes.items()}
        bib, entries = export_bibliography(source_bytes['references.md'].decode('utf-8'))
        (output / 'references.bib').write_text(bib)
        (output / 'input.json').write_text(json.dumps(entries, indent=2, ensure_ascii=False) + '\n')
        if args.export_only:
            print(f'Exported {len(entries)} references to {output}')
            return 0
        python = args.python.absolute()
        if not python.is_file():
            raise ValueError('Install requirements-refchecker.txt into .venv-refchecker first')
        # Confirm the actual installed origin, not merely its mutable version label.
        inspect = ('from importlib.metadata import distribution; import json; '
                   'd=distribution("academic-refchecker"); '
                   'print(json.dumps({"version":d.version,"origin":json.loads(d.read_text("direct_url.json") or "{}")}))')
        installed = json.loads(subprocess.check_output([str(python), '-c', inspect], text=True))
        if installed['origin'].get('vcs_info', {}).get('commit_id') != REVISION:
            raise ValueError('RefChecker origin differs from requirements-refchecker.txt; reinstall the pinned requirements')
        report = output / 'report.json'
        report.unlink(missing_ok=True)
        command = [str(python), '-m', 'refchecker', '--paper', str(output / 'references.bib'),
                   '--report-file', str(report), '--report-format', 'json', '--max-workers', '3']
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'
        if args.llm_provider:
            command.extend(['--llm-provider', args.llm_provider])
        else:
            # Upstream auto-detects web-search credentials separately from extraction.
            for key in list(env):
                if key.endswith('API_KEY') or key == 'OPENAI_CHAT_KEY':
                    if key != 'SEMANTIC_SCHOLAR_API_KEY':
                        env.pop(key)
            env['REFCHECKER_USE_LLM'] = 'false'
        started = datetime.now(timezone.utc).isoformat()
        print(f'Checking {len(entries)} references; log: {output / "run.log"}', flush=True)
        with (output / 'run.log').open('w') as log:
            completed = subprocess.run(command, cwd=output, env=env, stdin=subprocess.DEVNULL,
                                       stdout=log, stderr=subprocess.STDOUT)
        payload = json.loads(report.read_text()) if report.exists() else {}
        summary = payload.get('summary', {})
        source_unchanged = all((ROOT / name).read_bytes() == data for name, data in source_bytes.items())
        complete = (source_unchanged and completed.returncode == 0 and summary.get('total_papers_processed') == 1
                    and summary.get('total_references_processed') == len(entries))
        provenance = {'started_at': started, 'finished_at': datetime.now(timezone.utc).isoformat(),
                      'complete': complete, 'exit_code': completed.returncode,
                      'expected_references': len(entries), 'refchecker': installed,
                      'llm_provider': args.llm_provider, 'summary': summary,
                      'source_unchanged': source_unchanged, 'source_sha256': source_hashes,
                      'input_sha256': sha256(bib.encode()).hexdigest(),
                      'note': 'Database metadata findings require review; unverified does not mean fabricated.'}
        (output / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
        print(json.dumps(summary, indent=2))
        if not complete:
            raise ValueError('Incomplete RefChecker run; inspect run.log and provenance.json')
        findings = any(summary.get(k, 0) for k in ['total_errors_found', 'total_warnings_found',
                                                  'total_unverified_refs', 'flagged_records'])
        print('Completed reference check' + ('; findings require review.' if findings else '.'))
        return 1 if args.strict and findings else 0
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(f'Reference check failed: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
