---
title: 'Bounded Agency: Ontology-Driven Authority for Delegated Intelligence'
author: "Timothy O'Brien"
orcid: 'https://orcid.org/0009-0001-2589-347X'
date: '9 October 2026'
lang: en
version: '0.1.0-preprint'
license: 'CC-BY-4.0'
license-url: 'https://creativecommons.org/licenses/by/4.0/'
---

*Preprint (not peer reviewed). Version 0.1.0-preprint.*

# Abstract

Autonomous systems may have permission to invoke an operation without having an institutional mandate to select the outcome expressed by that operation. Ontology-grounded policies can make such mandates explicit, but they introduce a change-control problem: revising classifications, relationships, or inference rules can alter what a fixed policy permits. This paper examines bounded agency as delegated independent judgment constrained by decision scope, consequences, and an admitted semantic basis. It separates domain ontology, situation facts, evidence, decision policy, execution permission, and authority to promote semantic changes. A lightweight model separates a candidate eligibility envelope from live admission and defines a policy-relative expansion test; a positive-taxonomy counterexample shows how a subclass axiom enlarges that envelope without editing policy text. A reference architecture connects change-impact assessment, explicit authority ratification, version-bound decision admission, and mediated execution. Insurance and customer-support thought experiments illustrate both semantic expansion and changes to facts that require different controls. Building on semantic-policy and ontology-evolution research, the contribution is a design synthesis centered on authority-relative semantic-change admission. The cases and finite taxonomy illustration are explanatory; operational effectiveness remains to be evaluated.

**Keywords:** bounded agency; delegated intelligence; decision authority; ontology evolution; semantic policy; agent governance; authority-sensitive change.

# 1. Introduction

Consider a claims-processing agent with credentials that permit updates to a claim record. Its assigned task is to identify missing documentation. The same update endpoint accepts a final disposition field. A technically valid request setting that field to `denied` may exceed the agent's mandate, even if authentication and a coarse operation-level permission check succeed. An institution has delegated one kind of judgment and the software has exercised another.

This is a configuration and modeling problem rather than evidence that authorization systems are intrinsically limited to identity and resource access. Attribute-based, relationship-based, and usage-control systems can express rich business conditions [4-6]. A final-disposition action can be modeled directly in such systems. The issue is whether the deployment represents and enforces the intended decision rights, evidence conditions, and consequences. Tool access does not supply those representations automatically.

A shared ontology can support them. Domain concepts such as claim, evidence, coverage, exclusion, disposition, and appeal provide a common language for relating a situation to a permissible decision. Yet the language itself can change. Suppose a policy permits an agent to approve routine claims. A revised ontology classifies a category not previously entailed to be routine as routine. In a deployment that adopts this revision without grant review, the policy text and tool credentials remain unchanged, while the agent can now approve more claims. The change has institutional significance because classification helps determine the extension of a delegated right.

The question examined here is: **How can an autonomous intelligence be given a bounded scope of independent judgment, grounded in a shared model of its operating world, without allowing learning or semantic evolution to silently expand its authority?** The word *silently* matters. An institution may intentionally expand a mandate. The design objective is to make a relevant expansion detectable, reviewable, and explicitly admitted, rather than to freeze knowledge or prohibit institutional change.

We call the delegated scope of independent judgment *bounded agency*. The proposed distinctions concern which decisions an agent may settle, which consequences it may authorize, and which representations it may promote into the basis for those decisions. They do not purport to constrain every concept entertained inside a language model.

The paper makes three contributions. First, it gives an explicit comparison target for changes to the effective permissible-decision set under a fixed policy and controlled context. Second, it connects that comparison to a proposed semantic-change admission procedure and a version-bound decision envelope. Third, it develops two operational thought experiments that distinguish ontology revisions from ordinary facts and classification assertions. These contributions are architectural proposals and explanatory formalization. They build on established authorization and semantic-change mechanisms; their operational benefits require evaluation.

# 2. Related work

## 2.1 Scope of comparison

This comparison draws on targeted searches of primary papers, official specifications and documentation, and references from closely related work. Coverage is selective rather than systematic. Recent preprints and live specifications are discussed as proposals, not independently validated systems. The bibliography identifies the versions examined. For the enterprise framework [14], publisher-indexed passages were accessible, but complete direct retrieval was limited.

## 2.2 Semantic policy and institutional meaning

KAoS provides ontology-based policy specification, analysis, management, and enforcement for agents and distributed services [1, 23]. Rei connects policy rules to domain ontologies and supports permissions, obligations, delegation, and revocation [2, 28]. These frameworks establish ontology-grounded agent-policy specification, management, and enforcement.

