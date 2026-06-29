# Loop Lifecycle

Use this reference when moving a loop from idea to operation.

## Lifecycle Stages

| Stage | Goal | Exit criteria |
| --- | --- | --- |
| 0. Concept | Decide whether the work is a good loop candidate. | Candidate fit, risk class, and owner are clear. |
| 1. Spec | Write the loop contract and manifest. | Goal, scope, tools, brakes, evals, and human gates are defined. |
| 2. Manual Run | Run only when a person starts it. | Several runs produce stable value and clear failure taxonomy. |
| 3. Evaluated Loop | Run against core and edge eval cases. | Eval threshold passes and failures are understood. |
| 4. Scheduled Verified Loop | Trigger automatically with strict brakes. | Scheduler, budget, stop rules, and escalation all work. |
| 5. Observed Loop | Review traces, logs, cost, and production-like feedback. | Run data feeds new eval cases and improvement backlog. |
| 6. Governed Portfolio | Manage several loops as an operating system. | Owners, standards, audits, and recurring cleanup are in place. |

## Default Path

1. Write a manifest.
2. Create a small eval dataset.
3. Run manually.
4. Fix failures and expand evals.
5. Schedule only after manual runs and evals are stable.
6. Observe real runs.
7. Feed observed failures back into evals and docs.

## Agentic Toolchain Path

When a loop builds or operates an agent, use this fuller path:

| Phase | Loop question | Evidence to save |
| --- | --- | --- |
| Spec | What should the agent do, with which tools and constraints? | Loop spec, success criteria, forbidden actions |
| Scaffold | What repeatable project or runbook skeleton prevents blank-folder drift? | Generated files, manifest, commands, eval folders |
| Build | What agent, prompt, tool, or workflow body changed? | Diff, prompt version, tool contract |
| Orchestrate | Does the work need specialists with separate tool surfaces? | Routing rule, subagent list, handoff contract |
| Evaluate | What traces, scores, and failures prove readiness? | Dataset version, score report, failure clusters |
| Deploy | Where does the loop or agent run, and how is it rolled back? | Dry-run, smoke test, metadata, rollback path |
| Publish | How do people or other agents discover it safely? | Registry entry, PR/ticket link, owner, access policy |
| Observe | What production or manual-run evidence feeds the next eval? | Trace, run log, cost, latency, feedback |

Use all phases only when applicable. A draft-producing Codex loop can map deploy to "draft PR created" and publish to "PR linked from the source ticket."

## Deployment Or Scheduling Gate

Do not schedule, deploy, or publish a loop until:

- Core eval cases pass.
- Human-gate eval cases stop correctly.
- The run log schema captures enough audit evidence.
- The loop has a rollback or clean-state plan.
- Cost, timeout, and retry limits are tested.
- The owner accepts remaining risks.

## Google Agents CLI Mapping

When building Google ADK or Gemini Enterprise agents, `google/agents-cli` maps to these lifecycle phases:

| Agents CLI idea | Loop lifecycle equivalent |
| --- | --- |
| Installed skill suite | Toolchain capability slots |
| `.agents-cli-spec.md` | Loop spec |
| `scaffold` | Spec to project structure |
| ADK code skill | Build and orchestrate |
| `eval generate` and `eval grade` | Evaluated Loop |
| `eval compare` | Baseline vs candidate comparison |
| `eval analyze` | Failure taxonomy |
| `eval optimize` | Improvement loop |
| `deploy` | Scheduled or deployed loop |
| `publish gemini-enterprise` | Publisher / Registry |
| observability guides | Observed Loop |

Do not require Google Cloud or ADK for ordinary Codex loops. Treat it as an optional implementation path when the loop is specifically a Google agent project.
