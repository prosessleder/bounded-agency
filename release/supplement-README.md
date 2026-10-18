# Bounded Agency: supplementary materials

Timothy O'Brien · 0.1.2-preprint · 18 October 2026

ORCID: [0009-0001-2589-347X](https://orcid.org/0009-0001-2589-347X).

This archive accompanies *Bounded Agency: Ontology-Driven Authority for Delegated Intelligence*. It contains the paper's sources and a finite illustration of how a changed taxonomy or accepted classification can affect decision eligibility while authorization to act remains bound to an approved version.

This corrected-version candidate adds an explicit whole-change composition control and corrects the schema witness identifier. See `release/revision-notes-v0.1.2.md`. The bibliography is unchanged; the saved reference scan is historical, not a fresh check of the revised prose.

## Contents

| File | Purpose |
| --- | --- |
| `paper.md` | Manuscript source |
| `references.md` | Selected bibliography |
| `output/pdf/bounded-agency.tex` | Standalone LaTeX source |
| `examples/semantic_drift.py` | Executable illustration using Python's standard library |
| `examples/change-admission.yaml` | Illustrative admission schema |
| `examples/semantic-drift-result.json` | Recorded illustration output |
| `scripts/build_paper.py` | Generate LaTeX and HTML; optionally run reference verification |
| `scripts/check_project.py` | Offline source-integrity checks |
| `scripts/check_references.py`, `scripts/test_check_references.py` | Online reference check and offline regression tests |
| `requirements-refchecker.txt` | Pinned upstream RefChecker revision |
| `validation/refchecker/` | Recorded reference-screening inputs, results, provenance, and release binding |
| `release/license-notice.txt` | License notice used by the build |
| `LICENSE.md`, `CITATION.cff` | License and citation metadata |

## Run the illustration

With Python 3.9 or newer, from the extracted archive directory run:

```sh
python3 examples/semantic_drift.py
```

The output should match `examples/semantic-drift-result.json`. The program compares four fixed proposals under a finite positive taxonomy. It distinguishes candidate eligibility from current version-bound operational authorization and illustrates both ontology and accepted-fact changes.

The recorded controls also distinguish a removal-only revision (non-expansion without permit-set equivalence) from a replacement revision that both adds and removes permits. These results cover the four enumerated proposals only.

The cases and this finite example are synthetic. They do not implement a deployed agent, general OWL reasoning, complete mediation, or a validated semantic-change assessor, and they provide no empirical estimate of safety or performance.

## Rebuild the paper

Generating the standalone source and HTML requires Python 3.9 or newer and Pandoc:

```sh
python3 scripts/build_paper.py
```

Open the generated `.tex` file in a compatible LaTeX editor. The source uses the standard [`elsarticle`](https://ctan.org/pkg/elsarticle) preprint class (12-point, single column) and Latin Modern text and math fonts. Its footer identifies an unreviewed preprint; it does not name a journal. A local PDF export additionally requires Tectonic with its required resources available:

```sh
python3 scripts/build_paper.py --pdf
```

The primary paper PDF is supplied separately with the deposit. The archive also includes the source-integrity checker and release packaging script.

## Reference screening

Reference metadata was screened using [RefChecker](https://github.com/markrussinovich/refchecker) 3.1.6. Its final scan checked 28 references with no errors, warnings, or unverified entries. No LLM or paid web-search checks were enabled. See `validation/refchecker/README.txt` for scope and the relationship between the scan and this release.

To reproduce the online check, install Python 3.11 or newer and the pinned requirements in an isolated environment:

```sh
python3.11 -m venv .venv-refchecker
.venv-refchecker/bin/python -m pip install -r requirements-refchecker.txt
python3 scripts/build_paper.py --check-references
```

The check requires network access; findings depend on live scholarly databases and require review. The offline checks remain available:

```sh
python3 scripts/check_project.py
python3 scripts/test_check_references.py
```

## License and assistance

The paper and these original supporting materials are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); see `LICENSE.md`. Third-party sources retain their own rights.

OpenAI Codex assisted literature discovery, manuscript drafting, generation of illustrative code, and internal critical review. Reference metadata was screened with RefChecker 3.1.6, and automated findings were reviewed against publisher and other primary-source records. The author is responsible for the manuscript's content, references, and conclusions.