Normative multiagent-system research supplies a closely related conceptual foundation. Boella and van der Torre distinguish regulative norms from constitutive rules that determine what counts as an institutional fact [3]. Classification can therefore carry normative consequences, and authority over institutional rules is not reducible to an agent's ability to act. Jones and Sergot also distinguish institutional power from permission and practical possibility [25]. The category-expansion example applies this established relationship to semantic-change admission.

ODRL specifies permissions, prohibitions, duties, constraints, and parties [9]. OWL supplies formal ontology constructs and entailment semantics [10]; SHACL supplies graph validation against shapes [11]. None of those specifications alone establishes the legitimacy of a business decision. They are usable components whose normative significance depends on the institution's policy and implementation.

## 2.3 Authorization, delegation, and enforceable behavior

ABAC evaluates attributes of subjects, objects, operations, and environment [4]; Zanzibar demonstrates relationship-based authorization at scale [5]; UCON integrates authorizations, obligations, conditions, and mutable attributes with ongoing usage control [6]. Cedar provides a policy language, evaluator, and formal analysis facilities [7]. OPA separates policy decisions from application code [8]. Thus independent decision evaluation and rich contextual authority conditions are established capabilities.

The decision-rights literature separates management of a decision from its ratification and monitoring [21]. This supports treating evidence gathering, proposing an outcome, approving it, and executing it as different assignments. It does not imply that an agent becomes the legal bearer of accountability when it receives a software role.

Runtime enforcement is also established. Schneider's analysis concerns the security properties enforceable by execution monitors [20]. Our enforcement claims are correspondingly limited to represented, mediated operational behavior. An evaluator cannot inspect or prohibit all private inference, nor can a gate prevent effects that bypass it.

## 2.4 Semantic evolution and recent governed agents

Ontology-evolution research already investigates preservation and change impact. Conservative extensions and inseparability provide formal ways to ask whether relevant consequences or queries change [12]. Security co-evolution work uses ontology change patterns to detect security impact and propose adaptations [13]. The effective-authority comparison proposed here is therefore an application-specific target for established change-analysis techniques, rather than a new general theory of semantic difference. Lopes and colleagues already propagate permission annotations across RDF inference premises [24], illustrating why classification and its evidential basis belong in the comparison.

Recent work addresses related governance boundaries. Jørgensen and Ma combine enterprise semantics, contextual knowledge, process orchestration, decision authority, execution control, and provenance in a bounded-autonomy framework [14]. AgentBound separates behavioral and semantic constraints and binds action governance to versioned artifacts [15]. The Authority Resolution Framework models contextual authority and provenance through an ontology [16]. Agent libOS separates evolving action surfaces from admission authority [17], and AgentFlow addresses delegated task scope, runtime monitoring, and bounded policy verification [18]. Salas specifies commit-time authority checks over changing normative and model dependencies [19]. These works overlap with important parts of the proposed architecture, although they differ in emphasis and evidence.

An undated live artifact-evolution specification also separates proposals, qualified approval, immutable versions, realization, and declared semantic comparison coverage [22]. Its public text is relevant overlap, but the review does not establish its historical priority.

The focus here is an explicit permissible-decision-set comparison and its connection to mandate ratification, including the distinction between ontology revisions and fact admission. The paper develops a synthesis and specialization of the mechanisms above; it makes no claim of priority for ontology-based agent governance or for the combination as a whole.

# 3. Delegation and the dimensions of bounded agency

## 3.1 Four distinctions

*Delegated intelligence* emphasizes the relationship between a system and the human or institution entrusting it with work. It complements rather than replaces a technical description of artificial intelligence. A delegation can assign a problem, access, interpretation, choice among outcomes, execution, investigation, or adaptation. Those assignments need not travel together. Authenticated delegation and intelligent-delegation research already addresses task scope and the transfer of authority and responsibility [26, 27].

We distinguish four operational concepts:

1. **Capability:** the computation or operation the system can technically perform. Capability does not establish reliable competence.
2. **Execution permission:** authorization to invoke an operation on a resource. A sophisticated implementation may already condition this permission on business meaning.
3. **Decision authority:** a delegated institutional right to select, approve, or initiate a specified outcome under stated conditions.
4. **Semantic authority:** a right to promote a representation or inference regime into the authoritative basis of operational decisions.

*Semantic authority* is preferable here to *epistemic authority*. The latter can refer to credibility, expertise, or entitlement to believe. Our concern is narrower: whether an ontology axiom, mapping, classifier output, or evidence-admission rule is approved for operational use. Approval does not make it true. Similarly, a passing policy evaluation is an implementation's representation of a mandate, not proof of ethical or legal legitimacy.

