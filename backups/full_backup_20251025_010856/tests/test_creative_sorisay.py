"""
빠른 창조형 소리새 테스트
"""
from modules.ai_code_manager.creative_sorisay_engine import CreativeSorisayEngine

# 창조형 엔진 테스트
creative = CreativeSorisayEngine()

print("🎨 창조형 소리새 시작!")
print()

# 창조적 아이디어 생성
print("💡 창조적 아이디어:")
for i in range(3):
    idea = creative.generate_creative_idea()
    print(f"   {i+1}. {idea}")

print()

# 개선 제안
print("🚀 자가 개선 제안:")
for i in range(3):
    suggestion = creative.suggest_improvements()
    print(f"   {i+1}. {suggestion}")

print()

# 웹 검색 시뮬레이션  
print("🌐 웹 검색 학습:")
topics = ["AI 개발", "음성 인식", "자동화"]
for topic in topics:
    result = creative.web_search_and_learn(topic)
    print(f"   • {result}")

print()
print("✨ 창조형 소리새가 스스로 발전하고 있습니다!")