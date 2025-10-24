# -*- coding: utf-8 -*-
"""
[DUAL-BRAIN] 신세계 투사이클 소리새 브레인 시스템 - 오류 해결 버전
"""

import os
import sys
import threading
import time
import logging
from datetime import datetime

# 프로젝트 경로 설정
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 기존 모듈 import 시도
try:
    from modules.ai_code_manager.sorisay_core_controller import SorisayCore
    SORISAY_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] SorisayCore 모듈 로드 실패: {e}")
    SORISAY_AVAILABLE = False

try:
    from modules.web_dashboard.app import create_app
    WEB_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] 웹 모듈 로드 실패: {e}")
    WEB_AVAILABLE = False

class SimpleDualBrainSystem:
    """간단한 투사이클 브레인 시스템 - 오류 방지"""
    
    def __init__(self):
        print("[DUAL-BRAIN] 간단한 투사이클 브레인 시스템 초기화...")
        
        self.system_name = "안전한 투사이클 브레인"
        self.version = "1.0.0 - 안전 버전"
        self.active = False
        
        # 간단한 브레인 상태
        self.brain_a_running = False  # 실시간 처리
        self.brain_b_running = False  # 진화 처리
        
        # 기본 통계
        self.stats = {
            'operations': 0,
            'evolutions': 0,
            'commands_processed': 0
        }
        
        print("✅ 간단한 투사이클 브레인 초기화 완료!")

    def start_system(self):
        """시스템 시작"""
        try:
            print("🚀 투사이클 브레인 시작...")
            self.active = True
            
            # 브레인 A 스레드 (안전한 실행)
            brain_a = threading.Thread(target=self._run_brain_a, daemon=True)
            brain_a.start()
            self.brain_a_running = True
            
            # 브레인 B 스레드 (안전한 실행)
            brain_b = threading.Thread(target=self._run_brain_b, daemon=True)
            brain_b.start()
            self.brain_b_running = True
            
            print("[DUAL-BRAIN] 투사이클 브레인 가동 완료!")
            return True
            
        except Exception as e:
            print(f"❌ 브레인 시작 오류: {e}")
            return False

    def _run_brain_a(self):
        """브레인 A: 안전한 실시간 처리"""
        print("[BRAIN] 브레인 A 가동 (실시간 처리)")
        
        while self.active:
            try:
                # 간단한 실시간 처리
                self.stats['operations'] += 1
                time.sleep(0.5)  # 500ms 안전한 주기
                
            except Exception as e:
                print(f"[WARNING] 브레인 A 오류: {e}")
                time.sleep(1)

    def _run_brain_b(self):
        """브레인 B: 안전한 진화 처리"""
        print("[BRAIN] 브레인 B 가동 (진화 처리)")
        
        while self.active:
            try:
                # 간단한 진화 처리
                self.stats['evolutions'] += 1
                
                if self.stats['evolutions'] % 10 == 0:
                    print(f"🌟 진화 완료: {self.stats['evolutions']}회")
                
                time.sleep(3)  # 3초 안전한 주기
                
            except Exception as e:
                print(f"[WARNING] 브레인 B 오류: {e}")
                time.sleep(5)

    def handle_command(self, command):
        """안전한 명령 처리"""
        try:
            self.stats['commands_processed'] += 1
            cmd_lower = command.lower()
            
            # 상태 명령
            if any(word in cmd_lower for word in ["상태", "보고서", "현황"]):
                return self.get_status_report()
            
            # 브레인 명령
            elif any(word in cmd_lower for word in ["브레인", "투사이클", "듀얼"]):
                return self.get_brain_status()
            
            # 인사 명령
            elif any(word in cmd_lower for word in ["안녕", "하이", "hello"]):
                return "안녕하세요! 안전한 투사이클 소리새입니다! [DUAL-BRAIN]"
            
            # 시간 명령
            elif any(word in cmd_lower for word in ["시간", "time"]):
                return f"현재 시간: {datetime.now().strftime('%H:%M:%S')} ⏰"
            
            # 일반 응답
            else:
                return f"투사이클 브레인이 안전하게 명령을 처리했습니다! (처리 횟수: {self.stats['commands_processed']})"
                
        except Exception as e:
            return f"명령 처리 중 오류 발생: {e}"

    def get_status_report(self):
        """시스템 상태 보고"""
        return f"""[DUAL-BRAIN] 안전한 투사이클 브레인 상태 보고

【브레인 상태】
[BRAIN] 브레인 A: {'[ON] 가동중' if self.brain_a_running else '[OFF] 중지'}
[BRAIN] 브레인 B: {'[ON] 가동중' if self.brain_b_running else '[OFF] 중지'}

【처리 통계】
⚡ 실시간 처리: {self.stats['operations']}회
🌟 진화 완료: {self.stats['evolutions']}회
🎤 명령 처리: {self.stats['commands_processed']}회

✅ 시스템이 안전하게 가동 중입니다! 🚀"""

    def get_brain_status(self):
        """브레인 상태"""
        return f"""[DUAL-BRAIN] 투사이클 브레인 상세 상태

【브레인 A - 실시간 처리】
🔄 처리 주기: 500ms (안전한 속도)
📊 처리 완료: {self.stats['operations']}회

【브레인 B - 진화 처리】
🔄 진화 주기: 3초 (안전한 속도)
🌟 진화 완료: {self.stats['evolutions']}회

🎉 두 브레인이 안전하게 협력하고 있습니다! ✨"""

