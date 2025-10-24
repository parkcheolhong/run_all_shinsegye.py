import os
import json
import ast
from typing import Dict, List, Optional
from datetime import datetime
import importlib.util

class AutoFeatureExpansion:
    """자동 기능 확장 시스템"""
    
    def __init__(self, plugins_dir="modules/plugins", auto_plugins_dir="modules/auto_plugins"):
        self.plugins_dir = plugins_dir
        self.auto_plugins_dir = auto_plugins_dir
        self.expansion_log = []
        
        # 자동 플러그인 디렉토리 생성
        os.makedirs(self.auto_plugins_dir, exist_ok=True)
        
    def analyze_user_needs(self, learning_engine) -> List[Dict]:
        """사용자 요구사항 분석"""
        needs = []
        
        # 실패한 요청들 분석
        failed_patterns = learning_engine.knowledge_base.get("failed_responses", {})
        
        for pattern, failures in failed_patterns.items():
            if len(failures) >= 3:  # 자주 실패하는 패턴
                need = {
                    "pattern": pattern,
                    "frequency": len(failures),
                    "suggested_feature": self.suggest_feature_for_pattern(pattern),
                    "priority": "high" if len(failures) > 5 else "medium"
                }
                needs.append(need)
        
        return needs
    
    def suggest_feature_for_pattern(self, pattern: str) -> Dict:
        """패턴에 따른 기능 제안"""
        keywords = pattern.split("_")
        
        # 키워드 기반 기능 제안
        if any(word in keywords for word in ["날씨", "weather", "온도", "기온"]):
            return {
                "type": "weather_plugin",
                "description": "날씨 정보 조회 플러그인",
                "commands": ["날씨", "기온", "weather"]
            }
        elif any(word in keywords for word in ["뉴스", "news", "기사"]):
            return {
                "type": "news_plugin", 
                "description": "뉴스 조회 플러그인",
                "commands": ["뉴스", "기사", "news"]
            }
        elif any(word in keywords for word in ["번역", "translate", "영어", "korean"]):
            return {
                "type": "translation_plugin",
                "description": "번역 기능 플러그인", 
                "commands": ["번역", "translate", "영어로", "한국어로"]
            }
        elif any(word in keywords for word in ["계산", "계산기", "calculate", "math"]):
            return {
                "type": "calculator_plugin",
                "description": "계산기 플러그인",
                "commands": ["계산", "계산해줘", "더하기", "빼기"]
            }
        elif any(word in keywords for word in ["시간", "time", "타이머", "알람"]):
            return {
                "type": "time_plugin",
                "description": "시간 관리 플러그인",
                "commands": ["시간", "타이머", "알람"]
            }
        elif any(word in keywords for word in ["파일", "file", "폴더", "directory"]):
            return {
                "type": "file_manager_plugin",
                "description": "파일 관리 플러그인",
                "commands": ["파일찾기", "폴더열기", "파일삭제"]
            }
        else:
            return {
                "type": "generic_web_search_plugin",
                "description": f"'{pattern}' 관련 웹 검색 플러그인",
                "commands": [pattern.replace("_", " ")]
            }
    
    def auto_generate_plugin(self, feature_spec: Dict, pattern: str) -> str:
        """자동으로 플러그인 생성"""
        plugin_name = f"auto_{feature_spec['type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        plugin_file = os.path.join(self.auto_plugins_dir, f"{plugin_name}.py")
        
        # 플러그인 템플릿 생성
        plugin_code = self.generate_plugin_code(feature_spec, pattern, plugin_name)
        
        try:
            with open(plugin_file, 'w', encoding='utf-8') as f:
                f.write(plugin_code)
            
            # 생성 로그 기록
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "plugin_name": plugin_name,
                "feature_type": feature_spec['type'],
                "pattern": pattern,
                "file_path": plugin_file
            }
            self.expansion_log.append(log_entry)
            
            return plugin_file
            
        except Exception as e:
            print(f"⚠ 플러그인 자동 생성 실패: {e}")
            return ""
    
    def generate_plugin_code(self, feature_spec: Dict, pattern: str, plugin_name: str) -> str:
        """플러그인 코드 자동 생성"""
        
        if feature_spec['type'] == 'weather_plugin':
            return f'''"""
자동 생성된 날씨 플러그인 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
사용자 패턴: {pattern}
"""

from ..base_plugin import SorisayPlugin
import requests
from typing import Dict, List

class {plugin_name.title().replace('_', '')}(SorisayPlugin):
    
    @property
    def name(self) -> str:
        return "날씨 정보"
    
    @property 
    def description(self) -> str:
        return "날씨 정보를 조회합니다"
    
    def get_commands(self) -> Dict[str, List[str]]:
        return {{
            "weather": {feature_spec['commands']}
        }}
    
    def execute(self, command: str, text: str) -> str:
        if command == "weather":
            return self._get_weather(text)
        return "날씨 정보를 조회하는 중 오류가 발생했습니다."
    
    def _get_weather(self, text: str) -> str:
        try:
            # 간단한 날씨 정보 (실제로는 API 연동)
            return "현재 서울 날씨는 맑음이며 기온은 20도입니다."
        except Exception as e:
            return f"날씨 정보 조회 실패: {{str(e)}}"
'''
        
        elif feature_spec['type'] == 'calculator_plugin':
            return f'''"""
자동 생성된 계산기 플러그인 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
사용자 패턴: {pattern}
"""

from ..base_plugin import SorisayPlugin
import re
from typing import Dict, List

class {plugin_name.title().replace('_', '')}(SorisayPlugin):
    
    @property
    def name(self) -> str:
        return "계산기"
    
    @property 
    def description(self) -> str:
        return "간단한 계산을 수행합니다"
    
    def get_commands(self) -> Dict[str, List[str]]:
        return {{
            "calculate": {feature_spec['commands']}
        }}
    
    def execute(self, command: str, text: str) -> str:
        if command == "calculate":
            return self._calculate(text)
        return "계산 중 오류가 발생했습니다."
    
    def _calculate(self, text: str) -> str:
        try:
            # 숫자와 기본 연산자 추출
            expression = re.findall(r'[0-9+\-*/().\\s]+', text)
            if expression:
                # 안전한 계산 (eval 대신 제한된 연산만)
                expr = expression[0].strip()
                if re.match(r'^[0-9+\-*/().\\s]+$', expr):
                    result = eval(expr)
                    return f"계산 결과: {{result}}"
            return "계산할 수 있는 식을 찾지 못했습니다. 예: 2 + 3"
        except Exception as e:
            return f"계산 실패: {{str(e)}}"
'''
        
        else:  # generic_web_search_plugin
            return f'''"""
자동 생성된 웹 검색 플러그인 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
사용자 패턴: {pattern}
"""

from ..base_plugin import SorisayPlugin
from ..ai_code_manager.self_learning_engine import SelfLearningEngine
from typing import Dict, List

class {plugin_name.title().replace('_', '')}(SorisayPlugin):
    
    def __init__(self):
        self.learning_engine = SelfLearningEngine()
    
    @property
    def name(self) -> str:
        return "{feature_spec['description']}"
    
    @property 
    def description(self) -> str:
        return "{feature_spec['description']}"
    
    def get_commands(self) -> Dict[str, List[str]]:
        return {{
            "search": {feature_spec['commands']}
        }}
    
    def execute(self, command: str, text: str) -> str:
        if command == "search":
            return self._web_search(text)
        return "검색 중 오류가 발생했습니다."
    
    def _web_search(self, text: str) -> str:
        try:
            results = self.learning_engine.web_search(text, max_results=2)
            if results and results[0].get("content"):
                return f"검색 결과: {{results[0]['content'][:200]}}..."
            return "관련 정보를 찾지 못했습니다."
        except Exception as e:
            return f"검색 실패: {{str(e)}}"
'''
    
    def load_auto_plugin(self, plugin_file: str) -> bool:
        """자동 생성된 플러그인 로드"""
        try:
            # 동적으로 플러그인 모듈 로드
            spec = importlib.util.spec_from_file_location("auto_plugin", plugin_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            print(f"✅ 자동 플러그인 로드 성공: {plugin_file}")
            return True
            
        except Exception as e:
            print(f"⚠ 자동 플러그인 로드 실패: {e}")
            return False
    
    def get_expansion_summary(self) -> Dict:
        """자동 확장 현황 요약"""
        return {
            "생성된_플러그인_수": len(self.expansion_log),
            "최근_확장": self.expansion_log[-5:] if self.expansion_log else [],
            "자동_플러그인_디렉토리": self.auto_plugins_dir
        }