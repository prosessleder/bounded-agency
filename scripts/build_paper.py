#!/usr/bin/env python3
"""Generate a standalone elsarticle manuscript and HTML from Markdown.

Compile the saved .tex in the native editor for diagnostics. The --pdf option
exports a PDF with an installed Tectonic; the diagnostic tool does not export.
"""
from pathlib import Path
import argparse
import copy
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--pdf', action='store_true')
parser.add_argument('--check-references', action='store_true',
                    help='Run the online RefChecker audit before building')
parser.add_argument('--strict-references', action='store_true',
                    help='Run RefChecker and stop the build on any finding')
args = parser.parse_args()
if args.check_references or args.strict_references:
    command = [sys.executable, str(ROOT / 'scripts/check_references.py')]
    if args.strict_references:
        command.append('--strict')
    subprocess.run(command, check=True)
out = ROOT / 'output' / 'pdf'
out.mkdir(parents=True, exist_ok=True)
body = (ROOT / 'paper.md').read_text()
references = '[1]' + (ROOT / 'references.md').read_text().split('\n\n[1]', 1)[1]
license_notice = (ROOT / 'release' / 'license-notice.txt').read_text().strip()


def pandoc(text, *options):
    return subprocess.run(['pandoc', *options], input=text, text=True,
                          capture_output=True, check=True).stdout


def latex(markdown):
    return pandoc(markdown, '--from=markdown+tex_math_dollars', '--to=latex').strip()


ast = json.loads(pandoc(body, '--from=markdown+tex_math_dollars', '--to=json'))


def metadata_text(key):
    value = ast['meta'][key]
    if value['t'] == 'MetaString':
        return value['c']
    if value['t'] != 'MetaInlines':
        raise ValueError('Expected text metadata: ' + key)
    fragment = {'pandoc-api-version': ast['pandoc-api-version'], 'meta': {},
                'blocks': [{'t': 'Plain', 'c': value['c']}]}
    return pandoc(json.dumps(fragment), '--from=json', '--to=plain', '--wrap=none').strip()


title, author, date, version, orcid = [metadata_text(key) for key in
                                     ['title', 'author', 'date', 'version', 'orcid']]
if not re.fullmatch(r'https://orcid\.org/\d{4}-\d{4}-\d{4}-\d{3}[\dX]', orcid):
    raise ValueError('Expected a complete ORCID URL')
# Keep the human-readable source conventional; use the class's native abstract
# and keyword environments in the PDF instead of generic section headings.
preamble, abstract_section = body.split('\n# Abstract\n\n', 1)
abstract_text, rest = abstract_section.split('\n\n**Keywords:** ', 1)
keyword_text, _ = rest.split('\n\n# 1. Introduction', 1)
blocks = ast['blocks']
intro = next(i for i, block in enumerate(blocks)
             if block['t'] == 'Header' and block['c'][1][0] == 'introduction')
pdf_ast = copy.deepcopy(ast)
pdf_ast['blocks'] = blocks[intro:]
# Let the journal class number sections rather than including numbers in titles.
for block in pdf_ast['blocks']:
    if block['t'] != 'Header':
        continue
    inlines = block['c'][2]
    if inlines and inlines[0]['t'] == 'Str' and re.fullmatch(r'\d+(?:\.\d+)*\.?', inlines[0]['c']):
        del inlines[0]
        if inlines and inlines[0]['t'] == 'Space':
            del inlines[0]
    else:
        block['c'][1][1].append('unnumbered')

