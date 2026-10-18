# Changes in 0.1.2-preprint

This revision follows a consistency review against the semantic/evidence distinctions developed in subsequent research. It introduces no new model measurements and makes no claim that unfinished research validates a deployed architecture.

- **Schema identifier correction:** the expansion witness in `examples/change-admission.yaml` now uses `sensor-anomaly`, the actual proposal identifier in the recorded executable result. The earlier schema used a different illustrative label without declaring its mapping.
- **Conflict semantics (§4.1):** inconsistency is no longer listed as if it automatically makes every decision indeterminate. The revised text requires an explicit conflict policy, preserves decisions established by unaffected facts, and excludes vacuous permission when no admissible interpretation exists. This clarifies the abstract evaluator; the Boolean illustration still does not implement a full conflict reasoner.
- **Authority and evidence (§3.1):** authority to adopt a semantic or evidence policy is distinct from warrant to accept a claim. Approval does not establish source truth or independence.
- **Composition (§4.4 and §6.2):** comparison must cover the complete proposed change. For sequential admission, relevant prefixes need checking. The new finite control demonstrates two individually non-expanding edits whose combination creates an expansion, on the same four proposals.

The monotonic positive-taxonomy proposition remains unchanged under its stated assumptions. Its proof does not extend to arbitrary conflicts, negation, evidence policies or full deployments. Existing controls for removals, mixed changes, grants, revocation and admitted facts remain intact.

The bibliography is byte-identical to the previous version. The 15 October reference metadata scan remains historical evidence; no new online scan or external peer review is claimed. Previous deposited PDFs, supplements and metadata are preserved byte-for-byte. Version-specific new files do not replace the files attached to DOI 10.5281/zenodo.23401477.
