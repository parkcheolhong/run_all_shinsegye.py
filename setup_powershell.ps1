# 소리새 AI PowerShell 환경 설정 스크립트

Write-Host "🔧 소리새 AI PowerShell 환경 설정 중..." -ForegroundColor Cyan
Write-Host ""

# PowerShell 프로파일 경로 확인
$profilePath = $PROFILE
$profileDir = Split-Path $profilePath

Write-Host "📁 PowerShell 프로파일 위치: $profilePath" -ForegroundColor Yellow

# 프로파일 디렉터리가 없으면 생성
if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force
    Write-Host "✅ 프로파일 디렉터리 생성됨" -ForegroundColor Green
}

# 기존 프로파일 백업
if (Test-Path $profilePath) {
    $backupPath = "$profilePath.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item $profilePath $backupPath
    Write-Host "💾 기존 프로파일 백업됨: $backupPath" -ForegroundColor Yellow
}

# 소리새 AI 설정 추가
$sorisayConfig = @"

# ===========================================
# 소리새 AI 설정 (자동 추가됨)
# ===========================================

# 소리새 AI 실행을 위한 별칭들
function sorisay { 
    Set-Location "C:\Projects\Shinsegye_Main"
    python run_all_shinsegye.py 
}

function 소리새 { 
    Set-Location "C:\Projects\Shinsegye_Main"
    python run_all_shinsegye.py 
}

# 오타 방지 함수들
function github { 
    Write-Host "❌ 'github' 명령어는 존재하지 않습니다!" -ForegroundColor Red
    Write-Host "✅ 올바른 명령어: sorisay 또는 python run_all_shinsegye.py" -ForegroundColor Green
}

function pythub { 
    Write-Host "❌ 'pythub'은 오타입니다! 'python'을 사용하세요." -ForegroundColor Red
    Write-Host "✅ 올바른 명령어: sorisay 또는 python run_all_shinsegye.py" -ForegroundColor Green
}

function gitub { 
    Write-Host "❌ 'gitub'은 오타입니다!" -ForegroundColor Red
    Write-Host "✅ 올바른 명령어: sorisay 또는 python run_all_shinsegye.py" -ForegroundColor Green
}

# 도움말 함수
function sorisay-help {
    Write-Host "🌟 소리새 AI 실행 방법:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  sorisay              # 어디서든 실행" -ForegroundColor Green
    Write-Host "  소리새               # 한글 명령어" -ForegroundColor Green  
    Write-Host ""
    Write-Host "💡 팁: 'sorisay'만 입력하면 자동으로 프로젝트 폴더로 이동하여 실행됩니다!" -ForegroundColor Yellow
}

Write-Host "✅ 소리새 AI PowerShell 환경이 준비되었습니다! 'sorisay' 또는 '소리새'로 실행하세요." -ForegroundColor Green

"@

# 프로파일에 설정 추가
Add-Content -Path $profilePath -Value $sorisayConfig

Write-Host ""
Write-Host "🎉 설치 완료!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 다음 단계:" -ForegroundColor Cyan
Write-Host "  1. PowerShell을 재시작하거나" -ForegroundColor White
Write-Host "  2. '. `$PROFILE' 명령어로 프로파일 새로고침" -ForegroundColor White
Write-Host "  3. 'sorisay' 또는 '소리새' 명령어로 실행" -ForegroundColor White
Write-Host ""
Write-Host "💡 'sorisay-help'로 도움말을 확인하세요!" -ForegroundColor Yellow

Read-Host "아무 키나 눌러서 계속"