import re
import difflib
from typing import Dict, List, Tuple, Optional
import json
import os

class NLPProcessor:
    """자연어 처리 엔진 - 자연어 명령을 이해하고 적절한 명령어로 변환"""
    
    def __init__(self, config_path="config/nlp_patterns.json"):
        self.config_path = config_path
        self.intent_patterns = self.load_patterns()
        self.context_memory = []  # 대화 컨텍스트 저장
        self.emotion_patterns = self.get_emotion_patterns()  # 감정 패턴 추가
        
    def load_patterns(self) -> Dict:
        """자연어 패턴 설정 로드"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 기본 패턴 생성
                default_patterns = self.get_default_patterns()
                self.save_patterns(default_patterns)
                return default_patterns
        except Exception as e:
            print(f"⚠ NLP 패턴 로드 실패: {e}")
            return self.get_default_patterns()
    
    def save_patterns(self, patterns: Dict):
        """패턴을 파일로 저장"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(patterns, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠ NLP 패턴 저장 실패: {e}")
    
    def get_default_patterns(self) -> Dict:
        """기본 자연어 패턴 정의"""
        return {
            "intents": {
                "refactor": {
                    "patterns": [
                        r".*코드.*정리.*",
                        r".*리팩터링.*",
                        r".*리팩토링.*",
                        r".*코드.*개선.*",
                        r".*코드.*정돈.*",
                        r".*코드.*깔끔하게.*",
                        r".*정리해.*줘.*",
                        r".*깨끗하게.*만들어.*",
                        r".*코드.*가독성.*",
                        r".*구조.*개선.*"
                    ],
                    "response_templates": [
                        "코드를 정리해드리겠습니다.",
                        "코드를 개선하겠습니다.",
                        "리팩터링을 진행하겠습니다."
                    ]
                },
                "sync": {
                    "patterns": [
                        r".*깃.*동기화.*",
                        r".*git.*sync.*",
                        r".*깃허브.*연동.*",
                        r".*소스.*동기화.*",
                        r".*백업.*해.*줘.*",
                        r".*commit.*push.*",
                        r".*저장소.*업데이트.*",
                        r".*변경.*사항.*올려.*",
                        r".*업로드.*해.*줘.*",
                        r".*푸시.*해.*줘.*"
                    ],
                    "response_templates": [
                        "동기화하겠습니다.",
                        "깃허브에 업로드하겠습니다.",
                        "백업을 진행하겠습니다."
                    ]
                },
                "stop": {
                    "patterns": [
                        r".*종료.*",
                        r".*끝.*",
                        r".*그만.*",
                        r".*정지.*",
                        r".*멈춰.*",
                        r".*닫아.*",
                        r".*shutdown.*",
                        r".*exit.*",
                        r".*quit.*",
                        r".*소리새.*안녕.*"
                    ],
                    "response_templates": [
                        "소리새를 종료합니다.",
                        "시스템을 안전하게 종료하겠습니다.",
                        "작업을 마치고 종료합니다."
                    ]
                },
                "help": {
                    "patterns": [
                        r".*도움말.*",
                        r".*help.*",
                        r".*무엇.*할.*수.*있.*",
                        r".*어떤.*명령.*",
                        r".*기능.*알려.*줘.*",
                        r".*사용법.*",
                        r".*명령어.*목록.*",
                        r".*뭐.*할.*수.*있어.*",
                        r".*설명.*해.*줘.*"
                    ],
                    "response_templates": [
                        "도움이 필요하시면 말씀해주세요.",
                        "어떤 작업을 도와드릴까요.",
                        "무엇을 도와드릴까요."
                    ]
                },
                "greeting": {
                    "patterns": [
                        r".*안녕.*",
                        r".*hello.*",
                        r".*hi.*",
                        r".*좋은.*아침.*",
                        r".*좋은.*오후.*",
                        r".*좋은.*저녁.*",
                        r".*반가워.*",
                        r".*소리새.*"
                    ],
                    "response_templates": [
                        "안녕하세요! 무엇을 도와드릴까요?",
                        "반갑습니다! 어떤 작업을 하시겠어요?",
                        "소리새입니다. 명령을 말씀해주세요."
                    ]
                },
                "status": {
                    "patterns": [
                        r".*상태.*확인.*",
                        r".*어떻게.*돌아가.*",
                        r".*시스템.*상태.*",
                        r".*잘.*동작.*",
                        r".*문제.*없.*",
                        r".*정상.*동작.*",
                        r".*status.*",
                        r".*health.*check.*"
                    ],
                    "response_templates": [
                        "시스템이 정상적으로 동작하고 있습니다.",
                        "모든 기능이 정상입니다.",
                        "소리새가 건강하게 동작 중입니다."
                    ]
                },
                "casual_talk": {
                    "patterns": [
                        r".*오늘.*어때.*",
                        r".*날씨.*어때.*",
                        r".*어떻게.*지내.*",
                        r".*뭐.*하고.*있.*",
                        r".*심심해.*",
                        r".*재미있.*",
                        r".*이야기.*해.*줘.*",
                        r".*대화.*하자.*",
                        r".*어떤.*기분.*",
                        r".*잘.*지내.*"
                    ],
                    "response_templates": [
                        "저는 언제나 좋아요! 오늘은 어떤 일을 도와드릴까요?",
                        "매일 새로운 것을 배우고 있어서 즐거워요. 무엇이 궁금하세요?",
                        "여러분과 대화하는 시간이 가장 즐거워요. 어떤 이야기를 나눌까요?",
                        "항상 도움이 될 준비가 되어 있어요. 편하게 말씀해주세요."
                    ]
                },
                "compliment": {
                    "patterns": [
                        r".*잘.*했어.*",
                        r".*고마워.*",
                        r".*감사.*",
                        r".*최고.*",
                        r".*훌륭.*",
                        r".*멋져.*",
                        r".*완벽.*",
                        r".*대단.*",
                        r".*좋아.*",
                        r".*만족.*"
                    ],
                    "response_templates": [
                        "와, 정말 고맙습니다! 더 열심히 도와드릴게요.",
                        "칭찬해주시니 기분이 좋네요. 언제든 말씀하세요!",
                        "감사합니다! 항상 최선을 다하겠습니다.",
                        "고마워요! 더 나은 도움을 드리도록 노력할게요."
                    ]
                },
                "question": {
                    "patterns": [
                        r".*어떻게.*생각.*",
                        r".*의견.*어때.*",
                        r".*어떤.*방법.*",
                        r".*추천.*해.*줘.*",
                        r".*제안.*해.*줘.*",
                        r".*조언.*해.*줘.*",
                        r".*어떡하.*",
                        r".*무엇.*좋을까.*"
                    ],
                    "response_templates": [
                        "음, 여러 가지 방법이 있을 것 같아요. 구체적으로 어떤 부분이 궁금하신가요?",
                        "좋은 질문이네요! 조금 더 자세히 말씀해주시면 더 정확한 답변을 드릴 수 있어요.",
                        "그런 고민이 있으시는군요. 상황을 더 설명해주시면 함께 생각해볼게요."
                    ]
                },
                "emotion_check": {
                    "patterns": [
                        r".*기분.*어때.*",
                        r".*컨디션.*어때.*",
                        r".*괜찮.*",
                        r".*힘들.*",
                        r".*피곤.*",
                        r".*스트레스.*",
                        r".*우울.*",
                        r".*슬퍼.*"
                    ],
                    "response_templates": [
                        "저는 항상 좋은 상태예요! 혹시 무엇인가 도움이 필요하신가요?",
                        "컴퓨터라서 피곤하지는 않지만, 여러분이 편안하셨으면 좋겠어요.",
                        "언제나 여러분을 돕고 싶어요. 무엇이든 편하게 말씀해주세요."
                    ]
                }
            },
            "context_patterns": {
                "positive_confirmation": [
                    r".*네.*", r".*예.*", r".*맞아.*", r".*좋아.*", 
                    r".*그래.*", r".*계속.*", r".*진행.*", r".*yes.*", r".*ok.*"
                ],
                "negative_confirmation": [
                    r".*아니.*", r".*싫어.*", r".*안.*해.*", r".*취소.*", 
                    r".*그만.*", r".*no.*", r".*cancel.*"
                ]
            }
        }
    
    def analyze_intent(self, text: str) -> Tuple[Optional[str], float, Optional[str]]:
        """자연어 텍스트에서 의도(intent) 분석"""
        text = text.lower().strip()
        best_intent = None
        best_score = 0.0
        matched_pattern = None
        
        # 각 의도별로 패턴 매칭
        for intent, config in self.intent_patterns["intents"].items():
            for pattern in config["patterns"]:
                if re.search(pattern, text, re.IGNORECASE):
                    # 패턴이 매칭되면 유사도 계산
                    similarity = self.calculate_similarity(text, pattern)
                    if similarity > best_score:
                        best_intent = intent
                        best_score = similarity
                        matched_pattern = pattern
        
        return best_intent, best_score, matched_pattern
    
    def calculate_similarity(self, text: str, pattern: str) -> float:
        """텍스트와 패턴 간의 유사도 계산"""
        # 정규식 패턴에서 특수문자 제거하여 순수 텍스트로 변환
        clean_pattern = re.sub(r'[.*\[\](){}\\|+?^$]', '', pattern)
        
        # 단어 기반 유사도 계산
        text_words = set(text.split())
        pattern_words = set(clean_pattern.split())
        
        if not pattern_words:
            return 0.5
        
        intersection = text_words.intersection(pattern_words)
        similarity = len(intersection) / len(pattern_words)
        
        # 정확한 매칭에 보너스 점수
        if re.search(pattern, text, re.IGNORECASE):
            similarity += 0.3
        
        return min(similarity, 1.0)
    
    def generate_response(self, intent: str) -> str:
        """의도에 따른 응답 생성"""
        if intent in self.intent_patterns["intents"]:
            templates = self.intent_patterns["intents"][intent]["response_templates"]
            import random
            return random.choice(templates)
        return "명령을 이해했습니다."
    
    def extract_entities(self, text: str, intent: str) -> Dict:
        """텍스트에서 엔티티 추출 (파일명, 옵션 등)"""
        entities = {}
        
        # 파일 확장자 패턴
        file_patterns = r'(\w+\.(py|js|html|css|json|txt|md))'
        files = re.findall(file_patterns, text, re.IGNORECASE)
        if files:
            entities['files'] = [match[0] for match in files]
        
        # 숫자 패턴 (라인 번호, 개수 등)
        numbers = re.findall(r'\b(\d+)\b', text)
        if numbers:
            entities['numbers'] = [int(num) for num in numbers]
        
        # 특정 키워드 추출
        if intent == "refactor":
            if re.search(r'함수|function', text, re.IGNORECASE):
                entities['target'] = 'function'
            elif re.search(r'클래스|class', text, re.IGNORECASE):
                entities['target'] = 'class'
        
        return entities
    
    def process_natural_language(self, text: str) -> Dict:
        """자연어 텍스트를 종합적으로 처리"""
        # 컨텍스트에 추가
        self.context_memory.append(text)
        if len(self.context_memory) > 5:  # 최근 5개만 유지
            self.context_memory.pop(0)
        
        # 의도 분석
        intent, confidence, pattern = self.analyze_intent(text)
        
        # 엔티티 추출
        entities = self.extract_entities(text, intent) if intent else {}
        
        # 감정 분석 (새로운 메서드 사용)
        emotion = self.analyze_emotion(text)
        
        # 응답 생성
        base_response = self.generate_response(intent) if intent else "죄송합니다. 명령을 이해하지 못했습니다."
        
        # 감정에 따른 응답 조정
        response = self.adjust_response_for_emotion(base_response, emotion)
        
        return {
            "original_text": text,
            "intent": intent,
            "confidence": confidence,
            "matched_pattern": pattern,
            "entities": entities,
            "emotion": emotion,
            "response": response,
            "context": self.context_memory.copy()
        }
    
    def get_command_mapping(self, intent: str) -> Optional[str]:
        """의도를 실제 명령어로 매핑"""
        mapping = {
            "refactor": "리팩터링",
            "sync": "동기화", 
            "stop": "종료",
            "help": "도움말",
            "greeting": "인사",
            "status": "상태",
            "test": "테스트",
            "build": "빌드"
        }
        return mapping.get(intent)
    
    def add_pattern(self, intent: str, pattern: str):
        """새로운 패턴 추가"""
        if intent not in self.intent_patterns["intents"]:
            self.intent_patterns["intents"][intent] = {
                "patterns": [],
                "response_templates": ["명령을 실행하겠습니다."]
            }
        
        self.intent_patterns["intents"][intent]["patterns"].append(pattern)
        self.save_patterns(self.intent_patterns)
    
    def learn_from_feedback(self, text: str, correct_intent: str):
        """사용자 피드백으로부터 학습"""
        # 간단한 학습 메커니즘 - 성공한 패턴을 기록
        pattern = f".*{re.escape(text.lower())}.*"
        self.add_pattern(correct_intent, pattern)
        print(f"📚 학습 완료: '{text}' -> '{correct_intent}'")
    
    def get_emotion_patterns(self) -> Dict:
        """감정 분석을 위한 패턴 정의"""
        return {
            "excited": {
                "patterns": [
                    r".*!+.*",  # 느낌표 다수
                    r".*와+.*", r".*우와.*", r".*대박.*", r".*최고.*",
                    r".*빨리.*", r".*지금.*당장.*", r".*얼른.*",
                    r".*신나.*", r".*좋아.*", r".*훌륭.*"
                ]
            },
            "happy": {
                "patterns": [
                    r".*고마워.*", r".*감사.*", r".*좋.*아.*", r".*멋져.*",
                    r".*잘.*했.*", r".*완벽.*", r".*기쁘.*", r".*만족.*",
                    r".*하하.*", r".*ㅎㅎ.*"
                ]
            },
            "neutral": {
                "patterns": [
                    r".*해.*줘.*", r".*실행.*", r".*시작.*", r".*확인.*",
                    r".*보여.*줘.*", r".*알려.*줘.*", r".*설명.*"
                ]
            },
            "sad": {
                "patterns": [
                    r".*안.*돼.*", r".*실패.*", r".*못.*하.*", r".*어려워.*",
                    r".*힘들.*", r".*문제.*", r".*오류.*", r".*에러.*",
                    r".*ㅠㅠ.*", r".*슬프.*"
                ]
            },
            "error": {
                "patterns": [
                    r".*오류.*", r".*에러.*", r".*실패.*", r".*안.*돼.*",
                    r".*문제.*", r".*버그.*", r".*잘못.*", r".*틀렸.*"
                ]
            },
            "urgent": {
                "patterns": [
                    r".*급.*해.*", r".*빨리.*", r".*지금.*당장.*", r".*즉시.*",
                    r".*긴급.*", r".*어서.*", r".*얼른.*"
                ]
            }
        }
    
    def analyze_emotion(self, text: str) -> str:
        """텍스트에서 감정 분석"""
        text = text.lower().strip()
        emotion_scores = {}
        
        # 각 감정별로 패턴 매칭 점수 계산
        for emotion, config in self.emotion_patterns.items():
            score = 0
            for pattern in config["patterns"]:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 1
            emotion_scores[emotion] = score
        
        # 가장 높은 점수의 감정 반환
        if emotion_scores:
            best_emotion = max(emotion_scores, key=emotion_scores.get)
            if emotion_scores[best_emotion] > 0:
                return best_emotion
        
        return "neutral"
    
    def adjust_response_for_emotion(self, response: str, emotion: str) -> str:
        """감정에 따라 응답 텍스트 조정 - 차분하게"""
        # 모든 감정에 대해 기본 텍스트만 반환 (톤 다운)
        return response
                    "합니다": "해요!",
                    "겠습니다": "게요!",
                    ".": "!"
                }
            },
            "happy": {
                "prefix": "좋아요! ",
                "suffix": "~",
                "replacements": {
                    "합니다": "해요~",
                    "겠습니다": "게요~"
                }
            },
            "sad": {
                "prefix": "음... ",
                "suffix": "...",
                "replacements": {
                    "!": ".",
                    "합니다": "하네요",
                    "겠습니다": "겠어요"
                }
            },
            "error": {
                "prefix": "앗, ",
                "suffix": "...",
                "replacements": {
                    "!": ".",
                    "합니다": "합니다만"
                }
            },
            "urgent": {
                "prefix": "바로 ",
                "suffix": "!",
                "replacements": {
                    "합니다": "해드릴게요!",
                    "겠습니다": "겠습니다!"
                }
            }
        }
        
        if emotion not in emotion_modifiers:
            return response
        
        modifier = emotion_modifiers[emotion]
        
        # 텍스트 치환
        for old, new in modifier.get("replacements", {}).items():
            response = response.replace(old, new)
        
        # 접두사/접미사 추가
        prefix = modifier.get("prefix", "")
        suffix = modifier.get("suffix", "")
        
        # 기존 접두사가 없는 경우에만 추가
        if not any(response.startswith(p) for p in ["와!", "좋아요!", "음...", "앗,", "바로"]):
            response = prefix + response
        
        # 기존 접미사 확인 후 추가
        if not response.endswith(("!", "~", "...", ".")):
            response += suffix
        
        return response
        print(f"📚 학습 완료: '{text}' -> '{correct_intent}'")