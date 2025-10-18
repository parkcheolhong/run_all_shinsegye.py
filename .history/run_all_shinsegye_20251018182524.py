# --- Sorisay 최소 안정 버전: 음성 듣기/말하기 ---
import time
import speech_recognition as sr
import pyttsx3
from modules.sorisay.core import Sorisay

def speak(engine, "..."):
    print(f"[소리새] {text}")
    engine.say(text)
    engine.runAndWait()

def main():
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    speak(engine, "소리새가 시작되었습니다. '끝'이라고 말하면 종료합니다.")

    while True:
        try:
            with sr.Microphone() as source:
                print("🎤 명령을 말씀하세요...")

                # 감도/대기 설정 + 주변 소음 보정
                recognizer.dynamic_energy_threshold = True
                recognizer.energy_threshold = 300
                recognizer.pause_threshold = 1.0
                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                # 음성 듣기 (무한대기/장문 방지)
                audio = recognizer.listen(
                    source,
                    timeout=8,            # 8초 안에 말 시작 없으면 다음 루프로
                    phrase_time_limit=15  # 한 번에 최대 15초 듣기
                )

                # 음성 → 텍스트
                text = recognizer.recognize_google(audio, language="ko-KR")
                print(f"🪶 인식: {text}")

                if "끝" in text:
                    speak(engine, "소리새를 종료합니다.")
                    break

                speak(engine, f"들린 문장: {text}")

        except sr.WaitTimeoutError:
            print("...대기 유지")
            continue
        except sr.UnknownValueError:
            speak(engine, "잘 못 들었습니다.")
        except sr.RequestError:
            speak(engine, "네트워크 연결에 문제가 있습니다.")
        except Exception as e:
            print(f"[오류] {e}")
            time.sleep(0.3)

if __name__ == "__main__":
    app = Sorisay()
    app.speak("소리새 음성 시스템이 시작되었습니다.")
    app.listen_loop()