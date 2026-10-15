# Bounded Agency

**Ontology-Driven Authority for Delegated Intelligence**

Timothy O'Brien · Conceptual preprint · 15 October 2026 · v0.1.1-preprint

ORCID: [0009-0001-2589-347X](https://orcid.org/0009-0001-2589-347X).

This project investigates how an autonomous system can receive a bounded scope of independent judgment without semantic evolution silently broadening it. The paper separates capability, execution permission, decision authority, and authority to adopt an operational semantic model. It proposes authority-relative semantic-change review and version-bound operational authorization.

The paper develops a conceptual synthesis of established semantic-policy, ontology-evolution, and authorization mechanisms. Its focus is authority-relative semantic-change admission: checking whether proposed changes in meaning broaden a specified agent's decision scope before approving their operational use. Building-safety and customer-support thought experiments illustrate the mechanism. The cases and executable illustration are synthetic; no deployment evaluation is reported.

## Paper and supplementary materials

| File | Purpose |
|---|---|
| [paper.md](paper.md) | Full manuscript source |
| [output/pdf/bounded-agency.pdf](output/pdf/bounded-agency.pdf) | Typeset preprint |
| [output/pdf/bounded-agency.tex](output/pdf/bounded-agency.tex) | Standalone source, editable in the native LaTeX editor |
| [references.md](references.md) | Selected bibliography |
| [examples/semantic_drift.py](examples/semantic_drift.py) | Executable finite-taxonomy illustration |
| [examples/change-admission.yaml](examples/change-admission.yaml) | Example change-admission schema |
| [examples/semantic-drift-result.json](examples/semantic-drift-result.json) | Recorded illustration output |
| [release/bounded-agency-v0.1.1-preprint-research.zip](release/bounded-agency-v0.1.1-preprint-research.zip) | Curated scientific supplement: sources, examples, and reproducibility instructions |
| [release/zenodo-upload.md](release/zenodo-upload.md) | Zenodo deposit record and metadata |

The supplement includes the manuscript and bibliography, standalone TeX, the illustrative code and schema, recorded example output, and the files needed to rebuild the paper.

## Verify and build

Requires Python 3.9 or newer and Pandoc. The manuscript uses the standard [`elsarticle`](https://ctan.org/pkg/elsarticle) preprint class (12-point, single column), with a preprint status footer and no journal affiliation. Exporting a PDF requires a local Tectonic installation. No agent framework or network credentials are required for the finite illustration or local content checks.

```sh
python3 examples/semantic_drift.py
python3 scripts/check_project.py
python3 scripts/build_paper.py
```

Open `output/pdf/bounded-agency.tex` in the native LaTeX editor and compile for diagnostics. The native compiler needs no local TeX installation. For a local exported PDF, after source validation:

```sh
python3 scripts/build_paper.py --pdf
python3 scripts/package_release.py
```

To include online bibliography verification in a build, install the pinned
[RefChecker](https://github.com/markrussinovich/refchecker) revision in an isolated
Python 3.11+ environment (the ordinary build still needs only Python 3.9+):

```sh
python3.11 -m venv .venv-refchecker
.venv-refchecker/bin/python -m pip install -r requirements-refchecker.txt
python3 scripts/build_paper.py --check-references
```

The audit exports all numbered entries in `references.md` to structured BibTeX
before invoking upstream RefChecker. This preserves titles, author lists,
identifiers, and undated records that its generic LaTeX parser can misread.
Results, the console log, original citations, and source/version hashes are saved
under `output/refchecker/` (ignored by Git). The default audit uses public scholarly
databases and disables LLM calls and paid web search. It requires network access;
the regular build and source checks remain offline.

```sh
python3 scripts/check_references.py                 # standalone audit
python3 scripts/build_paper.py --strict-references  # stop on any finding
python3 scripts/check_references.py --export-only   # offline input inspection
python3 scripts/test_check_references.py            # offline regression checks
```

`--check-references` stops on a failed or incomplete scan and allows a completed
scan with findings for human review. `--strict-references` also stops on errors,
warnings, unverified entries, or hallucination flags. A database mismatch or
unverified specification is not proof of a fabricated reference. The JSON report
contains findings rather than a record for every clean entry; `input.json` lists
every submitted citation. Optional LLM searches can be enabled explicitly with
`scripts/check_references.py --llm-provider openai` (or another supported provider)
using that provider's environment credentials; provider charges may apply.
Use `--python PATH` to select a different environment containing the pinned revision.
The audit does not edit the bibliography or the immutable deposited release.

The illustration exhaustively compares four fixed candidates in a finite positive taxonomy. It distinguishes shadow eligibility from current version-bound authorization and shows both ontology and accepted-type-fact paths. It is neither an LLM experiment nor a production implementation.

The recorded controls also distinguish a removal-only revision (non-expansion without permit-set equivalence) from a replacement revision that both adds and removes permits. These results cover the four enumerated proposals only.

## Publication status and rights

Version 0.1.1-preprint adds reproducible RefChecker build integration and discloses its use in reference screening. The scientific claims and bibliography are unchanged. The paper has not been peer reviewed.

Published on 15 October 2026 on [Zenodo](https://zenodo.org/records/23401477), with version DOI [10.5281/zenodo.23401477](https://doi.org/10.5281/zenodo.23401477). The [original version](https://zenodo.org/records/23332953) remains available. The supplement is a snapshot prepared before publication with the reserved DOI; current repository metadata records publication. Prior deposited files and metadata are preserved under `release/versions/`; published PDF and ZIP files are never overwritten under an existing version.

The paper and original supporting materials are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/); see [LICENSE.md](LICENSE.md) for scope. Linked third-party sources retain their own rights.
