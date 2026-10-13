#!/usr/bin/env python3
"""Package checked preprint artifacts for manual Zenodo upload; never publishes."""
from pathlib import Path
from hashlib import sha256
import json
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
release = ROOT / 'release'
version = 'v0.1.0-preprint'
subprocess.run(['python3', str(ROOT / 'scripts' / 'check_project.py')], check=True)
source_pdf = ROOT / 'output' / 'pdf' / 'bounded-agency.pdf'
if not source_pdf.is_file():
    raise SystemExit('Build and visually inspect the PDF before packaging.')
pdf = release / f'bounded-agency-{version}.pdf'
shutil.copyfile(source_pdf, pdf)
archive = release / f'bounded-agency-{version}-research.zip'
# Explicitly list the scientific supplementary materials.
files = {name: ROOT / name for name in [
    'LICENSE.md', 'CITATION.cff', 'paper.md', 'references.md',
    'output/pdf/bounded-agency.tex', 'examples/semantic_drift.py',
    'examples/change-admission.yaml', 'examples/semantic-drift-result.json',
    'scripts/build_paper.py',
    'release/license-notice.txt',
]}
files['README.md'] = release / 'supplement-README.md'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for name, path in sorted(files.items()):
        content = path.read_bytes()
        item = zipfile.ZipInfo(name, date_time=(2026,10,12,0,0,0))
        item.compress_type = zipfile.ZIP_DEFLATED
        item.external_attr = 0o100644 << 16
        z.writestr(item, content)
checks = {}
for path in [pdf, archive, release / 'zenodo-upload-metadata.json']:
    checks[path.name] = {'sha256':sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}
(release / 'SHA256SUMS.txt').write_text(''.join(f"{v['sha256']}  {k}\n" for k,v in checks.items()))
(release / 'release-manifest.json').write_text(json.dumps({
    'version':version,'manuscript_date':'2026-10-12','publication_status':'not published',
    'doi_assigned':False,'repository_visibility':'public','license':'CC-BY-4.0','files':checks,
    'archive_entry_count':len(files),'archive_contents':sorted(files),
},indent=2)+'\n')
with zipfile.ZipFile(archive) as z:
    if z.testzip() is not None:
        raise ValueError('Archive integrity failure')
print(json.dumps(checks,indent=2))
