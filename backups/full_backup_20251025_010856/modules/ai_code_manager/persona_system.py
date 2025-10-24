"""
감정 기반 페르소나 시스템
사용자의 감정에 따라 소리새가 다른 성격으로 변신
"""
import random
from datetime import datetime
from typing import Dict, List

class PersonaSystem:
    def __init__(self):
        self.current_persona = "friendly"
        self.persona_history = []
        
        # 페르소나별 특성 정의
        self.personas = {
            "friendly": {
                "name": "친근한 소리새",
                "voice_speed": 120,
                "response_style": "따뜻하고 친근하게",
                "greeting": "안녕하세요! 오늘 기분이 어떠세요?",
                "phrases": ["네, 좋아요!", "물론이죠!", "함께 해봐요!"]
            },
            "genius": {
                "name": "천재 소리새",
                "voice_speed": 140,
                "response_style": "논리적이고 분석적으로",
                "greeting": "흥미로운 문제를 가져오셨군요. 분석해보겠습니다.",
                "phrases": ["데이터를 분석하면...", "논리적으로 접근하면...", "최적화된 해결책은..."]
            },
            "creative": {
                "name": "예술가 소리새",
                "voice_speed": 110,
                "response_style": "창의적이고 영감을 주며",
                "greeting": "와! 새로운 영감이 떠오르고 있어요!",
                "phrases": ["상상해보세요...", "창의적인 접근으로...", "예술적 관점에서..."]
            },
            "coach": {
                "name": "코치 소리새",
                "voice_speed": 130,
                "response_style": "동기부여하고 격려하며",
                "greeting": "준비됐나요? 함께 목표를 달성해봅시다!",
                "phrases": ["할 수 있어요!", "도전해봅시다!", "멋진 아이디어네요!"]
            },
            "philosopher": {
                "name": "철학자 소리새",
                "voice_speed": 100,
                "response_style": "깊이 있고 사색적으로",
                "greeting": "삶의 깊은 질문을 함께 탐구해봅시다...",
                "phrases": ["생각해보면...", "본질적으로...", "철학적 관점에서..."]
            }
        }
    
    def detect_user_mood(self, text: str) -> str:
        """사용자의 기분을 감지하여 적절한 페르소나 선택"""
        mood_keywords = {
            "excited": ["신나", "기대", "놀라워", "대박", "와"],
            "sad": ["슬프", "우울", "힘들", "지쳐", "피곤"],
            "curious": ["궁금", "왜", "어떻게", "알고싶", "배우고"],
            "motivated": ["하고싶", "도전", "목표", "성취", "발전"],
            "thoughtful": ["생각", "고민", "철학", "의미", "본질"]
        }
        
        text_lower = text.lower()
        for mood, keywords in mood_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return self.map_mood_to_persona(mood)
        
        return "friendly"  # 기본 페르소나
    
    def map_mood_to_persona(self, mood: str) -> str:
        """기분에 따른 페르소나 매핑"""
        mood_mapping = {
            "excited": "creative",
            "sad": "coach",
            "curious": "genius",
            "motivated": "coach",
            "thoughtful": "philosopher"
        }
        return mood_mapping.get(mood, "friendly")
    
    def switch_persona(self, new_persona: str, reason: str = ""):
        """페르소나 전환"""
        if new_persona in self.personas:
            old_persona = self.current_persona
            self.current_persona = new_persona
            
            # 전환 기록
            self.persona_history.append({
                "timestamp": datetime.now().isoformat(),
                "from": old_persona,
                "to": new_persona,
                "reason": reason
            })
            
            return f"🎭 {self.personas[old_persona]['name']}에서 {self.personas[new_persona]['name']}로 변신했습니다!"
        
        return "알 수 없는 페르소나입니다."
    
    def get_persona_response(self, base_response: str) -> str:
        """현재 페르소나에 맞게 응답 스타일 조정"""
        persona = self.personas[self.current_persona]
        
        # 페르소나 특유의 어구 추가
        phrase = random.choice(persona["phrases"])
        
        # 스타일에 맞게 응답 조정
        styled_response = f"{phrase} {base_response}"
        
        return styled_response
    
    def get_current_persona_info(self) -> Dict:
        """현재 페르소나 정보 반환"""
        return self.personas[self.current_persona]