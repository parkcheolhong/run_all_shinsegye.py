"""
기억의 궁전 시스템 (Memory Palace System)
사용자와의 모든 대화를 구조화하여 장기 기억으로 저장
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import hashlib

class MemoryPalace:
    def __init__(self, memory_file="memories/sorisay_memories.json"):
        self.memory_file = memory_file
        self.memories = self.load_memories()
        self.conversation_context = []
        
        # 기억 카테고리
        self.memory_categories = {
            "personal": [],      # 사용자 개인 정보
            "preferences": [],   # 선호도
            "projects": [],      # 프로젝트 관련
            "emotions": [],      # 감정 상태 기록
            "achievements": [],  # 성취 기록
            "failures": [],      # 실패 학습
            "patterns": []       # 행동 패턴
        }
    
    def load_memories(self) -> Dict:
        """기억 파일 로드"""
        try:
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"기억 로드 실패: {e}")
        
        return {
            "conversations": [],
            "user_profile": {},
            "emotional_history": [],
            "learning_moments": [],
            "creative_collaborations": []
        }
    
    def save_memories(self):
        """기억 파일 저장"""
        try:
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memories, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"기억 저장 실패: {e}")
    
    def remember_conversation(self, user_input: str, ai_response: str, emotion: str = "neutral"):
        """대화 내용을 기억에 저장"""
        memory = {
            "id": hashlib.md5(f"{datetime.now().isoformat()}{user_input}".encode()).hexdigest()[:8],
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "ai_response": ai_response,
            "emotion_detected": emotion,
            "context_tags": self.extract_context_tags(user_input),
            "importance_score": self.calculate_importance(user_input)
        }
        
        self.memories["conversations"].append(memory)
        
        # 중요한 정보는 사용자 프로필에 추가
        self.update_user_profile(user_input)
        
        # 메모리 정리 (1000개 이상 시 오래된 것 삭제)
        if len(self.memories["conversations"]) > 1000:
            self.memories["conversations"] = self.memories["conversations"][-1000:]
        
        self.save_memories()
    
    def extract_context_tags(self, text: str) -> List[str]:
        """텍스트에서 컨텍스트 태그 추출"""
        tags = []
        
        # 기술 관련 태그
        tech_keywords = ["코딩", "프로그래밍", "개발", "AI", "머신러닝", "웹", "앱"]
        personal_keywords = ["이름", "나이", "직업", "취미", "좋아하는", "싫어하는"]
        project_keywords = ["프로젝트", "작업", "일", "업무", "계획", "목표"]
        
        text_lower = text.lower()
        
        for keyword in tech_keywords:
            if keyword in text_lower:
                tags.append("tech")
                break
        
        for keyword in personal_keywords:
            if keyword in text_lower:
                tags.append("personal")
                break
                
        for keyword in project_keywords:
            if keyword in text_lower:
                tags.append("project")
                break
        
        return tags
    
    def calculate_importance(self, text: str) -> int:
        """대화의 중요도 계산 (1-10)"""
        importance = 1
        
        # 개인정보 언급 시 중요도 높음
        if any(keyword in text.lower() for keyword in ["이름", "나이", "직업", "가족"]):
            importance += 3
        
        # 목표나 계획 언급 시 중요도 높음
        if any(keyword in text.lower() for keyword in ["목표", "계획", "하고싶", "배우고싶"]):
            importance += 2
        
        # 감정 표현 시 중요도 증가
        if any(keyword in text.lower() for keyword in ["기쁘", "슬프", "화나", "걱정", "행복"]):
            importance += 1
        
        return min(importance, 10)
    
    def update_user_profile(self, text: str):
        """사용자 프로필 업데이트"""
        text_lower = text.lower()
        
        # 이름 추출
        if "제 이름은" in text_lower or "내 이름은" in text_lower:
            # 간단한 이름 추출 로직
            words = text.split()
            for i, word in enumerate(words):
                if word in ["이름은", "이름이"]:
                    if i + 1 < len(words):
                        self.memories["user_profile"]["name"] = words[i + 1]
        
        # 선호도 추출
        if "좋아해" in text_lower or "좋아하는" in text_lower:
            preferences = self.memories["user_profile"].get("likes", [])
            preferences.append(text)
            self.memories["user_profile"]["likes"] = preferences[-10:]  # 최근 10개만 유지
    
    def recall_memories(self, query: str, limit: int = 5) -> List[Dict]:
        """관련 기억 검색"""
        relevant_memories = []
        query_lower = query.lower()
        
        for memory in self.memories["conversations"]:
            score = 0
            
            # 텍스트 유사도 기반 점수
            if query_lower in memory["user_input"].lower():
                score += 3
            if query_lower in memory["ai_response"].lower():
                score += 2
            
            # 태그 매칭 점수
            query_tags = self.extract_context_tags(query)
            common_tags = set(query_tags) & set(memory["context_tags"])
            score += len(common_tags)
            
            # 중요도 점수
            score += memory["importance_score"] * 0.1
            
            if score > 0:
                memory_with_score = memory.copy()
                memory_with_score["relevance_score"] = score
                relevant_memories.append(memory_with_score)
        
        # 점수순으로 정렬하여 상위 결과 반환
        relevant_memories.sort(key=lambda x: x["relevance_score"], reverse=True)
        return relevant_memories[:limit]
    
    def get_personality_insights(self) -> str:
        """사용자 성격 인사이트 생성"""
        if not self.memories["conversations"]:
            return "아직 대화가 충분하지 않아 성격을 파악하기 어려워요."
        
        # 감정 패턴 분석
        emotions = [conv["emotion_detected"] for conv in self.memories["conversations"]]
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
        
        # 관심사 분석
        tech_talks = len([conv for conv in self.memories["conversations"] if "tech" in conv["context_tags"]])
        personal_talks = len([conv for conv in self.memories["conversations"] if "personal" in conv["context_tags"]])
        
        insights = f"""
🧠 성격 인사이트:
• 주된 감정: {dominant_emotion}
• 기술적 대화: {tech_talks}번
• 개인적 대화: {personal_talks}번
• 총 대화 횟수: {len(self.memories['conversations'])}번

💡 특징: {"기술에 관심이 많으시네요!" if tech_talks > personal_talks else "개인적인 이야기를 좋아하시는군요!"}
        """.strip()
        
        return insights