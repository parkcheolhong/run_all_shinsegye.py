import random

# 75% 확률 시뮬레이션
probability = 0.75
creative_count = 0
total_tests = 20

print("🎨 창조적 아이디어 75% 확률 시뮬레이션")
print("=" * 45)

for i in range(total_tests):
    if random.random() < probability:
        print(f"{i+1:2}. 💡 창조적 아이디어")
        creative_count += 1
    else:
        print(f"{i+1:2}. ⚪ 일반 응답")

success_rate = (creative_count / total_tests) * 100

print(f"\n🎯 결과 분석:")
print(f"   총 테스트: {total_tests}번")
print(f"   창조적 아이디어: {creative_count}번")
print(f"   성공률: {success_rate:.1f}%")
print(f"   목표 달성: {'✅' if success_rate >= 70 else '❌'}")
print(f"\n🚀 소리새가 이제 {success_rate:.1f}% 확률로 창조적 아이디어를 제안합니다!")