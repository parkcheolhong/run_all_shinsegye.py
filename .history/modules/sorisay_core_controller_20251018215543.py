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
        self.setup_tts_voice(tts_config)
        
        # 플러그인 매니저 초기화
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()
        
        # 자연어 처리기 초기화
        self.nlp_processor = NLPProcessor()
        
        self.running = True
        
        # 대시보드에 시스템 시작 알림
        broadcast_system_status("소리새 시스템 시작됨")

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
            "tts": {
                "rate": 150,
                "voice_index": 0,
                "volume": 0.9,
                "voice_gender": "female",
                "language": "ko",
                "emotion": "friendly",
                "pitch": 0,
                "voice_effects": {
                    "enable_emotion": true,
                    "enable_speed_variation": true,
                    "enable_pause_insertion": true
                }
            }
        }

    def setup_tts_voice(self, tts_config):
        """TTS 음성 설정"""
        try:
            # 기본 TTS 속성 설정
            rate = tts_config.get("rate", 150)
            volume = tts_config.get("volume", 0.9)
            voice_index = tts_config.get("voice_index", 0)
            
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            
            # 사용 가능한 음성 목록 가져오기
            voices = self.engine.getProperty('voices')
            
            if voices:
                # 한국어 음성 찾기 (선호도 순)
                korean_voices = []
                female_voices = []
                
                for i, voice in enumerate(voices):
                    voice_name = voice.name.lower()
                    voice_id = voice.id.lower()
                    
                    # 한국어 음성 우선 선택
                    if any(keyword in voice_name or keyword in voice_id 
                          for keyword in ['korean', 'ko-kr', 'korea', '한국']):
                        korean_voices.append((i, voice))
                    
                    # 여성 음성 우선 선택  
                    if any(keyword in voice_name or keyword in voice_id
                          for keyword in ['female', 'woman', 'zira', 'hazel']):
                        female_voices.append((i, voice))
                
                # 음성 선택 우선순위: 한국어 > 여성 > 인덱스
                selected_voice = None
                if korean_voices:
                    selected_voice = korean_voices[0]
                    print(f"🎤 한국어 음성 선택: {selected_voice[1].name}")
                elif female_voices:
                    selected_voice = female_voices[0]
                    print(f"🎤 여성 음성 선택: {selected_voice[1].name}")
                elif voice_index < len(voices):
                    selected_voice = (voice_index, voices[voice_index])
                    print(f"🎤 음성 선택: {selected_voice[1].name}")
                
                if selected_voice:
                    self.engine.setProperty('voice', selected_voice[1].id)
                
            print(f"🔊 TTS 설정 완료 - 속도: {rate}, 볼륨: {volume}")
            
        except Exception as e:
            print(f"⚠ TTS 설정 중 오류: {e}")

    def speak_with_emotion(self, text, emotion="neutral", speed_modifier=1.0):
        """감정과 속도 조절이 가능한 음성 출력"""
        try:
            tts_config = self.config.get("tts", {})
            effects = tts_config.get("voice_effects", {})
            
            # 원래 속도 저장
            original_rate = self.engine.getProperty('rate')
            
            # 감정에 따른 속도 조절
            if effects.get("enable_speed_variation", True):
                emotion_rates = {
                    "excited": original_rate * 1.2,
                    "happy": original_rate * 1.1, 
                    "neutral": original_rate,
                    "sad": original_rate * 0.8,
                    "error": original_rate * 0.9,
                    "success": original_rate * 1.05
                }
                new_rate = int(emotion_rates.get(emotion, original_rate) * speed_modifier)
                self.engine.setProperty('rate', new_rate)
            
            # 감정에 따른 텍스트 수정
            if effects.get("enable_emotion", True):
                text = self.add_emotional_markers(text, emotion)
            
            # 자연스러운 일시정지 추가
            if effects.get("enable_pause_insertion", True):
                text = self.add_natural_pauses(text)
            
            print(f"🗣 [{emotion}] {text}")
            self.engine.say(text)
            self.engine.runAndWait()
            
            # 원래 속도로 복원
            self.engine.setProperty('rate', original_rate)
            
        except Exception as e:
            print(f"⚠ 음성 출력 오류: {e}")
            # 기본 speak 메서드로 fallback
            self.speak(text)

    def add_emotional_markers(self, text, emotion):
        """감정에 따른 텍스트 마커 추가"""
        emotion_prefixes = {
            "excited": "와! ",
            "happy": "좋아요! ",
            "success": "훌륭해요! ",
            "error": "앗, ",
            "sad": "음... ",
            "neutral": ""
        }
        
        emotion_suffixes = {
            "excited": "!",
            "happy": "~",
            "success": "!",
            "error": "...",
            "sad": ".",
            "neutral": ""
        }
        
        prefix = emotion_prefixes.get(emotion, "")
        suffix = emotion_suffixes.get(emotion, "")
        
        return f"{prefix}{text}{suffix}"

    def add_natural_pauses(self, text):
        """자연스러운 일시정지 추가"""
        # 문장 부호 뒤에 일시정지 추가
        import re
        
        # 쉼표 뒤 짧은 일시정지
        text = re.sub(r',', ', <break time="300ms"/>', text)
        
        # 마침표, 느낌표, 물음표 뒤 긴 일시정지  
        text = re.sub(r'[.!?]', r'\g<0> <break time="500ms"/>', text)
        
        # "음", "어" 같은 간투사 뒤 일시정지
        text = re.sub(r'(음|어|그|자)\s', r'\1 <break time="200ms"/> ', text)
        
        return text

    def speak(self, text, emotion="neutral"):
        """개선된 음성 출력 (감정 지원)"""
        self.speak_with_emotion(text, emotion)

    def listen(self):
        try:
            voice_config = self.config.get("voice_recognition", {})
            with sr.Microphone() as source:
                print("🎧 듣는 중...")
                self.recognizer.adjust_for_ambient_noise(
                    source, 
                    duration=voice_config.get("ambient_noise_duration", 0.5)
                )
                audio = self.recognizer.listen(
                    source, 
                    timeout=voice_config.get("timeout", 5), 
                    phrase_time_limit=voice_config.get("phrase_time_limit", 3)
                )
                
                cmd = self.recognizer.recognize_google(audio, language="ko-KR")
                print(f"🎙 인식된 명령: '{cmd}'")
                return cmd.strip()
                
        except sr.WaitTimeoutError:
            print("⏱ 음성 입력 대기 시간 초과")
            return None
        except sr.UnknownValueError:
            print("⚠ 음성을 인식하지 못했습니다")
            self.speak("다시 말씀해 주세요", "neutral")
            return None
        except sr.RequestError as e:
            print(f"🚫 Google Speech Recognition 오류: {e}")
            self.speak("인터넷 연결을 확인해주세요", "error")
            return None

    def run(self):
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
            
            # 🧠 자연어 처리를 통한 의도 분석
            nlp_result = self.nlp_processor.process_natural_language(cmd)
            intent = nlp_result["intent"]
            confidence = nlp_result["confidence"]
            
            print(f"🧠 NLP 분석: 의도='{intent}', 신뢰도={confidence:.2f}")
            
            # 높은 신뢰도로 의도가 파악된 경우
            if intent and confidence > 0.5:
                # 의도를 실제 명령어로 변환
                mapped_command = self.nlp_processor.get_command_mapping(intent)
                emotion = nlp_result.get("emotion", "neutral")
                
                if mapped_command:
                    # 플러그인을 통한 명령어 실행
                    plugin_name, command, keyword = self.plugin_manager.find_command(mapped_command)
                    
                    if plugin_name and command:
                        print(f"✅ 자연어 명령 실행: '{cmd}' -> '{mapped_command}' (플러그인: {plugin_name})")
                        broadcast_voice_command(cmd, "success")
                        
                        # NLP 응답을 감정과 함께 제공
                        nlp_response = nlp_result["response"]
                        self.speak(nlp_response, emotion)
                        
                        try:
                            response = self.plugin_manager.execute_command(plugin_name, command, cmd)
                            if response != nlp_response:  # 중복 응답 방지
                                # 명령 결과에 따라 감정 조정
                                result_emotion = "success" if "완료" in response or "성공" in response else emotion
                                self.speak(response, result_emotion)
                            
                            # 종료 명령어 처리
                            if command == "stop":
                                self.running = False
                                broadcast_system_status("시스템 종료 중")
                                
                        except Exception as e:
                            error_msg = f"명령어 실행 중 오류가 발생했습니다: {str(e)}"
                            print(f"❌ {error_msg}")
                            self.speak(error_msg, "error")
                            broadcast_voice_command(cmd, "failed")
                            
                        yield cmd
                    else:
                        # 특별한 명령어들 (인사, 상태확인 등) 직접 처리
                        print(f"✅ 자연어 응답: '{intent}'")
                        self.speak(nlp_result["response"], emotion)
                        broadcast_voice_command(cmd, "success")
                        yield cmd
                else:
                    print(f"⚠ 매핑되지 않은 의도: '{intent}'")
                    self.speak(nlp_result["response"], emotion)
                    broadcast_voice_command(cmd, "warning")
                    yield cmd
            else:
                # 낮은 신뢰도이거나 의도 파악 실패 시 기존 방식으로 처리
                print(f"🔄 기존 방식으로 처리 시도...")
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
                    self.speak("죄송합니다. 명령을 이해하지 못했습니다. '도움말'이라고 말씀하시면 사용 가능한 명령어를 알려드리겠습니다.")
                    broadcast_voice_command(cmd, "failed")
                    yield cmd
            
            if not self.running:
                break
            time.sleep(0.5)
