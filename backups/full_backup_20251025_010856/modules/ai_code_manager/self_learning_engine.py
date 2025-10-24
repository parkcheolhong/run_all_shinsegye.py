import requests
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import re
from urllib.parse import quote

class SelfLearningEngine:
    """자가 학습 및 진화 엔진"""
    
    def __init__(self, knowledge_path="data/knowledge_base.json"):
        self.knowledge_path = knowledge_path
        self.knowledge_base = self.load_knowledge()
        self.learning_log = []
        self.improvement_suggestions = []
        
    def load_knowledge(self) -> Dict:
        """지식 베이스 로드"""
        try:
            if os.path.exists(self.knowledge_path):
                with open(self.knowledge_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.create_initial_knowledge()
        except Exception as e:
            print(f"⚠ 지식 베이스 로드 실패: {e}")
            return self.create_initial_knowledge()
    
    def create_initial_knowledge(self) -> Dict:
        """초기 지식 베이스 생성"""
        return {
            "learned_patterns": {},
            "user_preferences": {},
            "successful_responses": {},
            "failed_responses": {},
            "web_search_cache": {},
            "improvement_history": [],
            "capabilities": [
                "음성 인식", "자연어 처리", "코드 관리", 
                "웹 검색", "자가 학습", "기능 확장"
            ]
        }
    
    def save_knowledge(self):
        """지식 베이스 저장"""
        try:
            os.makedirs(os.path.dirname(self.knowledge_path), exist_ok=True)
            with open(self.knowledge_path, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠ 지식 베이스 저장 실패: {e}")
    
    def web_search(self, query: str, max_results: int = 3) -> List[Dict]:
        """웹 검색 수행"""
        try:
            # 캐시된 결과가 있는지 확인
            cache_key = f"search_{hash(query)}"
            if cache_key in self.knowledge_base["web_search_cache"]:
                cached_result = self.knowledge_base["web_search_cache"][cache_key]
                # 24시간 이내 캐시만 사용
                if (datetime.now() - datetime.fromisoformat(cached_result["timestamp"])).hours < 24:
                    return cached_result["results"]
            
            # DuckDuckGo Instant Answer API 사용 (무료)
            url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(url, timeout=10)
            
            results = []
            if response.status_code == 200:
                data = response.json()
                
                # Abstract 정보
                if data.get("Abstract"):
                    results.append({
                        "title": data.get("AbstractText", "")[:100],
                        "content": data.get("Abstract", ""),
                        "source": data.get("AbstractURL", ""),
                        "type": "abstract"
                    })
                
                # Related Topics
                for topic in data.get("RelatedTopics", [])[:max_results-1]:
                    if isinstance(topic, dict) and topic.get("Text"):
                        results.append({
                            "title": topic.get("Text", "")[:100],
                            "content": topic.get("Text", ""),
                            "source": topic.get("FirstURL", ""),
                            "type": "related"
                        })
            
            # 결과 캐시
            self.knowledge_base["web_search_cache"][cache_key] = {
                "results": results,
                "timestamp": datetime.now().isoformat()
            }
            self.save_knowledge()
            
            return results
            
        except Exception as e:
            print(f"⚠ 웹 검색 실패: {e}")
            return [{"title": "검색 실패", "content": f"웹 검색 중 오류가 발생했습니다: {str(e)}", "source": "", "type": "error"}]
    
    def learn_from_interaction(self, user_input: str, response: str, success: bool):
        """사용자 상호작용에서 학습"""
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "response": response,
            "success": success
        }
        
        self.learning_log.append(learning_entry)
        
        if success:
            # 성공한 응답 패턴 저장
            pattern_key = self.extract_pattern(user_input)
            if pattern_key not in self.knowledge_base["successful_responses"]:
                self.knowledge_base["successful_responses"][pattern_key] = []
            self.knowledge_base["successful_responses"][pattern_key].append(response)
        else:
            # 실패한 응답 분석
            pattern_key = self.extract_pattern(user_input)
            if pattern_key not in self.knowledge_base["failed_responses"]:
                self.knowledge_base["failed_responses"][pattern_key] = []
            self.knowledge_base["failed_responses"][pattern_key].append(response)
            
            # 개선 제안 생성
            self.suggest_improvement(user_input, response)
        
        self.save_knowledge()
    
    def extract_pattern(self, text: str) -> str:
        """텍스트에서 패턴 추출"""
        # 키워드 기반 패턴 추출
        keywords = re.findall(r'\b\w+\b', text.lower())
        return "_".join(sorted(set(keywords))[:5])  # 상위 5개 키워드
    
    def suggest_improvement(self, user_input: str, failed_response: str):
        """개선 제안 생성"""
        suggestion = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "failed_response": failed_response,
            "suggestion": f"'{user_input}' 패턴에 대한 더 나은 응답 방법을 학습해야 합니다.",
            "priority": "medium"
        }
        
        # 웹 검색으로 관련 정보 찾기
        search_results = self.web_search(user_input)
        if search_results:
            suggestion["web_insights"] = search_results
            suggestion["suggestion"] += f" 웹 검색 결과 {len(search_results)}개의 관련 정보를 찾았습니다."
        
        self.improvement_suggestions.append(suggestion)
        
    def analyze_and_improve(self) -> List[str]:
        """분석 후 자가 개선"""
        improvements = []
        
        # 실패 패턴 분석
        for pattern, failures in self.knowledge_base["failed_responses"].items():
            if len(failures) >= 3:  # 3번 이상 실패한 패턴
                improvements.append(f"패턴 '{pattern}'에 대한 응답 개선 필요")
                
                # 웹에서 관련 정보 검색
                search_query = pattern.replace("_", " ")
                search_results = self.web_search(search_query)
                
                if search_results:
                    # 새로운 응답 패턴 생성
                    new_response = self.generate_improved_response(search_results)
                    if new_response:
                        if pattern not in self.knowledge_base["learned_patterns"]:
                            self.knowledge_base["learned_patterns"][pattern] = []
                        self.knowledge_base["learned_patterns"][pattern].append(new_response)
                        improvements.append(f"패턴 '{pattern}'에 대한 새로운 응답 생성: {new_response[:50]}...")
        
        # 새로운 기능 제안
        self.suggest_new_features()
        
        self.save_knowledge()
        return improvements
    
    def generate_improved_response(self, search_results: List[Dict]) -> Optional[str]:
        """검색 결과를 바탕으로 개선된 응답 생성"""
        if not search_results:
            return None
        
        # 검색 결과에서 유용한 정보 추출
        content_parts = []
        for result in search_results[:2]:  # 상위 2개 결과만 사용
            if result.get("content") and len(result["content"]) > 20:
                content_parts.append(result["content"][:200])
        
        if content_parts:
            combined_content = " ".join(content_parts)
            return f"검색 결과를 바탕으로 말씀드리면, {combined_content[:300]}... 더 자세한 정보가 필요하시면 말씀해주세요."
        
        return None
    
    def suggest_new_features(self):
        """새로운 기능 제안"""
        current_time = datetime.now()
        
        # 사용 패턴 분석
        if len(self.learning_log) > 50:  # 충분한 데이터가 있을 때
            recent_interactions = [log for log in self.learning_log 
                                 if (current_time - datetime.fromisoformat(log["timestamp"])).days <= 7]
            
            # 자주 실패하는 요청 타입 분석
            failed_interactions = [log for log in recent_interactions if not log["success"]]
            
            if len(failed_interactions) > 10:
                feature_suggestion = {
                    "timestamp": current_time.isoformat(),
                    "type": "new_feature",
                    "description": "사용자가 자주 요청하지만 처리하지 못하는 기능들에 대한 새로운 플러그인 개발 필요",
                    "priority": "high",
                    "details": f"최근 7일간 {len(failed_interactions)}개의 실패한 요청 분석됨"
                }
                
                self.improvement_suggestions.append(feature_suggestion)
    
    def get_learning_summary(self) -> Dict:
        """학습 현황 요약"""
        return {
            "총_학습_횟수": len(self.learning_log),
            "성공_응답_패턴": len(self.knowledge_base["successful_responses"]),
            "실패_응답_패턴": len(self.knowledge_base["failed_responses"]),
            "학습된_새_패턴": len(self.knowledge_base["learned_patterns"]),
            "개선_제안": len(self.improvement_suggestions),
            "웹_검색_캐시": len(self.knowledge_base["web_search_cache"]),
            "현재_능력": self.knowledge_base["capabilities"]
        }
    
    def smart_response(self, user_input: str) -> Optional[str]:
        """학습된 지식을 바탕으로 스마트 응답 생성"""
        pattern = self.extract_pattern(user_input)
        
        # 학습된 패턴이 있는지 확인
        if pattern in self.knowledge_base["learned_patterns"]:
            responses = self.knowledge_base["learned_patterns"][pattern]
            if responses:
                return responses[-1]  # 가장 최근 학습된 응답
        
        # 성공한 응답 패턴 확인
        if pattern in self.knowledge_base["successful_responses"]:
            responses = self.knowledge_base["successful_responses"][pattern]
            if responses:
                return responses[-1]  # 가장 최근 성공한 응답
        
        # 웹 검색을 통한 새로운 응답 생성
        if len(user_input.split()) > 2:  # 충분히 구체적인 질문
            search_results = self.web_search(user_input)
            if search_results:
                return self.generate_improved_response(search_results)
        
        return None