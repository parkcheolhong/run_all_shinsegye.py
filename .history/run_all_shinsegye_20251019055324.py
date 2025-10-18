import threading
import time
import os
from datetime import datetime

# 안전한 모듈 import
try:
    from modules.ai_code_manager.sorisay_core_controller import SorisayCore
    SORISAY_OK = True
except ImportError as e:
    SORISAY_OK = False
    print(f"⚠️ Sorisay 코어 모듈을 불러올 수 없습니다: {e}")

try:
    from modules.sorisay_dashboard_web import run_dashboard
    DASHBOARD_OK = True
except ImportError as e:
    DASHBOARD_OK = False
    print(f"⚠️ 대시보드 모듈을 불러올 수 없습니다: {e}")
    # 대체 함수 정의
    def run_dashboard():
        print("🌐 대시보드가 비활성화되었습니다.")

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "voice_history.txt")

# 로그 폴더 생성
os.makedirs(LOG_DIR, exist_ok=True)

def log_voice_command(text):
    """음성 명령을 로그에 기록"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {text}\n")

def main():
    print("🚀 신세계 통합 프로젝트 실행 중...")

    # 대시보드 웹 서버 스레드 시작
    threading.Thread(target=run_dashboard, daemon=True).start()
    time.sleep(1)

    # 소리새 엔진 구동
    sorisay = SorisayCore()

    try:
        for text in sorisay.run():  # 제너레이터로 명령어를 받아옴
            print(f"[사용자 명령]: {text}")
            log_voice_command(text)  # 로그 저장
    except KeyboardInterrupt:
        print("🧹 사용자가 수동 종료했습니다.")
    finally:
        print("🛑 시스템 종료 완료")
        log_voice_command("=== 세션 종료 ===")

if __name__ == "__main__":
    demo = main()
    print("\n✅ 보안 시스템 데모 완료!")