Responsibility and accountability remain distinct from these permissions. An agent may be assigned to produce a recommendation; a designated institutional role may remain responsible for ratifying it and answering for its consequences. The architecture must identify that role rather than rely on a statement that the agent is accountable.

## 3.2 Scope, constraints, and admitted semantic basis

The first dimension is **decision scope**: subjects and decision classes entrusted to the agent. Documentation completeness and fraud determination are different decision classes even if both concern the same claim.

The second is **decision constraints**: permitted outcomes, conditions, and consequences. An agent may recommend a denial while lacking authority to finalize it. Amount, jurisdiction, recipient, appeal opportunity, evidence freshness, and cumulative exposure may constrain an otherwise permitted class.

The third is **the admitted semantic basis**: which formal representations and admission rules may support those operational judgments. An agent can recognize a possible new category, preserve evidence, and propose a model change without being allowed to treat the proposal as an approved ground for action.

These dimensions interact. A taxonomy change affects scope; a changed relationship may affect an outcome condition; a new assertion can affect both without revising the ontology. They are analytical distinctions, not independent mathematical axes.

A frontier model's latent knowledge is broader than a domain ontology. We do not claim to remove that knowledge from its weights or prevent internal speculation. The enforceable boundary concerns represented proposals, admissible evidence and classifications, adopted model changes, and operational effects. Out-of-scope analysis can itself have consequences when it discloses data or produces an influential institutional record; those outputs must be represented as effects if they are to be governed.

# 4. A lightweight model of effective authority

## 4.1 Separate objects

Let $A$ identify an agent acting through an authenticated role and delegation chain. Let $O_v$ be a versioned domain ontology, $K$ a situation knowledge base, and $E$ evidence supporting assertions in $K$. Observations enter through an admission process; they are not automatically authoritative facts.

Let $P$ be the substantive decision-authority policy, $L$ the substantive delegation mandate, and $C$ the operational context, including relevant time, jurisdiction, workflow state, revocation, and previously committed consequences. Let a **semantic bundle** be

$$ B = (O_v, I, M, R, T), $$

where $I$ identifies imports, $M$ mappings and entity-resolution rules, $R$ the inference regime, and $T$ assertion-admission rules, including validators, shape versions, and classifier artifacts. A manifest identifies their immutable versions or digests. The bundle is broader than the ontology because policy interpretation can change through any of these inputs. The deployment manifest additionally identifies evaluator semantics and implementation, effect-contract versions, and trusted adapter versions; changes to these artifacts enter the same admission and freshness boundary.

A proposal is

$$ q = (d,x,y,h), $$

where $d$ is the decision class, $x$ the governed subject or subjects, $y$ the proposed outcome, and $h$ a represented effect plan. The effect plan identifies intended operations and declared consequence dependencies. It is not an oracle for every real-world consequence.

Define a **counterfactual eligibility evaluator**

$$ U(A,q;P,L,B,K,E,C) \in \{\mathsf{permit},\mathsf{deny},\mathsf{indeterminate}\}. $$

It checks substantive policy and mandate conditions, supported situation assertions, and represented consequences under the supplied bundle. For comparison, it intentionally excludes the requirement that the candidate bundle already be admitted by an active production grant. It runs in a shadow context with no authority to cause effects. Indeterminate covers missing evidence, unsupported inference, unknown classification, inconsistent inputs, or inability to resolve required conditions. Deployment rules must specify this treatment; unrestricted classical entailment from an inconsistent theory is unsuitable for a permit test.

For a fixed proposal universe $Q$, define the candidate eligibility envelope

$$ \widehat{\mathcal{H}}_{Q}(A;P,L,B,K,E,C)
= \{q\in Q \mid U(A,q;P,L,B,K,E,C)=\mathsf{permit}\}. $$

Let $G$ identify the active version-bound grant. Operational admission $V$ additionally requires that $G$ admit this exact policy, mandate, semantic and deployment basis; that the grant and evidence remain current; and that the effect can be faithfully mediated. Thus $U=\mathsf{permit}$ is necessary but not sufficient for $V=\mathsf{permit}$. A candidate $B_1$ can enlarge $\widehat{\mathcal{H}}_Q$ while remaining inadmissible for production under $G_0$.

The operational authority envelope contains only proposals permitted by $V$ under an active grant. Separating it from the candidate envelope avoids a circular change test: if the comparison already demanded ratification of the candidate, it would conceal the very prospective expansion being reviewed. Neither envelope establishes substantive correctness or institutional legitimacy.

## 4.2 Authority-relative change

Hold $A,P,L,K,E,C,Q$ fixed and compare bundles $B_0$ and $B_1$. This comparison also holds evaluator and effect-contract semantics fixed. Changes to evaluator, adapter, or effect-contract versions require a separately declared comparison or revalidation of those deployment artifacts. Define the expansion witnesses

