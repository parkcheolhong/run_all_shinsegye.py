@echo off
chcp 65001 > nul
REM 소리새 AI 자동 설치 스크립트 (Windows)
REM Sorisay AI Automated Installation Script

echo ======================================
echo 🌟 소리새 AI 설치 시작
echo 🌟 Sorisay AI Installation
echo ======================================
echo.

REM Check if Python is installed
echo 🔍 Python 설치 확인 중...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다.
    echo Python 3.8 이상을 설치한 후 다시 실행해주세요.
    echo 다운로드: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% 발견
echo.

REM Check if pip is installed
echo 🔍 pip 설치 확인 중...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip이 설치되어 있지 않습니다.
    echo pip를 설치한 후 다시 실행해주세요.
    pause
    exit /b 1
)
echo ✅ pip 발견
echo.

REM Create virtual environment
echo 📦 가상환경 생성 중...
if exist "venv" (
    echo ⚠️  기존 venv 폴더 발견. 재생성합니다...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ❌ 가상환경 생성 실패
    pause
    exit /b 1
)
echo ✅ 가상환경 생성 완료
echo.

REM Activate virtual environment
echo 🔧 가상환경 활성화 중...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 가상환경 활성화 실패
    pause
    exit /b 1
)
echo ✅ 가상환경 활성화됨
echo.

REM Upgrade pip
echo 📦 pip 업그레이드 중...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo ⚠️  pip 업그레이드 실패했지만 계속 진행합니다...
)
echo ✅ pip 업그레이드 완료
echo.

REM Install dependencies
echo 📦 필수 패키지 설치 중...
echo    이 작업은 몇 분 정도 걸릴 수 있습니다...
echo.

if not exist "requirements.txt" (
    echo ❌ requirements.txt 파일을 찾을 수 없습니다.
    pause
    exit /b 1
)

echo 📋 requirements.txt에서 패키지 설치 중...
echo.

REM Install packages one by one with error handling
setlocal enabledelayedexpansion
set "failed_packages="

for /f "usebackq tokens=*" %%a in ("requirements.txt") do (
    set "line=%%a"
    REM Skip comments and empty lines
    echo !line! | findstr /r "^[[:space:]]*#" >nul
    if errorlevel 1 (
        if not "!line!"=="" (
            echo   📥 설치 중: !line!
            pip install "!line!" --no-cache-dir
            if errorlevel 1 (
                echo     ❌ 설치 실패: !line!
                set "failed_packages=!failed_packages! !line!"
            ) else (
                echo     ✅ 설치 성공: !line!
            )
        )
    )
)

if not "!failed_packages!"=="" (
    echo.
    echo ⚠️  다음 패키지 설치에 실패했습니다:
    echo !failed_packages!
    echo 이 패키지들은 선택사항일 수 있습니다.
)

echo.
echo ✅ 패키지 설치 완료
echo.

REM Create necessary directories
echo 📁 필요한 디렉토리 생성 중...
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "config" mkdir config
if not exist "memories" mkdir memories
echo ✅ 디렉토리 생성 완료
echo.

REM Create config files from templates if they don't exist
echo ⚙️  설정 파일 확인 중...
if exist "config\settings.json.template" (
    if not exist "config\settings.json" (
        copy "config\settings.json.template" "config\settings.json" >nul
        echo ✅ config\settings.json 생성
    )
)
echo.

REM Download NLTK data if needed
echo 📚 NLTK 데이터 다운로드 중...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)" 2>nul
echo ✅ NLTK 데이터 다운로드 완료
echo.

REM Run verification
echo 🔍 설치 확인 중...
if exist "verify_install.py" (
    python verify_install.py
) else (
    echo ⚠️  verify_install.py를 찾을 수 없습니다. 수동 확인이 필요합니다.
)
echo.

REM Installation complete
echo ======================================
echo 🎉 설치 완료!
echo ======================================
echo.
echo 다음 단계:
echo.
echo 1. 가상환경 활성화:
echo    venv\Scripts\activate.bat
echo.
echo 2. 소리새 AI 실행:
echo    python run_all_shinsegye.py
echo.
echo 또는 배치 스크립트 사용:
echo    start_sorisay.bat
echo.
echo 문제가 있으면 TROUBLESHOOTING.md를 참조하세요.
echo.
echo 🌟 소리새 AI를 사용해주셔서 감사합니다! 🌟
echo.
pause
