import speech_recognition as sr
import pyttsx3
import time

class SorisayCore:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # 음성 인식 성능 향상 설정
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        
        self.engine = pyttsx3.init()
        # TTS 속도 조절
        self.engine.setProperty('rate', 150)
        
        self.commands = {
            "리팩터링": self.refactor,
            "리팩토링": self.refactor,
            "동기화": self.sync,
            "싱크": self.sync,
            "종료": self.stop,
            "끝": self.stop,
            "정지": self.stop
        }
        self.running = True

    def speak(self, text):
        print(f"🗣 {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("🎧 듣는 중...")
            audio = self.recognizer.listen(source)
            try:
                cmd = self.recognizer.recognize_google(audio, language="ko-KR")
                print(f"🎙 인식: {cmd}")
                return cmd
            except:
                self.speak("명령을 이해하지 못했어요.")
                return None

    def refactor(self):
        self.speak("코드 리팩터링 실행 완료!")

    def sync(self):
        self.speak("깃허브 동기화 중입니다... 완료!")

    def stop(self):
        self.speak("시스템 종료합니다.")
        self.running = False

    def run(self):
        self.speak("소리새가 준비되었습니다.")
        while self.running:
            cmd = self.listen()
            if not cmd: continue
            for key, func in self.commands.items():
                if key in cmd:
                    func()
                    break
            time.sleep(0.5)