$$ \Delta^+_Q(B_0,B_1)
= \widehat{\mathcal{H}}_Q(A;P,L,B_1,K,E,C)
\smallsetminus \widehat{\mathcal{H}}_Q(A;P,L,B_0,K,E,C). $$

A nonempty set exhibits expansion under the controlled comparison. An indeterminate proposal under the old basis becoming permitted under the new one counts as expansion. A removal set can likewise be defined by reversing the difference; lost permissions can require review even without expansion.

This definition separates semantic effects from ordinary changes in the situation. In production, $K$, $E$, and $C$ also vary. Controlled replay can compare the same snapshot to isolate the bundle's impact, while operational admission evaluates the current admitted context. Holding already-admitted $K$ fixed tests downstream interpretation only. To compare changes to $T$ or classifiers, replay the same original observations and evidence through both admission pipelines and compare their resulting situation models; this is a distinct controlled comparison. A newly eligible customer under an unchanged mandate is not necessarily a new delegation; it may be an intended application of the existing rule. A falsely admitted classification can nevertheless create an unauthorized effect. The controls on $T$, $K$, and $E$ therefore matter independently of ontology release controls.

A stronger preservation obligation would quantify over an explicitly chosen comparison family $\mathcal{W}$ of situation/evidence/context triples chosen independently of either candidate's acceptance rules:

$$ \forall(K,E,C)\in\mathcal{W},\quad
\widehat{\mathcal{H}}_Q(A;P,L,B_1,K,E,C)
\subseteq\widehat{\mathcal{H}}_Q(A;P,L,B_0,K,E,C). $$

Both $Q$ and $\mathcal{W}$ are fixed before comparison, over declared relevant input and decision signatures, including any proposed new vocabulary. That statement names the scope of the obligation; this paper supplies no general algorithm proving it. A finite replay corpus establishes preservation only over that corpus. Conservative extension over an old ontology signature is not automatically preservation over new decision vocabulary, future instances, mappings, and policy queries. The relevant signatures, data domain, and query language must be specified.

## 4.3 A restricted counterexample

Consider finite class names and individuals, positive subclass axioms, positive type assertions, and transitive classification. Fix one policy permitting approval of an individual $x$ exactly when $K\cup O$ entails `RoutineClaim(x)` and the unchanged amount/evidence/context predicates pass. There are no overriding denials, negation, inconsistent assertions, or other inference rules.

**Proposition.** For counterfactual eligibility in this fragment, adding subclass axioms cannot remove a previously permitted approval. It can add an approval without changing the policy.

**Proof.** Every existing derivation of `RoutineClaim(x)` remains available after axioms are added, and the other predicates are fixed. Therefore the permitted set cannot shrink. For strict growth, choose $K$ and $O_0$ such that $K$ contains `DeviceLossClaim(c)`, the unchanged amount/evidence/context predicates pass, and $K\cup O_0$ does not entail `RoutineClaim(c)`. Under the evaluator's stipulated positive-membership permit rule, approval of $c$ is not permitted. Add `DeviceLossClaim` subclass of `RoutineClaim` to obtain $O_1$. The new axiom derives `RoutineClaim(c)`, so approval is permitted. The policy is identical. $\square$

This is a direct consequence of monotone positive inference, not a new mathematical theorem. Non-entailment is not an OWL assertion of non-membership; the gate simply refuses to permit without the required entailment. Deny precedence, negative tests, changed evidence, inconsistent ontologies, or nonmonotonic rules invalidate the general monotonicity claim. The companion executable example demonstrates only this finite fragment.

# 5. Proposed reference architecture

## 5.1 Components and trust boundaries

The architecture has six components, with traditional IAM retaining identity, authentication, resource access, and authenticated delegation-chain responsibilities.

| Component | Responsibility | Output used by the next boundary |
|---|---|---|
| Semantic service | Serve admitted ontology, imports, mappings, inference regime, and assertion rules | Immutable bundle manifest and relevant semantic slice |
| Situation/evidence service | Admit observations, maintain facts, preserve provenance and disputed assertions | Versioned decision snapshot with evidence references |
| Authority registry | Store mandates, decision policies, approval roles, revocation and consequence rules | Versioned authority context |
| Decision evaluator | Independently check typed proposals against current authority and supported facts | Permit, deny, or indeterminate with reasons and dependencies |
| Enforcement adapter | Mediate governed operations and bind actual parameters to admitted effects | Execution or refusal plus effect receipt |
| Governance process | Review semantic and authority changes, approve releases and rollout | Separate semantic acceptance and authority-ratification records |

