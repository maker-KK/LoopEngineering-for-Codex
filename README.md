# Loop Engineering for Codex

Codex에서 반복 업무를 안전하게 설계하고 운영하기 위한 `loop` 스킬입니다.

이 스킬은 단순히 "AI에게 일을 시키는 법"이 아니라, AI가 반복해서 일할 때 필요한 완료 조건, 중단 조건, 검증, 평가 데이터셋, 실행 로그, 사람 승인 지점을 함께 설계하도록 돕습니다.

## 무엇을 도와주나요?

- 반복 업무를 Loop로 설계합니다.
- 자동화해도 되는 업무인지 먼저 평가합니다.
- AI가 할 수 있는 일과 하면 안 되는 일을 나눕니다.
- "AI가 끝났다고 말했다"가 아니라 실제 검증 기준으로 완료를 판단하게 합니다.
- 실패 유형을 기록하고 다음 평가 데이터셋으로 되돌립니다.
- 실행 로그, 비용, 도구 호출, 사람 개입 이유를 남기도록 설계합니다.
- 스캐폴드, 평가, 배포, 등록, 관찰성을 하나의 운영 흐름으로 묶습니다.

## 설치 방법

Windows PowerShell에서 이 저장소를 받은 뒤 아래 명령을 실행하시면 됩니다.

```powershell
$src = ".\skills\loop"
$dst = "$HOME\.codex\skills\loop"
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
if (Test-Path $dst) {
  Remove-Item -LiteralPath $dst -Recurse -Force
}
Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
```

설치 후 Codex 앱을 새로 열면 `$loop` 스킬을 사용할 수 있습니다.

## 사용 예시

Codex에 이렇게 요청하시면 됩니다.

```text
$loop 매주 반복하는 보고서 작성 업무를 안전한 반자동 Loop로 설계해줘.
```

```text
$loop 고객지원 답변 초안을 자동화하고 싶은데, 사람이 승인해야 하는 지점까지 포함해서 설계해줘.
```

```text
$loop 이 코딩 작업을 자동으로 반복 실행하려면 완료 조건, 중단 조건, 평가 데이터셋, 실행 로그가 어떻게 필요할지 정리해줘.
```

## 포함된 구성

```text
skills/loop/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- references/
|   |-- agentic-engineering-toolchain.md
|   |-- evaluator-rubric.md
|   |-- loop-design-canvas.md
|   |-- loop-evaluation-quality-flywheel.md
|   |-- loop-lifecycle.md
|   |-- loop-manifest-template.yaml
|   |-- loop-observability-run-log.md
|   |-- loop-spec-template.yaml
|   `-- runtime-brakes-context-tools.md
`-- scripts/
    `-- validate_loop_spec.py
```

## 핵심 개념

Loop는 다음 순서로 움직입니다.

1. Discover: 어떤 일을 처리할지 찾습니다.
2. Prepare: 필요한 맥락과 제약을 준비합니다.
3. Execute: AI가 도구를 사용해 결과를 만듭니다.
4. Verify: 독립 기준으로 성공 여부를 확인합니다.
5. Persist & Decide: 기록을 남기고 다음 행동을 정합니다.

중요한 원칙은 하나입니다.

> 모델이 멈췄다는 것은 일이 끝났다는 뜻이 아닙니다. 완료는 검증으로 증명해야 합니다.

## 검증

스킬 형식 검증:

```powershell
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\skills\loop"
```

Loop spec 템플릿 검증:

```powershell
python ".\skills\loop\scripts\validate_loop_spec.py" ".\skills\loop\references\loop-spec-template.yaml"
```

## 참고한 방향

- Loop Engineering 통합 백서 기반 구조
- Daily Dose of Data Science의 Loop Engineering 설명에서 정리한 brakes, context rot, tool safety
- Andrej Karpathy의 agentic engineering 관점: 속도를 높이되 전문 품질 기준을 유지
- Google `agents-cli`의 skill suite, scaffold, eval, deploy, publish, observe 생애주기 아이디어
