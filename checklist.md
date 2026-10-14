<!-- Generated from checklist.yaml by scripts/build.py. Do not edit by hand. -->

# AI Agent Security Review Checklist

Version 0.1.0, updated 2026-10-14. 33 items in 10 groups.

How to read each item:

- **Question**: how buyers usually phrase it in a questionnaire or review call.
- **Why they ask**: the risk or obligation behind it.
- **Evidence that satisfies it**: what to have ready.
- **Not enough on its own**: answers that usually trigger a follow-up.
- **References**: framework controls that cover the topic, with how we checked them (*verified* = primary text; *secondary source* = primary is gated, checked via a reliable secondary source; *title only* = only the control title was available).
- Items marked **Hard to evidence today** are the ones most vendors answer with a policy statement rather than proof.

## Contents

- [ACC · Access & scope](#acc--access--scope) (3)
- [ACT · Action records](#act--action-records) (7)
- [OUT · Outcome verification](#out--outcome-verification) (2)
- [TMP · Tamper evidence](#tmp--tamper-evidence) (3)
- [INC · Incident reconstruction](#inc--incident-reconstruction) (3)
- [RET · Retention](#ret--retention) (4)
- [CHG · Model & prompt changes](#chg--model--prompt-changes) (4)
- [DAT · Data handling](#dat--data-handling) (2)
- [HUM · Human oversight (as the buyer defines it)](#hum--human-oversight-as-the-buyer-defines-it) (2)
- [SUB · Sub-processors](#sub--sub-processors) (3)

## ACC · Access & scope

What the agent can do in the buyer's systems, under which identity, and how that is enforced.

### ACC-01

> What actions can your agent take in our systems, and how are those permissions enforced at the moment a tool is called?

**Why they ask.** The buyer stays responsible for everything that happens in its systems. An agent acting outside its intended authority is a named risk in agent frameworks, and instructions in a prompt are not an enforcement mechanism.

**Evidence that satisfies it**

- Per-agent inventory of tools and actions, with the systems and scopes each one can touch.
- Enforcement in code at the tool-invocation layer (allowlists, parameter validation, scoped credentials), not only in the prompt.
- Test results showing out-of-scope calls are blocked.
- Per-action records that show which scope or permission applied.

**Not enough on its own**

- The model is instructed not to do X.
- A workflow diagram with no enforcement point.

**References**

- FINOS AIR [AIR-PREV-018](https://air-governance-framework.finos.org/mitigations/mi-18_agent-authority-least-privilege-framework.html): Agent authority least privilege *(verified)*
- FINOS AIR [AIR-SEC-024](https://air-governance-framework.finos.org/risks/ri-24_agent-action-authorization-bypass.html): Risk: agent action authorization bypass *(verified)*
- FINOS AIR [AIR-PREV-019](https://air-governance-framework.finos.org/mitigations/mi-19_tool-chain-validation-and-sanitization.html): Tool chain validation and sanitization *(verified)*
- CSA AICM IAM-19: Agent access restriction *(title only)*
- CSA AICM AIS-11: Agents security boundaries *(title only)*
- CSA AICM IAM-05: Least privilege *(title only)*
- NYDFS 500 [500.7(a)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.7): Limit access and privileged accounts to what is needed *(verified)*
- NYDFS AI Letter Access controls: Least privilege and access review apply to AI *(verified)*
- ISO 42001 A.9.4: Intended use of the AI system *(secondary source)*
- DORA [Art. 9(4)](https://www.digital-operational-resilience-act.com/Article_9.html): Least-privilege access and strong authentication *(verified)*
- SIG AI domain: Domain-level only; question text not reviewed *(title only)*

### ACC-02

> For every write in our systems, which identity performed it? Which agent and version, under which credential and scope, on whose behalf? **Hard to evidence today.**

**Why they ask.** Agents often act through shared service accounts or human-style browser logins, so the buyer's own logs cannot tell the agent from a staff member, and the vendor's logs cannot be matched to the buyer's.

**Evidence that satisfies it**

- A distinct non-human identity per agent deployment, visible in the buyer's system logs.
- Each action record carries agent ID and version, credential ID (never the secret), scope, and the initiating user, case or ticket.
- Credentials isolated from the model and injected per call.

**Not enough on its own**

- A shared integration user for all agent traffic.
- Identity known only inside the vendor's database.

**References**

- FINOS AIR [AIR-PREV-023](https://air-governance-framework.finos.org/mitigations/mi-23_agentic-system-credential-protection-framework.html): Agentic credential protection, signed agent API requests *(verified)*
- FINOS AIR [AIR-DET-021](https://air-governance-framework.finos.org/mitigations/mi-21_agent-decision-audit-and-explainability.html): Record who or what initiated each agent decision *(verified)*
- FINOS AIR [AIR-SEC-029](https://air-governance-framework.finos.org/risks/ri-29_agent-mediated-credential-discovery-and-harvesting.html): Risk: agent-mediated credential harvesting *(verified)*
- CSA AICM IAM-13: Uniquely identifiable users, including non-human *(title only)*
- CSA AICM IAM-19: Agent access restriction *(title only)*
- CSA AICM LOG-12: Access control logs *(title only)*
- NYDFS 500 [500.7(a)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.7): Access privileges and management *(verified)*
- NYDFS 500 [500.11(b)(1)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.11): Third-party access control guidelines *(verified)*

### ACC-03

> What stops prompt injection or a manipulated tool chain from causing the agent to take an action in our systems?

**Why they ask.** Agents read untrusted content (emails, documents, web pages, tool outputs). If that content can steer a tool call, an attacker can act inside the buyer's systems through the agent.

**Evidence that satisfies it**

- Separation of instructions from untrusted data, plus input and output filtering.
- Validation of tool selection and parameters before execution.
- Red-team results that include indirect injection through retrieved content.
- Detection of out-of-pattern actions in the action records.

**Not enough on its own**

- We use a safe model.

**References**

- FINOS AIR [AIR-SEC-025](https://air-governance-framework.finos.org/risks/ri-25_tool-chain-manipulation-and-injection.html): Risk: tool chain manipulation and injection *(verified)*
- FINOS AIR [AIR-SEC-010](https://air-governance-framework.finos.org/risks/ri-10_prompt-injection.html): Risk: prompt injection *(verified)*
- FINOS AIR [AIR-PREV-019](https://air-governance-framework.finos.org/mitigations/mi-19_tool-chain-validation-and-sanitization.html): Tool chain validation and sanitization *(verified)*
- FINOS AIR [AIR-PREV-003](https://air-governance-framework.finos.org/mitigations/mi-3_user-app-model-firewalling-filtering.html): User/app/model firewalling and filtering *(verified)*
- CSA AICM AIS-15: Prompt differentiation *(title only)*
- CSA AICM AIS-08 / AIS-09: Input and output validation *(title only)*
- CSA AICM MDS-06 / MDS-07: Adversarial attack analysis and robustness *(title only)*
- NIST AI 600-1 MS-2.7-007: Red-team for prompt injection and related attacks *(verified)*
- NIST AI RMF MEASURE 2.7: Security and resilience evaluated and documented *(verified)*
- EU AI Act [Art. 15(5)](https://artificialintelligenceact.eu/article/15/): Resilience against manipulation of inputs and outputs (high-risk) *(verified)*

## ACT · Action records

What is recorded for each agent action, and whether one action can be produced end to end.

### ACT-01

> For any single agent action, can you produce the complete record? What triggered it, which inputs and sources it used, the exact tool call and arguments, the system's response, and the downstream effect. **Hard to evidence today.**

**Why they ask.** Reviewers and examiners pick one case and ask you to walk through it. If the record is spread across chat transcripts, APM traces and the vendor UI, the answer takes days and cannot be checked.

**Evidence that satisfies it**

- A per-action record with trigger, inputs, retrieved sources, tool name, arguments (redacted where needed), the system response, timestamps and a trace ID.
- A sample export for one real (redacted) case, produced on request in minutes.

**Not enough on its own**

- A chat transcript without the tool calls.
- Infrastructure logs only.

**References**

- FINOS AIR [AIR-DET-021](https://air-governance-framework.finos.org/mitigations/mi-21_agent-decision-audit-and-explainability.html): Log inputs, reasoning, tool selection, actions taken and downstream effects *(verified)*
- CSA AICM LOG-11: Transaction/activity logging *(title only)*
- CSA AICM LOG-08: Log records contain relevant security information *(secondary source)*
- CSA AICM LOG-14 / LOG-15: AI input and output monitoring *(title only)*
- EU AI Act [Art. 12(1)-(2)](https://artificialintelligenceact.eu/article/12/): Automatic event logging over the lifetime that enables traceability (high-risk) *(verified)*
- ISO 42001 A.6.2.8: AI system recording of event logs *(secondary source)*
- NYDFS 500 [500.6(a)(1)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.6): Systems able to reconstruct material financial transactions *(verified)*
- NAIC AI Bulletin Sec. 3, 3.3(b)-(c): Model documentation, traceability and auditability *(secondary source)*
- NYDFS CL7 ¶19: Be able to explain at all times how the AIS operates *(verified)*

### ACT-02

> Which model and version handled a given action, including actions served by versions you have since retired? **Hard to evidence today.**

**Why they ask.** Vendors route between several models and providers. When a past decision is challenged, the buyer must know which model produced it, even if that model is gone.

**Evidence that satisfies it**

- Model provider, model name and pinned version stored on every action record.
- A model inventory that keeps retired versions with their active dates.

**Not enough on its own**

- A current list of providers with no per-action version.

**References**

- FINOS AIR [AIR-PREV-010](https://air-governance-framework.finos.org/mitigations/mi-10_ai-model-version-pinning.html): AI model version pinning *(verified)*
- FINOS AIR [AIR-OP-005](https://air-governance-framework.finos.org/risks/ri-5_foundation-model-versioning.html): Risk: foundation model versioning *(verified)*
- NIST AI 600-1 GV-1.6-003: Inventory records underlying models and versions *(verified)*
- NIST AI RMF GOVERN 1.6 / 1.7: AI inventory and decommissioning *(verified)*
- NAIC AI Bulletin Sec. 3, 3.3(a): Model inventory *(secondary source)*
- NYDFS CL7 ¶29: Inventory including retired AIS, with change tracking *(verified)*
- CSA AICM MDS-03 to MDS-05: Model documentation *(title only)*
- CSA AICM MDS-09: Model signing and ownership verification *(title only)*

### ACT-03

> Show every model endpoint and external service the agent actually called for our traffic, not just the list in your inventory. **Hard to evidence today.**

**Why they ask.** An inventory says what should be called. Destination records show what was called, which is what data-flow and data-residency reviews need.

**Evidence that satisfies it**

- Per-action record of each outbound call (provider, endpoint, region).
- A periodic summary per buyer comparing actual destinations with the declared sub-processor list.

**Not enough on its own**

- A static sub-processor page.

**References**

- CSA AICM STA-16: Service bill of materials *(title only)*
- CSA AICM DSP-05: Data flow documentation *(title only)*
- FINOS AIR [AIR-DET-004](https://air-governance-framework.finos.org/mitigations/mi-4_ai-system-observability.html): AI system observability, centralized logs *(verified)*
- FINOS AIR [AIR-PREV-020](https://air-governance-framework.finos.org/mitigations/mi-20_mcp-server-security-governance.html): Log all MCP traffic *(verified)*
- NYDFS AI Letter Monitoring: Monitor AI tool use for unusual query behaviour *(verified)*
- DORA [Art. 30(2)(b)](https://www.digital-operational-resilience-act.com/Article_30.html): Contract specifies data processing locations and notice of changes *(verified)*

### ACT-04

> Which documents and records contributed to each answer or action?

**Why they ask.** Reviewers need to trace an output back to its sources, both to check correctness and to confirm the agent only used data it was entitled to see.

**Evidence that satisfies it**

- Source IDs (document, record, version) stored on the action record.
- Entitlement checks that carry the source system's access controls into retrieval.

**Not enough on its own**

- Citations shown in the UI but not retained.

**References**

- FINOS AIR [AIR-DET-013](https://air-governance-framework.finos.org/mitigations/mi-13_providing-citations-and-source-traceability-for-ai-generated-information.html): Citations and source traceability *(verified)*
- FINOS AIR [AIR-DET-016](https://air-governance-framework.finos.org/mitigations/mi-16_preserving-source-data-access-controls-in-ai-systems.html): Preserve source data access controls *(verified)*
- CSA AICM DSP-20: Data provenance and transparency *(title only)*
- ISO 42001 A.7.5: Data provenance *(secondary source)*

### ACT-05

> What is the lineage of the data used in a decision? Where did each input come from, and how current was it?

**Why they ask.** Insurance and lending regulators ask for data lineage, and stale or wrong inputs are a common root cause of bad decisions.

**Evidence that satisfies it**

- Documented data flows per use case.
- Input source and retrieval timestamp stored with the decision.

**Not enough on its own**

- A generic architecture diagram.

**References**

- NAIC AI Bulletin Sec. 3, 3.2: Data practices incl. lineage and integrity *(secondary source)*
- NYDFS CL7 ¶29: Documentation of inputs and their sources *(verified)*
- ISO 42001 A.7.5: Data provenance *(secondary source)*
- CSA AICM DSP-20: Data provenance and transparency *(title only)*
- NIST AI 600-1 GV-6.1-008: Records of third-party content changes with sources and timestamps *(verified)*

### ACT-06

> For an adverse decision, can you give the specific reasons and the data relied on? A proprietary model is not an acceptable reason to withhold them.

**Why they ask.** Consumer-facing lenders and insurers must give specific reasons for adverse outcomes, and regulators reject vendor secrecy as an excuse.

**Evidence that satisfies it**

- Reason codes and the specific inputs relied on, stored per decision.
- A sample adverse-decision explanation produced from the stored record.

**Not enough on its own**

- Global feature importance for the model.

**References**

- NYDFS CL7 ¶39-¶40: Reasons include all information relied on; no proprietary-algorithm excuse *(verified)*
- NYDFS CL7 ¶44: Written reasons within 15 days in specified cases *(verified)*
- EU AI Act [Art. 86(1)](https://artificialintelligenceact.eu/article/86/): Right to explanation for affected persons (Annex III) *(verified)*
- NIST AI RMF MEASURE 2.9: Explain and interpret output in context *(verified)*
- CSA AICM GRC-13 / GRC-14: Explainability requirement and evaluation *(title only)*
- FINOS AIR [AIR-OP-017](https://air-governance-framework.finos.org/risks/ri-17_lack-of-explainability.html): Risk: lack of explainability *(verified)*

### ACT-07

> For customer-facing agents, can you show per interaction that the conduct rules for our use case were met, such as AI disclosure, contact-time windows and contact-frequency limits? **Hard to evidence today.**

**Why they ask.** In collections, servicing and sales, a single non-compliant contact can be a violation. Buyers want per-interaction proof, not a policy that the platform enforces rules.

**Evidence that satisfies it**

- Per-interaction record of the disclosure given, the time in the customer's time zone, and the frequency counter at the time of contact.
- Rule configuration and version applied to each interaction.

**Not enough on its own**

- QA reviews a sample of calls.

*Note: The specific conduct rules (for example debt-collection contact limits) come from the sector law for your use case and are not mapped here.*

**References**

- EU AI Act [Art. 50(1)](https://artificialintelligenceact.eu/article/50/): Inform people they are interacting with an AI system *(verified)*
- CSA AICM LOG-11: Transaction/activity logging *(title only)*

## OUT · Outcome verification

Whether what the agent reports matches what actually happened in the system of record.

### OUT-01

> When the agent says it did something, how do you know it actually happened in our system, as described? **Hard to evidence today.**

*Derived item, split out from ACT-01 (downstream effect) and INC-01.*

**Why they ask.** An agent's own summary ("refund issued") is not evidence. Agents can report success while the target system shows an error, a different amount or nothing at all. Reviewers want the system of record's response next to the claim.

**Evidence that satisfies it**

- Each action record stores both the agent's claim and the target system's actual response (status, object ID, returned values).
- Optional read-back that queries the system of record and records match or mismatch.
- Mismatch rate per period, reported to the buyer.

**Not enough on its own**

- The agent's final message.
- HTTP 200 without checking the returned object.

**References**

- FINOS AIR [AIR-DET-021](https://air-governance-framework.finos.org/mitigations/mi-21_agent-decision-audit-and-explainability.html): Log actions taken and their downstream effects *(verified)*
- NYDFS 500 [500.6(a)(1)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.6): Reconstruct material financial transactions *(verified)*
- EU AI Act [Art. 12(2)](https://artificialintelligenceact.eu/article/12/): Logs enable traceability and deployer monitoring *(verified)*
- NAIC AI Bulletin Sec. 3, 3.4: Validate and retest outputs after implementation *(secondary source)*
- NIST AI RMF MEASURE 2.4: Monitor behaviour in production *(verified)*

### OUT-02

> How do you detect and report actions that failed, only partly completed, or produced a different result than intended? **Hard to evidence today.**

*Derived item, split out from INC-02.*

**Why they ask.** Silent failures are the hardest to catch. A buyer wants to see failures counted and reported, not discovered by a customer.

**Evidence that satisfies it**

- Failed, partial and mismatched actions counted per period, with examples, in the buyer's report.
- Alert thresholds and owners.
- Reconciliation against the system of record for high-impact actions.

**Not enough on its own**

- Error rate from APM only.

**References**

- CSA AICM LOG-13: Failures and anomalies reporting *(title only)*
- CSA AICM MDS-11: Model failure *(title only)*
- FINOS AIR [AIR-DET-004](https://air-governance-framework.finos.org/mitigations/mi-4_ai-system-observability.html): Observability and alerting on anomalies *(verified)*
- NIST AI 600-1 MG-4.3-002: Track errors, near-misses and negative impacts *(verified)*
- ISO 42001 A.6.2.6: AI system operation and monitoring *(secondary source)*
- DORA [Art. 17(1)-(3)](https://www.digital-operational-resilience-act.com/Article_17.html): Detect, log, classify and track ICT incidents *(verified)*

## TMP · Tamper evidence

Whether records can be changed after the fact without anyone noticing, and who can check.

### TMP-01

> Are agent action records protected so that any edit, deletion, reordering or truncation after the fact is detectable? **Hard to evidence today.**

**Why they ask.** Access controls protect logs from outsiders, not from the party that writes them. "Immutable" is a claim; reviewers increasingly ask for the mechanism.

**Evidence that satisfies it**

- Hash-chained, append-only records (each record commits to the previous one).
- Digital signatures with keys separated from application operators.
- Periodic commitment of segment digests (for example a Merkle root) so truncation is detectable.
- Synchronized clocks and documented key management.

**Not enough on its own**

- "Logs are immutable" with no mechanism.
- Write-protected storage alone, where the vendor still controls the storage.

**References**

- FINOS AIR [AIR-DET-021](https://air-governance-framework.finos.org/mitigations/mi-21_agent-decision-audit-and-explainability.html): Tamper-evident logging and immutable records; names hash chaining and signed segments *(verified)*
- FINOS AIR [AIR-PREV-024](https://air-governance-framework.finos.org/mitigations/mi-24_human-in-the-loop-action-approval-gate.html): Tamper-evident approval record; hash chaining alone is not non-repudiation *(verified)*
- DORA [RTS 2024/1774 Art. 12](https://www.springlex.eu/en/packages/dora/rts-rmf-regulation/article-12/): Protect logging systems and log information against tampering and deletion *(secondary source)*
- CSA AICM LOG-09: Protect audit records from modification and deletion *(secondary source)*
- CSA AICM IAM-12: Safeguard logs integrity *(secondary source)*
- CSA AICM LOG-02: Audit logs protection *(secondary source)*
- CSA AICM LOG-06: Clock synchronization *(title only)*
- NIST AI 600-1 MS-2.8-003: Tamper-proof history of content with version control *(verified)*
- NYDFS 500 [500.6(a)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.6): Securely maintain audit trail systems (no cryptographic requirement) *(verified)*

### TMP-02

> Can we, our auditor or our regulator verify those records ourselves, without access to your systems and without relying on your word? **Hard to evidence today.**

**Why they ask.** Logs the vendor writes, stores and attests to are self-reported evidence. The strongest records are those a third party can check independently.

**Evidence that satisfies it**

- A verification tool the buyer can run offline on an exported bundle.
- Public keys and verification steps documented.
- Record digests anchored outside the vendor (for example an append-only transparency log) or held by the buyer.
- A worked example showing a tampered bundle failing verification.

**Not enough on its own**

- A screenshot or PDF export from the vendor's UI.
- A SOC 2 report, which covers controls, not individual records.

*Note: FINOS is the only framework found that states independent verifiability explicitly. Elsewhere it follows from audit and access rights.*

**References**

- FINOS AIR [AIR-DET-021](https://air-governance-framework.finos.org/mitigations/mi-21_agent-decision-audit-and-explainability.html): Records verifiable by deployer, auditor or authority without privileged access to the provider; anchoring to a transparency log *(verified)*
- DORA [Art. 30(3)(e)](https://www.digital-operational-resilience-act.com/Article_30.html): Unrestricted rights of access, inspection and audit (critical or important functions) *(verified)*
- EU AI Act [Art. 13(3)(f)](https://artificialintelligenceact.eu/article/13/): Mechanisms that let deployers collect, store and interpret logs (high-risk) *(verified)*

### TMP-03

> Who at your company can read, change or delete agent records, and is that access itself logged?

**Why they ask.** Privileged insiders are the main threat to record integrity. Reviewers expect named roles and an access trail.

**Evidence that satisfies it**

- Named roles with access to record storage and keys.
- Access to records logged against individual identities and reviewed.
- Separation between people who run the agent and people who can touch records or keys.

**Not enough on its own**

- "Only engineers have access."

**References**

- CSA AICM LOG-04: Audit log access restricted and attributable *(secondary source)*
- CSA AICM IAM-12: Logging infrastructure read-only to those with other write access *(secondary source)*
- CSA AICM IAM-04: Separation of duties *(title only)*
- NYDFS 500 [500.7(c)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.7): Privileged access monitoring (Class A companies) *(verified)*

## INC · Incident reconstruction

Detecting, reporting, stopping and reconstructing what went wrong.

### INC-01

> After an incident, can you reconstruct exactly what the agent did, in which of our systems, under which identity, and in what order? **Hard to evidence today.**

**Why they ask.** Incident response, root-cause analysis and regulator notifications all depend on an ordered, complete account. Gaps are what turn an incident into a finding.

**Evidence that satisfies it**

- For a time window or case, an ordered export of all actions across all buyer systems, with identity, scope, inputs and system responses.
- Evidence the sequence is complete (no gaps) and unaltered.
- A tabletop exercise or test showing how long reconstruction takes.

**Not enough on its own**

- Our engineers can query the database.

**References**

- FINOS AIR [AIR-DET-021](https://air-governance-framework.finos.org/mitigations/mi-21_agent-decision-audit-and-explainability.html): Tier 1 is reconstruction of what happened *(verified)*
- NYDFS 500 [500.6(a)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.6): Audit trails to reconstruct transactions and respond to cybersecurity events *(verified)*
- NYDFS 500 [500.16(a)(1)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.16): Incident response plan incl. documentation and root cause *(verified)*
- DORA [Art. 17(1)-(3)](https://www.digital-operational-resilience-act.com/Article_17.html): Incident detection, logging and root-cause analysis *(verified)*
- DORA [Art. 30(2)(f)](https://www.digital-operational-resilience-act.com/Article_30.html): Provider assists with ICT incidents *(verified)*
- EU AI Act [Art. 73](https://artificialintelligenceact.eu/article/73/): Serious incident reporting; do not alter the system before informing authorities *(verified)*
- CSA AICM SEF-09: Incident response *(title only)*
- CSA AICM LOG-05 / LOG-06: Audit log monitoring and clock synchronization *(title only)*
- NIST AI RMF MANAGE 4.3: Track and recover from incidents and errors *(verified)*

### INC-02

> How do you detect and report model failures, data leakage or harmful outputs, and on what timeline will we hear about them?

**Why they ask.** The buyer has its own notification clocks (72 hours under NYDFS 500, hours under DORA). Vendor timelines must fit inside them.

**Evidence that satisfies it**

- Contractual notification timeline that fits the buyer's obligations.
- Detection sources (monitoring, alerts, user reports) and owners.
- A recent incident report or tabletop record (redacted).

**Not enough on its own**

- A generic incident-response policy with no AI-specific triggers.

**References**

- NYDFS 500 [500.11(b)(3)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.11): Third-party notice of cybersecurity events *(verified)*
- NYDFS 500 [500.17(a)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.17): Notify DFS within 72 hours, incl. third-party incidents *(verified)*
- NYDFS AI Letter Risk assessments: Incident and continuity plans should address AI-related events *(verified)*
- DORA [Art. 19; RTS 2025/301](https://www.digital-operational-resilience-act.com/Article_19.html): Major ICT incident reporting and time limits *(secondary source)*
- EU AI Act [Art. 73(2)-(6)](https://artificialintelligenceact.eu/article/73/): Serious incident reporting deadlines (high-risk) *(verified)*
- CSA AICM SEF-07: Security breach notification *(title only)*
- CSA AICM MDS-11: Model failure *(title only)*
- ISO 42001 A.8.4: Communication of incidents *(secondary source)*
- NIST AI 600-1 MG-4.3-002: Track errors and negative impacts *(verified)*
- FINOS AIR [AIR-DET-001](https://air-governance-framework.finos.org/mitigations/mi-1_ai-data-leakage-prevention-and-detection.html): AI data leakage prevention and detection *(verified)*
- FS-ISAC GenAI Levels 2-3: Vulnerability management, DLP and log management in deeper due diligence *(verified)*

### INC-03

> How quickly can we stop the agent, or roll it back to a previous model or configuration?

**Why they ask.** When something goes wrong the first question is how to stop it. Rollback also matters when a provider changes a model underneath you.

**Evidence that satisfies it**

- A kill switch the buyer can trigger, with tested time to effect.
- Pinned model and prompt versions with a documented rollback path.
- Results of the last rollback test.

**Not enough on its own**

- Contact support.

**References**

- EU AI Act [Art. 14(4)(e)](https://artificialintelligenceact.eu/article/14/): Ability to interrupt the system with a stop procedure (high-risk) *(verified)*
- NIST AI RMF MANAGE 2.4: Mechanisms to supersede, disengage or deactivate *(verified)*
- NIST AI 600-1 MG-2.4-002 / MG-2.4-004: Escalation and deactivation criteria *(verified)*
- CSA AICM CCC-09: Change restoration *(title only)*
- FINOS AIR [AIR-PREV-010](https://air-governance-framework.finos.org/mitigations/mi-10_ai-model-version-pinning.html): Model version pinning *(verified)*
- ISO 42001 A.6.2.5: AI system deployment plan *(secondary source)*
- DORA [Art. 28(7)-(8); Art. 30(3)(f)](https://www.digital-operational-resilience-act.com/Article_28.html): Termination rights, exit plans and transition *(verified)*
- NYDFS 500 [500.16(a)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.16): Incident response and continuity plans *(verified)*

## RET · Retention

How long records are kept, by whom, and how the buyer gets them.

### RET-01

> What do you log about agent activity, how long do you keep it, who can access it, and can you export it to our SIEM or GRC tool?

**Why they ask.** Log management is an explicit topic in the deepest tier of bank AI due diligence. Short default retention is a common finding.

**Evidence that satisfies it**

- A list of logged event types for agent actions (not just infrastructure).
- Retention period per log type.
- Export mechanism (API or scheduled delivery) and a sample export.

**Not enough on its own**

- "Logs retained for 30 days" with no agent-action logs.

**References**

- FS-ISAC GenAI Level 3: Log management, audit validation and data retention *(verified)*
- CSA AICM LOG-01 / LOG-02 / LOG-07: Logging policy, protection and scope *(secondary source)*
- DORA [RTS 2024/1774 Art. 12](https://www.springlex.eu/en/packages/dora/rts-rmf-regulation/article-12/): Define logged events and retention *(secondary source)*
- ISO 42001 A.6.2.8: AI system recording of event logs *(secondary source)*
- FINOS AIR [AIR-DET-004](https://air-governance-framework.finos.org/mitigations/mi-4_ai-system-observability.html): Centralize AI logs, for example in a SIEM *(verified)*
- NYDFS AI Letter Monitoring: Monitor user activity and AI tool use *(verified)*
- SIG AI domain: Domain-level only; question text not reviewed *(title only)*

### RET-02

> Can we hold our own copy of the agent's event logs for the period our rules require? **Hard to evidence today.**

**Why they ask.** Under the EU AI Act, deployers of high-risk systems must keep the logs under their control for at least six months, and financial institutions keep them under their financial-services record rules. A vendor-only copy does not meet that.

**Evidence that satisfies it**

- Continuous or scheduled delivery of records into storage the buyer controls.
- Format documented so the buyer's copy remains verifiable on its own.

**Not enough on its own**

- We can send logs on request.

*Note: EU AI Act Annex III high-risk obligations (including credit scoring and life/health insurance pricing) apply from 2 Dec 2027 after the Digital Omnibus, Regulation (EU) 2026/1744.*

**References**

- EU AI Act [Art. 26(6)](https://artificialintelligenceact.eu/article/26/): Deployer keeps logs at least six months; financial institutions under financial law (high-risk) *(verified)*
- EU AI Act [Art. 19(1)-(2)](https://artificialintelligenceact.eu/article/19/): Provider keeps logs it controls at least six months *(verified)*
- EU AI Act [Art. 12(1)](https://artificialintelligenceact.eu/article/12/): Automatic logging over the lifetime *(verified)*
- NYDFS 500 [500.6(b)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.6): Covered entity keeps audit-trail records five years *(verified)*

### RET-03

> How do we get timely access to our data and to reports on the agent's activity, by type and frequency?

**Why they ask.** Buyers must be able to monitor the service and to give data to auditors and regulators on demand.

**Evidence that satisfies it**

- Report types and cadence in the contract (activity, failures, incidents, changes).
- Self-service export of the buyer's data and records.

**Not enough on its own**

- A dashboard with no export.

**References**

- DORA [Art. 30(2)(d)](https://www.digital-operational-resilience-act.com/Article_30.html): Access to and return of data in an accessible format *(verified)*
- DORA [RTS 2024/1773 Art. 3](https://advisera.com/cdr-2024-1773/governance-arrangements/): Effective data access for auditors and authorities *(secondary source)*
- EU AI Act [Art. 13(3)(f)](https://artificialintelligenceact.eu/article/13/): Log collection mechanisms described for deployers *(verified)*
- ISO 42001 A.8.5: Information for interested parties *(secondary source)*
- NAIC AI Bulletin Sec. 4, 1.1-1.3: Documents regulators may request *(secondary source)*

### RET-04

> Does the retention of agent records match our own record-keeping obligations, and what happens to the records when the contract ends?

*Derived item, split out from RET-01 and RET-02.*

**Why they ask.** Vendor defaults (often weeks) rarely match the buyer's retention duties (often years). On exit, the buyer still needs the records.

**Evidence that satisfies it**

- Retention configurable per buyer, set to the buyer's requirement.
- Exit clause covering return of records in a verifiable format before deletion.

**Not enough on its own**

- A fixed vendor-wide retention period.

**References**

- NYDFS 500 [500.6(b)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.6): Five-year retention for covered entities' audit trails *(verified)*
- EU AI Act [Art. 19(2); Art. 26(6)](https://artificialintelligenceact.eu/article/26/): Financial institutions keep logs under financial-services documentation rules *(verified)*
- DORA [Art. 28(8); Art. 30(2)(d)](https://www.digital-operational-resilience-act.com/Article_28.html): Exit plans and return of data *(verified)*
- NAIC AI Bulletin Sec. 3, 3.6: Data and record retention in the AIS program *(secondary source)*

## CHG · Model & prompt changes

Which models run, how changes are controlled, and how behaviour is monitored over time.

### CHG-01

> Which foundation models and providers sit behind each feature, and how will you notify us when they change?

**Why they ask.** The model is the most important sub-component. Silent model swaps change behaviour and can invalidate the buyer's validation.

**Evidence that satisfies it**

- Model and provider list per feature, with versions.
- Contractual advance notice of model or provider changes.
- Change log available to the buyer.

**Not enough on its own**

- We use leading LLMs.

**References**

- FS-ISAC GenAI Level 1: Identify the foundation model *(verified)*
- NIST AI 600-1 GV-1.6-003; GV-6.2-007: Inventory of models and versions; contracts request notice of changes *(verified)*
- FINOS AIR [AIR-PREV-007](https://air-governance-framework.finos.org/mitigations/mi-7_legal-and-contractual-frameworks-for-ai-systems.html): Contracts cover model versioning and change notification *(verified)*
- FINOS AIR [AIR-PREV-010](https://air-governance-framework.finos.org/mitigations/mi-10_ai-model-version-pinning.html): Advance notice of new versions and deprecations *(verified)*
- CSA AICM CCC-05; STA-08; STA-16: Change agreements, supply chain inventory, service BOM *(title only)*
- NYDFS AI Letter Data management: Inventory of all systems that use or rely on AI *(verified)*
- DORA [Art. 28(3)](https://www.digital-operational-resilience-act.com/Article_28.html): Register of ICT third-party arrangements *(verified)*
- ISO 42001 A.4.4; A.10.3: Tooling resources; suppliers *(secondary source)*

### CHG-02

> How are changes to prompts, agent logic, tools and models tested, approved and versioned before they reach our traffic?

**Why they ask.** For agents, a prompt edit is a code change. Buyers want the same change control they expect for software.

**Evidence that satisfies it**

- Versioned prompts, tool definitions and configs, with the version stored on each action record.
- Pre-release evaluation results and a named approver per change.
- Change history the buyer can review.

**Not enough on its own**

- Prompts edited in a vendor console with no history.

**References**

- FS-ISAC GenAI Level 3: Change management *(verified)*
- CSA AICM CCC-01 to CCC-09: Change control and configuration management *(title only)*
- NYDFS CL7 ¶17; ¶29: Test on material changes; track changes with approvers *(verified)*
- DORA [Art. 9(4)](https://www.digital-operational-resilience-act.com/Article_9.html): Recorded, tested and approved ICT changes *(verified)*
- ISO 42001 A.6.2.4; A.6.2.5: Verification and validation; deployment *(secondary source)*
- NIST AI RMF MANAGE 4.1: Post-deployment monitoring incl. change management *(verified)*
- FINOS AIR [AIR-PREV-005](https://air-governance-framework.finos.org/mitigations/mi-5_system-acceptance-testing.html): System acceptance testing *(verified)*
- FINOS AIR [AIR-PREV-025](https://air-governance-framework.finos.org/mitigations/mi-25_skill-plugin-integrity-and-governance.html): Skill and plugin integrity *(verified)*
- NIST AI 600-1 MS-2.8-003: Version control across the lifecycle *(verified)*

### CHG-03

> How is the agent validated, independently or on an ongoing basis, including drift and bias testing?

**Why they ask.** Banks and insurers apply model risk management to vendor models. They need validation evidence they can file.

**Evidence that satisfies it**

- Validation methodology and latest results, including bias testing where decisions affect consumers.
- Drift monitoring and re-validation triggers.
- Any independent validation report.

**Not enough on its own**

- Marketing benchmark numbers.

**References**

- FS-ISAC GenAI Level 2: Model validation *(verified)*
- NAIC AI Bulletin Sec. 3, 3.3(c); 3.4: Drift and auditability; validation and retesting *(secondary source)*
- NYDFS CL7 ¶15-¶17; ¶32: Testing and independent review *(verified)*
- NIST AI RMF MEASURE 2.3 / 2.5 / 2.11: Performance, validity and fairness *(verified)*
- CSA AICM MDS-10; GRC-11; A&A-02: Continuous monitoring, bias assessment, independent assessments *(title only)*
- ISO 42001 A.6.2.4: Verification and validation *(secondary source)*
- FINOS AIR [AIR-DET-015](https://air-governance-framework.finos.org/mitigations/mi-15_using-large-language-models-for-automated-evaluation-llm-as-a-judge-.html): LLM-as-a-judge evaluation calibrated to humans *(verified)*

### CHG-04

> What ongoing monitoring do you report to us? Performance, error rates, complaints and drift.

**Why they ask.** Third-party oversight is continuous, not a one-time review. The buyer needs regular data to show its own supervisors.

**Evidence that satisfies it**

- A recurring report with defined metrics and thresholds.
- Escalation when thresholds are breached.

**Not enough on its own**

- Ad-hoc updates on request.

**References**

- NIST AI RMF GOVERN 1.5; MEASURE 2.4; MANAGE 4.1: Planned and post-deployment monitoring *(verified)*
- EU AI Act [Art. 72](https://artificialintelligenceact.eu/article/72/): Post-market monitoring by the provider (high-risk) *(verified)*
- ISO 42001 A.6.2.6: Operation and monitoring *(secondary source)*
- CSA AICM MDS-10: Model continuous monitoring *(title only)*
- DORA [Art. 30(3)(a)](https://www.digital-operational-resilience-act.com/Article_30.html): Precise service levels and reporting *(verified)*
- NYDFS CL7 ¶29-¶30: Monitoring, drift testing and complaints *(verified)*
- FINOS AIR [AIR-DET-011](https://air-governance-framework.finos.org/mitigations/mi-11_human-feedback-loop-for-ai-systems.html): Human feedback loop *(verified)*

## DAT · Data handling

Training use, retention and deletion of buyer data, including inside agent records.

### DAT-01

> Is our data used to train or improve any model? How long are prompts, uploads and outputs kept, and how is deletion verified?

**Why they ask.** The first AI question in almost every questionnaire. Buyers also check that the vendor's model providers make the same commitment.

**Evidence that satisfies it**

- Contract terms on no training and on retention, including for model providers (zero retention where available).
- Retention schedule per data type.
- Deletion procedure and a deletion confirmation on request.

**Not enough on its own**

- A privacy policy page.

**References**

- FS-ISAC GenAI Category 2: Data privacy, retention and deletion *(verified)*
- NYDFS AI Letter Data management: Dispose of NPI no longer needed, including NPI used for AI *(verified)*
- NYDFS 500 [500.11(b)(4)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.11): Third-party representations and warranties *(verified)*
- CSA AICM DSP-02; DSP-12; DSP-15; DSP-16: Disposal, purpose limitation, production data use, retention and deletion *(title only)*
- DORA [Art. 30(2)(c)](https://www.digital-operational-resilience-act.com/Article_30.html): Contract provisions on data integrity and confidentiality *(verified)*
- FINOS AIR [AIR-RC-001](https://air-governance-framework.finos.org/risks/ri-1_information-leaked-to-hosted-model.html): Risk: information leaked to hosted model *(verified)*
- NIST AI 600-1 MG-4.1-006: Track dataset deletions and rectifications *(verified)*

### DAT-02

> What personal or confidential data ends up inside your agent action records, and how is it minimized, redacted or protected?

*Derived item, split out from DAT-01 and ACT-01.*

**Why they ask.** Detailed action records are a second copy of customer data. Reviewers will ask the same data questions about the records as about the product.

**Evidence that satisfies it**

- Field-level redaction or hashing of sensitive arguments before records are stored.
- Documented data classes per record field.
- Access and retention rules for records match the data policy.

**Not enough on its own**

- Full request and response bodies logged by default.

**References**

- NYDFS AI Letter Data management: Data minimization *(verified)*
- FINOS AIR [AIR-PREV-014](https://air-governance-framework.finos.org/mitigations/mi-14_encryption-of-ai-data-at-rest.html): Encryption of AI data at rest *(verified)*
- FINOS AIR [AIR-DET-001](https://air-governance-framework.finos.org/mitigations/mi-1_ai-data-leakage-prevention-and-detection.html): Data leakage prevention and detection *(verified)*
- CSA AICM DSP-12: Limitation of purpose *(title only)*
- DORA [Art. 30(2)(c)](https://www.digital-operational-resilience-act.com/Article_30.html): Data confidentiality provisions *(verified)*

## HUM · Human oversight (as the buyer defines it)

Evidence that the oversight model the buyer chose was actually followed.

### HUM-01

> Under the oversight model we define for this use case, which agent actions need human review, and can you show that the review happened whenever it was required? **Hard to evidence today.**

**Why they ask.** The buyer chooses how much oversight a use case needs (by risk, amount, customer impact). What it needs from the vendor is evidence that its chosen model was followed, including that review came before execution where the buyer requires that.

**Evidence that satisfies it**

- Oversight rules expressed as configuration the buyer can read and change.
- Per-action record showing whether review applied, who reviewed, the decision, and its timing relative to execution.
- An exceptions report for actions that should have been reviewed but were not.

**Not enough on its own**

- A workflow screenshot.
- A statement that "humans are in the loop".

**References**

- NAIC AI Bulletin Sec. 3 (risk factors): Extent of human involvement in final decisions *(secondary source)*
- NYDFS AI Letter Training: When human review must be part of verification *(verified)*
- NIST AI RMF GOVERN 3.2; MAP 3.5: Human-AI roles and oversight processes defined *(verified)*
- EU AI Act [Art. 14](https://artificialintelligenceact.eu/article/14/): Human oversight measures for high-risk systems *(verified)*
- FINOS AIR [AIR-PREV-024](https://air-governance-framework.finos.org/mitigations/mi-24_human-in-the-loop-action-approval-gate.html): Where a gate is used, a tamper-evident approval record bound to the action *(verified)*
- CSA AICM GRC-15; IAM-04: Human supervision; separation of duties *(title only)*
- ISO 42001 A.9.2: Processes for responsible use *(secondary source)*

### HUM-02

> What audit trail exists when a person overrides, corrects or reverses what the agent did or recommended?

**Why they ask.** Overrides show where the agent is wrong and who took responsibility. Both matter in a dispute.

**Evidence that satisfies it**

- Override records linked to the original action, with who, when, what changed and why.
- Override rates reported over time.

**Not enough on its own**

- Overrides visible only as a later edit in the target system.

**References**

- NIST AI RMF MANAGE 4.1; MEASURE 3.3: Appeal and override in monitoring; feedback channels *(verified)*
- EU AI Act [Art. 14(4)(d)](https://artificialintelligenceact.eu/article/14/): Overseers can disregard, override or reverse output (high-risk) *(verified)*
- CSA AICM IAM-18: Output modification and special authorization *(title only)*
- FINOS AIR [AIR-DET-011](https://air-governance-framework.finos.org/mitigations/mi-11_human-feedback-loop-for-ai-systems.html): Human feedback loop *(verified)*

## SUB · Sub-processors

Model, voice and tool providers behind the agent, and the buyer's audit and regulator rights.

### SUB-01

> Which model, voice, speech-to-text, text-to-speech and tool providers are involved, and what are their data retention and training terms?

**Why they ask.** Nth-party risk is its own category in bank AI due diligence. Each provider is another place customer data can go.

**Evidence that satisfies it**

- Complete sub-processor list including AI providers, with region and purpose.
- Each provider's retention and training terms.
- Notice process for sub-processor changes.

**Not enough on its own**

- "No subprocessors available."

**References**

- FS-ISAC GenAI Category 6: Nth-party risk and usage *(verified)*
- NYDFS 500 [500.11(a)](https://www.law.cornell.edu/regulations/new-york/23-NYCRR-500.11): Third-party service provider security policy *(verified)*
- NYDFS AI Letter TPSP and vendor management: Diligence on third parties' AI *(verified)*
- CSA AICM DSP-14; STA-08; STA-09; STA-16: Sub-processor disclosure, supply-chain inventory and risk, service BOM *(title only)*
- ISO 42001 A.10.2; A.10.3: Allocating responsibilities; suppliers *(secondary source)*
- NIST AI RMF GOVERN 6.1; MAP 4.1: Third-party AI risk policies and component mapping *(verified)*
- DORA [Art. 28(3); Art. 30(2)(b); RTS 2025/532](https://www.digital-operational-resilience-act.com/Article_28.html): Register, locations, subcontracting conditions *(secondary source)*
- FINOS AIR [AIR-SEC-026](https://air-governance-framework.finos.org/risks/ri-26_mcp-server-supply-chain-compromise.html): Risk: MCP server supply chain compromise *(verified)*

### SUB-02

> What audit rights or audit reports cover the AI system itself, not just your infrastructure? **Hard to evidence today.**

**Why they ask.** Insurers and banks are expected to secure audit rights over third-party AI. A SOC 2 report usually covers infrastructure and access, not agent behaviour.

**Evidence that satisfies it**

- Audit-rights clause covering the AI system.
- Reports whose scope includes agent behaviour, plus record samples the buyer can verify.

**Not enough on its own**

- A SOC 2 report alone.

**References**

- NAIC AI Bulletin Sec. 3, 4.2(a); 4.3: Audit rights or audit reports; exercise of audit rights *(secondary source)*
- NYDFS CL7 ¶37: Audit rights or reports in vendor contracts *(verified)*
- DORA [Art. 28(6); Art. 30(3)(e)](https://www.digital-operational-resilience-act.com/Article_30.html): Audits; access, inspection and audit rights *(verified)*
- FS-ISAC GenAI Level 3: Audit validation *(verified)*
- CSA AICM A&A-02: Independent assessments *(title only)*
- NIST AI 600-1 GV-6.1-006: Clauses allowing evaluation of third-party processes *(verified)*

### SUB-03

> Will you cooperate with regulatory inquiries and give examiners access to the documentation and records they ask for?

**Why they ask.** Regulators examine the buyer, and through the buyer, its AI vendors. Buyers need the cooperation in writing and the artifacts ready.

**Evidence that satisfies it**

- Regulatory cooperation clause.
- A ready evidence package: model documentation, validation, change history and verifiable action records.

**Not enough on its own**

- Best-effort cooperation with no artifacts.

**References**

- NAIC AI Bulletin Sec. 3, 4.2(b); Sec. 4: Cooperation with regulatory inquiries; documents regulators may request *(secondary source)*
- NYDFS CL7 ¶9; ¶37: DFS exam authority; cooperation clause *(verified)*
- DORA [Art. 30(2)(g)](https://www.digital-operational-resilience-act.com/Article_30.html): Full cooperation with competent authorities *(verified)*
- EU AI Act [Art. 18](https://artificialintelligenceact.eu/article/18/): Provider documentation kept for authorities *(verified)*
- ISO 42001 A.8.5: Information for interested parties incl. regulators *(secondary source)*

---

Framework details, versions and per-framework tables: [mappings/](mappings/).
