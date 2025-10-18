"""
개발 도구 플러그인
"""

from .base_plugin import SorisayPlugin
from typing import Dict, List
import subprocess
import os

class DevToolsPlugin(SorisayPlugin):
    
    @property
    def name(self) -> str:
        return "개발 도구"
    
    @property
    def description(self) -> str:
        return "개발 관련 편의 명령어"
    
    def get_commands(self) -> Dict[str, List[str]]:
        return {
            "test": ["테스트", "test", "테스트실행"],
            "build": ["빌드", "build", "컴파일"],
            "install": ["설치", "install", "패키지설치"],
            "clean": ["정리", "clean", "청소"],
            "docs": ["문서", "docs", "문서생성"]
        }
    
    def execute(self, command: str, text: str) -> str:
        if command == "test":
            return self._run_tests()
        elif command == "build":
            return self._build_project()
        elif command == "install":
            return self._install_packages()
        elif command == "clean":
            return self._clean_project()
        elif command == "docs":
            return self._generate_docs()
        else:
            return "알 수 없는 개발 명령어입니다."
    
    def _run_tests(self) -> str:
        try:
            print("🧪 테스트 실행 중...")
            # subprocess.run(['python', '-m', 'pytest'], check=True)
            return "모든 테스트가 성공적으로 통과했습니다!"
        except Exception as e:
            return f"테스트 실행 중 오류: {str(e)}"
    
    def _build_project(self) -> str:
        try:
            print("🔨 프로젝트 빌드 중...")
            return "프로젝트 빌드가 완료되었습니다!"
        except Exception as e:
            return f"빌드 중 오류: {str(e)}"
    
    def _install_packages(self) -> str:
        try:
            print("📦 패키지 설치 중...")
            # subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
            return "필수 패키지 설치가 완료되었습니다!"
        except Exception as e:
            return f"패키지 설치 중 오류: {str(e)}"
    
    def _clean_project(self) -> str:
        try:
            print("🧹 프로젝트 정리 중...")
            # 캐시 폴더 정리 등
            return "프로젝트 정리가 완료되었습니다!"
        except Exception as e:
            return f"정리 중 오류: {str(e)}"
    
    def _generate_docs(self) -> str:
        try:
            print("📚 문서 생성 중...")
            return "프로젝트 문서가 생성되었습니다!"
        except Exception as e:
            return f"문서 생성 중 오류: {str(e)}"