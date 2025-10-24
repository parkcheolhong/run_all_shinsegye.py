# 🔧 설치 문제 해결 가이드

**작성일**: 2025년 10월 21일  
**대상**: 소리새 AI 설치 중 문제를 겪는 사용자

---

## 📋 목차

1. [설치 전 준비사항](#설치-전-준비사항)
2. [단계별 설치 가이드](#단계별-설치-가이드)
3. [일반적인 문제 해결](#일반적인-문제-해결)
4. [시스템별 특이사항](#시스템별-특이사항)
5. [검증 및 테스트](#검증-및-테스트)

---

## 🎯 설치 전 준비사항

### 필수 요구사항

1. **Python 버전**: Python 3.8 이상
   ```bash
   python --version
   # 또는
   python3 --version
   ```

2. **pip 업그레이드**: 최신 버전의 pip 권장
   ```bash
   pip install --upgrade pip
   ```

3. **가상환경 사용 권장** (선택사항이지만 강력 권장)
   ```bash
   python -m venv venv
   
   # 활성화
   # Windows:
   venv\Scripts\activate
   
   # Linux/Mac:
   source venv/bin/activate
   ```

### 시스템 의존성

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y \
    portaudio19-dev \
    python3-dev \
    espeak \
    espeak-ng \
    build-essential
```

#### macOS
```bash
brew install portaudio espeak
```

#### Windows
1. **espeak**: https://espeak.sourceforge.net/ 에서 다운로드 및 설치
2. **Visual C++ Build Tools** (pyaudio 컴파일용):
   - https://visualstudio.microsoft.com/downloads/
   - "Desktop development with C++" 워크로드 선택

---

## 📦 단계별 설치 가이드

### 방법 1: 최소 설치 (빠른 시작, 권장)

핵심 기능만 설치하여 빠르게 시작:

```bash
# 1. 저장소 클론
git clone https://github.com/parkcheolhong/run_all_shinsegye.py.git
cd run_all_shinsegye.py

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

# 3. 최소 패키지 설치
pip install -r requirements-minimal.txt

# 4. 실행
python run_all_shinsegye.py
```

**이 방법의 장점**:
- ✅ 빠른 설치 (1-2분)
- ✅ 적은 디스크 공간 사용
- ✅ 핵심 음성 인식 및 웹 대시보드 작동

**제한사항**:
- ❌ 고급 NLP 기능 제한 (torch, transformers 미포함)
- ❌ 일부 AI 모델 기능 비활성화

### 방법 2: 전체 설치 (모든 기능)

모든 AI 기능을 사용하려면:

```bash
# 1-2단계는 방법 1과 동일

# 3. 전체 패키지 설치
pip install -r requirements.txt

# 주의: torch와 transformers는 용량이 크므로 시간이 걸릴 수 있습니다
# 예상 시간: 5-15분 (인터넷 속도에 따라)
# 예상 용량: 3-5GB

# 4. 실행
python run_all_shinsegye.py
```

### 방법 3: 단계별 수동 설치 (문제 발생 시)

문제가 발생하면 각 패키지를 개별적으로 설치:

```bash
# 핵심 패키지
pip install SpeechRecognition>=3.10.0
pip install pyttsx3>=2.90
pip install flask>=2.3.0
pip install flask-socketio>=5.3.0

# pyaudio (시스템 의존성 필요)
pip install pyaudio>=0.2.11

# 추가 패키지 (선택)
pip install nltk>=3.8
pip install python-dotenv>=1.0.0
```

---

## 🔧 일반적인 문제 해결

### 문제 1: speech_recognition 모듈을 찾을 수 없음

**오류 메시지**:
```
ModuleNotFoundError: No module named 'speech_recognition'
```

**해결 방법**:
```bash
# 주의: 설치는 SpeechRecognition (대문자), import는 speech_recognition (소문자)
pip install SpeechRecognition

# 확인
python -c "import speech_recognition; print('✅ 설치 성공')"
```

### 문제 2: pyaudio 설치 실패

**오류 메시지**:
```
ERROR: Could not build wheels for pyaudio
```

**원인**: portaudio 시스템 라이브러리 미설치

**해결 방법**:

#### Ubuntu/Debian:
```bash
sudo apt-get install portaudio19-dev python3-dev
pip install pyaudio
```

#### macOS:
```bash
brew install portaudio
pip install pyaudio
```

#### Windows:
```bash
# 방법 1: pipwin 사용 (가장 쉬움)
pip install pipwin
pipwin install pyaudio

# 방법 2: 사전 컴파일된 wheel 파일 사용
# 1. https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio 방문
# 2. Python 버전에 맞는 .whl 파일 다운로드
# 3. 설치
pip install pyaudio-0.2.11-cp312-cp312-win_amd64.whl
```

### 문제 3: pyttsx3 TTS 오류

**오류 메시지**:
```
RuntimeError: This means you probably do not have eSpeak or eSpeak-ng installed!
```

**해결 방법**:

#### Ubuntu/Debian:
```bash
sudo apt-get install espeak espeak-ng
```

#### macOS:
```bash
brew install espeak
```

#### Windows:
1. https://espeak.sourceforge.net/ 방문
2. 설치 프로그램 다운로드 및 실행
3. 시스템 재시작 또는 터미널 재시작

### 문제 4: 버전 충돌

**오류 메시지**:
```
ERROR: Cannot install package X because it conflicts with Y
```

**해결 방법**:
```bash
# 1. 가상환경 재생성 (권장)
deactivate
rm -rf venv  # Linux/Mac
# 또는
rmdir /s venv  # Windows

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. 의존성 재설치
pip install -r requirements.txt

# 또는 최소 버전만
pip install -r requirements-minimal.txt
```

### 문제 5: 로그 파일 권한 오류

**오류 메시지**:
```
PermissionError: [Errno 13] Permission denied: 'logs/voice_history.txt'
```

**자동 해결**: 프로그램이 자동으로 임시 디렉토리로 전환합니다.

**수동 해결**:
```bash
# Linux/Mac
chmod -R 755 logs/
sudo chown -R $USER:$USER logs/

# Windows
# 폴더 우클릭 > 속성 > 보안 > 편집 > 전체 제어 허용
```

### 문제 6: ImportError 발생

**해결 순서**:
```bash
# 1. 가상환경 활성화 확인
which python  # Linux/Mac
where python  # Windows
# venv 경로가 표시되어야 함

# 2. 패키지 설치 확인
pip list | grep speech
pip list | grep pyttsx3
pip list | grep flask

# 3. 필요한 패키지 설치
pip install speech_recognition pyttsx3 flask flask-socketio

# 4. Python 경로 확인
python -c "import sys; print('\n'.join(sys.path))"
```

---

## 💻 시스템별 특이사항

### Windows 사용자

1. **PowerShell 실행 정책 설정**:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Visual C++ Build Tools 필요**:
   - pyaudio 컴파일에 필요
   - 또는 사전 컴파일된 wheel 파일 사용

3. **espeak 경로 설정**:
   - 설치 후 시스템 재시작
   - 또는 PATH 환경 변수에 추가

### macOS 사용자

1. **Homebrew 필수**:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Xcode Command Line Tools**:
   ```bash
   xcode-select --install
   ```

3. **M1/M2 칩 사용자**:
   - Rosetta 2 필요할 수 있음
   - torch는 ARM64 네이티브 버전 사용

### Linux 사용자

1. **Ubuntu/Debian**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y portaudio19-dev python3-dev espeak espeak-ng
   ```

2. **Fedora/CentOS**:
   ```bash
   sudo dnf install portaudio-devel python3-devel espeak espeak-ng
   ```

3. **Arch Linux**:
   ```bash
   sudo pacman -S portaudio python espeak espeak-ng
   ```

---

## ✅ 검증 및 테스트

### 설치 확인

```bash
# 1. Python 버전
python --version

# 2. 핵심 패키지 import 테스트
python << EOF
try:
    import speech_recognition
    import pyttsx3
    import flask
    from modules.logging_config import setup_logger
    print("✅ 모든 핵심 모듈 설치 완료")
except ImportError as e:
    print(f"❌ 설치 실패: {e}")
EOF

# 3. 프로그램 실행 테스트
python run_all_shinsegye.py
```

### 기능별 테스트

```bash
# 음성 인식 테스트
python -c "import speech_recognition as sr; r = sr.Recognizer(); print('✅ 음성 인식 OK')"

# TTS 테스트
python -c "import pyttsx3; engine = pyttsx3.init(); print('✅ TTS OK')"

# 웹 대시보드 테스트
python -c "from flask import Flask; app = Flask(__name__); print('✅ Flask OK')"
```

---

## 🆘 추가 도움말

### 로그 파일 확인

문제 발생 시 로그 파일을 확인:

```bash
# 실행 로그
cat logs/sorisay.log

# 음성 명령 히스토리
cat logs/voice_history.txt

# 오류 로그
cat logs/error.log
```

### 디버그 모드로 실행

```bash
# 상세 출력 모드
python run_all_shinsegye.py --verbose

# 또는 환경 변수 설정
export SORISAY_LOG_LEVEL=DEBUG  # Linux/Mac
set SORISAY_LOG_LEVEL=DEBUG     # Windows
python run_all_shinsegye.py
```

### 이슈 보고

문제가 계속되면 다음 정보와 함께 이슈를 제출하세요:

1. **시스템 정보**:
   ```bash
   python --version
   pip --version
   cat /etc/os-release  # Linux
   sw_vers              # macOS
   ver                  # Windows
   ```

2. **설치된 패키지**:
   ```bash
   pip list > installed_packages.txt
   ```

3. **오류 메시지**: 전체 traceback 포함

4. **실행 명령어**: 정확히 어떻게 실행했는지

---

## 📚 추가 문서

- [프로그램 상세 검토](PROGRAM_REVIEW_DETAILED_KO.md) - 모든 문제점과 해결 방안
- [README.md](README.md) - 프로젝트 개요 및 사용법
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 일반적인 문제 해결

---

**최종 업데이트**: 2025년 10월 21일  
**도움이 필요하면**: GitHub Issues에 문의하세요
