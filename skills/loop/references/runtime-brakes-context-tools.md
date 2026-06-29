# Runtime Brakes, Context, And Tool Contracts

Use this reference when a loop may run longer than one turn, retry side effects, or accumulate noisy context.

## Brakes

A model stop signal means the turn ended; it does not prove the job is done. Add brakes that the generator does not control:

| Brake | Design requirement |
| --- | --- |
| Max iterations | Set the maximum number of execute/verify cycles before escalation. |
| Timeout | Set wall-clock runtime and per-step timeout limits. |
| Cost cap | Set token, model, tool, or dollar limits per run. |
| No-progress detection | Detect repeated tool calls, unchanged diffs, identical failures, or no new evidence. |
| Completion check | Define an automated or independent condition that proves success. |
| Human stop | Define who can stop, approve, or override the loop. |

Retry only when the next attempt will use new evidence, a changed plan, or a narrower scope.

## Context Management

Treat context as a budget.

- Keep only the next-decision slice in the active context.
- Move large tool outputs, logs, screenshots, traces, and long diffs into files.
- Summarize long runs into a compact progress artifact.
- Preserve durable state separately from transient reasoning.
- Use subagents or isolated passes for messy subtasks, then return clean findings.
- Restart from persisted state when context rot makes the active context unreliable.

Include these fields in a loop spec:

```yaml
context_management:
  max_active_context: "only evidence needed for the next decision"
  compaction_trigger: "after each failed iteration or when context exceeds budget"
  offload_targets: ["logs/", "artifacts/", "run-log.json"]
  return_to_context: ["root cause", "changed files", "verification result", "next action"]
  stale_context_policy: "restart from progress log when prior reasoning conflicts with ground truth"
```

## Tool Contract

Loop tools need stricter contracts than one-shot tools because errors and side effects feed the next turn.

| Tool property | Requirement |
| --- | --- |
| Focus | Keep tools few and non-overlapping. |
| Selection clarity | A human should be able to tell which tool fits the situation. |
| Idempotent writes | Retrying a write must not create duplicate records, charges, messages, or tickets. |
| Duplicate guards | Side-effecting calls need request IDs, upsert keys, dry-run modes, or existence checks. |
| Actionable errors | Error messages should state what failed, why it likely failed, and what to try next. |
| Least privilege | Tools should expose only the data and actions needed for the loop. |

Example spec block:

```yaml
tool_design:
  focused_tool_count: true
  non_overlapping_tools: true
  idempotent_writes_required: true
  duplicate_guard: "use task_id as idempotency key before creating external records"
  actionable_error_contract: "errors must include cause, retryability, and next corrective action"
```
