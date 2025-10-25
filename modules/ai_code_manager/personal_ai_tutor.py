"""
🎓 개인 맞춤 AI 튜터 시스템
사용자의 학습 패턴과 코딩 스타일을 분석해서 맞춤형 교육 제공
"""

import json
import os
from datetime import datetime, timedelta
import random
from typing import Dict, List, Any

class PersonalAITutor:
    def __init__(self):
        self.user_profile_file = "data/user_learning_profile.json"
        self.learning_sessions = []
        self.user_profile = self.load_user_profile()
        self.coding_patterns = {}
        self.weakness_areas = []
        self.strength_areas = []
        
    def load_user_profile(self):
        """사용자 학습 프로필 로드"""
        if os.path.exists(self.user_profile_file):
            try:
                with open(self.user_profile_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️ 사용자 프로필 로드 실패: {e}")
                pass
        
        # 기본 프로필 생성
        return {
            "learning_style": "visual",  # visual, auditory, kinesthetic
            "skill_level": "beginner",   # beginner, intermediate, advanced
            "preferred_languages": ["python"],
            "learning_pace": "normal",   # slow, normal, fast
            "interests": ["web_development", "ai", "data_science"],
            "session_count": 0,
            "total_learning_time": 0,
            "last_session": None,
            "achievements": [],
            "current_goals": []
        }
    
    def save_user_profile(self):
        """사용자 프로필 저장"""
        os.makedirs(os.path.dirname(self.user_profile_file), exist_ok=True)
        with open(self.user_profile_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_profile, f, ensure_ascii=False, indent=2)
    
    def analyze_coding_pattern(self, code_snippet: str, language: str):
        """코딩 패턴 분석"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "language": language,
            "code_length": len(code_snippet),
            "complexity_indicators": {
                "functions": code_snippet.count("def "),
                "classes": code_snippet.count("class "),
                "loops": code_snippet.count("for ") + code_snippet.count("while "),
                "conditions": code_snippet.count("if ") + code_snippet.count("elif "),
                "comments": code_snippet.count("#") + code_snippet.count('"""'),
            },
            "style_indicators": {
                "has_docstrings": '"""' in code_snippet,
                "uses_type_hints": ":" in code_snippet and "->" in code_snippet,
                "proper_spacing": "  " in code_snippet,
                "meaningful_names": len([word for word in code_snippet.split() if len(word) > 3]) > 0
            }
        }
        
        # 패턴 데이터베이스에 추가
        if language not in self.coding_patterns:
            self.coding_patterns[language] = []
        self.coding_patterns[language].append(analysis)
        
        return self.generate_personalized_feedback(analysis)
    
    def generate_personalized_feedback(self, analysis: Dict):
        """개인 맞춤 피드백 생성"""
        feedback = []
        style = analysis["style_indicators"]
        complexity = analysis["complexity_indicators"]
        
        # 스타일 피드백
        if not style["has_docstrings"]:
            feedback.append("💡 함수와 클래스에 독스트링을 추가하면 코드 이해가 쉬워집니다!")
        
        if not style["uses_type_hints"]:
            feedback.append("🎯 타입 힌트를 사용하면 코드의 안정성이 높아집니다!")
        
        if style["meaningful_names"]:
            feedback.append("👍 변수명을 잘 지었네요! 가독성이 좋습니다.")
        
        # 복잡도 피드백
        if complexity["functions"] == 0:
            feedback.append("🔧 코드를 함수로 나누어 재사용성을 높여보세요!")
        
        if complexity["comments"] > complexity["functions"] * 2:
            feedback.append("✨ 주석을 잘 활용하고 있네요! 훌륭합니다.")
        
        return feedback
    
    def suggest_learning_path(self):
        """개인 맞춤 학습 경로 제안"""
        skill_level = self.user_profile["skill_level"]
        interests = self.user_profile["interests"]
        
        learning_paths = {
            "beginner": {
                "python": [
                    "변수와 데이터 타입 마스터하기",
                    "조건문과 반복문 연습",
                    "함수 정의와 활용",
                    "리스트와 딕셔너리 다루기",
                    "간단한 프로젝트 만들기"
                ],
                "web_development": [
                    "HTML 기초 구조 이해",
                    "CSS로 스타일링하기",
                    "JavaScript 기본 문법",
                    "간단한 웹페이지 만들기"
                ]
            },
            "intermediate": {
                "python": [
                    "객체지향 프로그래밍 마스터",
                    "파일 입출력과 예외처리",
                    "라이브러리 활용법",
                    "API 연동하기",
                    "데이터베이스 연결"
                ],
                "ai": [
                    "머신러닝 기초 이론",
                    "pandas와 numpy 활용",
                    "scikit-learn으로 모델 만들기",
                    "데이터 시각화",
                    "실제 프로젝트 적용"
                ]
            }
        }
        
        path = []
        for interest in interests:
            if interest in learning_paths.get(skill_level, {}):
                path.extend(learning_paths[skill_level][interest][:3])
        
        return path[:5]  # 최대 5개까지
    
    def generate_personalized_challenge(self):
        """개인 맞춤 도전 과제 생성"""
        challenges = {
            "beginner": [
                "간단한 계산기 만들기",
                "숫자 맞히기 게임 만들기", 
                "To-Do 리스트 만들기",
                "간단한 채팅봇 만들기"
            ],
            "intermediate": [
                "웹 크롤러 만들기",
                "REST API 서버 만들기",
                "데이터 분석 대시보드 만들기",
                "자동화 스크립트 만들기"
            ],
            "advanced": [
                "머신러닝 모델 배포하기",
                "마이크로서비스 아키텍처 구현",
                "실시간 채팅 애플리케이션",
                "AI 기반 추천 시스템"
            ]
        }
        
        level_challenges = challenges.get(self.user_profile["skill_level"], challenges["beginner"])
        return random.choice(level_challenges)
    
    def track_learning_progress(self, session_data: Dict):
        """학습 진도 추적"""
        self.user_profile["session_count"] += 1
        self.user_profile["total_learning_time"] += session_data.get("duration", 0)
        self.user_profile["last_session"] = datetime.now().isoformat()
        
        # 성취도 계산
        if session_data.get("completed_tasks", 0) > 0:
            achievement = f"Day {self.user_profile['session_count']}: {session_data['completed_tasks']}개 과제 완료!"
            self.user_profile["achievements"].append(achievement)
        
        self.save_user_profile()
    
    def get_personalized_encouragement(self):
        """개인 맞춤 격려 메시지"""
        session_count = self.user_profile["session_count"]
        
        if session_count < 5:
            messages = [
                "🌱 코딩 여정의 시작이네요! 차근차근 해나가요.",
                "💪 매일 조금씩 발전하고 있어요!",
                "🎯 꾸준함이 가장 중요해요. 잘하고 계세요!"
            ]
        elif session_count < 20:
            messages = [
                "🚀 벌써 많이 늘었네요! 실력이 쌓이고 있어요.",
                "✨ 이제 기초가 단단해지고 있어요!",
                "🎉 코딩이 재미있어지기 시작했죠?"
            ]
        else:
            messages = [
                "🏆 이제 진짜 개발자가 되어가고 있네요!",
                "🌟 여러분의 열정이 정말 대단해요!",
                "🚀 이제 더 도전적인 프로젝트를 시작해볼까요?"
            ]
        
        return random.choice(messages)
    
    def generate_study_plan(self, goal: str, timeframe: int):
        """목표 기반 학습 계획 생성"""
        plans = {
            "web_developer": {
                "4주": [
                    "1주차: HTML/CSS 기초 + 간단한 웹페이지",
                    "2주차: JavaScript 기본 + 동적 요소 추가",
                    "3주차: React 기초 + 컴포넌트 개발",
                    "4주차: 포트폴리오 프로젝트 완성"
                ],
                "8주": [
                    "1-2주차: 프론트엔드 기초 (HTML, CSS, JS)",
                    "3-4주차: React + 상태관리",
                    "5-6주차: 백엔드 기초 (Node.js, Express)",
                    "7-8주차: 풀스택 프로젝트 + 배포"
                ]
            },
            "ai_engineer": {
                "4주": [
                    "1주차: Python 기초 + 데이터 타입",
                    "2주차: pandas, numpy 데이터 처리",
                    "3주차: 머신러닝 기초 이론 + scikit-learn",
                    "4주차: 실제 ML 프로젝트 구현"
                ]
            }
        }
        
        timeframe_key = f"{timeframe}주"
        if goal in plans and timeframe_key in plans[goal]:
            return plans[goal][timeframe_key]
        
        return ["맞춤 학습 계획을 준비중입니다!"]

