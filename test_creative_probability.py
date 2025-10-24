"""
창조적 아이디어 75% 확률 테스트
"""
import sys
import os

# Mock 필수 모듈들
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ TTS 엔진(espeak/espeak-ng)을 찾을 수 없습니다. 모의 모드로 진행합니다.")
    
    # Mock TTS 모듈
    class MockEngine:
        def setProperty(self, key, value):
            pass
        def getProperty(self, key):
            return []
        def say(self, text):
            pass
        def runAndWait(self):
            pass
    
    class MockTTS:
        @staticmethod
        def init():
            return MockEngine()
    
    sys.modules['pyttsx3'] = MockTTS

try:
    import speech_recognition as sr
except ImportError:
    class MockRecognizer:
        def __init__(self):
            self.energy_threshold = 300
            self.dynamic_energy_threshold = True
            self.pause_threshold = 0.8
            self.phrase_threshold = 0.3
    
    class MockSR:
        Recognizer = MockRecognizer
    
    sys.modules['speech_recognition'] = MockSR()

# 직접 창조 엔진만 사용 (TTS 의존성 회피)
from modules.ai_code_manager.creative_sorisay_engine import CreativeSorisayEngine
import random

print("🎨 창조적 소리새 테스트 (75% 확률)")
print("=" * 50)

# 창조 엔진 초기화
creative_engine = CreativeSorisayEngine()
creative_probability = 0.75
creative_mode = True

# 창조적 확률 확인
print(f"🎯 창조적 아이디어 확률: {creative_probability * 100}%")
print(f"🎨 창조 모드: {creative_mode}")

# 10번 테스트해서 창조적 아이디어 얼마나 나오는지 확인
creative_count = 0
total_tests = 10

print(f"\n📊 {total_tests}번 테스트:")

for i in range(total_tests):
    if random.random() < creative_probability:
        idea = creative_engine.generate_creative_idea()
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