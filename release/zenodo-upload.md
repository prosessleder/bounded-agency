# Zenodo upload package

Prepared for a direct preprint upload. No Zenodo record or DOI has been created.

## Files

Upload `bounded-agency-v0.1.0-preprint.pdf` as the primary paper. Optionally add `bounded-agency-v0.1.0-preprint-research.zip` as a scientific supplement containing manuscript sources, bibliography, illustrative code/schema/output, and build instructions. `SHA256SUMS.txt` identifies the bytes.

## Record fields

Use `zenodo-upload-metadata.json` as a field-by-field aid for the deposit form.

- Resource type: Publication → Preprint.
- Title: Bounded Agency: Ontology-Driven Authority for Delegated Intelligence.
- Creator: O'Brien, Timothy. ORCID: [0009-0001-2589-347X](https://orcid.org/0009-0001-2589-347X). Leave affiliation blank.
- Version: 0.1.0-preprint.
- Date: use the actual deposit publication date. The manuscript is dated 12 October 2026.
- Description: supplied abstract, conceptual preprint/not peer reviewed status, and the factual AI-use disclosure in the metadata document.
- Keywords: supplied in the metadata document.
- Access: choose public paper files when ready; the GitHub repository is already public.
- Rights: select **Creative Commons Attribution 4.0 International (CC BY 4.0)**, matching the PDF notice, `LICENSE.md`, and the metadata rights field. License identifier: `CC-BY-4.0`; Zenodo license ID: `cc-by-4.0`.

Zenodo requires a license and defaults to CC BY 4.0; its interface also supports custom licenses. See [official license instructions](https://help.zenodo.org/docs/deposit/describe-records/licenses/). CC BY permits sharing and adaptation with attribution, including commercial reuse; see [the official deed](https://creativecommons.org/licenses/by/4.0/).

## Deposit

Create a new upload, attach the files, fill the record fields, and save the draft. Check that the author details, disclosures, and license match the manuscript. Publish when ready. Zenodo assigns a DOI on publication; reserve one beforehand through the deposit interface if you want it printed in the PDF. See [official quick start](https://help.zenodo.org/docs/get-started/quickstart/).

After publication, record the version DOI in `CITATION.cff`, the README, and the manuscript metadata. If paper files change, create a new record version; metadata-only corrections follow Zenodo's edit workflow. Use the specific version DOI when citing a fixed preprint. See [official versioning guidance](https://zenodo.org/help/versioning).

The record description includes the manuscript's AI-assistance disclosure. See [Zenodo's guidance for AI-assisted deposits](https://support.zenodo.org/help/en-gb/13/227).