The semantic service need not be a single physical server or require a universal ontology. A governed domain model can be shared through a knowledge graph or registry. Agents can retrieve small slices, provided the evaluator resolves the authoritative closure and manifest rather than trusting an agent-supplied fragment to be complete. Multiagent retrieval does not imply equal grants: common meaning and delegated authority are separate.

The evaluator should be independently controlled relative to the operating agent. Policies may use decision classes, ontology predicates, state transitions, outcome constraints, evidence conditions, and delegation context. Whether those checks are implemented in Cedar, OPA, a rule engine, or a custom reasoner is a deployment choice. Using a general language model as the final evaluator requires additional evidence of reliability; calling it an independent reviewer is insufficient.

## 5.2 Decision envelopes and commit

A submitted envelope should name the authenticated role and delegation chain; mandate and policy versions; semantic and deployment manifests, including evaluator, effect-contract, and adapter versions; situation/evidence snapshot; decision class, subject, outcome, and effect plan; evidence dependencies; expiry; and an effect identity for replay and idempotency. These are proposed fields, not a new credential standard.

Before commitment, the enforcement path must confirm that the envelope is still admitted under the current grant and revocation rules. It must bind the permitted outcome to actual adapter parameters. A permission to recommend cannot authorize an adapter call that commits the recommendation as a final decision. Side effects of routing, communications, and disclosure must be included where they are institutionally governed.

A version check alone is not a transaction. A policy, evidence snapshot, or grant may change between evaluation and effect. An implementation needs a transaction, reservation, lease/fence protocol, or other explicitly analyzed mechanism that gives admission and execution defined freshness semantics. Salas already addresses closely related commit-time dependencies [19]; we adopt that engineering requirement without claiming a new concurrency protocol.

Version pinning also needs revocation. An agent cannot indefinitely retain a permissive historical bundle after the institution withdraws its grant. A migration may deliberately keep an old contract active for a defined scope, but that continued use must itself be admitted. Ordinary receipt replay explains what happened; it does not authorize a new action today.

## 5.3 Proposed invariants and their limits

The design seeks four invariants:

- Every governed effect passes a controlled enforcement path and matches an admitted proposal.
- Every permit identifies its authority and semantic basis and sufficient current evidence.
- A semantic release cannot substitute a new operational basis into a grant without the required authority review.
- An authority-sensitive change produces an explicit decision to reject, retain a defined old scope, or admit a revised grant.

These are design requirements, not established properties of an implemented system. They depend on complete mediation, credential isolation, authenticated versions, policy correctness, adequate dependency discovery, and faithful adapters. A tamper-resistant receipt can support audit while still faithfully recording a mistaken decision. Availability failures must have defined refusal behavior; safety by refusal can impose substantial operational costs.

# 6. Admission of semantic and knowledge changes

## 6.1 Different changes require different questions

Learning new facts about familiar concepts is not the same as changing the conceptual scheme. The distinction helps assign review, but it is not a reliable security boundary by itself.

| Change | Example | Appropriate control question |
|---|---|---|
| Observation or ordinary fact | Receipt received for a known claim | Is the assertion supported, current, and admitted under the existing evidence rule? |
| New instance | A new claim of an existing kind | Does normal enrollment and the existing mandate cover this instance? |
| Classification assertion | An existing claim is now marked routine | Who can attest this type, and what evidence permits operational reliance? |
| Relationship or mapping | External issue code mapped to courtesy issue | Does the mapping change policy-relevant entailments or governed subjects? |
| New class or changed definition | Device loss becomes a routine subclass | Does this alter the decisions or consequences permitted under current mandates? |
| Imports or inference settings | A reasoner begins using an additional relation rule | Does the admitted closure or evaluation behavior change? |
| Authority policy or mandate | Agent receives denial authority | Is the delegating role entitled to grant it, and has the change been explicitly ratified? |

A factual update can legitimately alter current eligibility while leaving the delegated rule unchanged. It can also improperly launder a disputed classification into a permit. Assertions that supply policy-relevant types or relationships should therefore pass an approved admission rule. They need not receive the same governance ceremony as every ontology revision.

Likewise, a new concept unrelated to any policy dependency may be harmless for a particular agent's authority. The appropriate target is authority impact relative to declared decisions and context, rather than indiscriminate approval of all learning. Impact analysis may be incomplete, so an unrelated-change verdict needs an explicit coverage claim.

## 6.2 Proposed change-review procedure

The reference procedure is:

