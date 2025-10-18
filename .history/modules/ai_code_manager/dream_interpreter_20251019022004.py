# -*- coding: utf-8 -*-
"""
🌙 AI 꿈 해석 시스템 (Dream Interpreter System)
심리학, 상징주의, 문화적 해석을 통한 지능형 꿈 분석
"""

import random
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

class DreamInterpreter:
    """AI 꿈 해석 시스템"""
    
    def __init__(self):
        self.setup_logging()
        
        # 꿈 상징 사전 (심리학 기반)
        self.dream_symbols = {
            "물": {"의미": ["감정", "잠재의식", "정화", "변화"], "색상": "💧"},
            "불": {"의미": ["열정", "분노", "변화", "창조력"], "색상": "🔥"},
            "날다": {"의미": ["자유", "해방", "권력", "무한가능성"], "색상": "🕊️"},
            "떨어지다": {"의미": ["불안", "통제력상실", "실패걱정"], "색상": "⬇️"},
            "동물": {"의미": ["본능", "원시성", "내면의힘"], "색상": "🐺"},
            "집": {"의미": ["자아", "안정", "가족", "내면세계"], "색상": "🏠"},
            "죽음": {"의미": ["변화", "새로운시작", "두려움"], "색상": "💀"},
            "바다": {"의미": ["무의식", "모성", "광대함"], "색상": "🌊"},
            "산": {"의미": ["목표", "도전", "성장", "영성"], "색상": "⛰️"},
            "추적": {"의미": ["회피", "죄책감", "스트레스"], "색상": "🏃"}
        }
        
        # 감정 분석 패턴
        self.emotion_patterns = {
            "긍정": ["행복", "즐거", "웃", "기쁘", "평화", "따뜻", "밝"],
            "부정": ["무서", "두려", "슬프", "화나", "답답", "어둡", "차가"],
            "불안": ["걱정", "초조", "떨림", "긴장", "조급", "불안"],
            "호기심": ["궁금", "신기", "흥미", "탐구", "발견"]
        }
        
        # 프로이드식 해석 패턴
        self.freudian_patterns = {
            "억압된욕망": ["금지된", "숨겨진", "비밀", "금기"],
            "성적상징": ["탑", "터널", "열쇠", "문", "뱀"],
            "부모갈등": ["아버지", "어머니", "권위", "보호"]
        }
        
        # 융 심리학 원형
        self.jungian_archetypes = {
            "그림자": ["어둠", "숨김", "거부", "부정"],
            "아니마": ["여성성", "직관", "감성", "창조"],
            "아니무스": ["남성성", "논리", "행동", "결단"],
            "현자": ["지혜", "가르침", "노인", "조언"]
        }
        
        # 문화별 해석
        self.cultural_meanings = {
            "한국": {
                "돼지꿈": "재물운 상승",
                "용꿈": "출세와 성공",
                "뱀꿈": "지혜와 변화",
                "토끼꿈": "행운과 기회"
            },
            "서양": {
                "고양이": "독립성과 신비",
                "개": "충성과 보호",
                "말": "자유와 힘",
                "새": "영성과 메시지"
            }
        }

    def setup_logging(self):
        """로깅 설정"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def analyze_dream(self, dream_text: str, dreamer_age: int = 30, 
                     culture: str = "한국") -> Dict:
        """꿈 종합 분석"""
        try:
            analysis = {
                "입력_꿈": dream_text,
                "분석_시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "기본_정보": {
                    "나이대": self._get_age_group(dreamer_age),
                    "문화권": culture,
                    "꿈_길이": len(dream_text),
                    "복잡도": self._calculate_complexity(dream_text)
                }
            }
            
            # 단계별 분석
            analysis["상징_분석"] = self._analyze_symbols(dream_text)
            analysis["감정_분석"] = self._analyze_emotions(dream_text)
            analysis["심리_분석"] = self._psychological_analysis(dream_text)
            analysis["문화_해석"] = self._cultural_interpretation(dream_text, culture)
            analysis["미래_예측"] = self._predict_future_themes(dream_text)
            analysis["조언"] = self._generate_advice(analysis)
            analysis["점수"] = self._calculate_significance_score(analysis)
            
            self.logger.info(f"꿈 분석 완료: {len(dream_text)}자")
            return analysis
            
        except Exception as e:
            self.logger.error(f"꿈 분석 오류: {e}")
            return {"오류": str(e)}

    def _analyze_symbols(self, dream_text: str) -> Dict:
        """꿈 상징 분석"""
        found_symbols = {}
        symbol_count = 0
        
        for symbol, data in self.dream_symbols.items():
            if symbol in dream_text:
                found_symbols[symbol] = {
                    "발견위치": dream_text.find(symbol),
                    "의미": data["의미"],
                    "상징": data["색상"],
                    "해석": self._interpret_symbol_context(symbol, dream_text)
                }
                symbol_count += 1
        
        return {
            "발견된_상징": found_symbols,
            "상징_개수": symbol_count,
            "상징_밀도": round(symbol_count / len(dream_text) * 100, 2),
            "주요_상징": self._get_dominant_symbol(found_symbols)
        }

    def _analyze_emotions(self, dream_text: str) -> Dict:
        """감정 패턴 분석"""
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_patterns.items():
            score = 0
            found_words = []
            
            for keyword in keywords:
                count = dream_text.count(keyword)
                score += count
                if count > 0:
                    found_words.append(keyword)
            
            if score > 0:
                emotion_scores[emotion] = {
                    "점수": score,
                    "발견어": found_words,
                    "강도": self._calculate_emotion_intensity(score)
                }
        
        dominant_emotion = max(emotion_scores.items(), 
                             key=lambda x: x[1]["점수"]) if emotion_scores else None
        
        return {
            "감정_분석": emotion_scores,
            "지배적_감정": dominant_emotion[0] if dominant_emotion else "중립",
            "감정_복합성": len(emotion_scores),
            "감정_균형": self._analyze_emotional_balance(emotion_scores)
        }

    def _psychological_analysis(self, dream_text: str) -> Dict:
        """심리학적 해석"""
        freudian_analysis = {}
        jungian_analysis = {}
        
        # 프로이드 분석
        for pattern, keywords in self.freudian_patterns.items():
            matches = []
            for keyword in keywords:
                if keyword in dream_text:
                    matches.append(keyword)
            
            if matches:
                freudian_analysis[pattern] = {
                    "발견어": matches,
                    "해석": self._freudian_interpretation(pattern, matches)
                }
        
        # 융 분석
        for archetype, keywords in self.jungian_archetypes.items():
            matches = []
            for keyword in keywords:
                if keyword in dream_text:
                    matches.append(keyword)
            
            if matches:
                jungian_analysis[archetype] = {
                    "발견어": matches,
                    "원형의미": self._jungian_interpretation(archetype, matches)
                }
        
        return {
            "프로이드_분석": freudian_analysis,
            "융_분석": jungian_analysis,
            "심리학적_중요도": self._calculate_psychological_significance(
                freudian_analysis, jungian_analysis
            ),
            "잠재의식_메시지": self._extract_subconscious_message(dream_text)
        }

    def _cultural_interpretation(self, dream_text: str, culture: str) -> Dict:
        """문화적 해석"""
        cultural_symbols = self.cultural_meanings.get(culture, {})
        found_cultural = {}
        
        for symbol, meaning in cultural_symbols.items():
            if symbol in dream_text:
                found_cultural[symbol] = {
                    "전통적의미": meaning,
                    "현대적해석": self._modernize_interpretation(symbol, meaning),
                    "문화적중요도": random.uniform(0.7, 1.0)
                }
        
        return {
            "문화권": culture,
            "전통상징": found_cultural,
            "문화적_일치도": len(found_cultural) / len(cultural_symbols) if cultural_symbols else 0,
            "지역적_특성": self._analyze_regional_characteristics(dream_text, culture)
        }

    def _predict_future_themes(self, dream_text: str) -> Dict:
        """미래 테마 예측"""
        prediction_themes = {
            "관계": ["사랑", "우정", "가족", "갈등해결"],
            "성장": ["학습", "발전", "새로운기회", "자기계발"],
            "변화": ["이직", "이사", "새로운시작", "전환점"],
            "도전": ["시험", "경쟁", "목표달성", "극복"]
        }
        
        future_predictions = {}
        
        for theme, predictions in prediction_themes.items():
            theme_score = 0
            relevant_predictions = []
            
            # 꿈 내용과 테마 연관성 계산
            for pred in predictions:
                if any(keyword in dream_text for keyword in [pred[:2], pred]):
                    theme_score += 1
                    relevant_predictions.append(pred)
            
            if theme_score > 0:
                future_predictions[theme] = {
                    "예상확률": min(theme_score * 25, 95),
                    "관련예측": relevant_predictions,
                    "시기예상": self._predict_timing(),
                    "조치사항": self._suggest_actions(theme)
                }
        
        return {
            "미래_테마": future_predictions,
            "전체적_전망": self._generate_overall_forecast(future_predictions),
            "핵심_예측": self._extract_key_prediction(future_predictions)
        }

    def _generate_advice(self, analysis: Dict) -> Dict:
        """개인화된 조언 생성"""
        advice_categories = {
            "심리적_건강": [],
            "인간관계": [],
            "자기계발": [],
            "주의사항": []
        }
        
        # 감정 분석 기반 조언
        dominant_emotion = analysis.get("감정_분석", {}).get("지배적_감정", "중립")
        
        if dominant_emotion == "부정":
            advice_categories["심리적_건강"].append("스트레스 관리와 긍정적 사고 필요")
            advice_categories["주의사항"].append("부정적 감정의 원인 파악 권장")
        
        elif dominant_emotion == "불안":
            advice_categories["심리적_건강"].append("안정감 확보와 명상 실천")
            advice_categories["자기계발"].append("자신감 증진 활동 참여")
        
        # 상징 분석 기반 조언
        symbols = analysis.get("상징_분석", {}).get("발견된_상징", {})
        
        if "물" in symbols:
            advice_categories["자기계발"].append("감정 정화와 새로운 시작 준비")
        
        if "날다" in symbols:
            advice_categories["인간관계"].append("자유로운 표현과 새로운 도전")
        
        return {
            "조언_카테고리": advice_categories,
            "우선순위_조언": self._prioritize_advice(advice_categories),
            "실천방법": self._suggest_practical_methods(advice_categories),
            "전문가_상담": self._recommend_professional_help(analysis)
        }

    def interpret_recurring_dream(self, dream_records: List[str]) -> Dict:
        """반복 꿈 패턴 분석"""
        if not dream_records:
            return {"오류": "분석할 꿈 기록이 없습니다"}
        
        common_elements = self._find_common_elements(dream_records)
        pattern_evolution = self._analyze_pattern_evolution(dream_records)
        psychological_significance = self._assess_recurring_significance(common_elements)
        
        return {
            "반복_횟수": len(dream_records),
            "공통_요소": common_elements,
            "패턴_변화": pattern_evolution,
            "심리적_의미": psychological_significance,
            "해결방안": self._suggest_resolution_methods(common_elements),
            "추적_권장사항": self._recommend_tracking_methods()
        }

    def create_dream_report(self, analysis: Dict) -> str:
        """꿈 분석 보고서 생성"""
        report_lines = []
        report_lines.append("=" * 50)
        report_lines.append("🌙 AI 꿈 해석 분석 보고서")
        report_lines.append("=" * 50)
        report_lines.append(f"분석 시간: {analysis.get('분석_시간', 'N/A')}")
        report_lines.append("")
        
        # 기본 정보
        basic_info = analysis.get("기본_정보", {})
        report_lines.append("📊 기본 정보")
        report_lines.append(f"  나이대: {basic_info.get('나이대', 'N/A')}")
        report_lines.append(f"  문화권: {basic_info.get('문화권', 'N/A')}")
        report_lines.append(f"  복잡도: {basic_info.get('복잡도', 'N/A')}")
        report_lines.append("")
        
        # 상징 분석
        symbol_analysis = analysis.get("상징_분석", {})
        report_lines.append("🔮 상징 분석")
        symbols = symbol_analysis.get("발견된_상징", {})
        for symbol, data in symbols.items():
            report_lines.append(f"  {data['상징']} {symbol}: {', '.join(data['의미'])}")
        report_lines.append(f"  주요 상징: {symbol_analysis.get('주요_상징', 'N/A')}")
        report_lines.append("")
        
        # 감정 분석
        emotion_analysis = analysis.get("감정_분석", {})
        report_lines.append("💭 감정 분석")
        report_lines.append(f"  지배적 감정: {emotion_analysis.get('지배적_감정', 'N/A')}")
        report_lines.append(f"  감정 복합성: {emotion_analysis.get('감정_복합성', 'N/A')}")
        report_lines.append("")
        
        # 조언
        advice = analysis.get("조언", {})
        priority_advice = advice.get("우선순위_조언", [])
        if priority_advice:
            report_lines.append("💡 우선순위 조언")
            for i, adv in enumerate(priority_advice[:3], 1):
                report_lines.append(f"  {i}. {adv}")
            report_lines.append("")
        
        # 미래 예측
        future = analysis.get("미래_예측", {})
        key_prediction = future.get("핵심_예측", "")
        if key_prediction:
            report_lines.append("🔮 핵심 예측")
            report_lines.append(f"  {key_prediction}")
            report_lines.append("")
        
        report_lines.append("=" * 50)
        return "\n".join(report_lines)

    # 헬퍼 메소드들
    def _get_age_group(self, age: int) -> str:
        if age < 20: return "청소년"
        elif age < 30: return "청년"
        elif age < 50: return "중년"
        else: return "장년"

    def _calculate_complexity(self, text: str) -> str:
        length = len(text)
        if length < 50: return "단순"
        elif length < 200: return "보통"
        else: return "복잡"

    def _interpret_symbol_context(self, symbol: str, text: str) -> str:
        # 상황별 해석 로직
        context_interpretations = {
            "물": "정서적 변화나 새로운 시작을 의미할 수 있습니다",
            "불": "열정적 에너지나 변화의 욕구를 나타냅니다",
            "날다": "자유에 대한 갈망이나 현실 초월 욕구를 보여줍니다"
        }
        return context_interpretations.get(symbol, "개인적 경험과 연관해 해석해보세요")

    def _get_dominant_symbol(self, symbols: Dict) -> str:
        if not symbols:
            return "없음"
        # 첫 번째 발견된 상징을 주요 상징으로 (실제로는 더 복잡한 로직 필요)
        return list(symbols.keys())[0] if symbols else "없음"

    def _calculate_emotion_intensity(self, score: int) -> str:
        if score >= 3: return "강함"
        elif score >= 2: return "보통"
        else: return "약함"

    def _analyze_emotional_balance(self, emotions: Dict) -> str:
        if not emotions:
            return "중립적"
        
        positive_count = sum(1 for emotion in emotions if emotion in ["긍정", "호기심"])
        negative_count = sum(1 for emotion in emotions if emotion in ["부정", "불안"])
        
        if positive_count > negative_count:
            return "긍정적"
        elif negative_count > positive_count:
            return "부정적"
        else:
            return "균형적"

    def _freudian_interpretation(self, pattern: str, matches: List[str]) -> str:
        interpretations = {
            "억압된욕망": "내재된 욕구가 꿈을 통해 표출되고 있습니다",
            "성적상징": "생명력과 창조적 에너지의 상징일 수 있습니다",
            "부모갈등": "권위와의 관계나 독립성에 대한 고민을 반영합니다"
        }
        return interpretations.get(pattern, "프로이드적 관점에서 무의식적 충동을 나타냅니다")

    def _jungian_interpretation(self, archetype: str, matches: List[str]) -> str:
        interpretations = {
            "그림자": "숨겨진 자아나 받아들이지 못한 측면을 상징합니다",
            "아니마": "내면의 여성적 특질이나 직관적 지혜를 나타냅니다",
            "아니무스": "내면의 남성적 특질이나 행동력을 의미합니다",
            "현자": "내면의 지혜나 멘토적 역할을 상징합니다"
        }
        return interpretations.get(archetype, "집단 무의식의 원형적 에너지를 나타냅니다")

    def _calculate_psychological_significance(self, freudian: Dict, jungian: Dict) -> str:
        total_elements = len(freudian) + len(jungian)
        if total_elements >= 3: return "높음"
        elif total_elements >= 1: return "보통"
        else: return "낮음"

    def _extract_subconscious_message(self, text: str) -> str:
        # 간단한 키워드 기반 메시지 추출
        if "변화" in text or "새로" in text:
            return "변화와 새로운 시작에 대한 내적 준비가 되어있습니다"
        elif "두려" in text or "무서" in text:
            return "현재 상황에 대한 불안감을 해결할 필요가 있습니다"
        else:
            return "현재 내면의 상태를 돌아보고 균형을 찾으시기 바랍니다"

    def _modernize_interpretation(self, symbol: str, traditional: str) -> str:
        return f"현대적 관점에서 {traditional}은 개인의 성장과 발전을 의미합니다"

    def _analyze_regional_characteristics(self, text: str, culture: str) -> str:
        if culture == "한국":
            return "집단주의적 가치관과 관계 중심적 사고가 반영됨"
        else:
            return "개인주의적 가치관과 자아실현 욕구가 나타남"

    def _predict_timing(self) -> str:
        timings = ["1-2주 내", "한 달 내", "2-3개월 내", "반년 내"]
        return random.choice(timings)

    def _suggest_actions(self, theme: str) -> List[str]:
        actions = {
            "관계": ["적극적인 소통", "갈등 해결 시도", "새로운 만남 추구"],
            "성장": ["새로운 학습 시작", "기술 개발", "경험 확장"],
            "변화": ["계획 수립", "준비 과정", "점진적 변화"],
            "도전": ["목표 설정", "단계별 접근", "지속적 노력"]
        }
        return actions.get(theme, ["현재 상황 분석", "신중한 판단"])

    def _generate_overall_forecast(self, predictions: Dict) -> str:
        if not predictions:
            return "현재는 안정적인 시기로 보입니다"
        
        high_prob = [k for k, v in predictions.items() if v.get("예상확률", 0) > 70]
        if high_prob:
            return f"{', '.join(high_prob)} 분야에서 중요한 변화가 예상됩니다"
        else:
            return "다양한 가능성이 열려있는 시기입니다"

    def _extract_key_prediction(self, predictions: Dict) -> str:
        if not predictions:
            return "특별한 예측 없음"
        
        highest = max(predictions.items(), key=lambda x: x[1].get("예상확률", 0))
        return f"{highest[0]} 분야: {highest[1].get('예상확률', 0)}% 확률"

    def _prioritize_advice(self, advice_categories: Dict) -> List[str]:
        all_advice = []
        for category, advices in advice_categories.items():
            all_advice.extend(advices)
        return all_advice[:3]  # 상위 3개만 반환

    def _suggest_practical_methods(self, advice_categories: Dict) -> List[str]:
        return [
            "일기 쓰기로 감정 정리",
            "명상이나 요가 실천",
            "신뢰할 수 있는 사람과 대화",
            "새로운 취미나 활동 시작"
        ]

    def _recommend_professional_help(self, analysis: Dict) -> str:
        psychological_sig = analysis.get("심리_분석", {}).get("심리학적_중요도", "낮음")
        if psychological_sig == "높음":
            return "전문 상담사와의 상담을 권장합니다"
        else:
            return "현재 상태는 정상 범위 내입니다"

    def _find_common_elements(self, dreams: List[str]) -> Dict:
        # 반복 꿈에서 공통 요소 찾기
        all_words = []
        for dream in dreams:
            all_words.extend(dream.split())
        
        word_count = {}
        for word in all_words:
            if len(word) > 1:  # 한 글자는 제외
                word_count[word] = word_count.get(word, 0) + 1
        
        # 2번 이상 나타나는 단어들
        common_words = {k: v for k, v in word_count.items() if v >= 2}
        
        return {
            "공통_단어": common_words,
            "반복_빈도": len(common_words),
            "핵심_테마": max(common_words.items(), key=lambda x: x[1])[0] if common_words else "없음"
        }

    def _analyze_pattern_evolution(self, dreams: List[str]) -> Dict:
        return {
            "패턴_변화": "점진적 변화 감지됨" if len(dreams) > 3 else "패턴 확립 중",
            "강도_변화": "유지됨",
            "새로운_요소": "현재까지 일관성 유지"
        }

    def _assess_recurring_significance(self, common_elements: Dict) -> str:
        frequency = common_elements.get("반복_빈도", 0)
        if frequency >= 5:
            return "높은 심리적 의미 - 중요한 내면의 메시지"
        elif frequency >= 3:
            return "보통 의미 - 해결이 필요한 과제"
        else:
            return "낮은 의미 - 일시적 현상일 가능성"

    def _suggest_resolution_methods(self, common_elements: Dict) -> List[str]:
        return [
            "꿈 일기 작성으로 패턴 추적",
            "스트레스 요인 식별 및 관리",
            "이완 기법 연습",
            "생활 패턴 개선"
        ]

    def _recommend_tracking_methods(self) -> List[str]:
        return [
            "매일 꿈 기록하기",
            "감정 상태와 함께 기록",
            "꿈의 선명도 평가",
            "주기적 패턴 분석"
        ]

if __name__ == "__main__":
    # 테스트 코드
    interpreter = DreamInterpreter()
    
    # 샘플 꿈 분석
    sample_dream = "물에 떨어져서 무서웠지만 날개가 생겨서 하늘을 날아다녔다. 집에 돌아오니 가족들이 웃고 있었다."
    
    result = interpreter.analyze_dream(sample_dream, dreamer_age=25, culture="한국")
    
    print("🌙 꿈 해석 시스템 테스트")
    print("=" * 40)
    print(f"입력 꿈: {sample_dream}")
    print("\n📊 분석 결과:")
    print(f"발견된 상징: {len(result.get('상징_분석', {}).get('발견된_상징', {}))}")
    print(f"지배적 감정: {result.get('감정_분석', {}).get('지배적_감정', 'N/A')}")
    print(f"심리적 중요도: {result.get('심리_분석', {}).get('심리학적_중요도', 'N/A')}")
    
    # 보고서 생성
    report = interpreter.create_dream_report(result)
    print("\n" + report)