# 소리새와 연동을 위한 인터페이스
def create_ai_tutor_response(command: str) -> str:
    """소리새용 AI 튜터 응답 생성"""
    tutor = PersonalAITutor()
    
    if "학습" in command and "계획" in command:
        path = tutor.suggest_learning_path()
        return f"🎓 개인 맞춤 학습 계획:\n" + "\n".join([f"{i+1}. {item}" for i, item in enumerate(path)])
    
    elif "도전" in command or "과제" in command:
        challenge = tutor.generate_personalized_challenge()
        return f"🎯 오늘의 도전 과제: {challenge}"
    
    elif "격려" in command or "응원" in command:
        encouragement = tutor.get_personalized_encouragement()
        return encouragement
    
    else:
        return "🎓 AI 튜터가 준비되었습니다! '학습 계획', '도전 과제', '격려' 등을 말씀해보세요."

if __name__ == "__main__":
    # 테스트
    tutor = PersonalAITutor()
    print("🎓 개인 맞춤 AI 튜터 시스템 테스트")
    print("="*40)
    
    print("📚 추천 학습 경로:")
    for i, path in enumerate(tutor.suggest_learning_path(), 1):
        print(f"  {i}. {path}")
    
    print(f"\n🎯 오늘의 도전: {tutor.generate_personalized_challenge()}")
    print(f"💪 격려 메시지: {tutor.get_personalized_encouragement()}")