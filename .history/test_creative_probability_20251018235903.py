"""
창조적 아이디어 75% 확률 테스트
"""
from modules.sorisay_core_controller import SorisayCore
import time

print("🎨 창조적 소리새 테스트 (75% 확률)")
print("=" * 50)

# 소리새 초기화
sorisay = SorisayCore()

# 창조적 확률 확인
print(f"🎯 창조적 아이디어 확률: {sorisay.creative_probability * 100}%")
print(f"🎨 창조 모드: {sorisay.creative_mode}")

# 10번 테스트해서 창조적 아이디어 얼마나 나오는지 확인
creative_count = 0
total_tests = 10

print(f"\n📊 {total_tests}번 테스트:")

for i in range(total_tests):
    import random
    if random.random() < sorisay.creative_probability:
        idea = sorisay.creative_engine.generate_creative_idea()
        if isinstance(idea, dict):
            print(f"   {i+1}. 💡 {idea['name']}: {idea['description']}")
        else:
            print(f"   {i+1}. 💡 {idea}")
        creative_count += 1
    else:
        print(f"   {i+1}. ⚪ 일반 응답")

success_rate = (creative_count / total_tests) * 100
print(f"\n🎯 결과: {total_tests}번 중 {creative_count}번 창조적 아이디어 제안")
print(f"📈 실제 성공률: {success_rate}%")
print(f"🎊 목표 달성: {'✅' if success_rate >= 70 else '❌'}")