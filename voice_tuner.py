#!/usr/bin/env python3
"""
🎙️ 소리새 AI 음성 조절 도구
Voice Tuner for Sorisay AI System

이 도구는 소리새 AI의 음성 인식 및 음성 출력 설정을 실시간으로 조정할 수 있습니다.
"""

import json
import os
import pyttsx3
import speech_recognition as sr
from datetime import datetime

class VoiceTuner:
    def __init__(self):
        self.config_path = "config/voice_settings.json"
        self.load_current_settings()
        self.init_engines()
        
        # AI 튜터 기능
        self.ai_tutor = PersonalAITutor()

        # 게임 생성 기능  
        self.game_generator = RealTimeGameGenerator()
        
    def load_current_settings(self):
        """현재 음성 설정 로드"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            else:
                self.settings = self.get_default_settings()
        except Exception as e:
            print(f"⚠️ 설정 로드 실패: {e}")
            self.settings = self.get_default_settings()
    
    def get_default_settings(self):
        """기본 음성 설정"""
        return {
            "speech_recognition": {
                "energy_threshold": 300,
                "dynamic_energy_threshold": True,
                "pause_threshold": 0.8,
                "phrase_threshold": 0.3,
                "timeout": 5,
                "phrase_time_limit": 3,
                "language": "ko-KR"
            },
            "text_to_speech": {
                "rate": 150,
                "volume": 0.9,
                "voice_id": None
            },
            "system": {
                "log_commands": True,
                "debug_mode": False,
                "auto_adjust_noise": True,
                "ambient_noise_duration": 0.5
            }
        }
    
    def init_engines(self):
        """음성 엔진 초기화"""
        self.tts_engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.apply_current_settings()
    
    def apply_current_settings(self):
        """현재 설정을 엔진에 적용"""
        # TTS 설정
        tts = self.settings["text_to_speech"]
        self.tts_engine.setProperty('rate', tts["rate"])
        self.tts_engine.setProperty('volume', tts["volume"])
        
        # 음성 선택
        voices = self.tts_engine.getProperty('voices')
        if voices and tts.get("voice_id"):
            for voice in voices:
                if voice.id == tts["voice_id"]:
                    self.tts_engine.setProperty('voice', voice.id)
                    break
        
        # 음성 인식 설정
        sr_config = self.settings["speech_recognition"]
        self.recognizer.energy_threshold = sr_config["energy_threshold"]
        self.recognizer.dynamic_energy_threshold = sr_config["dynamic_energy_threshold"]
        self.recognizer.pause_threshold = sr_config["pause_threshold"]
        self.recognizer.phrase_threshold = sr_config["phrase_threshold"]
    
    def test_voice_output(self, text="안녕하세요! 소리새 AI입니다. 음성이 잘 들리시나요?"):
        """음성 출력 테스트"""
        print(f"🔊 테스트 음성: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def test_voice_input(self):
        """음성 입력 테스트"""
        try:
            with sr.Microphone() as source:
                print("🎤 음성 인식 테스트 중... 아무 말이나 해보세요 (5초):")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                text = self.recognizer.recognize_google(audio, language="ko-KR")
                print(f"✅ 인식된 음성: '{text}'")
                return text
        except sr.WaitTimeoutError:
            print("⏱️ 시간 초과 - 음성이 감지되지 않았습니다")
        except sr.UnknownValueError:
            print("❌ 음성을 인식할 수 없습니다")
        except sr.RequestError as e:
            print(f"❌ 음성 인식 서비스 오류: {e}")
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
        return None
    
    def list_available_voices(self):
        """사용 가능한 음성 목록"""
        voices = self.tts_engine.getProperty('voices')
        print("\n🎭 사용 가능한 음성들:")
        print("=" * 50)
        
        for i, voice in enumerate(voices):
            languages = getattr(voice, 'languages', [])
            gender = "여성" if 'female' in voice.name.lower() else "남성" if 'male' in voice.name.lower() else "불명"
            
            print(f"{i+1:2d}. {voice.name}")
            print(f"    ID: {voice.id}")
            print(f"    성별: {gender}")
            if languages:
                print(f"    언어: {', '.join(languages)}")
            print()
    
    def adjust_speech_rate(self, new_rate):
        """음성 속도 조절"""
        if 50 <= new_rate <= 400:
            self.settings["text_to_speech"]["rate"] = new_rate
            self.tts_engine.setProperty('rate', new_rate)
            print(f"🎵 음성 속도를 {new_rate}로 설정했습니다")
            return True
        else:
            print("❌ 음성 속도는 50-400 범위여야 합니다")
            return False
    
    def adjust_volume(self, new_volume):
        """볼륨 조절"""
        if 0.0 <= new_volume <= 1.0:
            self.settings["text_to_speech"]["volume"] = new_volume
            self.tts_engine.setProperty('volume', new_volume)
            print(f"🔊 볼륨을 {new_volume:.1f}로 설정했습니다")
            return True
        else:
            print("❌ 볼륨은 0.0-1.0 범위여야 합니다")
            return False
    
    def adjust_energy_threshold(self, new_threshold):
        """음성 인식 에너지 임계값 조절"""
        if 50 <= new_threshold <= 2000:
            self.settings["speech_recognition"]["energy_threshold"] = new_threshold
            self.recognizer.energy_threshold = new_threshold
            print(f"🎚️ 마이크 감도를 {new_threshold}로 설정했습니다")
            print("   (값이 낮을수록 더 민감하게 인식)")
            return True
        else:
            print("❌ 에너지 임계값은 50-2000 범위여야 합니다")
            return False
    
    def set_voice_by_index(self, voice_index):
        """음성을 인덱스로 선택"""
        voices = self.tts_engine.getProperty('voices')
        if 0 <= voice_index < len(voices):
            selected_voice = voices[voice_index]
            self.tts_engine.setProperty('voice', selected_voice.id)
            self.settings["text_to_speech"]["voice_id"] = selected_voice.id
            print(f"🎭 음성을 '{selected_voice.name}'로 변경했습니다")
            return True
        else:
            print(f"❌ 잘못된 음성 인덱스입니다 (0-{len(voices)-1} 범위)")
            return False
    
    def save_settings(self):
        """설정 저장"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            # 백업 생성
            if os.path.exists(self.config_path):
                backup_path = f"{self.config_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                import shutil
                shutil.copy2(self.config_path, backup_path)
                print(f"💾 기존 설정을 {backup_path}에 백업했습니다")
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 설정이 {self.config_path}에 저장되었습니다")
            return True
            
        except Exception as e:
            print(f"❌ 설정 저장 실패: {e}")
            return False
    
    def show_current_settings(self):
        """현재 설정 표시"""
        print("\n🔧 현재 음성 설정:")
        print("=" * 40)
        
        tts = self.settings["text_to_speech"]
        print(f"📢 음성 출력:")
        print(f"   속도: {tts['rate']}")
        print(f"   볼륨: {tts['volume']}")
        
        sr_config = self.settings["speech_recognition"]
        print(f"\n🎤 음성 인식:")
        print(f"   에너지 임계값: {sr_config['energy_threshold']}")
        print(f"   동적 조절: {sr_config['dynamic_energy_threshold']}")
        print(f"   일시정지 임계값: {sr_config['pause_threshold']}")
        print(f"   언어: {sr_config['language']}")
        
        # 현재 음성 정보
        voices = self.tts_engine.getProperty('voices')
        current_voice = self.tts_engine.getProperty('voice')
        for voice in voices:
            if voice.id == current_voice:
                print(f"\n🎭 현재 음성: {voice.name}")
                break
    
    def interactive_tuning(self):
        """대화형 음성 조절"""
        print("🎙️ 소리새 AI 음성 조절 도구")
        print("=" * 50)
        
        while True:
            print("\n📋 메뉴:")
            print("1. 현재 설정 보기")
            print("2. 음성 출력 테스트")  
            print("3. 음성 인식 테스트")
            print("4. 사용 가능한 음성 목록")
            print("5. 음성 속도 조절")
            print("6. 볼륨 조절")
            print("7. 마이크 감도 조절")
            print("8. 음성 변경")
            print("9. 설정 저장")
            print("0. 종료")
            
            choice = input("\n선택하세요 (0-9): ").strip()
            
            if choice == '0':
                print("👋 음성 조절 도구를 종료합니다")
                break
            elif choice == '1':
                self.show_current_settings()
            elif choice == '2':
                test_text = input("테스트할 텍스트를 입력하세요 (엔터 시 기본값): ").strip()
                if not test_text:
                    self.test_voice_output()
                else:
                    self.test_voice_output(test_text)
            elif choice == '3':
                self.test_voice_input()
            elif choice == '4':
                self.list_available_voices()
            elif choice == '5':
                try:
                    new_rate = int(input(f"새로운 속도 입력 (현재: {self.settings['text_to_speech']['rate']}, 범위: 50-400): "))
                    if self.adjust_speech_rate(new_rate):
                        self.test_voice_output("속도가 변경되었습니다")
                except ValueError:
                    print("❌ 숫자를 입력해주세요")
            elif choice == '6':
                try:
                    new_volume = float(input(f"새로운 볼륨 입력 (현재: {self.settings['text_to_speech']['volume']}, 범위: 0.0-1.0): "))
                    if self.adjust_volume(new_volume):
                        self.test_voice_output("볼륨이 변경되었습니다")
                except ValueError:
                    print("❌ 숫자를 입력해주세요")
            elif choice == '7':
                try:
                    new_threshold = int(input(f"새로운 마이크 감도 입력 (현재: {self.settings['speech_recognition']['energy_threshold']}, 범위: 50-2000): "))
                    if self.adjust_energy_threshold(new_threshold):
                        print("🧪 새로운 감도로 음성 인식 테스트를 해보세요")
                except ValueError:
                    print("❌ 숫자를 입력해주세요")
            elif choice == '8':
                self.list_available_voices()
                try:
                    voice_num = int(input("선택할 음성 번호: ")) - 1
                    if self.set_voice_by_index(voice_num):
                        self.test_voice_output("음성이 변경되었습니다")
                except ValueError:
                    print("❌ 숫자를 입력해주세요")
            elif choice == '9':
                self.save_settings()
            else:
                print("❌ 잘못된 선택입니다")

def main():
    """메인 함수"""
    try:
        tuner = VoiceTuner()
        tuner.interactive_tuning()
    except KeyboardInterrupt:
        print("\n\n👋 사용자가 종료했습니다")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()