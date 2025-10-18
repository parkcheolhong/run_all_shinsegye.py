@echo off
chcp 65001 > nul
title 소리새 AI 시스템

echo.
echo ====================================
echo 🌟 소리새 AI 시스템 실행 중...
echo ====================================
echo.

REM 가상환경 활성화 확인
if exist "venv\Scripts\activate.bat" (
    echo 🔧 가상환경 활성화 중...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️ 가상환경을 찾을 수 없습니다. 기본 Python을 사용합니다.
)

echo.
echo 🚀 Python으로 소리새 AI 실행...
echo.

python run_all_shinsegye.py

echo.
echo 📝 실행 완료. 아무 키나 눌러서 종료하세요.
pause > nul