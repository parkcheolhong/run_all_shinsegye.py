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
                        "코드 리팩터링을 시작합니다.",
                        "코드를 정리하고 개선하겠습니다.",
                        "코드 구조를 개선하겠습니다."
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
                        "깃허브와 동기화를 시작합니다.",
                        "소스 코드를 동기화하겠습니다.",
                        "변경사항을 깃허브에 업로드하겠습니다."
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
                        "소리새의 기능들을 설명해드리겠습니다.",
                        "사용 가능한 명령어들을 알려드리겠습니다.",
                        "도움말을 제공하겠습니다."
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
        
        # 감정 분석
        emotion = self.analyze_emotion(text, intent)
        
        # 응답 생성
        response = self.generate_response(intent) if intent else "죄송합니다. 명령을 이해하지 못했습니다."
        
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
    
    def analyze_emotion(self, text: str, intent: str) -> str:
        """텍스트와 의도에서 감정 분석"""
        text_lower = text.lower()
        
        # 긍정적 표현
        positive_patterns = [
            r'좋아', r'감사', r'고마워', r'훌륭', r'완벽', r'최고', r'멋져'
        ]
        
        # 부정적 표현  
        negative_patterns = [
            r'싫어', r'안돼', r'문제', r'오류', r'실패', r'안좋', r'나빠'
        ]
        
        # 급한/흥분 표현
        excited_patterns = [
            r'빨리', r'급해', r'당장', r'지금', r'!!!', r'!!'
        ]
        
        # 패턴 매칭으로 감정 판단
        for pattern in excited_patterns:
            if re.search(pattern, text_lower):
                return "excited"
                
        for pattern in positive_patterns:
            if re.search(pattern, text_lower):
                return "happy"
                
        for pattern in negative_patterns:
            if re.search(pattern, text_lower):
                return "sad"
        
        # 의도에 따른 기본 감정
        intent_emotions = {
            "greeting": "happy",
            "help": "friendly", 
            "stop": "neutral",
            "refactor": "success",
            "sync": "success",
            "test": "neutral",
            "build": "success",
            "status": "neutral"
        }
        
        return intent_emotions.get(intent, "neutral")
    
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