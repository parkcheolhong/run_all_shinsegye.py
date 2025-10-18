# ----- Sorisay 최소 안정 버전: 음성 듣기/말하기 -----# ----- Sorisay 최소 안정 버전: 음성 듣기/말하기 -----# ----- Sorisay 최소 안정 버전: 음성 듣기/말하기 -----

import sys

import osimport sysimport sys

import time

import speech_recognition as srimport osimport os

import pyttsx3

import timeimport time

# 현재 프로젝트 루트 경로 설정

BASE_DIR = os.path.dirname(os.path.abspath(__file__))import speech_recognition as srimport speech_recognition as sr

sys.path.append(os.path.join(BASE_DIR, "modules"))

import pyttsx3import pyttsx3

# 모듈 import

from sorisay.core import Sorisay



# 현재 프로젝트 루트 경로 설정# 현재 프로젝트 루트 경로 설정

def speak(engine, text):

    """TTS 엔진을 사용해 텍스트를 음성으로 출력"""BASE_DIR = os.path.dirname(os.path.abspath(__file__))BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    print(f"[소리새] {text}")

    engine.say(text)sys.path.append(os.path.join(BASE_DIR, "modules"))sys.path.append(os.path.join(BASE_DIR, "modules"))

    engine.runAndWait()



def main():

    """메인 음성 인식 루프"""# 모듈 import# 모듈 import

    # TTS 엔진 초기화

    engine = pyttsx3.init()from sorisay.core import Sorisayfrom sorisay.core import Sorisay

    engine.setProperty('rate', 150)  # 말하기 속도 설정

    

    # 음성 인식기 초기화

    recognizer = sr.Recognizer()

    

    # Sorisay 앱 초기화def speak(engine, text):def speak(engine, text):

    app = Sorisay()

        """TTS 엔진을 사용해 텍스트를 음성으로 출력"""    """TTS 엔진을 사용해 텍스트를 음성으로 출력"""

    speak(engine, "소리새가 시작되었습니다. '끝'이라고 말하면 종료합니다.")

    print(f"[소리새] {text}")    print(f"[소리새] {text}")

    while True:

        try:    engine.say(text)    engine.say(text)

            with sr.Microphone(device_index=0) as source:

                recognizer.dynamic_energy_threshold = True    engine.runAndWait()    engine.runAndWait()

                recognizer.energy_threshold = 300

                recognizer.pause_threshold = 1.0

                recognizer.adjust_for_ambient_noise(source)

                print("🎤 명령을 말씀하세요...")def main():def main():



                audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)    """메인 음성 인식 루프"""    """메인 음성 인식 루프"""

                text = recognizer.recognize_google(audio, language="ko-KR")

                print(f"🎧 인식 결과: {text}")    # TTS 엔진 초기화    # TTS 엔진 초기화



                if "끝" in text:    engine = pyttsx3.init()    engine = pyttsx3.init()

                    speak(engine, "소리새를 종료합니다.")

                    print("👋 소리새를 종료합니다.")    engine.setProperty('rate', 150)  # 말하기 속도 설정    engine.setProperty('rate', 150)  # 말하기 속도 설정

                    break

                        

                # 인식된 텍스트를 음성으로 응답

                speak(engine, f"말씀하신 내용은 '{text}' 입니다.")    # 음성 인식기 초기화    # 음성 인식기 초기화



        except sr.UnknownValueError:    recognizer = sr.Recognizer()    recognizer = sr.Recognizer()

            print("⚠ 음성을 인식하지 못했습니다.")

        except sr.RequestError:        

            print("🚫 음성 인식 서버 오류입니다.")

        except sr.WaitTimeoutError:    # Sorisay 앱 초기화    # Sorisay 앱 초기화

            print("⏳ 대기 유지 중...")

            continue    app = Sorisay()    app = Sorisay()



        

if __name__ == "__main__":

    main()    speak(engine, "소리새가 시작되었습니다. '끝'이라고 말하면 종료합니다.")    speak(engine, "소리새가 시작되었습니다. '끝'이라고 말하면 종료합니다.")



    while True:    while True:

        try:        try:

            with sr.Microphone(device_index=0) as source:            with sr.Microphone(device_index=0) as source:

                recognizer.dynamic_energy_threshold = True                recognizer.dynamic_energy_threshold = True

                recognizer.energy_threshold = 300                recognizer.energy_threshold = 300

                recognizer.pause_threshold = 1.0                recognizer.pause_threshold = 1.0

                recognizer.adjust_for_ambient_noise(source)                recognizer.adjust_for_ambient_noise(source)

                print("🎤 명령을 말씀하세요...")                print("🎤 명령을 말씀하세요...")



                audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)                audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)

                text = recognizer.recognize_google(audio, language="ko-KR")                text = recognizer.recognize_google(audio, language="ko-KR")

                print(f"🎧 인식 결과: {text}")                print(f"🎧 인식 결과: {text}")



                if "끝" in text:                if "끝" in text:

                    speak(engine, "소리새를 종료합니다.")                    speak(engine, "소리새를 종료합니다.")

                    print("👋 소리새를 종료합니다.")                    print("👋 소리새를 종료합니다.")

                    break                    break

                                

                # 인식된 텍스트를 음성으로 응답                # 인식된 텍스트를 음성으로 응답

                speak(engine, f"말씀하신 내용은 '{text}' 입니다.")                speak(engine, f"말씀하신 내용은 '{text}' 입니다.")



        except sr.UnknownValueError:        except sr.UnknownValueError:

            print("⚠ 음성을 인식하지 못했습니다.")            print("⚠ 음성을 인식하지 못했습니다.")

        except sr.RequestError:        except sr.RequestError:

            print("🚫 음성 인식 서버 오류입니다.")            print("🚫 음성 인식 서버 오류입니다.")

        except sr.WaitTimeoutError:        except sr.WaitTimeoutError:

            print("⏳ 대기 유지 중...")            print("⏳ 대기 유지 중...")

            continue            continue







if __name__ == "__main__":if __name__ == "__main__":

    main()    main()

