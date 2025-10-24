"""
창조적 코딩 어시스턴트 (Creative Coding Assistant)
코드를 예술작품처럼 아름답게 만드는 AI 시스템
"""
import ast
import random
from typing import Dict, List, Any, Tuple
import re

class CreativeCodingAssistant:
    def __init__(self):
        # 코딩 스타일 테마
        self.coding_themes = {
            "elegant": {
                "name": "우아한 미니멀리즘",
                "style": "간결하고 세련된 코드",
                "patterns": ["single_line_elegance", "functional_beauty"]
            },
            "artistic": {
                "name": "예술적 표현주의", 
                "style": "창의적이고 독창적인 코드",
                "patterns": ["visual_patterns", "poetic_naming"]
            },
            "futuristic": {
                "name": "미래형 하이테크",
                "style": "첨단 기술과 패턴 사용",
                "patterns": ["async_patterns", "AI_enhanced"]
            },
            "organic": {
                "name": "자연스러운 흐름",
                "style": "자연의 패턴을 모방한 코드",
                "patterns": ["tree_structures", "flow_patterns"]
            }
        }
        
        # 창조적 변수명 생성기
        self.creative_names = {
            "function_prefixes": ["weave", "craft", "sculpt", "paint", "compose", "orchestrate", "dance"],
            "variable_themes": ["aurora", "symphony", "cascade", "prism", "nexus", "harmony", "whisper"],
            "class_suffixes": ["Artisan", "Maestro", "Virtuoso", "Architect", "Alchemist", "Oracle"]
        }
        
        self.code_suggestions = []
        
    def analyze_code_aesthetics(self, code: str) -> Dict[str, Any]:
        """코드의 미학적 품질 분석"""
        analysis = {
            "beauty_score": 0,
            "creativity_index": 0,
            "readability": 0,
            "artistic_elements": [],
            "improvement_suggestions": []
        }
        
        # 코드 길이와 복잡도
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # 미학 점수 계산
        beauty_factors = []
        
        # 1. 일관성 검사 (들여쓰기, 네이밍)
        if self._check_consistency(code):
            beauty_factors.append("consistent_style")
            analysis["beauty_score"] += 20
        
        # 2. 창조적 네이밍 검사
        creative_score = self._analyze_naming_creativity(code)
        analysis["creativity_index"] = creative_score
        analysis["beauty_score"] += creative_score
        
        # 3. 코드 구조의 우아함
        structure_score = self._analyze_structure_elegance(code)
        analysis["beauty_score"] += structure_score
        
        # 4. 주석과 문서화의 예술성
        doc_score = self._analyze_documentation_art(code)
        analysis["beauty_score"] += doc_score
        
        # 개선 제안 생성
        analysis["improvement_suggestions"] = self._generate_improvement_suggestions(code, analysis)
        
        return analysis
    
    def beautify_code(self, code: str, theme: str = "elegant") -> str:
        """코드를 선택한 테마로 아름답게 만들기"""
        if theme not in self.coding_themes:
            theme = "elegant"
        
        theme_info = self.coding_themes[theme]
        beautified_code = code
        
        # 테마별 변환 적용
        if theme == "elegant":
            beautified_code = self._apply_elegant_style(beautified_code)
        elif theme == "artistic":
            beautified_code = self._apply_artistic_style(beautified_code)
        elif theme == "futuristic":
            beautified_code = self._apply_futuristic_style(beautified_code)
        elif theme == "organic":
            beautified_code = self._apply_organic_style(beautified_code)
        
        # 공통 개선사항 적용
        beautified_code = self._apply_common_beauty_rules(beautified_code)
        
        return beautified_code
    
    def generate_creative_function_name(self, purpose: str) -> str:
        """목적에 맞는 창의적 함수명 생성"""
        prefix = random.choice(self.creative_names["function_prefixes"])
        theme = random.choice(self.creative_names["variable_themes"])
        
        # 목적 키워드 분석
        if "process" in purpose.lower():
            return f"{prefix}_{theme}_flow"
        elif "create" in purpose.lower():
            return f"{prefix}_{theme}_essence"
        elif "analyze" in purpose.lower():
            return f"decode_{theme}_patterns"
        elif "transform" in purpose.lower():
            return f"metamorphose_{theme}"
        else:
            return f"{prefix}_{theme}_magic"
    
    def suggest_code_poetry(self, code_snippet: str) -> List[str]:
        """코드에 시적 요소 추가 제안"""
        suggestions = []
        
        # 변수명을 더 시적으로
        var_matches = re.findall(r'\b([a-z_]+)\s*=', code_snippet)
        for var in var_matches[:3]:  # 최대 3개만
            poetic_name = self._poeticize_variable_name(var)
            suggestions.append(f"'{var}' → '{poetic_name}' (더 시적인 표현)")
        
        # 함수를 더 예술적으로
        func_matches = re.findall(r'def\s+([a-zA-Z_]+)', code_snippet)
        for func in func_matches[:2]:
            artistic_name = self.generate_creative_function_name(func)
            suggestions.append(f"함수 '{func}' → '{artistic_name}' (예술적 명명)")
        
        # 주석을 더 창의적으로
        if "# " in code_snippet:
            suggestions.append("주석을 시나 은유로 표현해보세요: '# 데이터의 심장박동을 들어보며...'")
        
        # 구조적 개선
        if "for " in code_snippet:
            suggestions.append("반복문을 '춤추는 듯한 흐름'으로 표현해보세요")
        
        if not suggestions:
            suggestions.append("코드에 당신만의 예술적 터치를 추가해보세요! 🎨")
        
        return suggestions
    
    def _check_consistency(self, code: str) -> bool:
        """코드 일관성 검사"""
        lines = code.split('\n')
        
        # 들여쓰기 일관성
        indent_pattern = None
        for line in lines:
            if line.strip() and line.startswith(' '):
                current_indent = len(line) - len(line.lstrip())
                if indent_pattern is None:
                    indent_pattern = current_indent
                elif current_indent % indent_pattern != 0:
                    return False
        
        return True
    
    def _analyze_naming_creativity(self, code: str) -> int:
        """네이밍의 창의성 분석"""
        score = 0
        
        # 변수명 분석
        var_names = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=', code)
        for name in var_names:
            if len(name) > 3:  # 의미 있는 이름
                score += 5
            if '_' in name and len(name.split('_')) >= 2:  # 서술적 이름
                score += 3
            if any(word in name.lower() for word in self.creative_names["variable_themes"]):
                score += 10  # 창의적 키워드 사용
        
        return min(score, 50)
    
    def _analyze_structure_elegance(self, code: str) -> int:
        """구조의 우아함 분석"""
        score = 0
        
        # 함수 길이 적정성
        functions = re.findall(r'def\s+\w+.*?(?=\n(?:def|\Z))', code, re.DOTALL)
        for func in functions:
            func_lines = len([line for line in func.split('\n') if line.strip()])
            if 5 <= func_lines <= 20:  # 적정 길이
                score += 10
        
        # 클래스 사용
        if 'class ' in code:
            score += 15
        
        return min(score, 30)
    
    def _analyze_documentation_art(self, code: str) -> int:
        """문서화의 예술성 분석"""
        score = 0
        
        # 독스트링 존재
        if '"""' in code or "'''" in code:
            score += 10
        
        # 의미 있는 주석
        comments = re.findall(r'#\s*(.+)', code)
        for comment in comments:
            if len(comment.strip()) > 10:  # 의미 있는 주석
                score += 5
        
        return min(score, 20)
    
    def _generate_improvement_suggestions(self, code: str, analysis: Dict) -> List[str]:
        """개선 제안 생성"""
        suggestions = []
        
        if analysis["beauty_score"] < 50:
            suggestions.append("🎨 변수명을 더 서술적이고 창의적으로 만들어보세요")
        
        if analysis["creativity_index"] < 20:
            suggestions.append("✨ 함수명에 예술적 감성을 더해보세요")
        
        if '"""' not in code:
            suggestions.append("📚 독스트링으로 코드에 이야기를 담아보세요")
        
        if len(code.split('\n')) > 50:
            suggestions.append("🎯 함수를 더 작고 우아하게 분리해보세요")
        
        return suggestions
    
    def _apply_elegant_style(self, code: str) -> str:
        """우아한 스타일 적용"""
        # 한 줄로 표현 가능한 것들 최적화
        code = re.sub(r'if\s+(.+):\s*\n\s*return\s+(.+)', r'return \2 if \1 else None', code)
        
        # 리스트 컴프리헨션 제안 (주석으로)
        if 'for ' in code and 'append' in code:
            code += '\n# 💡 Consider using list comprehension for elegance'
        
        return code
    
    def _apply_artistic_style(self, code: str) -> str:
        """예술적 스타일 적용"""
        # 예술적 주석 추가
        artistic_comments = [
            "# 🎨 Painting data with logic brushstrokes",
            "# 🌟 Weaving algorithms like digital poetry",
            "# 🎭 Dancing through conditional expressions"
        ]
        
        lines = code.split('\n')
        if len(lines) > 5:
            lines.insert(2, random.choice(artistic_comments))
        
        return '\n'.join(lines)
    
    def _apply_futuristic_style(self, code: str) -> str:
        """미래형 스타일 적용"""
        # async/await 제안
        if 'def ' in code:
            code += '\n# 🚀 Consider async/await for futuristic performance'
        
        # 타입 힌트 제안
        if 'def ' in code and '->' not in code:
            code += '\n# 🔮 Add type hints for crystal-clear interfaces'
        
        return code
    
    def _apply_organic_style(self, code: str) -> str:
        """자연스러운 스타일 적용"""
        # 자연스러운 흐름 주석
        organic_comments = [
            "# 🌱 Growing data structures organically",
            "# 🌊 Flowing through natural logic patterns",
            "# 🌳 Branching into recursive possibilities"
        ]
        
        if 'if ' in code:
            code += f'\n{random.choice(organic_comments)}'
        
        return code
    
    def _apply_common_beauty_rules(self, code: str) -> str:
        """공통 미용 규칙 적용"""
        # 불필요한 공백 제거
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # 끝 공백 제거
            line = line.rstrip()
            # 너무 많은 연속 빈줄 제거
            if line.strip() or (cleaned_lines and cleaned_lines[-1].strip()):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _poeticize_variable_name(self, var_name: str) -> str:
        """변수명을 시적으로 변환"""
        poetry_map = {
            "data": "wisdom_essence",
            "result": "golden_harvest",
            "value": "precious_gem",
            "count": "star_count",
            "index": "pathway_marker",
            "temp": "fleeting_moment",
            "item": "treasure_piece",
            "list": "collection_symphony"
        }
        
        for original, poetic in poetry_map.items():
            if original in var_name.lower():
                return var_name.replace(original, poetic)
        
        # 일반적인 시적 변환
        theme = random.choice(self.creative_names["variable_themes"])
        return f"{theme}_{var_name}"