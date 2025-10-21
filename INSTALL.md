# 📦 소리새 AI 설치 가이드 / Sorisay AI Installation Guide

이 문서는 소리새 AI 시스템의 설치 방법을 상세히 설명합니다.

## 🎯 설치 전 준비사항

### 필수 요구사항

- **Python**: 3.8 이상 (3.12 권장)
- **운영체제**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **메모리**: 최소 4GB RAM (8GB 권장)
- **디스크**: 최소 2GB 여유 공간

### 선택적 요구사항

- **마이크**: 음성 인식 기능 사용 시 필요
- **인터넷**: 초기 패키지 다운로드 및 AI 모델 다운로드 시 필요

## 🚀 빠른 설치 (자동 설치 스크립트)

### Windows 사용자

1. **저장소 클론**
```cmd
git clone https://github.com/parkcheolhong/run_all_shinsegye.py.git
cd run_all_shinsegye.py
```

2. **자동 설치 실행**
```cmd
install.bat
```

자동 설치 스크립트가 다음 작업을 수행합니다:
- ✅ Python 및 pip 확인
- ✅ 가상환경 생성 및 활성화
- ✅ 모든 필수 패키지 설치
- ✅ 필요한 디렉토리 생성
- ✅ 설정 파일 초기화

### Linux/Mac 사용자

1. **저장소 클론**
```bash
git clone https://github.com/parkcheolhong/run_all_shinsegye.py.git
cd run_all_shinsegye.py
```

2. **스크립트 실행 권한 부여**
```bash
chmod +x install.sh
```

3. **자동 설치 실행**
```bash
./install.sh
```

## 🔧 수동 설치 (단계별 설명)

자동 설치가 작동하지 않거나 수동으로 설치하고 싶은 경우:

### 1단계: Python 설치 확인

```bash
python --version
# 또는
python3 --version
```

출력 예시: `Python 3.12.3`

