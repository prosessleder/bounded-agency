#!/usr/bin/env python3
"""Finite positive-taxonomy illustration for paper §4.3; no LLM or deployment.

The hypothetical evaluator excludes active-grant binding. Actual authorization
requires it. Each proposal closes one incident; no physical safety is certified.
No general OWL, negation, conflict precedence, legal rule, or safety proof.
"""
from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Basis:
    version: str
    subclasses: frozenset[tuple[str, str]]


@dataclass(frozen=True)
class Case:
    identity: str
    types: frozenset[str]
    within_assigned_site: bool
    evidence_attested: bool  # Provenance/completeness, not safety clearance.


def inferred_types(case: Case, basis: Basis) -> frozenset[str]:
    closure = set(case.types)
    while True:
        expanded = closure | {parent for child, parent in basis.subclasses if child in closure}
        if expanded == closure:
            return frozenset(closure)
        closure = expanded


def eligible(case: Case, basis: Basis) -> bool:
    """Counterfactual U: same substantive mandate/evidence, candidate semantics."""
    return (
        'RoutineNotice' in inferred_types(case, basis)
        and case.within_assigned_site
        and case.evidence_attested
    )


def authorized_to_act(case: Case, basis: Basis, active_grant_basis: str, revoked=False) -> bool:
    """Toy V: candidate eligibility alone cannot grant operational authority."""
    return not revoked and basis.version == active_grant_basis and eligible(case, basis)


def demonstration() -> dict:
    initial = Basis('B0', frozenset({('ServiceNotice', 'RoutineNotice')}))
    revised = Basis('B1', initial.subclasses | {('SensorAnomaly', 'RoutineNotice')})
    unrelated = Basis('B-unrelated', initial.subclasses | {('MaintenanceLog', 'Document')})
    removed = Basis('B-removal', frozenset())
    replaced = Basis('B-replacement', frozenset({('SensorAnomaly', 'RoutineNotice')}))
    cases = (
        Case('routine-service', frozenset({'ServiceNotice'}), True, True),
        Case('sensor-anomaly', frozenset({'SensorAnomaly'}), True, True),
        Case('other-site', frozenset({'SensorAnomaly'}), False, True),
        Case('missing-evidence', frozenset({'SensorAnomaly'}), True, False),
    )
    permitted = lambda basis: {c.identity for c in cases if eligible(c, basis)}
    before, after = permitted(initial), permitted(revised)
    assert before == {'routine-service'}
    assert after == {'routine-service', 'sensor-anomaly'}
    assert before <= after  # Exact only for these four enumerated candidates.
    assert permitted(unrelated) == before
    removal_after = permitted(removed)
    replacement_after = permitted(replaced)
    assert removal_after == set()
    assert before - removal_after == {'routine-service'}
    assert replacement_after - before == {'sensor-anomaly'}
    assert before - replacement_after == {'routine-service'}
    # Separately non-expanding edits can enable each other when composed.
    first = Basis('B-first', initial.subclasses | {('SensorAnomaly', 'ReviewCategory')})
    second = Basis('B-second', initial.subclasses | {('ReviewCategory', 'RoutineNotice')})
    combined = Basis('B-combined', first.subclasses | second.subclasses)
    assert permitted(first) == permitted(second) == before
    assert permitted(combined) - before == {'sensor-anomaly'}
    anomaly = cases[1]
    assert not authorized_to_act(anomaly, revised, 'B0')
    assert authorized_to_act(anomaly, revised, 'B1')
    assert not authorized_to_act(anomaly, revised, 'B1', revoked=True)
    assert not authorized_to_act(cases[2], revised, 'B1')
    assert not authorized_to_act(cases[3], revised, 'B1')
    # Fixed ontology, changed accepted type fact: different admission question.
    classified = Case('sensor-anomaly', anomaly.types | {'RoutineNotice'}, True, True)
    assert eligible(classified, initial)
    return {
        'scope': 'four fixed cases, positive finite taxonomy, one fixed incident-closure policy',
        'before_shadow_eligible': sorted(before),
        'after_shadow_eligible': sorted(after),
        'expansion_witnesses': sorted(after - before),
        'removed': sorted(before - after),
        'case_evaluations': [
            {'proposal': c.identity, 'eligible_B0': eligible(c, initial),
             'eligible_B1': eligible(c, revised)} for c in cases
        ],
        'removal_only_revision': {
            'expansion_witnesses': sorted(removal_after - before),
            'removal_witnesses': sorted(before - removal_after),
            'non_expansion_on_fixed_cases': removal_after <= before,
            'permit_set_equivalence_on_fixed_cases': removal_after == before,
        },
        'replacement_revision': {
            'expansion_witnesses': sorted(replacement_after - before),
            'removal_witnesses': sorted(before - replacement_after),
        },
        'composition_control': {
            'first_edit_expansion_witnesses': sorted(permitted(first) - before),
            'second_edit_expansion_witnesses': sorted(permitted(second) - before),
            'combined_expansion_witnesses': sorted(permitted(combined) - before),
            'coverage': 'same four fixed proposals only; not a general preservation proof',
        },
        'unrelated_revision_changes_eligibility': permitted(unrelated) != before,
        'candidate_authorized_under_old_grant': authorized_to_act(anomaly, revised, 'B0'),
        'candidate_authorized_after_ratification': authorized_to_act(anomaly, revised, 'B1'),
        'revoked_grant_authorizes_action': authorized_to_act(anomaly, revised, 'B1', revoked=True),
        'accepted_type_fact_can_change_fixed_ontology_eligibility': eligible(classified, initial),
        'limitations': 'illustration only; no safety-clearance verification, production mediation, authenticity, concurrency, or general entailment',
    }


if __name__ == '__main__':
    print(json.dumps(demonstration(), indent=2))
