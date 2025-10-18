# ----- Sorisay 최소 안정 버전: 음성 듣기/말하기 -----
import sys
import os
import time
import speech_recognition as sr
import pyttsx3

# 현재 프로젝트 루트 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "modules"))

# 모듈 import
from sorisay.core import Sorisay


def speak(engine, text):
    ""\"TTS 엔진을 사용해 텍스트를 음성으로 출력""\"
    print(f"[소리새] {text}")
    engine.say(text)
    engine.runAndWait()

def main():
    ""\"메인 음성 인식 루프""\"
    # TTS 엔진 초기화
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # 말하기 속도 설정
    
    # 음성 인식기 초기화
    recognizer = sr.Recognizer()
    
    speak(engine, "소리새가 시작되었습니다. '끝'이라고 말하면 종료합니다.")

    while True:
        try:
            with sr.Microphone(device_index=0) as source:
                recognizer.dynamic_energy_threshold = True
                recognizer.energy_threshold = 300
                recognizer.pause_threshold = 1.0
                recognizer.adjust_for_ambient_noise(source)
                print("🎤 명령을 말씀하세요...")

                audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
                text = recognizer.recognize_google(audio, language="ko-KR")
                print(f"🎧 인식 결과: {text}")

                if "끝" in text:
                    speak(engine, "소리새를 종료합니다.")
                    print("👋 소리새를 종료합니다.")
                    break
                
                # 인식된 텍스트를 음성으로 응답
                speak(engine, f"말씀하신 내용은 '{text}' 입니다.")

        except sr.UnknownValueError:
            print("⚠ 음성을 인식하지 못했습니다.")
        except sr.RequestError:
            print("🚫 음성 인식 서버 오류입니다.")
        except sr.WaitTimeoutError:
            print("⏳ 대기 유지 중...")
            continue


if __name__ == "__main__":
    main()
