import speech_recognition as sr
import pyttsx3
import time
import json
import os
from .plugins.plugin_manager import PluginManager
from .sorisay_dashboard_web import broadcast_voice_command, broadcast_system_status
from .ai_code_manager.nlp_processor import NLPProcessor

class SorisayCore:
    def __init__(self, config_path="config/settings.json"):
        # 설정 로드
        self.config = self.load_config(config_path)
        
        # 음성 인식 설정
        self.recognizer = sr.Recognizer()
        voice_config = self.config.get("voice_recognition", {})
        self.recognizer.energy_threshold = voice_config.get("energy_threshold", 300)
        self.recognizer.dynamic_energy_threshold = voice_config.get("dynamic_energy_threshold", True)
        self.recognizer.pause_threshold = voice_config.get("pause_threshold", 0.8)
        self.recognizer.phrase_threshold = voice_config.get("phrase_threshold", 0.3)
        
        # TTS 설정
        self.engine = pyttsx3.init()
        tts_config = self.config.get("tts", {})
        self.engine.setProperty('rate', tts_config.get("rate", 150))
        
        # 플러그인 매니저 초기화
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()
        
        # 자연어 처리 엔진 초기화
        self.nlp_processor = NLPProcessor()
        
        self.running = True
        
        # 대시보드에 시스템 시작 알림
        broadcast_system_status("소리새 시스템 시작됨 - 자연어 처리 기능 활성화")

    def load_config(self, config_path):
        """설정 파일 로드"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"⚠ 설정 파일을 찾을 수 없습니다: {config_path}")
                return self.get_default_config()
        except Exception as e:
            print(f"⚠ 설정 파일 로드 실패: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """기본 설정 반환"""
        return {
            "voice_recognition": {
                "energy_threshold": 300,
                "dynamic_energy_threshold": True,
                "pause_threshold": 0.8,
                "phrase_threshold": 0.3,
                "timeout": 5,
                "phrase_time_limit": 3
            },
            "tts": {"rate": 150}
        }

    def speak(self, text):
        print(f"🗣 {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        try:
            voice_config = self.config.get("voice_recognition", {})
            with sr.Microphone() as source:
                print("🎧 자연어 명령을 듣는 중... (자유롭게 말씀하세요)")
                self.recognizer.adjust_for_ambient_noise(
                    source, 
                    duration=voice_config.get("ambient_noise_duration", 0.5)
                )
                audio = self.recognizer.listen(
                    source, 
                    timeout=voice_config.get("timeout", 5), 
                    phrase_time_limit=voice_config.get("phrase_time_limit", 5)  # 자연어를 위해 시간 증가
                )
                
                cmd = self.recognizer.recognize_google(audio, language="ko-KR")
                print(f"🎙 인식된 자연어: '{cmd}'")
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

    def process_natural_language_command(self, text: str) -> tuple:
        """자연어 명령을 처리하고 적절한 명령어로 변환"""
        # NLP 처리
        nlp_result = self.nlp_processor.process_natural_language(text)
        
        print(f"🧠 NLP 분석 결과:")
        print(f"   의도: {nlp_result['intent']}")
        print(f"   신뢰도: {nlp_result['confidence']:.2f}")
        print(f"   엔티티: {nlp_result['entities']}")
        
        # 신뢰도가 낮으면 사용자에게 확인
        if nlp_result['confidence'] < 0.3:
            return None, None, nlp_result['response']
        
        # 의도를 실제 명령어로 변환
        intent = nlp_result['intent']
        command_keyword = self.nlp_processor.get_command_mapping(intent)
        
        if command_keyword:
            return intent, command_keyword, nlp_result['response']
        else:
            return None, None, "죄송합니다. 명령을 이해하지 못했습니다."
    
    def handle_special_intents(self, intent: str, original_text: str, entities: dict) -> str:
        """특별한 의도들 처리 (인사, 상태확인 등)"""
        if intent == "greeting":
            return "안녕하세요! 저는 소리새입니다. 코드 리팩터링, 깃허브 동기화 등을 도와드릴 수 있어요. 무엇을 도와드릴까요?"
        
        elif intent == "status":
            plugin_count = len(self.plugin_manager.plugins)
            return f"소리새가 정상 동작 중입니다. 현재 {plugin_count}개의 플러그인이 활성화되어 있어요."
        
        elif intent == "help":
            help_msg = "🤖 소리새 자연어 명령 가능한 기능들:\n"
            help_msg += "   📝 '코드를 정리해줘' - 리팩터링 실행\n"
            help_msg += "   🔄 '깃허브에 백업해줘' - 소스 동기화\n"
            help_msg += "   ❓ '상태 확인해줘' - 시스템 상태 점검\n"
            help_msg += "   👋 '안녕 소리새' - 인사\n"
            help_msg += "   🛑 '작업을 끝내줘' - 종료\n"
            help_msg += "\n자유롭게 자연어로 말씀해주세요!"
            return help_msg
        
        return "명령을 처리했습니다."
        self.speak("소리새가 준비되었습니다. 명령어를 말씀해주세요.")
        
        # 모든 플러그인의 도움말 출력
        help_text = self.plugin_manager.get_all_help()
        print(help_text)
        print("-" * 50)
        
        broadcast_system_status("음성 인식 대기 중")
        
        while self.running:
            cmd = self.listen()
            if not cmd: 
                time.sleep(0.5)
                continue
            
            # 플러그인을 통한 명령어 처리
            plugin_name, command, keyword = self.plugin_manager.find_command(cmd)
            
            if plugin_name and command:
                print(f"✅ '{keyword}' 명령어 실행 (플러그인: {plugin_name})")
                broadcast_voice_command(cmd, "success")
                
                try:
                    response = self.plugin_manager.execute_command(plugin_name, command, cmd)
                    self.speak(response)
                    
                    # 종료 명령어 처리
                    if command == "stop":
                        self.running = False
                        broadcast_system_status("시스템 종료 중")
                        
                except Exception as e:
                    error_msg = f"명령어 실행 중 오류가 발생했습니다: {str(e)}"
                    print(f"❌ {error_msg}")
                    self.speak(error_msg)
                    broadcast_voice_command(cmd, "failed")
                    
                yield cmd
            else:
                print(f"❓ 알 수 없는 명령어: '{cmd}'")
                self.speak("지원하지 않는 명령어입니다. 도움말이라고 말씀해보세요.")
                broadcast_voice_command(cmd, "failed")
                yield cmd
            
            if not self.running:
                break
            time.sleep(0.5)
