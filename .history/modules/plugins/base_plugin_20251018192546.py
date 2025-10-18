"""
소리새 명령어 플러그인 베이스 클래스
새로운 명령어를 추가하려면 이 클래스를 상속받아 구현하세요.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class SorisayPlugin(ABC):
    """소리새 플러그인 베이스 클래스"""
    
    @abstractmethod
    def get_commands(self) -> Dict[str, List[str]]:
        """
        플러그인이 처리할 명령어들을 반환
        Returns:
            Dict[str, List[str]]: {명령어_이름: [키워드1, 키워드2, ...]}
        """
        pass
    
    @abstractmethod
    def execute(self, command: str, text: str) -> str:
        """
        명령어 실행
        Args:
            command: 실행할 명령어 이름
            text: 사용자가 말한 전체 텍스트
        Returns:
            str: 사용자에게 들려줄 응답 메시지
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """플러그인 이름"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """플러그인 설명"""
        pass
    
    def get_help(self) -> str:
        """플러그인 도움말 반환"""
        commands = self.get_commands()
        help_text = f"{self.name}: {self.description}\n"
        for cmd, keywords in commands.items():
            help_text += f"  - {cmd}: {', '.join(keywords)}\n"
        return help_text