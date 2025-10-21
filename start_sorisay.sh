#!/bin/bash
# 소리새 AI 실행 스크립트 (Linux/Mac)
# Sorisay AI Start Script

echo "======================================"
echo "🌟 소리새 AI 시스템 실행 중..."
echo "🌟 Starting Sorisay AI System"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "🔧 가상환경 활성화 중..."
    source venv/bin/activate
    echo "✅ 가상환경 활성화됨"
else
    echo "⚠️  가상환경을 찾을 수 없습니다. 기본 Python을 사용합니다."
    echo "   install.sh를 먼저 실행하는 것을 권장합니다."
fi

echo ""
echo "🚀 Python으로 소리새 AI 실행..."
echo ""

# Run the main script
python3 run_all_shinsegye.py

echo ""
echo "📝 실행 완료."
