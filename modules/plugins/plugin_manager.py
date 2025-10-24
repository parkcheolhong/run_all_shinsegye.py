"""
플러그인 매니저
플러그인을 자동으로 로드하고 관리합니다.
"""

import os
import importlib
from typing import Dict, List, Type
from .base_plugin import SorisayPlugin

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, SorisayPlugin] = {}
        self.command_map: Dict[str, tuple] = {}  # {keyword: (plugin_name, command)}
        
    def load_plugins(self):
        """플러그인 폴더에서 모든 플러그인을 자동 로드"""
        plugin_dir = os.path.dirname(__file__)
        
        # 기본 플러그인들 수동 로드
        from .system_plugin import SystemPlugin
        from .devtools_plugin import DevToolsPlugin
        
        self.register_plugin(SystemPlugin())
        self.register_plugin(DevToolsPlugin())
        
        print(f"[SUCCESS] 총 {len(self.plugins)}개의 플러그인이 로드되었습니다.")
        
    def register_plugin(self, plugin: SorisayPlugin):
        """플러그인 등록"""
        self.plugins[plugin.name] = plugin
        
        # 명령어 매핑 업데이트
        commands = plugin.get_commands()
        for command, keywords in commands.items():
            for keyword in keywords:
                self.command_map[keyword.lower()] = (plugin.name, command)
        
        print(f"[PLUGIN] 플러그인 등록됨: {plugin.name}")
    
    def find_command(self, text: str) -> tuple:
        """
        텍스트에서 명령어 찾기
        Returns:
            tuple: (plugin_name, command, keyword) 또는 (None, None, None)
        """
        text_lower = text.lower()
        
        for keyword, (plugin_name, command) in self.command_map.items():
            if keyword in text_lower:
                return plugin_name, command, keyword
        
        return None, None, None
    
    def execute_command(self, plugin_name: str, command: str, text: str) -> str:
        """명령어 실행"""
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            return plugin.execute(command, text)
        else:
            return "플러그인을 찾을 수 없습니다."
    
    def get_all_help(self) -> str:
        """모든 플러그인의 도움말 반환"""
        help_text = "📋 사용 가능한 명령어:\n\n"
        for plugin in self.plugins.values():
            help_text += plugin.get_help() + "\n"
        return help_text
    
    def get_plugin_list(self) -> List[str]:
        """로드된 플러그인 목록 반환"""
        return list(self.plugins.keys())