1. **Register a proposal.** Preserve observations, evidence, proposed edits, proposer identity, and the immutable baseline. Keep proposed semantics separate from the admitted operational bundle.
2. **Resolve dependencies.** Identify relevant policies, mandates, decision classes, mappings, imports, assertion rules, and effect contracts. Use independently derived dependencies where possible; agent-declared dependencies are hints requiring validation.
3. **Compare under a stated regime.** Check logical consistency and graph conformance, then compare counterfactual eligibility under $U$ using controlled snapshots. State the proposal language, data domain, reasoner, and coverage. Seek expansion witnesses and removed permissions.
4. **Return a qualified result.** Distinguish witnessed expansion, witnessed removal, proven preservation under declared assumptions, bounded tests with no witnessed expansion, and indeterminate comparison. Do not relabel a successful regression suite as a universal proof.
5. **Obtain the required decisions.** Reviewer eligibility must be resolved under the pre-change admitted authority context; a candidate cannot create its own approver through a new class or relationship. A domain steward may accept a better ontology without possessing authority to broaden an agent's mandate. Where the policy requires it, an independently authorized role must ratify the affected grant. One person may hold both roles, but the two decisions remain explicit.
6. **Release and migrate.** Publish the admitted bundle, policy/grant versions, scope, effective time, expiry, and revocation behavior. Validate or invalidate pending proposals; retain a defined old scope only under an active grant.
7. **Monitor and retain evidence.** Preserve comparisons, approval reasons, admitted envelopes, and effect receipts. Observe unexpected classifications and effects, and route them to investigation.

The policy for approving a semantic release is itself a governed policy. Shadow comparison is read-only with respect to governed effects and cannot issue an execution grant. An operating agent must not be able to alter that rule or attest its own eligibility merely by proposing a new ontology relation. Escalation should not fall back to a permissive mode when the reviewer is unavailable.

## 6.3 Knowledge growth without automatic authority growth

The statement “an agent may expand its knowledge without automatically expanding its authority” is a design principle consistent with established separation of duties and admission controls. It does not imply that all facts leave the effective permit set unchanged. Facts are supposed to change decisions when a mandate is conditional on them.

The principle instead separates acquiring information, proposing or investigating a representation, approving its operational adoption, and renewing an affected delegation. An agent may record a candidate category in a nonauthoritative investigation store. It may use that candidate to explain an uncertainty or propose a review. No unadmitted semantic premise may discharge a required permit condition. The candidate can appear as a labeled hypothesis in a review submission, without supplying operational authorization.

Version binding alone prevents accidental substitution only if the bound bundle remains the evaluated basis and the grant is current. It does not decide whether the next bundle should be adopted. Authority-relative comparison serves that admission decision, while the execution gate enforces the admitted result.

# 7. Insurance-claims thought experiment

## 7.1 Initial mandate

All policy choices in this example are synthetic. They are not insurance law or recommendations for claims handling.

An insurer uses an ontology with `Claim`, `RoutineClaim`, `DeviceLossClaim`, `Policy`, `Coverage`, `Exclusion`, `Evidence`, `Disposition`, and `Appeal`. An agent may collect documentation and classify document completeness. It may recommend an outcome for review. It may approve a routine claim of at most 500 units when coverage and loss evidence have been independently attested. It may never autonomously finalize a denial or a fraud finding. A designated adjuster ratifies those outcomes.

The record-update API can technically write documentation status, recommendations, approvals, and denials. Its credentials are brokered through an adapter. The decision evaluator checks the decision class and actual resulting transition. A completeness check is admitted as a documentation update; it cannot carry a hidden final disposition. Reading a claimant's history is governed access and does not confer fraud-adjudication authority.

Recommendations are not automatically harmless. If a downstream workflow routinely treats a denial recommendation as final unless a reviewer interrupts it, the effect contract must represent that default. Labeling the decision a recommendation does not justify avoiding ratification.

## 7.2 Semantic expansion

A claim $c$ has type `DeviceLossClaim`, an amount of 300, and sufficient supported coverage/evidence facts. Under $O_0$, device-loss claims are not known to be routine; the positive-membership gate therefore refuses autonomous approval. The agent can preserve evidence and escalate.

An improvement process proposes the axiom

$$ \mathsf{DeviceLossClaim}\sqsubseteq\mathsf{RoutineClaim}. $$

Under $O_1$, the unchanged routine-approval policy permits approval of $c$. The shadow comparison has a concrete witness: the same subject, evidence, amount, decision, and substantive policy change from non-permit to permit under $U$. This is prospective eligibility expansion, while the active grant remains bound to $B_0$. The institution may welcome the result; operational adoption requires ratification before $V$ can admit the expanded scope.

