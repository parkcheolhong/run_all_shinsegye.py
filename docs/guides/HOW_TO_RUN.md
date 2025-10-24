# 🚀 소리새 AI 실행 가이드

## 🔍 **링크 클릭 vs 직접 입력 차이점**

**✅ 링크 클릭 시 (작동함)**:

- 미리 정의된 올바른 명령어 실행
- 오타 없이 정확한 `python` 사용

**❌ PowerShell 직접 입력 시 (오류 발생)**:

- 타이핑 실수: `github`, `pythub`, `gitub` 등
- PowerShell 자동완성 혼동

## ✅ **문제 해결 방법들**

### 🥇 방법 1: PowerShell 별칭 사용 (가장 추천)

```powershell
# PowerShell 환경 설정 (한 번만 실행)
.\setup_powershell.ps1

# 이후 간단하게 실행
sorisay              # 영문 별칭
소리새               # 한글 별칭
```

### 🥈 방법 2: 배치 파일 사용 (Windows 추천)

```cmd
start_sorisay.bat
```

### 🥉 방법 3: PowerShell 스크립트 사용

```powershell
.\start_sorisay.ps1
```

### 방법 4: 직접 Python 명령어 사용

```bash
python run_all_shinsegye.py
```

## ❌ 잘못된 명령어들 (사용하지 마세요!)

```bash
# 이런 명령어들은 오류를 발생시킵니다:
github run_all_shinsegye.py     # ❌ 'github' 명령어 존재하지 않음
github run_shinsegye.py         # ❌ 마찬가지로 오류
git run_all_shinsegye.py        # ❌ git도 실행 명령어가 아님
```

## 🔧 가상환경 활성화 (필요한 경우)

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
venv\Scripts\activate.bat
```

Linux/Mac:

```bash
source venv/bin/activate
```

## 📦 필수 시스템 의존성 설치

**참고**: `install.sh` (Linux/Mac) 또는 `install.bat` (Windows) 자동 설치 스크립트를 사용하면 이 단계가 자동으로 처리됩니다.

음성 합성(TTS) 기능을 사용하려면 espeak을 설치해야 합니다:

### Ubuntu/Debian:
```bash
# 자동 설치 사용 시 (권장):
./install.sh

# 또는 수동 설치:
sudo apt-get install espeak espeak-ng portaudio19-dev python3-pyaudio
```

### macOS:
```bash
brew install espeak portaudio
```

### Windows:
- https://espeak.sourceforge.net/ 에서 설치 프로그램 다운로드 후 설치

### Python 패키지 설치:
```bash
pip install -r requirements.txt
```

## 🆘 문제 해결

### "프로그램 이름을 찾을 수 없다" 오류

- **원인**: `github` 같은 존재하지 않는 명령어 사용
- **해결**: 위의 올바른 실행 방법 중 하나 사용

### Python을 찾을 수 없다는 오류

- Python 설치 확인: <https://python.org>
- PATH 환경변수에 Python 추가 확인

### 모듈을 찾을 수 없다는 오류

```bash
pip install -r requirements.txt
```

### espeak/TTS 관련 오류

**오류**: `RuntimeError: This means you probably do not have eSpeak or eSpeak-ng installed!`

**해결 방법**: 위의 "필수 시스템 의존성 설치" 섹션을 참고하여 espeak을 설치하세요.

## 📞 추가 도움

더 자세한 정보는 README.md 파일을 참고하세요.

start_sorisay.bat  # Windows에서 더블클릭하거나 터미널에서 실행

📦 소리새 AI
├── 🚀 start_sorisay.bat        # Windows 배치 파일 (추천)
├── 🔧 start_sorisay.ps1        # PowerShell 스크립트
├── 📖 HOW_TO_RUN.md            # 상세 실행 가이드
└── 📄 README.md                # 업데이트된 실행 방법
