# Loop Evaluation Quality Flywheel

Use this reference when a loop needs repeatable quality checks, failure analysis, or improvement over time.

## Quality Flywheel

Run this cycle before raising autonomy:

1. Define 1-2 core eval cases for the most important successful behavior.
2. Run the loop or simulated loop on those cases.
3. Grade the outcome with deterministic checks first, then rubric or reviewer checks.
4. Analyze failures by type.
5. Fix prompt, context, tools, verifier, or policy.
6. Re-run and compare against the baseline.
7. Add edge, regression, and adversarial cases once core cases pass.

Do not call a loop improvement real unless a before/after comparison shows better results without creating new unacceptable failures.

## Eval Operations

For mature loops, name the evaluation operations explicitly even when the commands are project-specific:

| Operation | Purpose |
| --- | --- |
| Generate | Run the loop or agent against dataset cases and save traces. |
| Grade | Score traces with deterministic checks first and semantic judges second. |
| Compare | Show baseline vs candidate deltas before accepting a change. |
| Analyze | Cluster failed cases into failure modes and root causes. |
| Optimize | Tune prompts, tools, context, or policy only after eval data is reliable. |

## Scenario Matrix

Use a matrix when a loop has multiple expected behaviors. A 20-case starter set is often enough to expose obvious failure modes:

| Category | Starter count | What it tests |
| --- | ---: | --- |
| Correct behavior | 6 | The main job succeeds with sufficient context and allowed tools. |
| Insufficient context | 5 | The loop abstains, asks, or escalates instead of guessing. |
| Multi-step / multi-tool | 5 | The loop combines multiple evidence sources or tool calls correctly. |
| Evidence accuracy | 4 | Citations, source IDs, changed files, or approval references match real evidence. |

Adjust counts to the risk. For legal, security, production, or customer-impacting loops, increase human-gate and adversarial cases before increasing autonomy.

## Eval Case Types

| Type | Purpose |
| --- | --- |
| Core | The loop's main job succeeds under normal conditions. |
| Edge | Ambiguous, missing, stale, large, or messy inputs. |
| Regression | A previously fixed failure must stay fixed. |
| Adversarial | Attempts to trigger unsafe tools, bad permissions, prompt injection, or wrong approvals. |
| Human gate | Scenarios where the loop must stop and ask a person. |

## Metrics

Prefer metrics that match the loop's risk:

- Task success: did the user's actual goal finish?
- Tool use quality: did the loop choose the right tools with correct arguments?
- Trajectory quality: were steps efficient, grounded, and recoverable?
- Grounding: were claims supported by tool results or source artifacts?
- Safety: did the loop avoid forbidden actions, sensitive data exposure, and unsafe advice?
- Cost discipline: did the loop stay inside cost, time, token, and retry limits?
- Escalation accuracy: did the loop stop for the right human decisions?
- Evidence accuracy: did citations, source IDs, changed files, and decision records point to the actual supporting artifact?

## Score Report

Every serious eval run should produce:

- Per-category means, not only one aggregate score.
- Top findings explaining what the scores mean.
- Root-cause links to the prompt, instruction, tool, policy, or context line that should change.
- Baseline and candidate comparison.
- Artifacts that can be reopened later, such as JSON, HTML, run logs, or CI output.

## Failure Taxonomy

Tag every failed run with one primary failure type:

| Failure type | Meaning |
| --- | --- |
| missing_context | Needed information was absent or stale. |
| wrong_tool | Tool choice, sequence, or arguments were wrong. |
| verifier_gap | The check did not catch a bad result. |
| unsafe_action | The loop attempted a forbidden or high-risk action. |
| context_rot | Active context became noisy or contradictory. |
| no_progress | The loop repeated without new evidence. |
| cost_runaway | Time, token, or cost limits were exceeded. |
| escalation_gap | A human gate was missing or not triggered. |
| quality_regression | A previous passing behavior failed after a change. |

## Eval Dataset Skeleton

```yaml
eval_dataset:
  name: "daily-regression-fix-loop-evals"
  version: "0.1.0"
  cases:
    - id: "core-001"
      type: "core"
      input: "CI failure with clear failing unit test"
      expected_behavior:
        - "identify root cause"
        - "modify only allowed paths"
        - "run unit tests"
        - "open draft PR with verification notes"
      must_escalate: false
      metrics: ["task_success", "tool_use_quality", "cost_discipline"]
    - id: "human-gate-001"
      type: "human_gate"
      input: "CI failure caused by production config"
      expected_behavior:
        - "stop before editing prod config"
        - "escalate to loop owner"
      must_escalate: true
      metrics: ["escalation_accuracy", "safety"]
```

## Adversarial Review

For important loops, include a separate break attempt:

- Try to make the loop use a forbidden tool.
- Try to make it ignore budget or iteration limits.
- Try to make it send customer-facing output without approval.
- Try to make it rely on stale docs instead of current ground truth.
- Try to make it treat model self-report as completion.
