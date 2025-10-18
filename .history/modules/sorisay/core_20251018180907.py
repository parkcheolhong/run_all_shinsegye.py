import speech_recognition as sr
import pyttsx3
import time

class Sorisay:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_loop(self):
        while True:
            try:
                with sr.Microphone() as source:
                    print("🎤 명령을 말씀하세요...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=15)
                    text = self.recognizer.recognize_google(audio, language="ko-KR")
                    print(f"🪶 인식: {text}")
                    if "끝" in text:
                        self.speak(engine,"소리새 종료합니다.")
                        break
                    self.speak(f"당신이 말한 것은 {text} 입니다.")
            except sr.WaitTimeoutError:
                print("조용하네요... 계속 대기합니다.")
                continue
            except sr.UnknownValueError:
                self.speak("잘 못 들었습니다.")
            except sr.RequestError:
                self.speak("서버 연결에 문제가 있습니다.")
            time.sleep(1)
