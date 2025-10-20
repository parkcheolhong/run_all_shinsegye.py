# 🌟 소리새 AI (Sorisay AI) - 진화형 AI 어시스턴트

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Production Ready](https://img.shields.io/badge/status-production%20ready-green.svg)](https://github.com/parkcheolhong/run_all_shinsegye.py)

> **"스스로 학습하고 진화하는 AI가 당신의 창작과 개발을 도와드립니다"**

## 📚 문서 가이드

- 🚀 **[빠른 시작 가이드](QUICKSTART.md)** - 5분 만에 시작하기
- 🔧 **[문제 해결](TROUBLESHOOTING.md)** - 일반적인 오류 해결
- 📖 **[실행 방법](HOW_TO_RUN.md)** - 상세한 실행 가이드
- 📊 **[코드 검토 보고서](CODE_REVIEW_REPORT.md)** - 전체 코드 품질 분석
- 📝 **[검토 요약 (한글)](REVIEW_SUMMARY_KO.md)** - 코드 검토 요약 (추천!)
- ✅ **[개선 체크리스트](IMPROVEMENT_CHECKLIST.md)** - 개선 작업 목록
- 📑 **[문서 색인](DOCUMENTATION_INDEX.md)** - 모든 문서 안내

## 🎯 개요

소리새 AI는 음성 인식, 자연어 처리, 창작 지원을 통합한 **차세대 AI 어시스턴트 시스템**입니다.  
단순한 명령 처리를 넘어서 **스스로 학습하고 진화**하며, 사용자와 함께 성장하는 지능형 파트너입니다.

### ✨ 핵심 특징

- 🎤 **음성 인식**: 한국어 실시간 음성 명령 처리
- 🧠 **자연어 처리**: 의도 분석 및 맥락 이해
- 🎨 **창작 지원**: AI 음악 작곡, 꿈 해석, 감정 분석
- 🤖 **개발 도구**: 가상 개발팀, 코드 리팩토링, 프로젝트 관리
- 🌐 **웹 대시보드**: 실시간 모니터링 및 제어
- 🔒 **보안 시스템**: 다층 인증 및 권한 관리
- 📚 **자가 학습**: 사용 패턴 학습 및 기능 자동 확장

## 🚀 빠른 시작

### 1. 설치 및 설정

```bash
# 저장소 클론
git clone https://github.com/parkcheolhong/run_all_shinsegye.py.git
cd run_all_shinsegye.py

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 2. 실행

#### 방법 1: 배치 파일 사용 (가장 쉬움, Windows 추천)

```cmd
start_sorisay.bat
```

#### 방법 2: PowerShell 스크립트 사용

```powershell
.\start_sorisay.ps1
```

#### 방법 3: 직접 Python 명령어 사용

```bash
# ✅ 올바른 실행 방법
python run_all_shinsegye.py

# ❌ 잘못된 실행 방법 (오류 발생)
# github run_all_shinsegye.py  # 'github'는 유효하지 않은 명령어입니다
# github run_shinsegye.py      # 이것도 마찬가지입니다
```

> **⚠️ 중요**: `github` 명령어는 존재하지 않습니다. 항상 `python` 명령어를 사용하세요!  
> **💡 팁**: 반복적인 오류를 방지하려면 `start_sorisay.bat` 파일을 사용하세요.

시스템이 시작되면:

- 🎤 음성 인식이 활성화됩니다
- 🌐 웹 대시보드가 <http://localhost:5050>에서 실행됩니다
- 📱 실시간 로그와 상태를 확인할 수 있습니다

## 🎵 주요 AI 기능들

### 1. 🎵 AI 음악 작곡가

```text
음성 명령: "음악", "작곡", "멜로디", "노래"
```

- 감정 기반 자동 작곡
- 코드-to-음악 변환
- ASCII 악보 생성
- 12가지 음악 이론 적용

### 2. 🌙 꿈 해석 시스템

```text
음성 명령: "꿈", "해석", "꿈해몽"
```

- 심리학적 꿈 분석
- 문화적 상징 해석
- 미래 예언 및 조언
- 상세 해석 보고서 생성

### 3. 🤖 가상 개발팀

```text
음성 명령: "개발팀", "프로젝트", "스프린트", "미팅"
```

- 8명의 AI 전문가 팀 (Frontend, Backend, DevOps, QA, PM, Designer, Architect)
- 프로젝트 생성 및 관리
- 일일 진행 시뮬레이션
- 팀 미팅 및 스프린트 계획

### 4. 🔮 미래 예측 엔진

```text
음성 명령: "미래", "예측", "트렌드", "시나리오"
```

- 기술/경제/사회 트렌드 분석
- 다차원 미래 예측
- 시나리오 시뮬레이션 (낙관/현실/비관)
- 예측 신뢰도 시스템

### 5. 🎨 감정 색채 치료사

```text
음성 명령: "감정", "색깔", "치료", "힐링"
```

- 실시간 감정 분석
- 색채 심리학 기반 치료
- 개인 맞춤형 힐링 프로그램
- 감정 상태 시각화

## 🎮 사용법

### 음성 명령

시스템이 실행되면 다음과 같은 음성 명령을 사용할 수 있습니다:

#### 시스템 제어

- **"리팩터링"** - 코드 자동 최적화
- **"동기화"** - Git 저장소 동기화
- **"상태"** - 시스템 상태 확인
- **"종료"** - 시스템 안전 종료

#### 개발 도구

- **"테스트"** - 자동 테스트 실행
- **"빌드"** - 프로젝트 빌드
- **"설치"** - 패키지 설치
- **"문서"** - 문서 생성

#### 창작 도구

- **"음악 작곡해줘"** - AI 음악 작곡
- **"꿈해몽해줘"** - 꿈 해석
- **"미래 예측해줘"** - 트렌드 예측
- **"감정 분석해줘"** - 감정 색채 치료

### 웹 대시보드

브라우저에서 `http://localhost:5050`으로 접속하면:

- 📊 **실시간 모니터링**: 시스템 상태, 명령 처리 현황
- 🎛️ **제어판**: 버튼을 통한 명령 실행
- 📈 **분석 차트**: 성공률, 응답 시간 통계
- 🔒 **보안 인증**: API 키 기반 접근 제어

## 🏗️ 시스템 아키텍처

```text
소리새 AI 시스템
├── 🎤 음성 인식 엔진 (SpeechRecognition + pyttsx3)
├── 🧠 자연어 처리 (NLP Processor + 의도 분석)
├── 🤖 AI 모듈들
│   ├── 🎵 음악 작곡가
│   ├── 🌙 꿈 해석기
│   ├── 👥 가상 개발팀
│   ├── 🔮 미래 예측기
│   └── 🎨 감정 치료사
├── 🌐 웹 대시보드 (Flask + SocketIO)
├── 🔒 보안 시스템 (API 키 + 토큰 인증)
├── 📚 학습 엔진 (패턴 학습 + 기능 확장)
└── 🔌 플러그인 시스템
```

## 📦 의존성

### 필수 패키지

```text
speechrecognition==3.10.0    # 음성 인식
pyttsx3==2.90               # 음성 합성
flask==2.3.3                # 웹 서버
flask-socketio==5.3.6       # 실시간 통신
nltk==3.8.1                 # 자연어 처리
transformers==4.35.0        # AI 모델
torch==2.1.0                # 딥러닝
```

### 선택적 패키지 (개발용)

```text
pytest==7.4.2              # 테스트
black==23.9.1               # 코드 포매팅
flake8==6.1.0               # 린팅
```

## 🔒 보안 설정

소리새 AI는 다층 보안 시스템을 제공합니다:

### API 키 생성

```bash
# 새 사용자 키 생성
python security_key_manager.py add-key --name myuser --type user

# 관리자 키 생성
python security_key_manager.py add-key --name admin --type admin
```

### 대시보드 인증

```bash
# URL 파라미터로 인증
http://localhost:5050?api_key=your_api_key_here

# 또는 대시보드 내에서 인증 버튼 사용
```

자세한 보안 설정은 [SECURITY_GUIDE.md](./SECURITY_GUIDE.md)를 참고하세요.

## 🧪 테스트

### 전체 시스템 테스트

```bash
# 보안 테스트
python security_test_suite.py

# AI 기능 테스트
python test_creative_sorisay.py

# 감정 NLP 테스트
python test_emotion_nlp.py
```

### 개별 기능 테스트

```bash
# 음성 인식 테스트
python -c "from modules.ai_code_manager.sorisay_core_controller import SorisayCore; core = SorisayCore(); print('✅ 음성 시스템 정상')"

# 웹 대시보드 테스트
python modules/sorisay_dashboard_web.py
```

## 📁 프로젝트 구조

```text
📦 소리새 AI
├── 📄 run_all_shinsegye.py          # 🚀 메인 실행 파일
├── 📄 requirements.txt              # 📦 의존성 목록
├── 📄 SECURITY_GUIDE.md            # 🔒 보안 가이드
├── 📄 PROJECT_COMPLETION_REPORT.md # 📊 완성 보고서
├── 📁 config/                      # ⚙️ 설정 파일들
│   ├── settings.json
│   ├── security_config.json
│   └── voice_settings.json
├── 📁 modules/                     # 🧩 핵심 모듈들
│   ├── 📁 ai_code_manager/        # 🤖 AI 관리자들
│   │   ├── sorisay_core_controller.py
│   │   ├── ai_music_composer.py
│   │   ├── dream_interpreter.py
│   │   ├── virtual_dev_team.py
│   │   ├── future_prediction_engine.py
│   │   └── emotion_color_therapist.py
│   ├── 📁 plugins/                # 🔌 플러그인들
│   └── sorisay_dashboard_web.py   # 🌐 웹 대시보드
├── 📁 data/                       # 📊 데이터 저장소
├── 📁 logs/                       # 📝 로그 파일들
└── 📁 tests/                      # 🧪 테스트 파일들
```

## 🔧 고급 설정

### 음성 인식 튜닝

`config/voice_settings.json`에서 음성 인식 민감도를 조정할 수 있습니다:

```json
{
  "energy_threshold": 300,
  "dynamic_energy_threshold": true,
  "pause_threshold": 0.8,
  "phrase_threshold": 0.3
}
```

### AI 모델 설정

각 AI 모듈의 설정은 `config/settings.json`에서 관리됩니다:

```json
{
  "ai_music_composer": {
    "default_emotion": "neutral",
    "complexity_level": 3
  },
  "dream_interpreter": {
    "interpretation_depth": "detailed",
    "cultural_context": "korean"
  }
}
```

## 🚨 문제 해결

### 일반적인 문제들

#### 1. "프로그램 이름을 찾을 수 없다" 오류

```bash
# ❌ 잘못된 명령어 (오류 발생)
github run_all_shinsegye.py
# 오류: 'github' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는 프로그램 이름으로 인식되지 않습니다

# ✅ 올바른 명령어
python run_all_shinsegye.py
```

#### 2. 음성 인식이 작동하지 않는 경우

```bash
# 마이크 권한 확인 (Windows)
# 설정 > 개인정보 > 마이크에서 앱 접근 허용

# pyaudio 재설치
pip uninstall pyaudio
pip install pyaudio
```

#### 3. 모듈 import 오류

```bash
# 가상환경 확인
which python  # Linux/Mac
where python  # Windows

# 의존성 재설치
pip install -r requirements.txt --force-reinstall
```

#### 4. 웹 대시보드 접속 불가

```bash
# 포트 충돌 확인
netstat -an | findstr :5050  # Windows
netstat -an | grep :5050     # Linux/Mac

# 방화벽 설정 확인
```

### 로그 확인

```bash
# 실행 로그
cat logs/voice_history.txt

# 오류 로그 (있는 경우)
cat logs/error.log
```

## 🛣️ 로드맵

### v2.0 (계획 중)

- [ ] 🌍 **다국어 지원** (영어, 일본어, 중국어)
- [ ] 🧠 **GPT 통합** (OpenAI API 연동)
- [ ] 📱 **모바일 앱** (React Native)
- [ ] ☁️ **클라우드 동기화** (AWS/Azure 지원)

### v1.1 (다음 릴리스)

- [ ] 🎯 **명령어 커스터마이징**
- [ ] 📊 **고급 분석 대시보드**
- [ ] 🔄 **자동 업데이트 시스템**
- [ ] 🎨 **UI/UX 개선**

## 🤝 기여하기

소리새 AI 프로젝트에 기여해주세요!

### 기여 방법

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 개발 환경 설정

```bash
# 개발용 의존성 설치
pip install -r requirements-dev.txt

# 코드 스타일 체크
black . && flake8 .

# 테스트 실행
pytest tests/
```

## 📜 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

## 👥 제작진

- **파크철홍** - *메인 개발자* - [@parkcheolhong](https://github.com/parkcheolhong)
- **소리새 AI** - *AI 어시스턴트 파트너*

## 🙏 감사의 말

이 프로젝트는 다음 오픈소스 라이브러리들의 도움을 받았습니다:

- [SpeechRecognition](https://github.com/Uberi/speech_recognition)
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3)
- [Flask](https://flask.palletsprojects.com/)
- [Transformers](https://huggingface.co/transformers/)

## 📞 연락처

프로젝트 링크: [https://github.com/parkcheolhong/run_all_shinsegye.py](https://github.com/parkcheolhong/run_all_shinsegye.py)

---

소리새 AI와 함께 창작과 개발의 새로운 경험을 시작하세요! 🚀

