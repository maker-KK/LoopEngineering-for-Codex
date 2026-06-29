# Loop Observability And Run Logs

Use this reference when a loop needs auditability, production feedback, or post-run analysis.

## Observability Rule

Record enough to explain the run without exposing sensitive content unnecessarily. Store prompts, responses, customer data, secrets, or private documents only when policy explicitly permits it.

## Run Log Schema

```yaml
run_log:
  run_id: "2026-06-29-001"
  loop_name: "daily-regression-fix-loop"
  loop_version: "0.1.0"
  trigger:
    type: "manual"
    source: "ci_failure"
    task_id: "CI-18422"
  input_summary: "unit test failure in auth module"
  context:
    entrypoint: "AGENTS.md"
    context_hash: "sha256:..."
    docs_used: ["docs/testing.md"]
    stale_context_warnings: []
  execution:
    iterations: 2
    tools_called:
      - name: "test_runner"
        count: 2
      - name: "git_diff"
        count: 1
    retries:
      count: 1
      reasons: ["unit_tests_failed"]
    no_progress_detected: false
  verification:
    checks:
      unit_tests: "pass"
      lint: "pass"
      forbidden_path_check: "pass"
    evaluator_score: 0.92
    eval_dataset_version: "daily-regression-fix-loop-evals@0.1.0"
    per_category_scores:
      correct_behavior: 0.95
      insufficient_context: 0.86
      multi_step_or_multi_tool: 0.90
      evidence_accuracy: 1.00
    top_findings:
      - "Evidence accuracy passed because all changed files and test results were cited."
      - "One insufficient-context case required human escalation."
    baseline_candidate_delta: "+0.07 overall, no new safety failures"
  toolchain:
    lifecycle_phase: "evaluate"
    scaffold_artifacts: ["loop-spec.yaml", "tests/eval/datasets/"]
    deployment_surface: "draft_pr"
    deployment_metadata:
      target: "draft_pr"
      url: "https://example.invalid/pr/123"
      rollback: "close draft PR and preserve run log"
    registry_surface:
      type: "ticket_or_pr_link"
      owner_visible: true
      access_policy: "repository reviewers only"
  cost:
    runtime_minutes: 31
    estimated_cost_usd: 1.84
    token_estimate: 42000
  outcome:
    status: "draft_pr_created"
    artifacts: ["progress.md", "draft_pr"]
    escalation_required: false
    escalation_reason: null
  failure_taxonomy: []
  privacy:
    prompt_response_logged: false
    sensitive_data_seen: false
    redactions_applied: []
  next_action: "human review within 24h"
```

## What To Watch

- Success rate by loop version.
- Failure types by frequency.
- Cost per successful task.
- Retry count and no-progress incidents.
- Human escalation rate.
- Tool error rate.
- Per-tool span counts and latency.
- Per-category eval scores and deltas.
- Deployment metadata, smoke-test result, and rollback readiness when applicable.
- Registry or publish status when other people or agents must discover the output.
- Verifier false positives and false negatives.
- Context freshness warnings.
- Safety or privacy events.

## Feedback Into Evals

Turn observed failures into dataset cases:

1. Summarize the failed run without secrets.
2. Add a regression eval case.
3. Add or adjust the metric that should have caught the failure.
4. Re-run baseline and candidate.
5. Update the manifest's `last_verified` only after the candidate passes.
