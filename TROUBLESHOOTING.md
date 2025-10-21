# 🔧 빠른 문제 해결 가이드 (Quick Troubleshooting Guide)

**프로젝트**: 소리새 AI  
**업데이트**: 2025년 10월 19일

---

## 🚨 자주 발생하는 문제와 해결 방법

### 1. "ModuleNotFoundError" 오류

#### 증상
```
ModuleNotFoundError: No module named 'speech_recognition'
ModuleNotFoundError: No module named 'pyttsx3'
```

#### 원인
필요한 Python 패키지가 설치되지 않음

#### 해결 방법
```bash
# 전체 의존성 설치
pip install -r requirements.txt

# 또는 개별 설치
pip install speechrecognition pyttsx3 flask flask-socketio
pip install nltk transformers torch

# pyaudio 설치 (Windows)
pip install pyaudio

# pyaudio 설치 (Linux/Mac)
brew install portaudio  # Mac
sudo apt-get install portaudio19-dev  # Linux
pip install pyaudio
```

---

### 2. "github 명령어를 찾을 수 없습니다" 오류

#### 증상
```
'github' 용어가 cmdlet, 함수, 스크립트 파일 또는 
실행할 수 있는 프로그램 이름으로 인식되지 않습니다.
```

#### 원인
잘못된 명령어 사용 (`github` 명령어는 존재하지 않음)

#### 해결 방법
```bash
# ❌ 잘못된 명령어
github run_all_shinsegye.py

# ✅ 올바른 명령어
python run_all_shinsegye.py

# 또는 배치 파일 사용 (Windows)
start_sorisay.bat

# 또는 PowerShell 스크립트 사용
.\start_sorisay.ps1
```

---

### 3. Import 오류 (중복 파일 관련)

#### 증상
```
ImportError: cannot import name 'SorisayCore'
AttributeError: module has no attribute 'SorisayCore'
```

#### 원인
중복된 파일로 인한 import 경로 혼란

#### 해결 방법
```bash
# 올바른 import 경로 사용
from modules.ai_code_manager.sorisay_core_controller import SorisayCore

# 루트 디렉토리의 중복 파일 확인 및 제거
# (modules/ai_code_manager/ 버전이 메인)
```

---

### 4. 음성 인식이 작동하지 않음

#### 증상
- 마이크 입력이 인식되지 않음
- "Listening..." 상태에서 멈춤

#### 원인
- 마이크 권한 문제
- pyaudio 설치 문제
- 마이크 설정 문제

#### 해결 방법
```bash
# 1. 마이크 권한 확인 (Windows)
# 설정 > 개인정보 > 마이크 > 앱이 마이크 접근 허용

# 2. pyaudio 재설치
pip uninstall pyaudio
pip install pyaudio

# 3. 마이크 테스트
python -c "import speech_recognition as sr; r = sr.Recognizer(); print('마이크 테스트 성공')"
```

---

### 4-1. 음성 합성(TTS)이 작동하지 않음

#### 증상
```
RuntimeError: This means you probably do not have eSpeak or eSpeak-ng installed!
```

#### 원인
시스템에 espeak 또는 espeak-ng TTS 엔진이 설치되지 않음

#### 해결 방법
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install espeak espeak-ng

# macOS
brew install espeak

# Windows
# https://espeak.sourceforge.net/ 에서 설치 프로그램 다운로드 후 설치

# 설치 확인
espeak --version
espeak-ng --version
```

**참고**: espeak 설치 후 시스템을 재시작하거나 터미널을 다시 열어주세요.

---

### 5. 웹 대시보드 접속 불가

#### 증상
- `http://localhost:5050` 접속 안 됨
- "연결할 수 없습니다" 오류

#### 원인
- Flask 서버가 시작되지 않음
- 포트 충돌
- 방화벽 차단

#### 해결 방법
```bash
# 1. 포트 사용 확인
netstat -an | findstr :5050  # Windows
netstat -an | grep :5050     # Linux/Mac

# 2. 다른 포트로 실행
# sorisay_dashboard_web.py 수정
# app.run(port=5051)

# 3. 방화벽 예외 추가
# Windows Defender 방화벽에서 Python 허용

# 4. 직접 대시보드 실행
python modules/sorisay_dashboard_web.py
```

---

### 6. 설정 파일을 찾을 수 없음

#### 증상
```
⚠ 설정 파일을 찾을 수 없습니다: config/settings.json
FileNotFoundError: [Errno 2] No such file or directory
```

#### 원인
설정 파일이 없거나 경로가 잘못됨

#### 해결 방법
```bash
# 1. config 디렉토리 확인
ls config/

# 2. 기본 설정 파일 확인
ls config/*.json

# 3. 프로그램은 자동으로 기본 설정 생성
# (처음 실행 시 자동 생성됨)
```

---

### 7. Git 관련 문제

#### 증상
- 불필요한 파일이 커밋됨 (`__pycache__`, `venv`)
- `.gitignore`가 작동하지 않음

#### 해결 방법
```bash
# 1. 이미 커밋된 파일 제거
git rm -r --cached __pycache__
git rm -r --cached venv
git rm -r --cached .history
git commit -m "Remove unnecessary files"

# 2. .gitignore 확인
cat .gitignore

# 3. .gitignore가 없으면 생성
# (최신 버전에는 이미 포함됨)
```

---

### 8. 테스트 실행 실패

#### 증상
```
python tests/final_system_test.py
# 오류 발생
```

#### 원인
- 의존성 미설치
- 모듈 경로 문제

#### 해결 방법
```bash
# 1. 현재 디렉토리 확인
pwd  # 프로젝트 루트여야 함

# 2. PYTHONPATH 설정
export PYTHONPATH=$PYTHONPATH:$(pwd)  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%CD%      # Windows

# 3. 테스트 실행
python tests/final_system_test.py

# 4. pytest 사용 (권장)
pip install pytest
pytest tests/
```

---

## 🔍 디버깅 팁

### 로그 확인
```bash
# 음성 인식 로그
cat logs/voice_history.txt

# 시스템 로그 (있는 경우)
cat logs/sorisay.log

# 최근 로그만 보기
tail -n 50 logs/voice_history.txt
```

### Python 버전 확인
```bash
python --version
# Python 3.8 이상 필요
```

### 가상환경 확인
```bash
# 가상환경 활성화 여부 확인
which python  # Linux/Mac
where python  # Windows

# 가상환경 활성화
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 모듈 설치 확인
```bash
# 설치된 패키지 목록
pip list

# 특정 패키지 확인
pip show speechrecognition
```

---

## 📞 추가 도움이 필요하면?

1. **코드 검토 보고서 참조**
   - `CODE_REVIEW_REPORT.md`

2. **개선 체크리스트 확인**
   - `IMPROVEMENT_CHECKLIST.md`

3. **한국어 요약 문서**
   - `REVIEW_SUMMARY_KO.md`

4. **메인 README**
   - `README.md`

---

## 🆘 긴급 문제 해결

### 모든 것이 작동하지 않을 때
```bash
# 1. 클린 설치
rm -rf venv __pycache__  # 기존 파일 제거
python -m venv venv       # 새 가상환경
source venv/bin/activate  # 활성화
pip install -r requirements.txt  # 재설치

# 2. 간단한 테스트
python -c "print('Python이 작동합니다!')"

# 3. 최소한의 기능 테스트
python -c "from modules.ai_code_manager.sorisay_core_controller import SorisayCore; print('모듈 import 성공!')"
```

---

**이 문서로 해결되지 않는 문제가 있으면, GitHub Issues에 보고해주세요!**
