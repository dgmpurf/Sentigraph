# LLM Semantic Annotation Schema v1

Status: planned / docs-only

This document defines the schema contract for future semantic annotations over sanitized EvidenceItem text. It does not implement a real LLM provider and does not enable external calls.

## 1. Schema Table

| Field | Type | Required | Allowed values / example | Downstream use | Affects weight? | Requires human review? | User-facing allowed? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| annotation_version | string | yes | llm_semantic_annotation_v1 | Reproducibility and validation | no | no | no |
| evidence_id | string | yes | evidence_example_id | Join annotation to EvidenceItem | no | no | no |
| mode | string | yes | mock_default, future_llm_provider, human_reviewed | Display and audit boundary | no | yes if future provider | yes |
| stance_hint | string | yes | support, neutral, oppose, mixed, unclear | Camp distribution feature | yes, as input feature only | yes if low confidence | yes |
| emotion_hint | string array | yes | anger, frustration, disappointment, sarcasm, fear, distrust, explanation, curiosity, fatigue, reconciliation, neutral, unclear | Sentiment and response tempo features | yes, as input feature only | yes for high-risk emotion labels | yes |
| topic_hint | string array | yes | account_linking, platform_policy, regional_access | Narrative clustering feature | yes, as input feature only | yes if report-facing | yes |
| claim_summary | string | optional | Short neutral summary | Report draft aid and reviewer context | no direct weight | yes if client-facing | yes after review |
| narrative_frame | string array | optional | communication_failure, trust_repair | InfluenceCore and narrative frame feature | yes, as input feature only | yes if sensitive | yes |
| meme_or_deconstruction_hint | string | optional | none, meme, satire, symbolic_deconstruction, cooling_joke, identity_marker, unclear | DeconstructionCore feature | yes, as input feature only | yes if used in report | yes |
| evidence_strength_hint | string | optional | direct_evidence, indirect_evidence, anecdote, opinion_only, joke_or_meme, unclear | Evidence confidence feature | yes, as input feature only | yes for high-impact claims | yes |
| logic_strength_hint | string | optional | strong, medium, weak, unclear | Argument quality feature | yes, as input feature only | yes if public-facing | yes |
| source_relevance_hint | string | optional | core_event, related_context, background, off_topic, unclear | Filtering and coverage context | yes, as input feature only | yes if excluding evidence | yes |
| risk_flags | string array | yes | harassment, slur, personal_attack, misinformation_risk, conspiracy_frame, brigading_claim, doxxing_risk, violent_language, self_harm, spam, none | Review gate and safety display | no direct weight by itself | yes when not none | limited |
| response_target_hint | string | optional | official, platform, developer, publisher, media, community, creator, unclear | Response strategy grouping | yes, as input feature only | yes if client-facing | yes |
| language_hint | string | optional | zh, en, mixed, unclear | Language routing and display | no | no | yes |
| confidence | number | yes | 0.0 to 1.0 | Downweight uncertain labels | yes, as uncertainty factor | yes if low | yes |
| needs_human_review | boolean | yes | true | Review queue routing | no | yes | yes |
| annotation_notes | string | optional | Brief reason for labels | Reviewer context | no | yes if report-facing | yes after review |
| safety_notes | string array | optional | annotation_only, not_fact_verification | UI boundary and audit | no | no | yes |
| input_hash | string | optional | hash label only | Cache and reproducibility | no | no | no |
| output_hash | string | optional | hash label only | Cache and reproducibility | no | no | no |
| created_at | string | optional | ISO-like local timestamp | Audit | no | no | no |

## 2. Allowed Values

### stance_hint

- support
- neutral
- oppose
- mixed
- unclear

### emotion_hint

- anger
- frustration
- disappointment
- sarcasm
- fear
- distrust
- explanation
- curiosity
- fatigue
- reconciliation
- neutral
- unclear

### meme_or_deconstruction_hint

- none
- meme
- satire
- symbolic_deconstruction
- cooling_joke
- identity_marker
- unclear

### evidence_strength_hint

- direct_evidence
- indirect_evidence
- anecdote
- opinion_only
- joke_or_meme
- unclear

### logic_strength_hint

- strong
- medium
- weak
- unclear

### source_relevance_hint

- core_event
- related_context
- background
- off_topic
- unclear

### response_target_hint

- official
- platform
- developer
- publisher
- media
- community
- creator
- unclear

### risk_flags

- harassment
- slur
- personal_attack
- misinformation_risk
- conspiracy_frame
- brigading_claim
- doxxing_risk
- violent_language
- self_harm
- spam
- none

## 3. Output Contract

```json
{
  "annotation_version": "llm_semantic_annotation_v1",
  "evidence_id": "evidence_example_id",
  "mode": "mock_default",
  "stance_hint": "oppose",
  "emotion_hint": ["frustration", "distrust"],
  "topic_hint": ["account_linking", "platform_policy"],
  "claim_summary": "A short neutral summary of the evidence claim.",
  "narrative_frame": ["communication_failure"],
  "meme_or_deconstruction_hint": "none",
  "evidence_strength_hint": "opinion_only",
  "logic_strength_hint": "medium",
  "source_relevance_hint": "core_event",
  "risk_flags": ["none"],
  "response_target_hint": "official",
  "language_hint": "en",
  "confidence": 0.7,
  "needs_human_review": true,
  "annotation_notes": "Annotation is based only on the provided sanitized evidence snippet.",
  "safety_notes": ["annotation_only", "not_fact_verification"]
}
```

Validation requirements:

- Unknown enum values should fail schema validation.
- Missing required fields should fail schema validation.
- Extra identity-like fields should fail schema validation.
- Long free-text values should be trimmed or rejected.
- JSON must be parsed as data only.