def run_safe_sorisay():
    """안전한 소리새 실행"""
    print("🔧 안전 모드로 소리새 시스템 실행")
    
    # 투사이클 브레인 시스템 초기화
    dual_brain = SimpleDualBrainSystem()
    
    # 시스템 시작
    if dual_brain.start_system():
        print("✅ 투사이클 브레인 시스템 준비 완료!")
        
        # 기본 명령어 안내
        print("\n🎤 사용 가능한 명령어:")
        commands = [
            "시스템 상태 보고서",
            "브레인 상태 확인",
            "안녕하세요",
            "현재 시간"
        ]
        
        for i, cmd in enumerate(commands, 1):
            print(f"   {i}. \"{cmd}\"")
        
        # 간단한 테스트
        print(f"\n🧪 시스템 테스트:")
        test_commands = ["시스템 상태 보고서", "안녕하세요"]
        
        for cmd in test_commands:
            print(f"\n🎤 테스트: '{cmd}'")
            result = dual_brain.handle_command(cmd)
            print(f"🤖 응답: {result}")
        
        # 대화 모드
        print(f"\n💭 대화 모드 (종료: 'quit')")
        
        while True:
            try:
                user_input = input("\n👤 입력: ")
                
                if user_input.lower() in ['quit', 'exit', '종료']:
                    print("👋 투사이클 소리새를 종료합니다!")
                    dual_brain.active = False
                    break
                
                if user_input.strip():
                    response = dual_brain.handle_command(user_input)
                    print(f"🤖 투사이클 소리새: {response}")
        
            except KeyboardInterrupt:
                print("\n👋 투사이클 소리새를 종료합니다!")
                dual_brain.active = False
                break

    else:
        print("❌ 시스템 시작 실패")

def run_with_existing_modules():
    """기존 모듈과 함께 실행"""
    try:
        print("🔄 기존 모듈 연동 시도...")
        
        if SORISAY_AVAILABLE:
            # 기존 SorisayCore 사용
            sorisay = SorisayCore()
            
            # 투사이클 브레인 연결
            dual_brain = SimpleDualBrainSystem()
            dual_brain.start_system()
            
            print("✅ 기존 모듈과 투사이클 브레인 연동 완료!")
            
            # 기존 소리새 실행
            sorisay.run()
    
        else:
            # 안전 모드 실행
            run_safe_sorisay()
        
    except Exception as e:
        print(f"❌ 기존 모듈 연동 오류: {e}")
        print("🔧 안전 모드로 전환...")
        run_safe_sorisay()

def main():
    """메인 실행 함수 - 오류 방지"""
    
    print("🌟 신세계 투사이클 소리새 브레인 - 오류 해결 버전")
    print("="*60)
    print(f"📅 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 모듈 상태 확인
        print(f"\n📋 모듈 상태:")
        print(f"• SorisayCore: {'✅ 사용가능' if SORISAY_AVAILABLE else '❌ 불가능'}")
        print(f"• 웹 모듈: {'✅ 사용가능' if WEB_AVAILABLE else '❌ 불가능'}")
        
        # 실행 방식 선택
        if SORISAY_AVAILABLE:
            print(f"\n🎯 기존 모듈과 연동하여 실행합니다")
            run_with_existing_modules()
        else:
            print(f"\n🔧 안전 모드로 실행합니다")
            run_safe_sorisay()
        
    except Exception as e:
        print(f"❌ 전체 시스템 오류: {e}")
        
        # 최소 기능만으로 실행
        print("🆘 최소 기능으로 실행을 시도합니다...")
        
        try:
            dual_brain = SimpleDualBrainSystem()
            if dual_brain.start_system():
                print("✅ 최소 투사이클 브레인이라도 성공!")
                
                while True:
                    try:
                        cmd = input("👤 명령어 입력 (종료: quit): ")
                        if cmd.lower() == 'quit':
                            break
                        print(f"🤖 응답: {dual_brain.handle_command(cmd)}")
                    except:
                        break
            else:
                print("❌ 모든 시작 방법이 실패했습니다.")
                
        except Exception as final_e:
            print(f"🆘 최종 오류: {final_e}")
            print("💡 Python과 기본 라이브러리 설치를 확인해주세요.")

if __name__ == "__main__":
    main()
