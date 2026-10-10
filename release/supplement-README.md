# Bounded Agency: supplementary materials

Timothy O'Brien · 0.1.0-preprint · 9 October 2026

ORCID: [0009-0001-2589-347X](https://orcid.org/0009-0001-2589-347X).

This archive accompanies *Bounded Agency: Ontology-Driven Authority for Delegated Intelligence*. It contains the paper's sources and a finite illustration of how a changed taxonomy or accepted classification can affect decision eligibility while live admission remains bound to an approved version.

## Contents

| File | Purpose |
| --- | --- |
| `paper.md` | Manuscript source |
| `references.md` | Selected bibliography |
| `output/pdf/bounded-agency.tex` | Standalone LaTeX source |
| `examples/semantic_drift.py` | Executable illustration using Python's standard library |
| `examples/change-admission.yaml` | Illustrative admission schema |
| `examples/semantic-drift-result.json` | Recorded illustration output |
| `scripts/build_paper.py` | Generate LaTeX and HTML from the manuscript |
| `release/license-notice.txt` | License notice used by the build |
| `LICENSE.md`, `CITATION.cff` | License and citation metadata |

## Run the illustration

With Python 3.9 or newer, from the extracted archive directory run:

```sh
python3 examples/semantic_drift.py
```

The output should match `examples/semantic-drift-result.json`. The program compares four fixed proposals under a finite positive taxonomy. It distinguishes candidate eligibility from current version-bound operational admission and illustrates both ontology and accepted-fact changes.

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

The primary paper PDF is supplied separately with the deposit. The project repository additionally provides a source-integrity checker and a release packaging script.

## License and assistance

The paper and these original supporting materials are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); see `LICENSE.md`. Third-party sources retain their own rights.

OpenAI Codex assisted literature discovery, manuscript drafting, generation of illustrative code, and internal critical review. The author is responsible for the manuscript's content, references, and conclusions.
