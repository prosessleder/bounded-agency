#!/usr/bin/env python3
"""Finite positive-taxonomy illustration for paper §4.3; no LLM or deployment.

The shadow evaluator excludes active-grant binding. The live gate requires it.
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
    amount: int
    evidence_attested: bool


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
        'RoutineClaim' in inferred_types(case, basis)
        and 0 <= case.amount <= 500
        and case.evidence_attested
    )


def live_permit(case: Case, basis: Basis, active_grant_basis: str, revoked=False) -> bool:
    """Toy V: candidate eligibility alone cannot grant operational authority."""
    return not revoked and basis.version == active_grant_basis and eligible(case, basis)


def demonstration() -> dict:
    initial = Basis('B0', frozenset({('BasicClaim', 'RoutineClaim')}))
    revised = Basis('B1', initial.subclasses | {('DeviceLossClaim', 'RoutineClaim')})
    unrelated = Basis('B-unrelated', initial.subclasses | {('Receipt', 'Document')})
    cases = (
        Case('ordinary', frozenset({'BasicClaim'}), 100, True),
        Case('device', frozenset({'DeviceLossClaim'}), 300, True),
        Case('too-large', frozenset({'DeviceLossClaim'}), 600, True),
        Case('missing-evidence', frozenset({'DeviceLossClaim'}), 300, False),
    )
    permitted = lambda basis: {c.identity for c in cases if eligible(c, basis)}
    before, after = permitted(initial), permitted(revised)
    assert before == {'ordinary'}
    assert after == {'ordinary', 'device'}
    assert before <= after  # Exact only for these four enumerated candidates.
    assert permitted(unrelated) == before
    device = cases[1]
    assert not live_permit(device, revised, 'B0')
    assert live_permit(device, revised, 'B1')
    assert not live_permit(device, revised, 'B1', revoked=True)
    assert not live_permit(cases[2], revised, 'B1')
    assert not live_permit(cases[3], revised, 'B1')
    # Fixed ontology, changed accepted type fact: different admission question.
    classified = Case('device', device.types | {'RoutineClaim'}, 300, True)
    assert eligible(classified, initial)
    return {
        'scope': 'four fixed cases, positive finite taxonomy, one fixed approval policy',
        'before_shadow_eligible': sorted(before),
        'after_shadow_eligible': sorted(after),
        'expansion_witnesses': sorted(after - before),
        'removed': sorted(before - after),
        'unrelated_revision_changes_eligibility': permitted(unrelated) != before,
        'candidate_live_permit_under_old_grant': live_permit(device, revised, 'B0'),
        'candidate_live_permit_after_ratification': live_permit(device, revised, 'B1'),
        'revoked_grant_live_permit': live_permit(device, revised, 'B1', revoked=True),
        'accepted_type_fact_can_change_fixed_ontology_eligibility': eligible(classified, initial),
        'limitations': 'illustration only; no production mediation, authenticity, concurrency, or general entailment',
    }


if __name__ == '__main__':
    print(json.dumps(demonstration(), indent=2))
