<!-- Generated from checklist.yaml by scripts/build.py. Do not edit by hand. -->

# FINOS AI Governance Framework

- Source: <https://air-governance-framework.finos.org/>
- Version used: Live site incl. v2.0 agentic additions (accessed 2026-10-14)
- Type: Industry framework
- Access: public
- Checked: 2026-10-14

| Control | What it covers | Checklist items | How we checked |
|---|---|---|---|
| [AIR-DET-001](https://air-governance-framework.finos.org/mitigations/mi-1_ai-data-leakage-prevention-and-detection.html) | AI data leakage prevention and detection; Data leakage prevention and detection | [DAT-02](../checklist.md#dat-02), [INC-02](../checklist.md#inc-02) | verified |
| [AIR-DET-004](https://air-governance-framework.finos.org/mitigations/mi-4_ai-system-observability.html) | AI system observability, centralized logs; Observability and alerting on anomalies; Centralize AI logs, for example in a SIEM | [ACT-03](../checklist.md#act-03), [OUT-02](../checklist.md#out-02), [RET-01](../checklist.md#ret-01) | verified |
| [AIR-DET-011](https://air-governance-framework.finos.org/mitigations/mi-11_human-feedback-loop-for-ai-systems.html) | Human feedback loop | [CHG-04](../checklist.md#chg-04), [HUM-02](../checklist.md#hum-02) | verified |
| [AIR-DET-013](https://air-governance-framework.finos.org/mitigations/mi-13_providing-citations-and-source-traceability-for-ai-generated-information.html) | Citations and source traceability | [ACT-04](../checklist.md#act-04) | verified |
| [AIR-DET-015](https://air-governance-framework.finos.org/mitigations/mi-15_using-large-language-models-for-automated-evaluation-llm-as-a-judge-.html) | LLM-as-a-judge evaluation calibrated to humans | [CHG-03](../checklist.md#chg-03) | verified |
| [AIR-DET-016](https://air-governance-framework.finos.org/mitigations/mi-16_preserving-source-data-access-controls-in-ai-systems.html) | Preserve source data access controls | [ACT-04](../checklist.md#act-04) | verified |
| [AIR-DET-021](https://air-governance-framework.finos.org/mitigations/mi-21_agent-decision-audit-and-explainability.html) | Log decision initiation, including the triggering event and context; Log inputs, reasoning, tool selection, actions taken and downstream effects; Log actions taken and their downstream effects; Tamper-evident logging and immutable records; names hash chaining and signed segments; Records verifiable by deployer, auditor or authority without privileged access to the provider; anchoring to a transparency log; Tier 1 is reconstruction of what happened | [ACC-02](../checklist.md#acc-02), [ACT-01](../checklist.md#act-01), [INC-01](../checklist.md#inc-01), [OUT-01](../checklist.md#out-01), [TMP-01](../checklist.md#tmp-01), [TMP-02](../checklist.md#tmp-02) | verified |
| [AIR-OP-005](https://air-governance-framework.finos.org/risks/ri-5_foundation-model-versioning.html) | Risk: foundation model versioning | [ACT-02](../checklist.md#act-02) | verified |
| [AIR-OP-017](https://air-governance-framework.finos.org/risks/ri-17_lack-of-explainability.html) | Risk: lack of explainability | [ACT-06](../checklist.md#act-06) | verified |
| [AIR-PREV-003](https://air-governance-framework.finos.org/mitigations/mi-3_user-app-model-firewalling-filtering.html) | User/app/model firewalling and filtering | [ACC-03](../checklist.md#acc-03) | verified |
| [AIR-PREV-005](https://air-governance-framework.finos.org/mitigations/mi-5_system-acceptance-testing.html) | System acceptance testing | [CHG-02](../checklist.md#chg-02) | verified |
| [AIR-PREV-007](https://air-governance-framework.finos.org/mitigations/mi-7_legal-and-contractual-frameworks-for-ai-systems.html) | Contracts cover model versioning and change notification | [CHG-01](../checklist.md#chg-01) | verified |
| [AIR-PREV-010](https://air-governance-framework.finos.org/mitigations/mi-10_ai-model-version-pinning.html) | AI model version pinning; Model version pinning; Advance notice of new versions and deprecations | [ACT-02](../checklist.md#act-02), [CHG-01](../checklist.md#chg-01), [INC-03](../checklist.md#inc-03) | verified |
| [AIR-PREV-014](https://air-governance-framework.finos.org/mitigations/mi-14_encryption-of-ai-data-at-rest.html) | Encryption of AI data at rest | [DAT-02](../checklist.md#dat-02) | verified |
| [AIR-PREV-018](https://air-governance-framework.finos.org/mitigations/mi-18_agent-authority-least-privilege-framework.html) | Agent authority least privilege | [ACC-01](../checklist.md#acc-01) | verified |
| [AIR-PREV-019](https://air-governance-framework.finos.org/mitigations/mi-19_tool-chain-validation-and-sanitization.html) | Tool chain validation and sanitization | [ACC-01](../checklist.md#acc-01), [ACC-03](../checklist.md#acc-03) | verified |
| [AIR-PREV-020](https://air-governance-framework.finos.org/mitigations/mi-20_mcp-server-security-governance.html) | Log all MCP traffic | [ACT-03](../checklist.md#act-03) | verified |
| [AIR-PREV-023](https://air-governance-framework.finos.org/mitigations/mi-23_agentic-system-credential-protection-framework.html) | Agentic credential protection, signed agent API requests | [ACC-02](../checklist.md#acc-02) | verified |
| [AIR-PREV-024](https://air-governance-framework.finos.org/mitigations/mi-24_human-in-the-loop-action-approval-gate.html) | Tamper-evident approval record; hash chaining alone is not non-repudiation; Where a gate is used, a tamper-evident approval record bound to the action | [HUM-01](../checklist.md#hum-01), [TMP-01](../checklist.md#tmp-01) | verified |
| [AIR-PREV-025](https://air-governance-framework.finos.org/mitigations/mi-25_skill-plugin-integrity-and-governance.html) | Skill and plugin integrity | [CHG-02](../checklist.md#chg-02) | verified |
| [AIR-RC-001](https://air-governance-framework.finos.org/risks/ri-1_information-leaked-to-hosted-model.html) | Risk: information leaked to hosted model | [DAT-01](../checklist.md#dat-01) | verified |
| [AIR-SEC-010](https://air-governance-framework.finos.org/risks/ri-10_prompt-injection.html) | Risk: prompt injection | [ACC-03](../checklist.md#acc-03) | verified |
| [AIR-SEC-024](https://air-governance-framework.finos.org/risks/ri-24_agent-action-authorization-bypass.html) | Risk: agent action authorization bypass | [ACC-01](../checklist.md#acc-01) | verified |
| [AIR-SEC-025](https://air-governance-framework.finos.org/risks/ri-25_tool-chain-manipulation-and-injection.html) | Risk: tool chain manipulation and injection | [ACC-03](../checklist.md#acc-03) | verified |
| [AIR-SEC-026](https://air-governance-framework.finos.org/risks/ri-26_mcp-server-supply-chain-compromise.html) | Risk: MCP server supply chain compromise | [SUB-01](../checklist.md#sub-01) | verified |
| [AIR-SEC-029](https://air-governance-framework.finos.org/risks/ri-29_agent-mediated-credential-discovery-and-harvesting.html) | Risk: agent-mediated credential harvesting | [ACC-02](../checklist.md#acc-02) | verified |
