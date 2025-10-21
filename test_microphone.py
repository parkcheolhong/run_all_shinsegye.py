#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
마이크 테스트 스크립트
음성 인식 문제 진단을 위한 상세 테스트
"""

import speech_recognition as sr
import sys

def test_microphone():
    """마이크 장치 및 음성 인식 테스트"""
    print("=" * 60)
    print("🎤 소리새 AI 마이크 진단 도구")
    print("=" * 60)
    print()
    
    recognizer = sr.Recognizer()
    
    # 1. 사용 가능한 마이크 나열
    print("📋 1단계: 사용 가능한 마이크 목록")
    print("-" * 60)
    try:
        mic_list = sr.Microphone.list_microphone_names()
        if not mic_list:
            print("❌ 사용 가능한 마이크가 없습니다!")
            print("   - 마이크가 연결되어 있는지 확인하세요.")
            print("   - 시스템 설정에서 마이크를 활성화했는지 확인하세요.")
            return False
        
        for index, name in enumerate(mic_list):
            print(f"  [{index}] {name}")
        print()
    except Exception as e:
        print(f"❌ 마이크 목록을 가져오는 중 오류 발생: {e}")
        return False
    
    # 2. 마이크 초기화 테스트
    print("📋 2단계: 마이크 초기화 테스트")
    print("-" * 60)
    try:
        with sr.Microphone() as source:
            print("✅ 마이크 초기화 성공!")
            print(f"   샘플 레이트: {source.SAMPLE_RATE} Hz")
            print(f"   청크 크기: {source.CHUNK}")
            print()
    except Exception as e:
        print(f"❌ 마이크 초기화 실패: {e}")
        print("   해결 방법:")
        print("   1. PyAudio 재설치: pip uninstall pyaudio && pip install pyaudio")
        print("   2. 마이크 연결 확인")
        print("   3. 다른 프로그램에서 마이크 사용 중인지 확인")
        return False
    
    # 3. 주변 소음 조정 테스트
    print("📋 3단계: 주변 소음 조정 테스트")
    print("-" * 60)
    try:
        with sr.Microphone() as source:
            print("🔇 주변 소음을 측정하는 중... (1초 소요)")
            print("   조용히 계시세요...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"✅ 소음 조정 완료!")
            print(f"   에너지 임계값: {recognizer.energy_threshold}")
            print(f"   동적 임계값 조정: {recognizer.dynamic_energy_threshold}")
            print()
    except Exception as e:
        print(f"❌ 소음 조정 실패: {e}")
        return False
    
    # 4. 오디오 캡처 테스트
    print("📋 4단계: 오디오 캡처 테스트")
    print("-" * 60)
    print("🎤 3초간 말씀해주세요...")
    print("   (예: '안녕하세요', '테스트', '소리새')")
    print()
    
    try:
        with sr.Microphone() as source:
            # 주변 소음 재조정
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # 오디오 듣기
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            print("✅ 오디오 캡처 성공!")
            print(f"   오디오 데이터 크기: {len(audio.get_raw_data())} bytes")
            print()
            
    except sr.WaitTimeoutError:
        print("❌ 타임아웃: 음성이 감지되지 않았습니다.")
        print("   해결 방법:")
        print("   1. 마이크 볼륨 증가")
        print("   2. 마이크에 더 가까이 말하기")
        print("   3. 마이크 권한 확인")
        print("   4. 에너지 임계값 조정 (config/settings.json)")
        return False
    except Exception as e:
        print(f"❌ 오디오 캡처 실패: {e}")
        return False
    
    # 5. 음성 인식 테스트
    print("📋 5단계: 음성 인식 테스트 (Google Speech Recognition)")
    print("-" * 60)
    print("🌐 인터넷 연결 및 음성 인식 시도 중...")
    
    try:
        text = recognizer.recognize_google(audio, language="ko-KR")
        print(f"✅ 음성 인식 성공!")
        print(f"   인식된 텍스트: '{text}'")
        print()
        
    except sr.UnknownValueError:
        print("⚠️  음성을 인식할 수 없습니다.")
        print("   가능한 원인:")
        print("   1. 너무 조용하게 말함")
        print("   2. 배경 소음이 너무 큼")
        print("   3. 마이크 품질 문제")
        print("   4. 불명확한 발음")
        print()
        print("   다시 시도해보세요!")
        return False
        
    except sr.RequestError as e:
        print(f"❌ Google Speech Recognition API 오류: {e}")
        print("   가능한 원인:")
        print("   1. 인터넷 연결 문제")
        print("   2. 방화벽이 Google API 차단")
        print("   3. Google API 일시적 장애")
        print()
        print("   해결 방법:")
        print("   - 인터넷 연결 확인: ping 8.8.8.8")
        print("   - 브라우저에서 https://www.google.com 접속 가능한지 확인")
        print("   - 방화벽 설정 확인")
        return False
        
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return False
    
    # 6. 최종 결과
    print("=" * 60)
    print("✅ 모든 테스트 통과!")
    print("=" * 60)
    print()
    print("🎉 마이크와 음성 인식이 정상적으로 작동합니다!")
    print("   이제 소리새 AI를 실행할 수 있습니다:")
    print("   python run_all_shinsegye.py")
    print()
    
    return True


def main():
    """메인 함수"""
    try:
        success = test_microphone()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  테스트가 사용자에 의해 중단되었습니다.")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ 치명적인 오류 발생: {e}")
        print("   VOICE_TROUBLESHOOTING_GUIDE.md를 참조하세요.")
        sys.exit(1)


if __name__ == "__main__":
    main()
