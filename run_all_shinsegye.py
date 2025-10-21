import threading
import time
import os
import logging
from datetime import datetime

# 로깅 설정 import
from modules.logging_config import setup_logger

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

# 로그 폴더 생성 (권한 오류 처리 포함)
try:
    os.makedirs(LOG_DIR, exist_ok=True)
    # 쓰기 권한 확인
    test_file = os.path.join(LOG_DIR, ".permission_test")
    with open(test_file, "w") as f:
        f.write("test")
    os.remove(test_file)
except PermissionError:
    print(f"⚠️ 로그 디렉토리 '{LOG_DIR}'에 대한 쓰기 권한이 없습니다.")
    print(f"💡 대안: 임시 디렉토리를 사용합니다.")
    import tempfile
    LOG_DIR = os.path.join(tempfile.gettempdir(), "sorisay_logs")
    LOG_FILE = os.path.join(LOG_DIR, "voice_history.txt")
    os.makedirs(LOG_DIR, exist_ok=True)
    print(f"✅ 임시 로그 디렉토리 사용: {LOG_DIR}")
except Exception as e:
    print(f"⚠️ 로그 디렉토리 생성 실패: {e}")
    print(f"💡 로그 기능이 제한될 수 있습니다.")

# 로거 설정
logger = setup_logger('run_all_shinsegye', level='INFO')

def log_voice_command(text):
    """음성 명령을 로그에 기록"""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {text}\n")
        logger.info(f"음성 명령 기록: {text}")
    except PermissionError as e:
        logger.error(f"로그 파일 쓰기 권한 없음: {e}")
        print(f"⚠️ 로그 파일 쓰기 권한이 없습니다: {e}")
    except IOError as e:
        logger.error(f"로그 파일 쓰기 오류: {e}", exc_info=True)
        print(f"⚠️ 로그 파일 쓰기 실패: {e}")
    except Exception as e:
        logger.error(f"로그 기록 중 예상치 못한 오류: {e}", exc_info=True)
        print(f"⚠️ 로그 기록 실패: {e}")

def start_dashboard():
    """대시보드 웹 서버를 백그라운드 스레드로 시작"""
    try:
        logger.info("대시보드 웹 서버 시작")
        threading.Thread(target=run_dashboard, daemon=True).start()
        time.sleep(1)
        logger.info("대시보드 웹 서버 시작 완료")
    except Exception as e:
        logger.warning(f"대시보드 시작 중 오류: {e}")
        print(f"⚠️ 대시보드를 시작할 수 없습니다: {e}")

def run_sorisay_engine():
    """소리새 엔진을 실행하고 음성 명령을 처리"""
    try:
        logger.info("소리새 엔진 초기화")
        sorisay = SorisayCore()
        
        for text in sorisay.run():  # 제너레이터로 명령어를 받아옴
            print(f"[사용자 명령]: {text}")
            log_voice_command(text)  # 로그 저장
            
    except KeyboardInterrupt:
        logger.info("사용자가 수동으로 종료")
        print("\n🧹 사용자가 수동 종료했습니다.")
    except Exception as e:
        logger.error(f"시스템 실행 중 오류 발생: {e}", exc_info=True)
        print(f"❌ 시스템 오류: {e}")
        raise
    finally:
        logger.info("시스템 종료 완료")
        print("🛑 시스템 종료 완료")
        log_voice_command("=== 세션 종료 ===")

def main():
    """메인 함수: 소리새 AI 시스템 시작"""
    logger.info("신세계 통합 프로젝트 시작")
    print("🚀 신세계 통합 프로젝트 실행 중...")

    # SORISAY_OK 확인
    if not SORISAY_OK:
        logger.error("Sorisay 코어 모듈이 로드되지 않아 시스템을 시작할 수 없습니다")
        print("❌ Sorisay 코어 모듈이 로드되지 않았습니다. 시스템을 종료합니다.")
        print("💡 해결 방법: pip install -r requirements.txt 실행 후 다시 시도하세요.")
        return

    try:
        # 대시보드 웹 서버 스레드 시작
        start_dashboard()
        
        # 소리새 엔진 구동
        run_sorisay_engine()
    
    except ImportError as e:
        logger.error(f"필수 모듈을 불러올 수 없습니다: {e}", exc_info=True)
        print(f"❌ 모듈 로드 실패: {e}")
        print("💡 해결 방법: pip install -r requirements.txt 실행 후 다시 시도하세요.")
    except Exception as e:
        logger.critical(f"시스템 초기화 중 심각한 오류: {e}", exc_info=True)
        print(f"❌ 시스템 초기화 실패: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 사용자가 프로그램을 종료했습니다.")
    except Exception as e:
        print(f"\n❌ 프로그램 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
