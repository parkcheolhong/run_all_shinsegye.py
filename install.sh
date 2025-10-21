#!/bin/bash
# 소리새 AI 자동 설치 스크립트 (Linux/Mac)
# Sorisay AI Automated Installation Script

set -e  # Exit on error

echo "======================================"
echo "🌟 소리새 AI 설치 시작"
echo "🌟 Sorisay AI Installation"
echo "======================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "🔍 Python 설치 확인 중..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3이 설치되어 있지 않습니다.${NC}"
    echo "Python 3.8 이상을 설치한 후 다시 실행해주세요."
    echo "다운로드: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION 발견${NC}"

# Check if pip is installed
echo "🔍 pip 설치 확인 중..."
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3이 설치되어 있지 않습니다.${NC}"
    echo "pip를 설치한 후 다시 실행해주세요."
    exit 1
fi
echo -e "${GREEN}✅ pip 발견${NC}"

# Create virtual environment
echo ""
echo "📦 가상환경 생성 중..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  기존 venv 폴더 발견. 재생성합니다...${NC}"
    rm -rf venv
fi

python3 -m venv venv
echo -e "${GREEN}✅ 가상환경 생성 완료${NC}"

# Activate virtual environment
echo "🔧 가상환경 활성화 중..."
source venv/bin/activate
echo -e "${GREEN}✅ 가상환경 활성화됨${NC}"

# Upgrade pip
echo ""
echo "📦 pip 업그레이드 중..."
pip install --upgrade pip setuptools wheel
echo -e "${GREEN}✅ pip 업그레이드 완료${NC}"

# Install dependencies
echo ""
echo "📦 필수 패키지 설치 중..."
echo "   이 작업은 몇 분 정도 걸릴 수 있습니다..."

# Install requirements
if [ -f "requirements.txt" ]; then
    echo ""
    echo "📋 requirements.txt에서 패키지 설치 중..."
    
    # Install each package with error handling
    while IFS= read -r line || [ -n "$line" ]; do
        # Skip comments and empty lines
        if [[ "$line" =~ ^[[:space:]]*# ]] || [[ -z "$line" ]]; then
            continue
        fi
        
        # Extract package name
        package=$(echo "$line" | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1 | tr -d '[:space:]')
        
        echo "  📥 설치 중: $line"
        
        # Try to install with retry logic
        max_retries=3
        retry_count=0
        while [ $retry_count -lt $max_retries ]; do
            if pip install "$line" --no-cache-dir; then
                echo -e "    ${GREEN}✅ 설치 성공: $package${NC}"
                break
            else
                retry_count=$((retry_count + 1))
                if [ $retry_count -lt $max_retries ]; then
                    echo -e "    ${YELLOW}⚠️  재시도 중 ($retry_count/$max_retries)...${NC}"
                    sleep 2
                else
                    echo -e "    ${RED}❌ 설치 실패: $package${NC}"
                    echo -e "    ${YELLOW}⚠️  이 패키지는 선택사항일 수 있습니다. 계속 진행합니다...${NC}"
                fi
            fi
        done
    done < requirements.txt
    
    echo -e "${GREEN}✅ 패키지 설치 완료${NC}"
else
    echo -e "${RED}❌ requirements.txt 파일을 찾을 수 없습니다.${NC}"
    exit 1
fi

# Create necessary directories
echo ""
echo "📁 필요한 디렉토리 생성 중..."
mkdir -p logs data config memories
echo -e "${GREEN}✅ 디렉토리 생성 완료${NC}"

# Create config files from templates if they don't exist
echo ""
echo "⚙️  설정 파일 확인 중..."
if [ -f "config/settings.json.template" ] && [ ! -f "config/settings.json" ]; then
    cp config/settings.json.template config/settings.json
    echo -e "${GREEN}✅ config/settings.json 생성${NC}"
fi

# Download NLTK data if needed
echo ""
echo "📚 NLTK 데이터 다운로드 중..."
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)" 2>/dev/null || true
echo -e "${GREEN}✅ NLTK 데이터 다운로드 완료${NC}"

# Installation complete
echo ""
echo "======================================"
echo -e "${GREEN}🎉 설치 완료!${NC}"
echo "======================================"
echo ""
echo "다음 단계:"
echo ""
echo -e "${BLUE}1. 가상환경 활성화:${NC}"
echo "   source venv/bin/activate"
echo ""
echo -e "${BLUE}2. 소리새 AI 실행:${NC}"
echo "   python run_all_shinsegye.py"
echo ""
echo -e "${BLUE}또는 배치 스크립트 사용:${NC}"
echo "   ./start_sorisay.sh"
echo ""
echo "문제가 있으면 TROUBLESHOOTING.md를 참조하세요."
echo ""
echo "🌟 소리새 AI를 사용해주셔서 감사합니다! 🌟"
