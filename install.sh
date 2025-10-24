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

# Install system dependencies (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo ""
    echo "🔧 시스템 의존성 확인 중..."
    
    # Check if running on a Debian/Ubuntu-based system
    if command -v apt-get &> /dev/null; then
        echo "📦 시스템 패키지 설치 중 (portaudio19-dev, python3-pyaudio, espeak)..."
        echo -e "${YELLOW}⚠️  이 작업은 sudo 권한이 필요합니다.${NC}"
        
        # Check if packages are already installed
        MISSING_PACKAGES=""
        
        if ! dpkg -l | grep -q "portaudio19-dev"; then
            MISSING_PACKAGES="$MISSING_PACKAGES portaudio19-dev"
        fi
        
        if ! dpkg -l | grep -q "python3-pyaudio"; then
            MISSING_PACKAGES="$MISSING_PACKAGES python3-pyaudio"
        fi
        
        if ! dpkg -l | grep -q "^ii.*espeak[^-]"; then
            MISSING_PACKAGES="$MISSING_PACKAGES espeak"
        fi
        
        if [ -n "$MISSING_PACKAGES" ]; then
            echo "설치가 필요한 패키지:$MISSING_PACKAGES"
            echo ""
            
            # Try to install packages
            if sudo apt-get update && sudo apt-get install -y$MISSING_PACKAGES; then
                echo -e "${GREEN}✅ 시스템 패키지 설치 완료${NC}"
            else
                echo -e "${YELLOW}⚠️  시스템 패키지 설치에 실패했습니다.${NC}"
                echo "수동으로 다음 명령을 실행해주세요:"
                echo "  sudo apt-get update"
                echo "  sudo apt-get install -y portaudio19-dev python3-pyaudio espeak"
                echo ""
                echo -e "${YELLOW}계속 진행하시겠습니까? (y/n)${NC}"
                read -r response
                if [[ ! "$response" =~ ^[Yy]$ ]]; then
                    echo "설치를 중단합니다."
                    exit 1
                fi
            fi
        else
            echo -e "${GREEN}✅ 필요한 시스템 패키지가 이미 설치되어 있습니다${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Debian/Ubuntu 기반 시스템이 아닙니다.${NC}"
        echo "수동으로 다음 패키지를 설치해주세요:"
        echo "  - portaudio19-dev"
        echo "  - python3-pyaudio"
        echo "  - espeak"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo "🍎 macOS 감지됨"
    echo -e "${YELLOW}⚠️  Homebrew를 사용하여 다음 패키지를 설치해주세요:${NC}"
    echo "  brew install portaudio"
    echo "  brew install espeak"
else
    echo ""
    echo -e "${YELLOW}⚠️  알 수 없는 운영체제입니다.${NC}"
    echo "수동으로 필요한 시스템 의존성을 설치해주세요."
fi

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
        
        # Extract package name for display.
        # This regex matches the package name (with optional extras) at the start of the line.
        # It supports most common pip requirement formats, but may not handle all edge cases (e.g., direct URLs without #egg).
        if [[ "$line" =~ ^[[:space:]]*([a-zA-Z0-9._-]+(\[[a-zA-Z0-9_,.-]+\])?) ]]; then
            package="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ \#egg=([a-zA-Z0-9._-]+) ]]; then
            package="${BASH_REMATCH[1]}"
        else
            package="$line"
        fi
        
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
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ NLTK 데이터 다운로드에 실패했습니다. 인터넷 연결을 확인하거나 Python/NLTK가 올바르게 설치되었는지 확인하세요.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ NLTK 데이터 다운로드 완료${NC}"

# Run verification
echo ""
echo "🔍 설치 확인 중..."
if [ -f "verify_install.py" ]; then
    python3 verify_install.py
    verify_result=$?
else
    echo -e "${YELLOW}⚠️  verify_install.py를 찾을 수 없습니다. 수동 확인이 필요합니다.${NC}"
    verify_result=0
fi

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
