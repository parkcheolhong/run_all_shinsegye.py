# 📋 설치 가이드 (Installation Guide)

> 소리새 투사이클 브레인 시스템 완전 설치 안내

## 📋 목차

1. [시스템 요구사항](#시스템-요구사항)
2. [빠른 설치](#빠른-설치)
3. [수동 설치](#수동-설치)
4. [Docker 설치](#docker-설치)
5. [문제 해결](#문제-해결)
6. [설치 검증](#설치-검증)

---

## 🖥️ 시스템 요구사항

### 최소 요구사항
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- **Python**: 3.8 이상 (3.9~3.12 권장)
- **메모리**: 8GB RAM (16GB 권장)
- **저장공간**: 2GB 여유공간
- **네트워크**: 인터넷 연결 (패키지 다운로드용)

### 권장 사양
- **OS**: Windows 11, macOS 13+, Ubuntu 22.04+
- **Python**: 3.11 또는 3.12
- **메모리**: 16GB+ RAM
- **저장공간**: 5GB+ 여유공간
- **GPU**: CUDA 지원 GPU (AI 가속용, 선택사항)

---

## 🚀 빠른 설치

### Windows 자동 설치
```powershell
# PowerShell을 관리자 권한으로 실행
git clone https://github.com/parkcheolhong/run_all_shinsegye.py.git
cd run_all_shinsegye.py
.\install.bat
```

### Linux/macOS 자동 설치
```bash
git clone https://github.com/parkcheolhong/run_all_shinsegye.py.git
cd run_all_shinsegye.py
chmod +x install.sh
./install.sh
```

### 설치 확인
```bash
python run_all_shinsegye.py --version
```

---

## 🔧 수동 설치

### 1단계: 저장소 클론
```bash
git clone https://github.com/parkcheolhong/run_all_shinsegye.py.git
cd run_all_shinsegye.py
```

### 2단계: Python 가상환경 생성
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS  
python3 -m venv venv
source venv/bin/activate
```

### 3단계: 시스템 의존성 설치

#### Windows
```powershell
# Chocolatey 설치 (선택사항)
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Git 설치 (미설치시)
choco install git

# Visual Studio Build Tools (PyAudio용)
choco install visualstudio2022buildtools
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y python3-pip python3-dev build-essential
sudo apt install -y portaudio19-dev python3-pyaudio
sudo apt install -y espeak espeak-data libespeak1 libespeak-dev
sudo apt install -y festival festvox-kallpc16k
```

#### macOS
```bash
# Homebrew 설치 (미설치시)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 의존성 설치
brew install portaudio
brew install espeak
brew install python@3.11
```

#### CentOS/RHEL/Fedora
```bash
# RHEL/CentOS
sudo yum install -y python3-pip python3-devel gcc
sudo yum install -y portaudio-devel
sudo yum install -y espeak espeak-devel

# Fedora
sudo dnf install -y python3-pip python3-devel gcc
sudo dnf install -y portaudio-devel
sudo dnf install -y espeak espeak-devel
```

### 4단계: Python 패키지 설치
```bash
# 기본 패키지 설치
pip install --upgrade pip
pip install -r requirements.txt

# 선택적 패키지 (AI 가속)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118  # CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu     # CPU only
```

### 5단계: 설정 초기화
```bash
# 기본 설정 복사
python -c "
import shutil, os
if not os.path.exists('config/settings.json'):
    shutil.copy('config/settings.json.example', 'config/settings.json')
print('설정 파일 초기화 완료!')
"
```

---

## 🐳 Docker 설치

### Docker Compose 사용 (권장)
```bash
# 저장소 클론
git clone https://github.com/parkcheolhong/run_all_shinsegye.py.git
cd run_all_shinsegye.py

# Docker 컨테이너 실행
docker-compose up -d

# 웹 대시보드 접속
# http://localhost:5000
```

### 수동 Docker 빌드
```bash
# 이미지 빌드
docker build -t sorisay-brain .

# 컨테이너 실행
docker run -d -p 5000:5000 -p 5001:5001 \
  --name sorisay \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  sorisay-brain

# 로그 확인
docker logs sorisay
```

---

## 🛠️ 문제 해결

### 일반적인 오류

#### PyAudio 설치 오류
```bash
# Windows
pip install pipwin
pipwin install pyaudio

# macOS
brew install portaudio
pip install pyaudio

# Ubuntu/Debian
sudo apt install portaudio19-dev
pip install pyaudio
```

#### espeak 음성엔진 오류
```bash
# Windows: https://espeak.sourceforge.net/download.html 에서 다운로드

# Ubuntu/Debian
sudo apt install espeak espeak-data

# macOS
brew install espeak
```

#### 권한 오류 (Linux/macOS)
```bash
# 마이크 권한 확인
sudo usermod -a -G audio $USER

# 파일 권한 설정
chmod +x start_sorisay.sh
chmod +x install.sh
```

#### 가상환경 활성화 오류 (Windows)
```powershell
# PowerShell 실행 정책 변경
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 가상환경 재생성
Remove-Item -Recurse -Force venv
python -m venv venv
venv\Scripts\Activate.ps1
```

### 네트워크 관련 오류

#### PyPI 연결 오류
```bash
# 미러 서버 사용
pip install -r requirements.txt -i https://pypi.douban.com/simple/

# 또는 타임아웃 증가
pip install -r requirements.txt --timeout 1000
```

#### Git 클론 오류
```bash
# SSH 대신 HTTPS 사용
git clone https://github.com/parkcheolhong/run_all_shinsegye.py.git

# 또는 ZIP 다운로드
wget https://github.com/parkcheolhong/run_all_shinsegye.py/archive/main.zip
unzip main.zip
```

---

## ✅ 설치 검증

### 1단계: 기본 검증
```bash
# Python 환경 확인
python --version
pip --version

# 패키지 확인
python -c "
import sys
print(f'Python: {sys.version}')

try:
    import speech_recognition
    import pyttsx3
    import flask
    import socketio
    print('✅ 모든 필수 패키지 설치됨')
except ImportError as e:
    print(f'❌ 패키지 누락: {e}')
"
```

### 2단계: 소리새 시스템 검증
```bash
# 시스템 검증 스크립트 실행
python verify_install.py

# 또는 테스트 실행
python run_all_tests.py
```

### 3단계: 웹 대시보드 테스트
```bash
# 대시보드 시작
python modules/sorisay_dashboard_web.py

# 브라우저에서 확인: http://localhost:5000
```

### 4단계: 음성 기능 테스트
```bash
# 음성 엔진 테스트
python -c "
import pyttsx3
engine = pyttsx3.init()
engine.say('소리새 설치가 완료되었습니다')
engine.runAndWait()
print('✅ TTS 테스트 완료')
"

# 음성 인식 테스트 (마이크 필요)
python -c "
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print('마이크 테스트 완료')
print('✅ STT 테스트 완료')
"
```

---

## 🎯 다음 단계

설치가 완료되면 다음 문서들을 참고하세요:

- **[QUICKSTART.md](QUICKSTART.md)**: 빠른 시작 가이드
- **[README.md](README.md)**: 전체 시스템 개요
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**: 상세 문제 해결
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)**: 테스트 실행 방법

### 시작하기
```bash
# 소리새 시스템 시작
python run_all_shinsegye.py

# 또는 웹 대시보드로 시작
python modules/sorisay_dashboard_web.py
```

---

## 📞 지원

설치 중 문제가 발생하면:

1. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** 확인
2. **[GitHub Issues](https://github.com/parkcheolhong/run_all_shinsegye.py/issues)** 검색
3. 새로운 이슈 생성 (로그 포함)

**즐거운 소리새 경험을 시작하세요!** 🎉🧠🧠