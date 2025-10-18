# 소리새 AI 시스템 실행 스크립트
# 사용법: .\start_sorisay.ps1

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "🌟 소리새 AI 시스템" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 현재 위치 확인
$currentPath = Get-Location
Write-Host "📁 현재 위치: $currentPath" -ForegroundColor Green

# Python 설치 확인
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Write-Host "🐍 Python: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Python이 설치되지 않았습니다!" -ForegroundColor Red
        Write-Host "   https://python.org 에서 Python을 다운로드하세요." -ForegroundColor Yellow
        Read-Host "아무 키나 눌러서 종료"
        exit
    }
} catch {
    Write-Host "❌ Python을 찾을 수 없습니다!" -ForegroundColor Red
    exit
}

# 가상환경 활성화
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "🔧 가상환경 활성화 중..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
    Write-Host "✅ 가상환경 활성화됨" -ForegroundColor Green
} else {
    Write-Host "⚠️ 가상환경을 찾을 수 없습니다. 기본 Python을 사용합니다." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 소리새 AI 시스템 시작..." -ForegroundColor Magenta
Write-Host ""

# 올바른 명령어 실행
try {
    python run_all_shinsegye.py
} catch {
    Write-Host ""
    Write-Host "❌ 실행 중 오류가 발생했습니다:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📝 실행 완료." -ForegroundColor Green
Read-Host "아무 키나 눌러서 종료"