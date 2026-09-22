# 로컬 실행

[README로 돌아가기](../README.md)

## 준비

Python과 가상환경을 준비합니다. 웹 서비스의 직접 의존성은 Flask와 OpenAI SDK이며, 루트 `requirements.txt`에는 모델 비교 실험용 라이브러리도 포함되어 있습니다. 기존 의존성 파일의 버전은 고정되어 있지 않습니다.

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
python -m pip install flask openai
```

모델 비교 실험까지 준비할 때는 별도 환경에서 `python -m pip install -r requirements.txt`를 실행하고 각 실험의 의존성과 호환성을 확인하세요.

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
cd AiTrainer_flaskServer
python app.py
```

`http://127.0.0.1:5000`에 접속합니다. 스크립트가 상대 경로로 실행되므로 반드시 `AiTrainer_flaskServer` 안에서 실행하세요. 현재 진입점은 Flask 디버그 모드이며 로컬 개발 확인용입니다.

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
