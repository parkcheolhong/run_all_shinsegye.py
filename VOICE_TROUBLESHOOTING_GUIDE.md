# 🎤 음성 문제 해결 가이드 (Voice Troubleshooting Guide)

**프로젝트**: 소리새 AI  
**업데이트**: 2025년 10월 21일  
**목적**: 음성 인식 및 음성 합성 관련 모든 문제의 포괄적 해결 방법 제공

---

## 📋 목차

1. [일반적인 음성 인식 문제](#1-일반적인-음성-인식-문제)
2. [PyAudio 설치 문제](#2-pyaudio-설치-문제)
3. [마이크 권한 및 설정 문제](#3-마이크-권한-및-설정-문제)
4. [음성 합성(TTS) 문제](#4-음성-합성tts-문제)
5. [네트워크 연결 문제](#5-네트워크-연결-문제)
6. [플랫폼별 상세 가이드](#6-플랫폼별-상세-가이드)
7. [대체 솔루션](#7-대체-솔루션)
8. [고급 디버깅](#8-고급-디버깅)

---

## 1. 일반적인 음성 인식 문제

### 🚨 증상
- 마이크 입력이 인식되지 않음
- "🎧 듣는 중..." 상태에서 계속 대기
- "⚠ 음성을 인식하지 못했습니다" 메시지 반복
- 음성 인식 후 아무 반응 없음

### 🔍 빠른 진단

#### 단계 1: Python 환경 확인
```bash
# Python 버전 확인 (3.8 이상 필요)
python --version

# 가상환경 활성화 여부 확인
which python    # Linux/Mac
where python    # Windows
```

#### 단계 2: 필수 패키지 설치 확인
```bash
# 설치된 패키지 확인
pip list | grep -i "speech\|audio"

# 또는 Windows에서
pip list | findstr /i "speech audio"

# 필요한 패키지들:
# - speechrecognition (3.10.0 이상)
# - pyaudio (0.2.11 이상)
# - pyttsx3 (2.90 이상)
```

#### 단계 3: 기본 마이크 테스트
```python
# 터미널에서 실행
python -c "import speech_recognition as sr; print('✅ SpeechRecognition 정상')"
python -c "import pyaudio; print('✅ PyAudio 정상')"
python -c "import pyttsx3; print('✅ pyttsx3 정상')"
```

### ✅ 해결 방법

#### 방법 1: 의존성 재설치
```bash
# 기존 패키지 제거
pip uninstall speechrecognition pyaudio pyttsx3 -y

# 최신 버전 재설치
pip install speechrecognition==3.10.0
pip install pyttsx3==2.90

# PyAudio는 플랫폼별로 다르게 설치 (아래 섹션 참조)
```

#### 방법 2: 전체 의존성 재설치
```bash
# 모든 의존성 재설치
pip install -r requirements.txt --force-reinstall

# 또는 캐시 없이 설치
pip install -r requirements.txt --no-cache-dir
```

#### 방법 3: 마이크 장치 확인
```python
# 사용 가능한 마이크 목록 확인
import speech_recognition as sr
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Microphone {index}: {name}")
```

---

## 2. PyAudio 설치 문제

PyAudio는 플랫폼마다 설치 방법이 다르며, 가장 많은 문제를 일으키는 패키지입니다.

### 🪟 Windows

#### 방법 1: pip 직접 설치 (가장 간단)
```bash
pip install pyaudio
```

#### 방법 2: 설치 실패 시 - 컴파일된 바이너리 사용
```bash
# Python 3.8-3.12용 Wheel 파일 다운로드
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio 방문

# 예: Python 3.12, 64bit Windows
pip install PyAudio-0.2.11-cp312-cp312-win_amd64.whl
```

#### 방법 3: Visual C++ 빌드 도구 설치 후 재시도
```bash
# Microsoft C++ Build Tools 설치 필요
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

# 설치 후 재시도
pip install pyaudio
```

### 🍎 macOS

#### 방법 1: Homebrew 사용 (권장)
```bash
# Homebrew 설치 (아직 설치 안 됨)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# PortAudio 설치
brew install portaudio

# PyAudio 설치
pip install pyaudio
```

#### 방법 2: 설치 실패 시
```bash
# XCode Command Line Tools 설치
xcode-select --install

# 환경 변수 설정 후 재시도
export CFLAGS="-I/opt/homebrew/include"
export LDFLAGS="-L/opt/homebrew/lib"
pip install pyaudio
```

### 🐧 Linux (Ubuntu/Debian)

#### 방법 1: 시스템 패키지 먼저 설치
```bash
# PortAudio 개발 패키지 설치
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-pyaudio

# PyAudio 설치
pip install pyaudio
```

#### 방법 2: 다른 의존성 설치
```bash
# 추가 의존성
sudo apt-get install -y python3-dev build-essential libasound2-dev

# PyAudio 재설치
pip install pyaudio
```

### 🐧 Linux (Fedora/CentOS/RHEL)

```bash
# PortAudio 설치
sudo dnf install portaudio-devel
# 또는
sudo yum install portaudio-devel

# PyAudio 설치
pip install pyaudio
```

### ⚠️ PyAudio 설치 실패 지속 시

#### 대체 솔루션: sounddevice 사용
```bash
# PyAudio 대신 sounddevice 사용 가능
pip install sounddevice

# 코드 수정 필요 (개발자 문의)
```

---

## 3. 마이크 권한 및 설정 문제

### 🪟 Windows

#### 1. 시스템 마이크 권한 확인
```
1. Windows 설정 열기 (Win + I)
2. 개인정보 > 마이크
3. "앱이 마이크에 액세스하도록 허용" ON
4. "데스크톱 앱이 마이크에 액세스하도록 허용" ON
5. Python이 목록에 있는지 확인
```

#### 2. 마이크가 기본 장치인지 확인
```
1. 제어판 > 소리
2. 녹음 탭
3. 사용할 마이크 선택 > "기본값으로 설정"
4. 마이크 테스트로 레벨 확인
```

#### 3. 마이크 드라이버 업데이트
```
1. 장치 관리자 열기 (Win + X > 장치 관리자)
2. 오디오 입력 및 출력 확장
3. 마이크 우클릭 > 드라이버 업데이트
```

### 🍎 macOS

#### 1. 시스템 마이크 권한 부여
```
1. 시스템 환경설정 > 보안 및 개인정보 보호
2. 개인정보 보호 탭 > 마이크
3. Python 또는 Terminal 체크
4. 앱 재시작
```

#### 2. 터미널에서 직접 권한 요청
```bash
# Python을 통해 마이크 접근 시도 (권한 대화상자 표시됨)
python -c "import speech_recognition as sr; r = sr.Recognizer(); with sr.Microphone() as source: print('권한 테스트')"
```

### 🐧 Linux

#### 1. ALSA 설정 확인
```bash
# 마이크 장치 확인
arecord -l

# 마이크 테스트 녹음
arecord -d 5 test.wav
aplay test.wav
```

#### 2. PulseAudio 설정
```bash
# PulseAudio 재시작
pulseaudio -k
pulseaudio --start

# 입력 장치 확인
pactl list sources short
```

#### 3. 사용자 권한 확인
```bash
# 오디오 그룹에 사용자 추가
sudo usermod -a -G audio $USER

# 재로그인 필요
```

---

## 4. 음성 합성(TTS) 문제

### 🚨 증상
- "🗣" 메시지는 보이지만 소리가 나지 않음
- TTS 엔진 초기화 오류
- "⚠ TTS 엔진 오류" 메시지

### ✅ 해결 방법

#### 방법 1: pyttsx3 재설치
```bash
pip uninstall pyttsx3 -y
pip install pyttsx3==2.90
```

#### 방법 2: 플랫폼별 TTS 엔진 확인

##### Windows
```bash
# Windows는 SAPI5 사용 (기본 내장)
# 음성 설정 확인:
# 설정 > 시간 및 언어 > 음성

# 한국어 음성 팩 설치 (선택사항)
# Windows Store에서 "한국어 음성 팩" 검색 설치
```

##### macOS
```bash
# macOS는 NSSpeechSynthesizer 사용 (기본 내장)
# 시스템 환경설정 > 손쉬운 사용 > 음성

# 한국어 음성 추가
# 시스템 환경설정 > 손쉬운 사용 > 음성 > 시스템 음성 > 사용자화
```

##### Linux
```bash
# Linux는 espeak 사용
sudo apt-get install espeak espeak-data
# 또는 Fedora
sudo dnf install espeak

# Festival 사용 (대체)
sudo apt-get install festival festvox-kallpc16k
```

#### 방법 3: TTS 없이 텍스트만 출력
```python
# config/settings.json 수정
{
  "tts": {
    "enabled": false  # TTS 비활성화
  }
}
```

---

## 5. 네트워크 연결 문제

### 🚨 증상
- "🚫 Google Speech Recognition 오류"
- "인터넷 연결을 확인해주세요" 메시지
- RequestError 발생

### 🔍 원인
소리새 AI는 Google Speech Recognition API를 사용하므로 인터넷 연결이 필요합니다.

### ✅ 해결 방법

#### 방법 1: 인터넷 연결 확인
```bash
# Google DNS 접속 테스트
ping 8.8.8.8

# Google 웹 접속 테스트
curl -I https://www.google.com
```

#### 방법 2: 방화벽 예외 추가
```bash
# Windows Defender 방화벽
1. 제어판 > Windows Defender 방화벽
2. 고급 설정
3. 아웃바운드 규칙 > 새 규칙
4. Python.exe 추가

# Linux iptables
sudo iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT
```

#### 방법 3: 프록시 설정
```bash
# 프록시 환경에서 작업 시
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="https://proxy.example.com:8080"

# Windows
set HTTP_PROXY=http://proxy.example.com:8080
set HTTPS_PROXY=https://proxy.example.com:8080
```

#### 방법 4: 오프라인 음성 인식 사용 (고급)
```python
# Vosk 또는 Whisper 같은 오프라인 대체 라이브러리 사용
# 개발자에게 문의하거나 향후 업데이트 대기
```

---

## 6. 플랫폼별 상세 가이드

### 🪟 Windows 10/11 완전 가이드

#### 1단계: 시스템 준비
```bash
# Python 3.8+ 설치 확인
python --version

# pip 업그레이드
python -m pip install --upgrade pip
```

#### 2단계: 필수 패키지 설치
```bash
# 의존성 설치
pip install -r requirements.txt

# PyAudio 설치 (재시도 필요시 위 섹션 참조)
pip install pyaudio
```

#### 3단계: 마이크 설정
```
1. 설정 > 시스템 > 소리
2. 입력 > 마이크 선택
3. "마이크 테스트" 버튼으로 레벨 확인
4. 볼륨 50% 이상 설정
```

#### 4단계: 권한 설정
```
1. 설정 > 개인정보 > 마이크
2. 모든 마이크 액세스 권한 ON
```

#### 5단계: 테스트
```bash
python run_all_shinsegye.py
```

### 🍎 macOS 완전 가이드

#### 1단계: Homebrew 및 의존성 설치
```bash
# Homebrew 설치
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 3.8+ 설치 (필요시)
brew install python@3.12

# PortAudio 설치
brew install portaudio
```

#### 2단계: Python 패키지 설치
```bash
# 의존성 설치
pip3 install -r requirements.txt

# PyAudio 설치
pip3 install pyaudio
```

#### 3단계: 마이크 권한
```
1. 시스템 환경설정 > 보안 및 개인정보 보호
2. 개인정보 보호 > 마이크
3. Terminal 또는 Python 체크
```

#### 4단계: 테스트
```bash
python3 run_all_shinsegye.py
```

### 🐧 Ubuntu/Debian 완전 가이드

#### 1단계: 시스템 패키지 설치
```bash
# 시스템 업데이트
sudo apt-get update
sudo apt-get upgrade

# 필수 패키지 설치
sudo apt-get install -y python3 python3-pip python3-dev
sudo apt-get install -y portaudio19-dev python3-pyaudio
sudo apt-get install -y alsa-utils pulseaudio
sudo apt-get install -y espeak espeak-data
```

#### 2단계: Python 패키지 설치
```bash
# 의존성 설치
pip3 install -r requirements.txt
```

#### 3단계: 오디오 시스템 설정
```bash
# ALSA 설정 확인
arecord -l

# PulseAudio 시작
pulseaudio --start

# 마이크 테스트
arecord -d 3 test.wav && aplay test.wav
```

#### 4단계: 테스트
```bash
python3 run_all_shinsegye.py
```

---

## 7. 대체 솔루션

### 옵션 1: 음성 인식 비활성화 (텍스트 입력 모드)

현재는 지원하지 않지만, 향후 업데이트에서 제공 예정:

```python
# 예정된 기능: 텍스트 입력 모드
# config/settings.json
{
  "voice_recognition": {
    "enabled": false,
    "use_text_input": true
  }
}
```

### 옵션 2: 다른 음성 인식 라이브러리 사용

#### Vosk (오프라인)
```bash
pip install vosk
# 한국어 모델 다운로드 필요
```

#### Whisper (고급, GPU 권장)
```bash
pip install openai-whisper
# 더 정확하지만 느림
```

### 옵션 3: 웹 대시보드만 사용

```bash
# 웹 대시보드만 실행
python modules/sorisay_dashboard_web.py

# 브라우저에서 http://localhost:5050 접속
# GUI 버튼으로 명령 실행
```

---

## 8. 고급 디버깅

### 로그 분석

#### 음성 인식 로그 확인
```bash
# 음성 명령 기록 확인
cat logs/voice_history.txt

# 실시간 모니터링
tail -f logs/voice_history.txt
```

#### 시스템 로그 확인
```bash
# 오류 로그 확인
cat logs/sorisay.log | grep -i error

# 최근 로그
tail -n 100 logs/sorisay.log
```

### Python 디버그 모드

#### 상세 오류 메시지 확인
```bash
# 디버그 모드로 실행
python -v run_all_shinsegye.py

# 또는 더 상세하게
python -vv run_all_shinsegye.py
```

#### 대화형 디버거 사용
```python
# 코드에 브레이크포인트 추가
import pdb; pdb.set_trace()

# 또는 IPython 사용
pip install ipython
ipython run_all_shinsegye.py
```

### 마이크 장치 상세 테스트

```python
# test_microphone.py 생성
import speech_recognition as sr

def test_microphone():
    recognizer = sr.Recognizer()
    
    # 사용 가능한 마이크 나열
    print("사용 가능한 마이크:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  [{index}] {name}")
    
    # 각 마이크 테스트
    print("\n마이크 테스트 시작...")
    with sr.Microphone() as source:
        print("주변 소음 조정 중...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"에너지 임계값: {recognizer.energy_threshold}")
        
        print("3초간 말씀해주세요...")
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            print("✅ 오디오 캡처 성공!")
            
            print("음성 인식 시도 중...")
            text = recognizer.recognize_google(audio, language="ko-KR")
            print(f"✅ 인식된 텍스트: {text}")
            
        except sr.WaitTimeoutError:
            print("❌ 타임아웃: 음성이 감지되지 않음")
        except sr.UnknownValueError:
            print("❌ 음성을 인식할 수 없음")
        except sr.RequestError as e:
            print(f"❌ API 오류: {e}")
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")

if __name__ == "__main__":
    test_microphone()
```

```bash
# 테스트 실행
python test_microphone.py
```

### 네트워크 연결 테스트

```python
# test_network.py 생성
import requests
import socket

def test_network():
    print("네트워크 연결 테스트...\n")
    
    # DNS 확인
    try:
        socket.gethostbyname("www.google.com")
        print("✅ DNS 정상")
    except socket.gaierror:
        print("❌ DNS 오류")
    
    # HTTPS 연결 확인
    try:
        response = requests.get("https://www.google.com", timeout=5)
        print(f"✅ HTTPS 연결 정상 (상태: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ HTTPS 연결 오류: {e}")
    
    # Google Speech API 엔드포인트 확인
    try:
        response = requests.get(
            "https://speech.googleapis.com",
            timeout=5
        )
        print("✅ Google Speech API 접근 가능")
    except requests.exceptions.RequestException as e:
        print(f"❌ Google Speech API 접근 불가: {e}")

if __name__ == "__main__":
    test_network()
```

```bash
# 테스트 실행
python test_network.py
```

---

## 🆘 그래도 해결이 안 될 때

### 1. 시스템 정보 수집

```bash
# 시스템 정보 수집 스크립트
echo "=== 시스템 정보 ===" > debug_info.txt
python --version >> debug_info.txt
pip list >> debug_info.txt
echo "" >> debug_info.txt

echo "=== 마이크 장치 ===" >> debug_info.txt
python -c "import speech_recognition as sr; [print(f'[{i}] {name}') for i, name in enumerate(sr.Microphone.list_microphone_names())]" >> debug_info.txt

echo "=== 음성 설정 ===" >> debug_info.txt
cat config/settings.json >> debug_info.txt

# Windows
systeminfo | findstr /B /C:"OS" >> debug_info.txt

# Linux/Mac
uname -a >> debug_info.txt
```

### 2. GitHub Issues 보고

수집한 정보를 포함하여 이슈 보고:
```
제목: [음성 문제] 간단한 설명

내용:
- 운영체제: Windows 11 / macOS 13 / Ubuntu 22.04
- Python 버전: 3.12.0
- 증상: 구체적인 증상 설명
- 시도한 해결 방법: 위에서 시도한 방법들
- 오류 메시지: 전체 오류 로그
- debug_info.txt 첨부
```

### 3. 커뮤니티 지원

- GitHub Discussions: 질문과 토론
- Issues: 버그 리포트
- 이메일: [프로젝트 관리자 이메일]

---

## ✅ 체크리스트

문제 해결 전 다음 항목들을 확인하세요:

- [ ] Python 3.8 이상 설치됨
- [ ] 가상환경이 활성화됨 (권장)
- [ ] requirements.txt의 모든 패키지 설치됨
- [ ] PyAudio가 올바르게 설치됨
- [ ] 마이크가 시스템에 인식됨
- [ ] 마이크 권한이 부여됨
- [ ] 마이크가 기본 장치로 설정됨
- [ ] 인터넷 연결이 정상임
- [ ] 방화벽이 Python을 차단하지 않음
- [ ] 최신 오디오 드라이버 설치됨
- [ ] 로그 파일에서 구체적인 오류 확인함

---

## 📚 관련 문서

- [메인 README](README.md)
- [빠른 시작 가이드](QUICKSTART.md)
- [일반 문제 해결](TROUBLESHOOTING.md)
- [실행 방법](HOW_TO_RUN.md)

---

## 🔄 업데이트 이력

- **2025-10-21**: 초기 버전 작성 - 포괄적인 음성 문제 해결 가이드 추가

---

**이 가이드로 해결되지 않는 문제가 있으면 GitHub Issues에 보고해주세요!**

🎤 행복한 음성 인식 되세요! 🚀
