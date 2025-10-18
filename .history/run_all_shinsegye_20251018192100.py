from modules.sorisay_core_controller import SorisayCore
from modules.sorisay_dashboard_web import run_dashboard
import threading
import time
import os
from datetime import datetime

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
        sorisay.run()  # 음성 인식 시작 (무한 루프)
    except KeyboardInterrupt:
        print("🧹 사용자가 수동 종료했습니다.")
    finally:
        print("🛑 시스템 종료 완료")
        log_voice_command("=== 세션 종료 ===")

if __name__ == "__main__":
    main()
