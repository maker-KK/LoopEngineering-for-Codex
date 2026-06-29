---
name: loop
description: Design, review, implement, or operate Loop Engineering systems for agentic AI workflows. Use when asked to create a Loop, loop spec, recurring agent workflow, autonomous or scheduled agent run, verifier/evaluator, eval dataset, quality flywheel, run ledger, observability plan, failure taxonomy, loop manifest, escalation policy, scaffold/eval/deploy/publish workflow, agent toolchain, cost/permission controls, 30/60/90 rollout, or when converting repeated prompt-driven work into a verified agent operating loop across Codex, MCP, CI, ticketing, support, sales, IT operations, documentation, or customer workflows.
---

# Loop Engineering

Use this skill to turn repeated prompt-driven agent work into a verified operating system. A Loop discovers work, prepares context, executes through an agent harness, verifies against independent evidence, persists state, and decides whether to stop, retry, compact context, escalate, or continue.

## Core Rule

Design for verifiability before autonomy. A model ending its turn is not proof that the task is complete. Preserve the professional quality bar while using agents to go faster. If a loop lacks an independent verifier, explicit brake, state artifact, context management plan, evaluation dataset, observability path, or human escalation path for risky decisions, keep it manual or advisory.

## Workflow

1. Classify the candidate task.
   - Good candidates are recurring, valuable, low to moderate risk, and objectively verifiable.
   - Weak candidates depend on negotiation, taste, politics, legal judgment, pricing, production authority, or sensitive data without a human gate.
2. Define the loop contract.
   - Specify goal, trigger, input source, allowed scope, forbidden actions, expected artifacts, owner, budget, and done criteria.
   - For formal specs, start from `references/loop-spec-template.yaml`.
3. Define the implementation toolchain.
   - Decide whether the loop needs scaffolding, code patterns, eval generation, deploy, publish or registry, observability, and CI/CD.
   - Package these as explicit capability slots in the manifest so the loop does not depend on hidden context or ad hoc terminal memory.
   - If the loop spans editor, terminal, browser, cloud console, and eval tooling, consolidate the workflow into a single runbook and state artifact.
4. Build the context map.
   - Use AGENTS.md or equivalent as the entrypoint and keep it short.
   - Put detailed knowledge in repo-local docs, runbooks, skills, memory, logs, prior run reports, and decision records.
   - Include freshness checks for stale docs and context drift.
5. Design the harness.
   - Limit tools, files, network, secrets, deployment, and write permissions by task.
   - Prefer isolated worktrees or sandboxes for coding loops.
   - Add checkpoints when work may cross sessions or context windows.
6. Design loop brakes before scheduling.
   - Add max iterations, runtime timeout, token or cost ceiling, no-progress detection, and an automated completion check.
   - Treat repeated identical tool calls, unchanged diffs, identical errors, or no new evidence as no-progress signals.
   - Make retry decisions depend on new evidence, not on model confidence.
7. Protect context quality.
   - Treat context as a budget, not a bucket.
   - Compact long runs, offload bulky outputs to files, and return only the slice needed for the next decision.
   - Use subagents or isolated passes for messy subtasks so only clean findings re-enter the main loop.
   - Persist durable state separately from transient reasoning.
8. Design tools for loops.
   - Keep tools few, focused, and non-overlapping.
   - Require idempotent writes or explicit duplicate guards for side-effecting tools.
   - Make tool errors actionable so the next turn knows the corrective action.
9. Design verification before scheduling.
   - Separate generator and evaluator for important work.
   - Combine deterministic checks with semantic review where needed.
   - Do not accept self-grading for merges, customer sends, security changes, pricing, contracts, legal, production, or customer-impacting actions.
10. Add the evaluation flywheel.
   - Start with 1-2 core evaluation cases, then expand to edge cases and adversarial cases.
   - Track failure categories so improvements target recurring failure modes, not anecdotes.
   - Compare baseline and candidate runs before calling a prompt, tool, or policy change an improvement.
11. Run manually first.
   - Use a person-triggered loop until success rate, failure taxonomy, cost/task, retry rate, and escalation patterns are understood.
   - Schedule only after repeated manual runs show stable value and bounded risk.
12. Observe the loop.
   - Record run IDs, task IDs, tool calls, verification results, costs, retry reasons, and human escalation reasons.
   - Keep sensitive prompts and responses out of shared traces unless an explicit privacy policy allows them.
   - Feed observed failures back into the evaluation dataset.
13. Persist and decide.
   - Save progress logs, run logs, cost ledgers, verification results, decision records, commits, PRs, ticket comments, or drafts.
   - Make the next run able to understand what happened, why, what failed, and what must not be repeated.

## Five Loop Actions

Use this sequence for loop design and review:

| Action | Question | Typical artifact |
| --- | --- | --- |
| Discover | What work should be handled now? | Task candidate, priority score |
| Prepare | What minimal context and constraints are needed? | Context bundle, loop prompt |
| Execute | What may the agent do? | Diff, report, ticket update, draft |
| Verify | What independent evidence proves success? | Test result, evaluator score, policy check |
| Persist & Decide | What state is saved and what happens next? | Progress log, retry/escalate/stop decision |

## Reference Architecture

Include these components unless there is a clear reason to omit one:

- Trigger / Scheduler: time, event, or manual approval that starts the loop.
- Work Finder: backlog, ticket, log, alert, PR, CRM, or document source that identifies candidate work.
- Context Builder: minimal sufficient docs, code, policies, memory, and prior artifacts.
- Manifest: versioned loop configuration, owner, lifecycle stage, allowed tools, eval threshold, and last verified date.
- Scaffolder / Template Pack: repeatable project, prompt, eval, runbook, CI, or deployment skeletons that prevent blank-folder drift.
- Agent Harness: tools, permissions, sandbox, checkout/worktree, network, secrets, and checkpoints.
- Brakes: iteration, timeout, budget, no-progress, and completion-check controls.
- Context Manager: compaction, offloading, state persistence, and stale-context controls.
- Tool Contract: focused tool list, idempotent writes, duplicate guards, and actionable errors.
- Generator: the agent run that produces the change, report, draft, ticket update, or other artifact.
- Verifier / Evaluator: tests, lint, policy checks, security scans, independent LLM review, or human gate.
- Evaluation Dataset: core, edge, regression, and adversarial cases used to check changes over time.
- Failure Analyzer: clusters failed runs by failure mode and turns them into fixes or new eval cases.
- Observability: traces, run logs, cost/token data, retry data, and privacy controls for operational review.
- Persistence / Memory: progress file, git history, run log, cost ledger, decision record, ticket comment.
- Publisher / Registry: optional registration, catalog entry, owner, IAM/access policy, and discoverability path after deployment.
- Escalation: named conditions, owner, and handoff path for ambiguity, risk, budget, or repeated failure.

## Verification Layers

Choose the narrowest reliable checks first, then add layers where risk requires them:

- Static: lint, schema validation, forbidden dependency or path checks.
- Dynamic: unit tests, e2e tests, builds, UI automation, log queries.
- Semantic: rubric-based evaluator, reviewer agent, acceptance criteria review.
- Security: secret scan, SAST, DLP, dependency scan, egress policy, least-privilege review.
- Business: human approval, product owner review, legal/compliance gate.

## Stop And Escalation Rules

Stop or escalate when any of these apply:

- The verifier is missing, circular, or only self-graded.
- The only completion signal is the model stopping or claiming completion.
- The loop fails the same way repeatedly, usually after 3 attempts unless a lower cap is set.
- The loop repeats the same tool call, diff, error, or plan without new evidence.
- Context has become too noisy to justify the next action; compact, offload, or restart from persisted state.
- Runtime, cost, token, or iteration budget is exceeded.
- Required permissions, secrets, production access, or customer-impacting authority are missing or unsafe.
- Sensitive data, legal, contract, pricing, security exception, production deployment, or customer-impacting decisions appear.
- Requirements are ambiguous enough that the agent would invent business judgment.
- Audit history cannot explain inputs, actions, tools used, checks passed, and approvals.

## Resources

- Read `references/loop-design-canvas.md` when creating or reviewing a new loop concept.
- Read `references/agentic-engineering-toolchain.md` when designing scaffold, eval, deploy, publish/registry, observability, CI/CD, or multi-tool agent workflows.
- Read `references/runtime-brakes-context-tools.md` when defining brakes, context compaction, no-progress detection, or loop-safe tools.
- Read `references/evaluator-rubric.md` when defining quality gates or independent evaluators.
- Read `references/loop-evaluation-quality-flywheel.md` when creating eval cases, metrics, failure taxonomy, or adversarial tests.
- Read `references/loop-lifecycle.md` when moving from concept to manual run, scheduled run, deployment, or continuous improvement.
- Read `references/loop-observability-run-log.md` when defining run logs, trace fields, privacy boundaries, or production feedback.
- Use `references/loop-spec-template.yaml` when the output should be a concrete loop specification.
- Use `references/loop-manifest-template.yaml` when the loop should have a versioned configuration artifact.
- Run `scripts/validate_loop_spec.py <spec.yaml>` when a loop spec file exists.

## Output Expectations

When producing a loop design, include:

- Candidate fit assessment.
- Minimal loop architecture.
- Implementation toolchain with scaffold, eval, deploy, publish or registry, observability, and CI/CD decisions where applicable.
- Loop spec or design canvas.
- Verification plan with independent evidence.
- Evaluation dataset plan with core, edge, regression, and adversarial cases.
- Brake plan with max iteration, timeout, budget, no-progress, and completion-check controls.
- Context management and compaction/offloading plan.
- Tool contract covering focused tools, idempotent writes, duplicate guards, and actionable errors.
- Lifecycle stage and next maturity move.
- Observability and privacy plan for run logs, traces, cost, retries, and human gates.
- Manifest fields that make the loop configuration versioned and inspectable.
- Stop, retry, budget, and escalation rules.
- State artifacts and audit trail.
- Manual-run plan before automation.
- Rollout recommendation, usually starting at maturity level 1 or 2 and only scheduling after stable manual runs.

## Source Basis

This skill is based on the Loop Engineering integrated whitepaper provided by the user. Its main operating model is Prompt -> Context -> Harness -> Loop, with the Loop layer responsible for repeated runs, verification, state, memory, scheduling, cost control, and escalation.