header = out / 'header.tex'
header.write_text(r'''\usepackage{microtype}
\usepackage{etoolbox}
\setlength{\emergencystretch}{3em}
\widowpenalty=10000
\clubpenalty=10000
\AtBeginEnvironment{longtable}{\footnotesize}
\AtBeginEnvironment{verbatim}{\small}
% Keep the standard manuscript page style without a submission claim.
\makeatletter
\def\ps@pprintTitle{%
  \let\@oddhead\@empty\let\@evenhead\@empty
  \def\@oddfoot{\hfil\thepage\hfil}%
  \let\@evenfoot\@oddfoot}
\makeatother
''')
tex = pandoc(json.dumps(pdf_ast), '--from=json', '--to=latex', '--standalone',
             '--number-sections', '--pdf-engine=tectonic',
             '--variable=documentclass:elsarticle', '--variable=fontsize:12pt',
             '--variable=classoption:preprint', '--variable=classoption:numbers',
             '--variable=classoption:nopreprintline', '--variable=papersize:a4',
             '--variable=indent:true',
             '--variable=colorlinks:true', '--variable=urlcolor:blue',
             '--variable=linkcolor:black', '--include-in-header=' + str(header))
frontmatter = '\n'.join([
    r'\begin{frontmatter}',
    r'\title{' + latex(title) + '}',
    r'\author{' + latex(author) + r'\fnref{orcid}}',
    r'\fntext[orcid]{ORCID: \url{' + orcid + '}}',
    r'\nonumnote{Preprint (not peer reviewed). Version ' + latex(version) +
    ', ' + latex(date) + r'.\\ ' + latex(license_notice) + '}',
    r'\begin{abstract}', latex(abstract_text), r'\end{abstract}',
    r'\begin{keyword}', r' \sep '.join(latex(k.strip().rstrip('.')) for k in keyword_text.split(';')),
    r'\end{keyword}', r'\end{frontmatter}',
])
# Pandoc's generic template declares the title before the document. elsarticle
# instead collects the full frontmatter and calls maketitle when it closes.
tex, count = re.subn(r'\\title\{.*?\\begin\{document\}\s*\\maketitle',
                     lambda _: '\\begin{document}\n' + frontmatter, tex,
                     count=1, flags=re.S)
if count != 1:
    raise ValueError('Pandoc title block did not match the expected template')
records = re.findall(r'^\[(\d+)\]\s+(.+?)(?=\n\n\[\d+\]|\Z)', references, re.M | re.S)
if len(records) != 28:
    raise ValueError('Expected 28 bibliography entries')
bibliography = '\n\n'.join(r'\bibitem{ref' + number + '}\n' + latex(text)
                              for number, text in records)
tex = tex.replace(r'\end{document}', '\n'.join([
    r'\begin{thebibliography}{99}', bibliography,
    r'\end{thebibliography}', r'\end{document}']))
# Long ontology identifiers may break at CamelCase boundaries without adding
# hyphens that would change their spelling.
tex = re.sub(r'\\texttt\{([A-Za-z][A-Za-z0-9]+)\}',
             lambda m: r'\texttt{' + re.sub(r'(?<=[a-z])(?=[A-Z])',
                                              lambda _: r'\allowbreak{}', m.group(1)) + '}', tex)
# Keep the evaluator's introduction with its display at the page boundary.
evaluator_intro = r'Define a \textbf{counterfactual eligibility evaluator}'
if tex.count(evaluator_intro) != 1:
    raise RuntimeError('Expected one counterfactual evaluator introduction')
tex = tex.replace(evaluator_intro, evaluator_intro + r'\nopagebreak[4]')
(out / 'bounded-agency.tex').write_text(tex)

# HTML retains ordinary Markdown headings and includes the same author ID/rights.
status = '*Preprint (not peer reviewed). Version ' + version + '.*'
assembled = body.replace(status, status + '\n\nORCID: <' + orcid + '>\n\n' + license_notice)
assembled += '\n\n# References\n\n' + references
assembled_path = out / 'paper-assembled.md'
assembled_path.write_text(assembled)
subprocess.run(['pandoc', str(assembled_path), '--standalone', '--mathml',
                '--metadata=pagetitle:Bounded Agency',
                '--output=' + str(ROOT / 'output' / 'paper.html')], check=True)
if args.pdf:
    subprocess.run(['tectonic', '--only-cached', '--keep-logs', '--keep-intermediates',
                    '--outdir', str(out), str(out / 'bounded-agency.tex')], check=True)
print('Generated standalone elsarticle source:', out / 'bounded-agency.tex')
