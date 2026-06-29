# Loop Evaluator Rubric

Use this rubric to define or review a loop verifier. Important loops need evidence outside the generator agent's own claims.

## Scoring Rubric

Score each item from 0 to 3.

| Criterion | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Requirement fit | Core requirement missing | Partially addressed | Mostly addressed | Fully satisfies stated criteria |
| Verifiability | Cannot be verified | Manual inspection only | Some automated checks | Automated checks pass with clear evidence |
| Risk control | High risk uncontrolled | Risk named only | Mitigation exists | Low risk or rollback/human gate is ready |
| State quality | No record | Result only | Includes decision basis | Next run can continue from the record |
| Permission control | Excessive access | Boundaries unclear | Mostly limited | Least privilege with audit trail |
| Cost control | No cap | Informal cap | Budget set | Budget tracked per run with retry policy |
| Brake quality | Uses model self-report | Has one informal stop rule | Has iteration/time/cost limits | Has external completion check plus no-progress detection |
| Context hygiene | Keeps everything in context | Ad hoc summaries | Has compaction/offload policy | Active context contains only next-decision evidence |
| Tool safety | Retried writes can duplicate side effects | Some tool boundaries exist | Idempotency or guards exist | Focused tools, duplicate guards, and actionable errors are enforced |
| Eval coverage | No repeatable cases | Only happy-path cases | Core and edge cases exist | Core, edge, regression, human-gate, and adversarial cases are tracked |
| Observability | No run log | Outcome only | Run log captures checks and costs | Run log supports failure analysis, privacy review, and eval feedback |

## Recommended Thresholds

- Exploratory advisory loop: average score 2.0 or higher, no 0 in risk control.
- Manual operational loop: average score 2.3 or higher, no 0 in verifiability, risk, or state.
- Scheduled verified loop: average score 2.6 or higher, no score below 2 in verifiability, risk, state, permission, or cost.

## Verification Layer Examples

| Layer | Examples |
| --- | --- |
| Static | Lint, schema validation, policy file check, forbidden path check |
| Dynamic | Unit test, build, e2e test, UI smoke test, log query |
| Semantic | Acceptance rubric, independent reviewer agent, requirement matrix |
| Security | Secret scan, SAST, dependency scan, DLP, egress policy |
| Business | Product owner, legal/compliance, sales owner, support owner approval |

## Reviewer Questions

- Does the verifier inspect the actual artifact or environment, not just the plan?
- Does the generator have incentives or context that make self-grading unreliable?
- Is the loop completion check independent of the model's decision to stop?
- Can the loop detect no progress before wasting another turn?
- Are context compaction and offloading rules explicit?
- Can side-effecting tools be retried without duplicating external records or actions?
- Do tool errors tell the agent what to do next?
- Are failures converted into regression eval cases?
- Does the run log capture enough evidence without storing sensitive content unnecessarily?
- Can a later reviewer reconstruct what passed, failed, and why?
- Are failures categorized so future runs can improve?
- Is there a clear path from verifier failure to retry, rollback, stop, or escalation?
