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
            "소리새그만": self.stop,
            "정지": self.stop
        }
        self.running = True

    def speak(self, text):
        print(f"🗣 {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("🎧 듣는 중... (명령어: 리팩터링, 동기화, 종료)")
                # 주변 소음에 맞춰 조정
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # 타임아웃과 구문 제한 시간 설정
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                
                # Google Speech Recognition으로 변환
                cmd = self.recognizer.recognize_google(audio, language="ko-KR")
                print(f"🎙 인식된 명령: '{cmd}'")
                return cmd.strip()
                
        except sr.WaitTimeoutError:
            print("⏱ 음성 입력 대기 시간 초과")
            return None
        except sr.UnknownValueError:
            print("⚠ 음성을 인식하지 못했습니다")
            self.speak("다시 말씀해 주세요")
            return None
        except sr.RequestError as e:
            print(f"🚫 Google Speech Recognition 오류: {e}")
            self.speak("인터넷 연결을 확인해주세요")
            return None

    def refactor(self):
        self.speak("코드 리팩터링 실행 완료!")

    def sync(self):
        self.speak("깃허브 동기화 중입니다... 완료!")

    def stop(self):
        self.speak("시스템 종료합니다.")
        self.running = False

    def run(self):
        self.speak("소리새가 준비되었습니다. 명령어를 말씀해주세요.")
        print("\n📋 사용 가능한 명령어:")
        print("   - 리팩터링 (또는 리팩토링)")
        print("   - 동기화 (또는 싱크)")
        print("   - 종료 (또는 소리새그만, 정지)")
        print("-" * 40)
        
        while self.running:
            cmd = self.listen()
            if not cmd: 
                time.sleep(0.5)  # 짧은 대기 후 다시 시도
                continue
                
            # 명령어 매칭 확인
            command_found = False
            for key, func in self.commands.items():
                if key in cmd:
                    print(f"✅ '{key}' 명령어 실행")
                    func()
                    command_found = True
                    break
            
            if not command_found:
                print(f"❓ 알 수 없는 명령어: '{cmd}'")
                self.speak("지원하지 않는 명령어입니다. 리팩터링, 동기화, 종료 중에서 말씀해주세요.")
            
            # 종료 명령어가 실행된 경우 루프 탈출
            if not self.running:
                break
            time.sleep(0.5)
