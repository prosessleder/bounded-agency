#!/usr/bin/env python3
"""Package checked preprint artifacts for Zenodo upload; never publishes.

Published versions are immutable and verified before a new candidate is built.
The source version selects the current release; old snapshots live in versions/.
"""
from pathlib import Path
from hashlib import sha256
import json
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def verify_manifest(directory):
    manifest = json.loads((directory / 'release-manifest.json').read_text())
    for name, expected in manifest['files'].items():
        data = (directory / name).read_bytes()
        if len(data) != expected['bytes'] or sha256(data).hexdigest() != expected['sha256']:
            raise ValueError('Published release checksum mismatch: ' + str(directory / name))
    return manifest


def main():
    release = ROOT / 'release'
    source = (ROOT / 'paper.md').read_text()
    version = 'v' + re.search(r"^version: '([^']+)'$", source, re.M).group(1)
    date = json.loads((release / 'zenodo-upload-metadata.json').read_text())['manuscript_date']
    manifest_path = release / 'release-manifest.json'
    if manifest_path.exists():
        published = json.loads(manifest_path.read_text())
        if published.get('doi_assigned'):
            if published['version'] == version:
                verify_manifest(release)
                print('Verified published release ' + published['doi'] + '; no files changed.')
                return
            archive = release / 'versions' / published['version']
            if not (archive / 'release-manifest.json').exists():
                archive.mkdir(parents=True, exist_ok=True)
                names = set(published['files']) | {'release-manifest.json', 'SHA256SUMS.txt',
                                                  'supplement-README.md', 'zenodo-upload.md'}
                for name in names:
                    shutil.copyfile(release / name, archive / name)
            verify_manifest(archive)
            for name, expected in published['files'].items():
                if name.endswith(('.pdf', '.zip')):
                    if sha256((release / name).read_bytes()).hexdigest() != expected['sha256']:
                        raise ValueError('Original deposited file changed: ' + name)
    for old_manifest in sorted((release / 'versions').glob('*/release-manifest.json')):
        verify_manifest(old_manifest.parent)
    subprocess.run([sys.executable, str(ROOT / 'scripts/check_project.py')], check=True)
    pdf_source = ROOT / 'output/pdf/bounded-agency.pdf'
    if not pdf_source.is_file():
        raise ValueError('Build and visually inspect the PDF before packaging.')
    audit = ROOT / 'validation/refchecker'
    provenance = json.loads((audit / 'provenance.json').read_text())
    bibliography_hash = sha256((ROOT / 'references.md').read_bytes()).hexdigest()
    if not provenance['complete'] or provenance['source_sha256']['references.md'] != bibliography_hash:
        raise ValueError('Reference audit does not cover the current bibliography')
    (audit / 'release-validation.json').write_text(json.dumps({
        'release_version': version, 'release_date': date,
        'source_sha256': {name: sha256((ROOT / name).read_bytes()).hexdigest()
                          for name in ['paper.md', 'references.md']},
        'reference_report_sha256': sha256((audit / 'report.json').read_bytes()).hexdigest(),
        'bibliography_unchanged_since_online_scan': True,
        'note': 'The online scan preceded only the release date/version and RefChecker disclosure update; no fresh online scan is claimed.',
    }, indent=2) + '\n')
    pdf = release / f'bounded-agency-{version}.pdf'
    shutil.copyfile(pdf_source, pdf)
    archive = release / f'bounded-agency-{version}-research.zip'
    names = [
        'LICENSE.md', 'CITATION.cff', 'paper.md', 'references.md',
        'output/pdf/bounded-agency.tex', 'examples/semantic_drift.py',
        'examples/change-admission.yaml', 'examples/semantic-drift-result.json',
        'requirements-refchecker.txt', 'scripts/build_paper.py',
        'scripts/check_project.py', 'scripts/check_references.py',
        'scripts/test_check_references.py', 'scripts/package_release.py',
        'release/license-notice.txt', 'release/supplement-README.md', 'release/zenodo-upload-metadata.json',
        'release/zenodo-upload.md',
    ] + [str(path.relative_to(ROOT)) for path in sorted(audit.iterdir()) if path.is_file()]
    files = {name: ROOT / name for name in names}
    files['README.md'] = release / 'supplement-README.md'
    year, month, day = map(int, date.split('-'))
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name, path in sorted(files.items()):
            item = zipfile.ZipInfo(name, date_time=(year, month, day, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            z.writestr(item, path.read_bytes())
    checks = {path.name: {'sha256': sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}
              for path in [pdf, archive, release / 'zenodo-upload-metadata.json']}
    (release / 'SHA256SUMS.txt').write_text(''.join(f"{v['sha256']}  {k}\n" for k, v in checks.items()))
    metadata = json.loads((release / 'zenodo-upload-metadata.json').read_text())
    manifest = {
        'version': version, 'manuscript_date': date,
        'publication_status': 'prepared for Zenodo publication; not peer reviewed',
        'doi_assigned': False, 'doi_reserved': True,
        'doi': metadata['doi'], 'concept_doi': metadata['concept_doi'],
        'record_url': metadata['record_url'], 'publication_date': date,
        'repository_visibility': 'public', 'license': 'CC-BY-4.0', 'files': checks,
        'archive_entry_count': len(files), 'archive_contents': sorted(files),
        'deposited_files': [pdf.name, archive.name],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None or set(z.namelist()) != set(files):
            raise ValueError('Archive integrity failure')
    print(json.dumps(checks, indent=2))


if __name__ == '__main__':
    main()
