# AGENTS.md

이 저장소는 Codex용 `loop` 스킬을 배포하기 위한 저장소입니다.

## 작업 원칙

- 실제 스킬 본문은 `skills/loop/SKILL.md`에 둡니다.
- 상세 지식은 `skills/loop/references/`에 둡니다.
- 반복 검증 로직은 `skills/loop/scripts/`에 둡니다.
- 스킬 파일을 바꾼 뒤에는 가능한 경우 다음 검증을 실행합니다.

```powershell
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\skills\loop"
python ".\skills\loop\scripts\validate_loop_spec.py" ".\skills\loop\references\loop-spec-template.yaml"
python ".\skills\loop\scripts\run_in_loop_checks.py" --manifest ".\skills\loop\references\project-check-manifest-template.yaml" --phase all --dry-run --cwd ".\skills\loop"
```

## 품질 기준

- `SKILL.md`는 짧고 절차 중심으로 유지합니다.
- 새 개념은 먼저 reference 파일로 분리합니다.
- Loop 스킬은 자동화보다 검증 가능성을 우선합니다.
- 모델의 완료 주장보다 테스트, 평가, 실행 로그, 사람 승인 같은 외부 증거를 우선합니다.