An ungoverned deployment might replace the ontology service's current content and continue using the policy as before. The proposed architecture instead retains the operating grant's admitted $B_0$ until the release decision is complete. The change assessor reports the witness and identifies other affected decisions. The domain steward evaluates the classification; the authorized claims role decides whether routine-approval delegation should now include device loss. Approval results in an explicit grant bound to $B_1$. If the institution rejects the delegation change, it can retain a compatible restricted contract or amend the policy before releasing the new operational basis.

Pinning an ontology name such as `current` is insufficient. Pinning the policy text while permitting the type hierarchy to drift is also insufficient. A grant must name the evaluated semantic basis. Conversely, listing an allowed parent class without controlling the meaning of descendant membership does not freeze its effective scope.

## 7.3 A fact-level alternative

Suppose the ontology remains $O_0$ but an agent writes `RoutineClaim(c)` into the situation store. The same policy can now permit approval. This is not ontology evolution. It is an assertion-admission problem.

The approved rule must identify who can attest routine status and from which evidence. If the operating agent is permitted only to classify completeness, its self-issued routine assertion cannot become an accepted premise for approval. New genuine routine instances may enter through the existing attestation procedure without requiring a revised ontology or a new delegation. This distinction allows operational learning while controlling policy-relevant assertions.

# 8. Customer-support thought experiment

## 8.1 Access, judgment, and consequences

A support agent can access customer records and issue a courtesy credit of at most 25 units for an attested `CourtesyEligibleIssue`. Its mandate excludes contract termination, fraud classification, and modification of contractual entitlements. It can propose those outcomes to a designated reviewer.

Access to a customer's subscription and payment history does not itself confer authority to cancel that subscription or label the customer fraudulent. If the tool exposes both credit and cancellation operations, the evaluator must distinguish those outcomes. Credit limits must also consider accumulated effects: four nominally allowed credits can violate a 25-unit per-incident limit. The relevant context includes previous credits and incident identity. Entity resolution and aggregation are part of the governing basis, not optional audit details.

The agent encounters duplicate renewals caused by a migration. The current issue model has no adequate category. It records the observations and proposes `MigrationDuplicateRenewal`. It may explain the mismatch to the improvement function. Until adopted through the required process, the proposed class does not justify an autonomous credit or a change to subscription status.

## 8.2 Change, review, and an allowed resolution

The improvement function proposes to place `MigrationDuplicateRenewal` beneath `CourtesyEligibleIssue`. For a taxonomy-only comparison, the change assessor fixes customer/evidence snapshots that include a supported `MigrationDuplicateRenewal` classification for the affected incidents, alongside fixed credit proposals. This candidate classification is available only for shadow analysis until operationally admitted. If the classifier or assertion-admission rule also changes, the original observations must instead be replayed through both admission pipelines, as described in Section 4.2. Credits previously refused because courtesy eligibility was not established become permitted under the new hierarchy. In addition, some duplicate charges exceed 25 units. The semantic expansion witness and amount constraint are different findings: new class membership does not remove an outcome ceiling.

A reviewer may adopt the new descriptive class while deciding that these cases require billing reconciliation rather than courtesy compensation. The domain ontology can correctly represent the issue without delegating its resolution to the support agent. Another deployment may explicitly authorize credits up to the existing ceiling, with larger corrections escalated. In either case, operational use follows a grant bound to the approved model, evidence rule, and policy.

An external ticket code mapping can cause the same problem without adding a class. If a new source code maps to courtesy eligibility, its effect on the policy query must be evaluated. An unsupervised classifier assigning courtesy status can also change current permits. All three mechanisms require control, but they need different owners and evidence.

## 8.3 Costs and failure cases

Conservative refusal delays some legitimate service. A narrow taxonomy can encode institutional blind spots, and an approval queue can preserve them. The architecture should therefore provide a clear unknown-category route, preserve contrary evidence, allow authorized exception decisions, and measure review burden. Bounded agency must not become a rationale for suppressing observations that challenge the model.

Nor does approval solve representation errors. A mistaken equivalence, misleading source mapping, fabricated receipt, or incomplete consequence contract can lead a deterministic evaluator to an incorrect permit. The system needs domain validation and monitoring in addition to formal consistency. Shared meanings can propagate a mistake across many agents, making governed semantic releases valuable and consequential at the same time.

# 9. Develop, operate, and improve

A shared semantic basis can support three functions with different grants.

**Develop** implements capabilities and adapters against an identified model and policy contract. Its permission to modify code or author test data does not entail permission to release production semantics, rewrite live mandates, or commit domain decisions. Development output remains a proposed artifact until the release authority admits it.

**Operate** interprets admitted situations and proposes or executes decisions within the active contract. It can collect observations and report mismatches. It cannot grant itself a broader decision class or make a candidate ontology extension authoritative simply because the extension appears useful.

