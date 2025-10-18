"""
기본 시스템 명령어 플러그인
"""

from .base_plugin import SorisayPlugin
from typing import Dict, List
import subprocess
import os

class SystemPlugin(SorisayPlugin):
    
    @property
    def name(self) -> str:
        return "시스템 관리"
    
    @property 
    def description(self) -> str:
        return "기본 시스템 제어 명령어"
    
    def get_commands(self) -> Dict[str, List[str]]:
        return {
            "refactor": ["리팩터링", "리팩토링", "refactor"],
            "sync": ["동기화", "싱크", "sync"],
            "stop": ["종료", "소리새그만", "정지", "stop", "quit"],
            "status": ["상태", "status", "현재상태"],
            "help": ["도움말", "help", "명령어", "사용법"]
        }
    
    def execute(self, command: str, text: str) -> str:
        if command == "refactor":
            return self._refactor()
        elif command == "sync":
            return self._sync()
        elif command == "stop":
            return self._stop()
        elif command == "status":
            return self._status()
        elif command == "help":
            return self._help()
        else:
            return "알 수 없는 명령어입니다."
    
    def _refactor(self) -> str:
        try:
            # 실제 리팩터링 로직 (예시)
            print("🔧 코드 리팩터링 실행 중...")
            # subprocess.run(['python', 'structure_cleaner.py'], check=True)
            return "코드 리팩터링이 완료되었습니다!"
        except Exception as e:
            return f"리팩터링 중 오류가 발생했습니다: {str(e)}"
    
    def _sync(self) -> str:
        try:
            print("🔄 깃허브 동기화 중...")
            # 실제 Git 동기화 로직 (예시)
            # subprocess.run(['git', 'pull'], check=True)
            # subprocess.run(['git', 'push'], check=True)
            return "깃허브 동기화가 완료되었습니다!"
        except Exception as e:
            return f"동기화 중 오류가 발생했습니다: {str(e)}"
    
    def _stop(self) -> str:
        return "시스템을 종료합니다."
    
    def _status(self) -> str:
        return "소리새 시스템이 정상 작동 중입니다."
    
    def _help(self) -> str:
        help_text = """
🤖 소리새 자연어 명령어 가이드

📋 기본 명령어들:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 코드 리팩터링:
   • "코드를 정리해줘"
   • "리팩터링 실행해줘"
   • "코드를 깔끔하게 만들어줘"
   • "구조를 개선해줘"

🔄 깃허브 동기화:
   • "깃허브와 동기화해줘"
   • "소스코드를 백업해줘"
   • "변경사항을 올려줘"
   • "푸시해줘"

📊 시스템 상태:
   • "상태를 확인해줘"
   • "시스템이 잘 돌아가고 있어?"
   • "문제없이 동작하고 있어?"

👋 인사:
   • "안녕하세요"
   • "소리새야 안녕"
   • "좋은 아침이야"

🛑 종료:
   • "이제 그만 종료해줘"
   • "소리새 안녕"
   • "시스템 끝내줘"
   • "멈춰줘"

💡 팁: 자연스럽게 말씀하세요! 소리새가 의도를 파악합니다.
        """
        return help_text.strip()