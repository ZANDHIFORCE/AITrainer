# 로컬 실행

[README로 돌아가기](../README.md)

## 준비

Python과 가상환경을 준비합니다. 웹 서비스의 직접 의존성은 Flask와 OpenAI SDK입니다. 루트 `requirements.txt`는 `web/requirements.txt`를 포함하며 웹 의존성의 버전은 고정되어 있지 않습니다.

```bash
git clone https://github.com/ZANDHIFORCE/AITrainer.git
cd AITrainer
python -m venv .venv
```

가상환경 활성화:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

웹 서비스만 실행할 때:

```bash
python -m pip install -r requirements.txt
```

모델 비교 실험은 별도 환경에서 준비합니다. [GPT 실험 의존성](../experiments/gpt/requirements.txt)과 [MediaPipe 실험 의존성](../experiments/mediapipe/requirements.txt)은 기존 실험 환경의 버전 기록입니다. 현재 Python·운영체제와의 설치 호환성은 다시 검증하지 않았습니다.

```bash
# GPT 실험
python -m pip install -r experiments/gpt/requirements.txt
# MediaPipe 실험 (별도 가상환경)
python -m pip install -r experiments/mediapipe/requirements.txt
```

GPT 실험 파일은 `experiment_01_trained_chatgpt.py`부터 `experiment_06_service_chatgpt.py`까지 기존 번호를 유지했습니다. MediaPipe의 `app.py`는 원래 함께 보관된 `experiments/mediapipe/squat_img` 이미지를 읽습니다. 루트의 `data/squat`으로 대체하지 않았습니다.

## API 키 설정

웹 화면 열기에는 키가 필요하지 않습니다. 실제 자세 분석·식단 제안은 유효한 API 키와 해당 모델 접근 권한이 필요하며 API 사용 비용이 발생할 수 있습니다. 키는 저장소에 기록하지 않습니다.

```powershell
# Windows PowerShell: 현재 터미널에만 적용
$env:OPENAI_API_KEY = "<your-api-key>"
```

```bash
# macOS / Linux: 현재 셸에만 적용
export OPENAI_API_KEY="<your-api-key>"
```

## 서버 실행

```bash
python web/app.py
```

저장소 루트에서 실행하고 `http://127.0.0.1:5000`에 접속합니다. AI 스크립트와 템플릿 경로는 `web/app.py` 위치를 기준으로 찾습니다. 다른 폴더에서는 `app.py`의 절대 경로로 실행할 수 있습니다. 현재 진입점은 Flask 디버그 모드이며 로컬 개발 확인용입니다.

## 예시 이미지 경로

자세 분석과 GPT 실험은 GitHub의 `data/squat`, `data/legacy_squat` 이미지를 URL로 전달합니다. 기본 브랜치는 `main`이며, 구조 변경 PR을 확인할 때는 해당 브랜치를 지정합니다.

```powershell
$env:AITRAINER_ASSET_REF = "codex/structure-cleanup"
```

```bash
export AITRAINER_ASSET_REF="codex/structure-cleanup"
```

새 경로는 선택한 브랜치가 원격에 올라간 뒤 접근할 수 있습니다. 병합 뒤에는 환경변수를 해제하여 기본 `main`을 사용합니다. 로컬 경로 확인과 외부 URL 접근·실제 AI 호출 확인은 구분합니다.

| 경로 | 기능 |
| :--- | :--- |
| `GET /` | 메뉴 |
| `GET /posture` | 이미지 URL 입력 |
| `POST /process` | 자세 분석 |
| `GET /intensity` | 운동 강도 입력 |
| `POST /calculate` | 계산 결과 |
| `GET /diet` | 식단 입력 |
| `POST /process_2` | 식단 제안 |

자세 분석에는 외부 API에서 읽을 수 있는 이미지 URL을 입력합니다. 로컬 파일 경로나 로그인해야 볼 수 있는 링크는 적합하지 않습니다. 운동 강도 입력의 키는 **cm**, 체중·골격근량은 **kg**입니다.

## 문제 확인

- 화면은 열리지만 AI 요청이 실패하면 API 키, 모델 접근 권한, 이미지 URL 접근 여부를 확인하세요.
- API 오류가 결과 화면에 그대로 표시될 수 있습니다. 현재 서비스는 구조화된 오류 응답을 별도로 정의하지 않았습니다.
- 실험 수치의 재현에는 같은 이미지, 프롬프트, 모델과 집계 조건의 확인이 필요합니다.

실제 확인한 범위는 [검증 기록](VALIDATION.md)을 참고하세요.