Python이 설치되어 있지 않다면 [python.org](https://www.python.org/downloads/)에서 다운로드하세요.

### 2단계: 저장소 클론

```bash
git clone https://github.com/parkcheolhong/run_all_shinsegye.py.git
cd run_all_shinsegye.py
```

### 3단계: 가상환경 생성

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

가상환경이 활성화되면 프롬프트에 `(venv)`가 표시됩니다.

### 4단계: pip 업그레이드

```bash
pip install --upgrade pip setuptools wheel
```

### 5단계: 의존성 패키지 설치

```bash
pip install -r requirements.txt
```

이 과정은 몇 분 정도 걸릴 수 있습니다.

### 6단계: 필요한 디렉토리 생성

```bash
# Windows
mkdir logs data config memories

# Linux/Mac
mkdir -p logs data config memories
```

### 7단계: NLTK 데이터 다운로드

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## 🎮 설치 확인

설치가 완료되었는지 확인하려면:

### 자동 확인 (권장)

```bash
python verify_install.py
```

이 스크립트는 다음을 확인합니다:
- ✅ Python 버전 (3.8 이상)
- ✅ 필수 패키지 설치 여부
- ✅ 선택적 패키지 설치 여부
- ✅ 필수 디렉토리 존재 여부
- ✅ 핵심 파일 존재 여부

### 수동 확인

```bash
python run_all_shinsegye.py --version
```

또는 간단한 테스트 실행:

```bash
python run_all_shinsegye.py --test
```

## 📦 개별 패키지 설치 문제 해결

일부 패키지가 설치되지 않는 경우:

### pyaudio 설치 문제 (Windows)

1. **방법 1: 미리 컴파일된 wheel 파일 사용**
   - [Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)에서 다운로드
   - 예: `pip install PyAudio‑0.2.11‑cp312‑cp312‑win_amd64.whl`

2. **방법 2: Microsoft C++ Build Tools 설치**
   - [Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) 다운로드
   - 설치 후 다시 `pip install pyaudio` 실행

### pyaudio 설치 문제 (Linux)

```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio

# Fedora/RHEL
sudo dnf install portaudio-devel

# 그 다음
pip install pyaudio
```

### pyaudio 설치 문제 (Mac)

```bash
brew install portaudio
pip install pyaudio
```

### torch 설치 문제

PyTorch는 큰 패키지이므로 설치에 시간이 걸립니다. 네트워크 문제가 있다면:

```bash
# CPU 전용 버전 (더 작음)
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### transformers 설치 문제

```bash
# 최신 버전 대신 안정 버전 설치 (권장: 4.35.0)
pip install transformers==4.35.0
```

## 🌐 프록시 환경에서 설치

회사나 학교 네트워크에서 프록시를 사용하는 경우:

```bash
# Windows PowerShell
$env:HTTP_PROXY="http://proxy.example.com:8080"
$env:HTTPS_PROXY="http://proxy.example.com:8080"

# Linux/Mac
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"

# 그 다음 설치 진행
pip install -r requirements.txt
```

## 🔍 설치 후 확인사항

### 1. 필수 패키지 확인

```bash
pip list | grep -E "(speechrecognition|pyttsx3|flask|nltk|transformers|torch)"
```

### 2. 디렉토리 구조 확인

```
소리새 AI/
├── logs/          ✅ 존재해야 함
├── data/          ✅ 존재해야 함
├── config/        ✅ 존재해야 함
├── memories/      ✅ 존재해야 함
├── modules/       ✅ 존재해야 함
└── venv/          ✅ 존재해야 함
```

### 3. Python 경로 확인

```bash
# Windows
where python

# Linux/Mac
which python
```

가상환경의 Python이 사용되고 있는지 확인하세요.

## 🐳 Docker를 사용한 설치 (고급)

Docker를 사용하면 환경 설정 없이 바로 실행할 수 있습니다:

```bash
# 이미지 빌드
docker build -t sorisay-ai .

# 컨테이너 실행
docker run -p 5050:5050 sorisay-ai
```

자세한 내용은 [DOCKER_GUIDE.md](DOCKER_GUIDE.md)를 참조하세요.

## 🎓 개발 환경 설정 (개발자용)

개발에 참여하거나 코드를 수정하려는 경우:

```bash
# 개발용 의존성도 함께 설치
pip install -r requirements.txt
pip install pytest black flake8 mypy

# 에디터블 모드로 설치
pip install -e .
```

## 🔄 업데이트

소리새 AI를 최신 버전으로 업데이트하려면:

```bash
# 저장소 업데이트
git pull origin main

# 가상환경 활성화
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.bat # Windows

# 의존성 업데이트
pip install -r requirements.txt --upgrade
```

## 🗑️ 제거

소리새 AI를 완전히 제거하려면:

```bash
# 가상환경 비활성화
deactivate

# 프로젝트 디렉토리 삭제
cd ..
rm -rf run_all_shinsegye.py  # Linux/Mac
rmdir /s /q run_all_shinsegye.py  # Windows
```

## 🆘 문제 해결

### "모듈을 찾을 수 없습니다" 오류

```bash
# 가상환경이 활성화되었는지 확인
# 프롬프트에 (venv)가 있어야 함

# 의존성 재설치
pip install -r requirements.txt --force-reinstall
```

### "권한이 거부되었습니다" 오류

```bash
# Linux/Mac - sudo 사용하지 말 것!
# 대신 가상환경 사용

# Windows - 관리자 권한으로 실행
```

### "메모리 부족" 오류

```bash
# 패키지를 하나씩 설치
pip install speechrecognition
pip install pyttsx3
pip install flask
# ... 계속
```

### 설치는 되었지만 실행되지 않음

```bash
# Python 버전 확인
python --version

# 3.8 이상인지 확인
# 필요하다면 Python 업그레이드
```

## 📞 도움 받기

추가 도움이 필요하시면:

1. **문제 해결 가이드**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. **이슈 보고**: [GitHub Issues](https://github.com/parkcheolhong/run_all_shinsegye.py/issues)
3. **문서**: [README.md](README.md)

## 📝 설치 체크리스트

설치 완료 후 다음을 확인하세요:

- [ ] Python 3.8+ 설치됨
- [ ] 가상환경 생성 및 활성화됨
- [ ] requirements.txt의 모든 패키지 설치됨
- [ ] logs/, data/, config/, memories/ 디렉토리 존재함
- [ ] `python verify_install.py` 명령어로 모든 항목 확인됨
- [ ] `python run_all_shinsegye.py --test` 명령어가 정상 작동함
- [ ] (선택) 마이크 권한 허용됨
- [ ] (선택) 웹 대시보드 접속 가능 (http://localhost:5050)

---

🌟 **설치를 완료하셨나요? [HOW_TO_RUN.md](HOW_TO_RUN.md)에서 실행 방법을 확인하세요!**
