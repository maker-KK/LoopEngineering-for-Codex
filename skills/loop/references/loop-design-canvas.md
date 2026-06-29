# Loop Design Canvas

Use this canvas before building or scheduling an agent loop.

## Candidate Fit

| Field | Guidance |
| --- | --- |
| Loop name | Name the recurring work in one sentence. |
| Business goal | Tie the loop to an operational outcome such as reduced review delay, faster ticket handling, or lower incident triage time. |
| Input source | Identify tickets, logs, alerts, PRs, CRM records, documents, CI failures, or scheduled checks. |
| Repetition pattern | Note frequency, volume, and whether the work pattern is stable. |
| Verifiability | List objective checks. If none exist, keep the loop advisory or manual. |
| Risk class | Mark data, customer, production, security, legal, pricing, contract, and brand risks. |
| Owner | Name the loop owner and verifier owner. |

## Operating Contract

| Field | Guidance |
| --- | --- |
| Agent action | List exactly what the agent may do. |
| Forbidden actions | List what the agent must not do, including paths, tools, systems, or decisions. |
| Allowed tools | Include tool names and permission boundaries. |
| Context entrypoint | Usually AGENTS.md, a runbook, a skill, or a ticket template. |
| Required docs | Architecture, testing, product policy, support policy, security policy, or release policy. |
| Done criteria | State concrete pass/fail conditions. |
| Verifier | Use tests, policy checks, evaluator rubric, reviewer agent, or human review. |
| Escalation | Define when to stop and who receives the handoff. |
| Budget | Set max time, max iterations, max cost, max tokens, and max retries. |
| State artifacts | Progress log, run-log.json, PR, ticket comment, decision record, or cost ledger. |
| Evaluation dataset | Core, edge, regression, human-gate, and adversarial examples. |
| Failure taxonomy | How failed runs will be categorized and turned into fixes. |
| Observability | Run log fields, trace fields, privacy boundaries, and cost tracking. |
| Manifest | Version, owner, lifecycle stage, allowed surface, quality bar, and last verified date. |

## Runtime Brakes

| Field | Guidance |
| --- | --- |
| Completion check | Define the external signal that proves done. Do not use model self-report as the completion check. |
| No-progress detection | Define repeated calls, unchanged diffs, identical errors, or lack of new evidence. |
| Timeout | Set wall-clock and per-step limits. |
| Cost ceiling | Set token, tool, model, or dollar limits. |
| Retry policy | Retry only when the next attempt has new evidence, a changed plan, or a narrower scope. |
| Human stop | Name who can stop, approve, or override the loop. |

## Context And Tool Safety

| Field | Guidance |
| --- | --- |
| Context budget | State what stays in active context and what is offloaded. |
| Compaction trigger | Define when to summarize or restart from persisted state. |
| Offload targets | Store large logs, traces, screenshots, long diffs, and bulky outputs outside the active prompt. |
| Tool focus | Keep tools few and non-overlapping. |
| Idempotency | Require duplicate guards for writes and external side effects. |
| Actionable errors | Ensure tool failures tell the agent what corrective action to try next. |

## Minimum Viable Loop

Start with:

1. One known input source.
2. One constrained agent harness.
3. One independent verifier.
4. One state artifact that the next run can read.

Do not add multi-agent routing, scheduling, or broad write permissions until manual runs show stable value.

## Readiness Checklist

- The task is recurring and worth automating.
- The output can be independently verified.
- The agent has only the tools and data it needs.
- The loop has explicit stop conditions.
- The loop has brakes for iterations, timeout, budget, no-progress, and completion checks.
- The loop treats context as a budget and has a compaction/offload plan.
- Side-effecting tools are idempotent or protected by duplicate guards.
- Tool errors are actionable enough to guide the next turn.
- The loop has named human gates for risky decisions.
- The next run can read prior state.
- Cost, runtime, token, and retry limits are set.
- Audit logs can explain inputs, actions, checks, and approvals.
- Eval cases cover normal success, edge cases, regressions, human gates, and adversarial break attempts.
- Observed failures feed back into evals and documentation.