## 4. Example: Helldivers-Style Core Event Evidence

Synthetic sanitized evidence snippet:

> The account linking change felt like a broken promise because people bought the game before this requirement became unavoidable.

Mock annotation:

```json
{
  "annotation_version": "llm_semantic_annotation_v1",
  "evidence_id": "synthetic_helldivers_core_001",
  "mode": "mock_default",
  "stance_hint": "oppose",
  "emotion_hint": ["frustration", "distrust"],
  "topic_hint": ["account_linking", "trust", "platform_policy"],
  "claim_summary": "The evidence argues that the account linking requirement damaged player trust.",
  "narrative_frame": ["broken_promise", "communication_failure"],
  "meme_or_deconstruction_hint": "none",
  "evidence_strength_hint": "opinion_only",
  "logic_strength_hint": "medium",
  "source_relevance_hint": "core_event",
  "risk_flags": ["none"],
  "response_target_hint": "official",
  "language_hint": "en",
  "confidence": 0.78,
  "needs_human_review": true,
  "annotation_notes": "The text directly discusses the central account-linking dispute but remains an opinion claim.",
  "safety_notes": ["annotation_only", "not_fact_verification"]
}
```

## 5. Example: Meme / Deconstruction Evidence

Synthetic sanitized evidence snippet:

> The community joke turned the controversy into a cape symbol, so the anger started becoming shared memory instead of only active complaint.

Mock annotation:

```json
{
  "annotation_version": "llm_semantic_annotation_v1",
  "evidence_id": "synthetic_helldivers_meme_001",
  "mode": "mock_default",
  "stance_hint": "mixed",
  "emotion_hint": ["sarcasm", "fatigue"],
  "topic_hint": ["meme_memory", "review_bombing", "long_term_reputation"],
  "claim_summary": "The evidence claims that community humor transformed part of the dispute into symbolic memory.",
  "narrative_frame": ["meme_deconstruction", "community_identity"],
  "meme_or_deconstruction_hint": "symbolic_deconstruction",
  "evidence_strength_hint": "opinion_only",
  "logic_strength_hint": "medium",
  "source_relevance_hint": "related_context",
  "risk_flags": ["none"],
  "response_target_hint": "community",
  "language_hint": "en",
  "confidence": 0.74,
  "needs_human_review": true,
  "annotation_notes": "The snippet uses symbolic language and should be reviewed before report usage.",
  "safety_notes": ["annotation_only", "not_fact_verification"]
}
```

## 6. Example: Off-Topic / Low-Relevance Evidence

Synthetic sanitized evidence snippet:

> The game balance patch changed a weapon I liked, and that is my main concern now.

Mock annotation:

```json
{
  "annotation_version": "llm_semantic_annotation_v1",
  "evidence_id": "synthetic_off_topic_001",
  "mode": "mock_default",
  "stance_hint": "unclear",
  "emotion_hint": ["frustration"],
  "topic_hint": ["background"],
  "claim_summary": "The evidence discusses a gameplay balance concern rather than the public-opinion event.",
  "narrative_frame": [],
  "meme_or_deconstruction_hint": "none",
  "evidence_strength_hint": "opinion_only",
  "logic_strength_hint": "unclear",
  "source_relevance_hint": "off_topic",
  "risk_flags": ["none"],
  "response_target_hint": "developer",
  "language_hint": "en",
  "confidence": 0.69,
  "needs_human_review": false,
  "annotation_notes": "Low relevance to the account-linking event.",
  "safety_notes": ["annotation_only", "not_fact_verification"]
}
```

## 7. Example: Rejected / Needs-Review Evidence

Synthetic sanitized evidence snippet:

> Someone claimed a private person caused the controversy, but the text provides no source and includes hostile language.

Mock annotation:

```json
{
  "annotation_version": "llm_semantic_annotation_v1",
  "evidence_id": "synthetic_review_needed_001",
  "mode": "mock_default",
  "stance_hint": "unclear",
  "emotion_hint": ["anger"],
  "topic_hint": ["trust"],
  "claim_summary": "The evidence makes an unsupported accusation and contains hostile framing.",
  "narrative_frame": ["communication_failure"],
  "meme_or_deconstruction_hint": "none",
  "evidence_strength_hint": "unclear",
  "logic_strength_hint": "weak",
  "source_relevance_hint": "unclear",
  "risk_flags": ["personal_attack", "misinformation_risk"],
  "response_target_hint": "unclear",
  "language_hint": "en",
  "confidence": 0.52,
  "needs_human_review": true,
  "annotation_notes": "The annotation should not be used in a public or client-facing report without human review.",
  "safety_notes": ["annotation_only", "not_fact_verification", "review_required"]
}
```

## 8. Downstream Use Rules

- Stance, emotion, topic, narrative, and meme hints may feed deterministic local features.
- Risk flags route evidence into review or warning flows.
- Confidence can reduce the impact of uncertain semantic labels.
- Needs-human-review should block high-impact report usage until reviewed.
- Claim summaries can help reviewers, but should not be treated as verified facts.
- No annotation field directly sets final Opinion Ecosystem weights.

## 9. Prohibited Output

The schema must reject or strip:

- Real user identity fields.
- Raw `author_id`.
- Raw `author_name`.
- Raw `profile_url`.
- Personality diagnosis.
- Persuasion or targeting instructions.
- Final trust score.
- Final risk score.
- Final PeopleCluster weight.
- Final InfluenceCore pull.
- Final EchoBox saturation.
- Tool-use instructions.
- External link execution instructions.