**Improve** investigates failures and gaps, compares alternatives, and proposes changes. It can have a broader research scope than the operating function while retaining narrower authority over effects. Discovery of a new category, a successful test, or a persuasive diagnosis does not itself approve adoption.

An orchestrator or another authorized mechanism governs transitions between these functions. They may be different agents, services, teams, or roles in one platform; naming three agents does not establish separation of duties if they share unrestricted credentials. The full develop/operate/improve lifecycle is outside this paper's scope. Here it shows why access to a common ontology need not imply a common authority envelope.

# 10. Discussion and future work

## 10.1 Relationship to existing mechanisms

The architecture combines established semantic authorization, normative modeling, ontology-change analysis, and version-bound enforcement [1-3, 12-19, 22]. Its organizing question is: *Does a candidate semantic change alter the decisions eligible under a stated delegation and comparison domain, and which role may ratify that effect?* The comparison target makes the effect of a semantic change explicit, while the admission procedure connects that effect to a designated authority. The taxonomy example illustrates this relationship in a restricted fragment; it does not establish a general preservation theorem.

A typed schema, curated decision table, state machine, or existing policy data model may represent a narrow domain more cheaply than an ontology. The ontology proposal is appropriate when shared relations and inference make policy interpretation depend on evolving meaning. It should be compared with simpler representations rather than treated as a mandatory foundation for every agent.

## 10.2 Technical and institutional limits

The formal model is relative to represented proposals, evidence, and consequences. It cannot certify that the institution's mandate is legitimate, that classifications are fair, or that the admitted evidence is true. Classical ontology consistency and SHACL conformance do not establish these claims.

Complete mediation may be infeasible across legacy tools and external workflows. Direct credentials, unmodeled notification effects, and data disclosed during retrieval can bypass a final write gate. Multiagent composition creates additional problems: individually allowed proposals can combine into an unauthorized outcome. Trace and aggregate constraints need state, concurrency control, and clearly attributed effects.

The semantic comparison problem can be expensive or undecidable for sufficiently expressive languages and open domains. Extracted dependencies can be incomplete. A narrower sound approximation may refuse benign changes; a broader heuristic may miss harmful ones. An indeterminate result must remain visible, with a policy defining which authority may accept the residual uncertainty.

Institutions can also approve an overbroad grant. Separating approval roles supports accountability; it does not guarantee prudent judgment. Evidence disputes, appeal, jurisdiction, and override procedures require domain-specific governance that this paper does not supply.

## 10.3 What an implementation study should test

A future study should compare four configurations on the same workflows and evidence: resource/operation permission checks alone; an explicit business-decision policy gate; that gate with version-bound semantics and current grants; and that gate with authority-relative semantic-change review. Baselines must be configured competently, since otherwise the study merely compares careful modeling with a deliberately weak system.

Tests should include subclass additions, equivalence and mapping changes, ordinary new instances, disputed type assertions, imported rules, reasoner changes, unrelated ontology edits, expired grants, concurrent releases, stale evidence, bypass credentials, cumulative credits, and recommendations that downstream systems finalize. Report expansion witnesses, unauthorized effects, false refusals, review workload, latency, and recovery separately. A bounded executable example does not constitute an experiment on agent reliability or a deployment evaluation.

Future work should specify a decidable comparison fragment, implement a change assessor, validate the mandates, and compare detection accuracy and cost against strong existing semantic-policy and ontology-change controls. These comparisons should establish whether the additional review detects consequential authority expansions at acceptable cost.

# 11. Conclusion

Delegated intelligence needs an explicit account of which judgments and consequences an institution has entrusted to it. An independently governed shared ontology can help express that account, while ontology revisions, mappings, admitted assertions, and inference choices can also change its effective scope. A policy can remain textually identical as the decisions it permits expand.

Bounded agency, as developed here, separates acquiring or proposing knowledge from adopting an authoritative operational basis and renewing affected decision rights. The proposed architecture pairs authority-relative semantic comparison with explicit ratification, current version-bound admission, and mediated effects. Future evaluation should test whether this obligation detects consequential semantic changes beyond existing controls and measure review burden and runtime cost.

# Declarations

**Nature of the work.** This is a conceptual design study. The cases and finite taxonomy illustration are synthetic thought experiments. No human-subject study, production deployment, or agent-performance experiment was conducted.

**Research artifacts.** Manuscript sources, the executable finite-taxonomy illustration, its recorded output, and an example change-admission schema are available in the supplementary archive and [project repository](https://github.com/prosessleder/bounded-agency).

**AI assistance.** OpenAI Codex assisted literature discovery, manuscript drafting, generation of illustrative code, and internal critical review. The author is responsible for the manuscript's content, references, and conclusions.
