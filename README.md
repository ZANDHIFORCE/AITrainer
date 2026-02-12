# AI Trainer for Fitness Beginners (초보를 위한 AI 피트니스 트레이너) 🏋️‍♂️

> **Kyung Hee University, School of Computing**  
> **저자**: 조동휘 (DongHwee Cho), 성무진 (Mujeen Sung)

본 프로젝트는 현대인의 건강한 운동 습관 형성을 돕기 위해 개발된 **통합 AI 홈 트레이닝 솔루션**입니다. 기존 AI 운동 분석 시스템의 한계를 극복하기 위해 컴퓨터 비전 기술과 거대 언어 모델(LLM)의 멀티모달 기능을 결합하여 높은 정밀도의 자세 교정 및 개인 맞춤형 가이드를 제공합니다.

# 비교모델
1. 딥러닝 기반 포즈 추정 모델: Teachable Machine
<img width="480" height="345" alt="image" src="https://github.com/user-attachments/assets/9cc82aa3-9757-4416-af3c-e178fd962cc6" />
<img width="277" height="283" alt="image" src="https://github.com/user-attachments/assets/fbfea461-99c1-41dc-a6b6-be1041482723" />


2. 규칙 기반 포즈 추정 모델: Mediapipe
<img width="480" height="309" alt="image" src="https://github.com/user-attachments/assets/a7e8bcd3-d361-4d66-a1e4-fa402daaebdd" />
<img width="477" height="380" alt="image" src="https://github.com/user-attachments/assets/ddab5ce8-0b94-4ffb-ab8b-232b51864fdc" />


3. ChatGpt4o 기반 추정 모델: ChatGpt4o
<img width="720" height="911" alt="image" src="https://github.com/user-attachments/assets/a2dcdc2a-dc83-494f-8ece-df49c87c6316" />


---

## 🚀 핵심 연구 및 기능

### 1. 지능형 자세 교정 (Posture Correction)
기존의 랜드마크 기반 모델(MediaPipe)과 이미지 분류 모델(Teachable Machine)의 약점을 보완하기 위해 **GPT-4o Vision**을 활용한 하이브리드 분석을 수행합니다.

- **분석 알고리즘**: **Improved ChatGPT (Few-shot Learning)**
  - 각 클래스별 5개의 고품질 트레이닝 데이터셋을 활용한 실시간 학습.
  - 시스템 역할(Role) 부여 및 영문 추론 후 한글 번역 방식을 통해 정확도 극대화.
- **판단 기준 (4 Classes)**:
  - **Shallow Squat**: 가동 범위 부족 (허벅지와 지면의 수평 여부)
  - **Knee Valgus**: 무릎 모임 (안쪽으로 굽어지는 현상)
  - **Wrong Spinal Alignment**: 잘못된 척추 정렬 (척추 중립 위반)
  - **Right Form**: 올바른 자세

### 2. 과학적 운동 강도 추천 (Intensity Recommendation)
단순한 추측이 아닌, 학술적 근거와 정량적 데이터를 바탕으로 적정 중량을 제안합니다.

- **골격근량(SMM) 산출**: `Lee et al. (2000)`의 공식을 활용하여 신체 데이터를 바탕으로 추정.
  - *남성*: $SMM = 0.244 \times 체중 + 7.8 \times 키(m) - 2.2$
  - *여성*: $SMM = 0.197 \times 체중 + 7.2 \times 키(m) - 2.5$
- **중량 설계**: `Strength Level` 데이터를 벤치마킹하여 사용자 수준별(Beginner/Novice) 1RM 기반 스쿼트 중량 추천.

### 3. 개인화 식단 제안 (Diet Suggestions)
- **모델**: GPT-4o-mini
- **로직**: 사용자의 골격근량 대비 필수 단백질 섭취량을 계산하고, 가정 내 보유 중인 식재료를 활용한 최적의 식단 조합을 생성합니다.

---

## 📊 모델 성능 비교 및 연구 결과 (Ablation Study)

본 연구에서는 최적의 성능을 도출하기 위해 다양한 모델 비교와 요소 분석을 진행했습니다.

| 모델 | 정밀도(Precision) | 재현율(Recall) | F1 Score | 정확도(Accuracy) |
| :--- | :---: | :---: | :---: | :---: |
| MediaPipe Pose | 0.862 | 0.825 | 0.829 | 0.812 |
| Plain ChatGPT | 0.740 | 0.525 | 0.450 | 0.525 |
| **Improved ChatGPT (최종)** | **0.962** | **0.925** | **0.929** | **0.912** |

- **주요 발견**: ChatGPT 모델에 **전문 용어 활용(영문)**, **시스템 역할 부여**, **최신 트레이닝 데이터셋**을 적용했을 때 MediaPipe 대비 약 10% 이상의 성능 향상을 보였습니다.
<img width="1444" height="253" alt="image" src="https://github.com/user-attachments/assets/34b7a898-4962-4cb5-baee-454d3bb82f28" />

---

## Flask 기반 웹서비스

<img width="882" height="763" alt="image" src="https://github.com/user-attachments/assets/e67ba586-6b09-43f0-ae6c-6ee952920225" />

<img width="591" height="267" alt="image" src="https://github.com/user-attachments/assets/b6c65851-d24b-4b80-8f02-dd60395865b7" />

<img width="786" height="675" alt="image" src="https://github.com/user-attachments/assets/e620a31d-22c2-45db-bbfb-3f9cdf513784" />

---
## 📂 프로젝트 구조

```text
├── AiTrainer_flaskServer/      # Flask 기반 웹 서비스 인터페이스
│   ├── app.py                  # 메인 서버 및 비즈니스 로직
│   ├── ask2GTP_posture.py      # Improved ChatGPT 자세 분석 엔진
│   └── ask2GTP_diet.py         # 영양학적 식단 생성 엔진
├── models_code/                # 모델 비교 연구 코드
│   ├── mediapipe/              # MediaPipe 기반 포즈 추출 모듈
│   └── Trained_ChatGPT_API/    # GPT 모델 최적화 실험 스크립트
├── squat_img/                  # 연구에 사용된 Few-shot 데이터셋
├── Result_img/                 # 연구 결과 그래프 및 인터페이스 캡처
└── AI Trainer for Fitness Beginner_조동휘.pdf # 연구 상세 보고서
```

---

## 🛠 설치 및 실행 방법

1. **의존성 설치**:
   ```bash
   pip install -r requirements.txt
   ```
2. **API 키 설정**:
   환경 변수에 `OPENAI_API_KEY`를 등록하세요.
3. **서버 실행**:
   ```bash
   cd AiTrainer_flaskServer
   python app.py
   ```

---

## 🎓 학술적 의의
본 프로젝트는 LLM의 멀티모달 능력을 도메인 특화 데이터(Few-shot)와 결합했을 때, 기존의 특화된 비전 모델보다 더 유연하고 정확한 분석이 가능함을 입증하였습니다. 특히 복잡한 정렬(Spinal Alignment) 문제에서 뛰어난 성능을 보입니다.
