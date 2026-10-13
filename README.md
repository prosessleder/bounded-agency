# Bounded Agency

**Ontology-Driven Authority for Delegated Intelligence**

Timothy O'Brien · Initial conceptual preprint · 12 October 2026 · v0.1.0-preprint

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
| [release/bounded-agency-v0.1.0-preprint-research.zip](release/bounded-agency-v0.1.0-preprint-research.zip) | Curated scientific supplement: sources, examples, and reproducibility instructions |
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

The illustration exhaustively compares four fixed candidates in a finite positive taxonomy. It distinguishes shadow eligibility from current version-bound authorization and shows both ontology and accepted-type-fact paths. It is neither an LLM experiment nor a production implementation.

The recorded controls also distinguish a removal-only revision (non-expansion without permit-set equivalence) from a replacement revision that both adds and removes permits. These results cover the four enumerated proposals only.

## Publication status and rights

Published on [Zenodo](https://zenodo.org/records/23332953) as a conceptual preprint, version 0.1.0-preprint, on 12 October 2026. Version DOI: [10.5281/zenodo.23332953](https://doi.org/10.5281/zenodo.23332953). The paper has not been peer reviewed.

The PDF and research ZIP in `release/` are the exact deposited files. The ZIP preserves the sources and citation metadata as they stood before DOI assignment; the current `CITATION.cff` supplies the assigned DOI. The packaging script verifies this published release without overwriting it. Changes to the manuscript or supplement require a new release version.

The paper and original supporting materials are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/); see [LICENSE.md](LICENSE.md) for scope. Linked third-party sources retain their own rights.
