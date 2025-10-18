# PowerShell 프로파일에 추가할 별칭들
# 사용법: PowerShell에서 $PROFILE 경로에 이 내용을 추가

# 소리새 AI 실행을 위한 별칭들
Set-Alias sorisay "python run_all_shinsegye.py"
Set-Alias 소리새 "python run_all_shinsegye.py"
Set-Alias start-sorisay "python run_all_shinsegye.py"

# 일반적인 오타 방지 함수들
function github { 
    Write-Host "❌ 'github' 명령어는 존재하지 않습니다!" -ForegroundColor Red
    Write-Host "✅ 올바른 명령어: python run_all_shinsegye.py" -ForegroundColor Green
}

function pythub { 
    Write-Host "❌ 'pythub'은 오타입니다! 'python'을 사용하세요." -ForegroundColor Red
    Write-Host "✅ 올바른 명령어: python run_all_shinsegye.py" -ForegroundColor Green
}

function gitub { 
    Write-Host "❌ 'gitub'은 오타입니다! 'python'을 사용하세요." -ForegroundColor Red
    Write-Host "✅ 올바른 명령어: python run_all_shinsegye.py" -ForegroundColor Green
}

# 도움말 함수
function sorisay-help {
    Write-Host "🌟 소리새 AI 실행 방법:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  1. sorisay           # 별칭 사용" -ForegroundColor Green
    Write-Host "  2. 소리새             # 한글 별칭" -ForegroundColor Green  
    Write-Host "  3. python run_all_shinsegye.py  # 직접 명령어" -ForegroundColor Green
    Write-Host "  4. .\start_sorisay.bat          # 배치 파일" -ForegroundColor Green
    Write-Host "  5. .\start_sorisay.ps1          # PowerShell 스크립트" -ForegroundColor Green
    Write-Host ""
}

Write-Host "✅ 소리새 AI 별칭이 로드되었습니다! 'sorisay-help'를 입력해보세요." -ForegroundColor Green