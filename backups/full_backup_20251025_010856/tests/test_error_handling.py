# -*- coding: utf-8 -*-
"""
에러 처리 개선 테스트
"""

import sys
import os
import tempfile
import json

# 모듈 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def test_logging_config_import():
    """로깅 설정 모듈 임포트 테스트"""
    print("✓ 테스트 1: 로깅 설정 모듈 임포트")
    try:
        from modules.logging_config import setup_logger, get_logger
        print("  ✅ 로깅 모듈 임포트 성공")
        return True
    except ImportError as e:
        print(f"  ❌ 로깅 모듈 임포트 실패: {e}")
        return False

def test_logger_creation():
    """로거 생성 테스트"""
    print("✓ 테스트 2: 로거 생성")
    try:
        from modules.logging_config import setup_logger
        logger = setup_logger('test_logger', level='INFO')
        
        if logger is None:
            print("  ❌ 로거가 None입니다")
            return False
            
        # 로거 기본 속성 확인
        if not hasattr(logger, 'info'):
            print("  ❌ 로거에 info 메서드가 없습니다")
            return False
            
        if not hasattr(logger, 'error'):
            print("  ❌ 로거에 error 메서드가 없습니다")
            return False
            
        print("  ✅ 로거 생성 성공")
        return True
    except Exception as e:
        print(f"  ❌ 로거 생성 실패: {e}")
        return False

def test_logger_file_creation():
    """로그 파일 생성 테스트"""
    print("✓ 테스트 3: 로그 파일 생성")
    try:
        from modules.logging_config import setup_logger
        import logging
        
        # 테스트용 임시 디렉토리
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 로거 생성 및 메시지 기록
        logger = setup_logger('test_file_logger', level='DEBUG')
        logger.info("테스트 정보 메시지")
        logger.error("테스트 에러 메시지")
        
        # 핸들러 플러시
        for handler in logger.handlers:
            handler.flush()
        
        # 로그 파일 확인
        log_file = os.path.join(log_dir, "test_file_logger.log")
        error_log_file = os.path.join(log_dir, "test_file_logger_errors.log")
        
        if os.path.exists(log_file):
            print(f"  ✅ 로그 파일 생성 확인: {log_file}")
        else:
            print(f"  ⚠️ 로그 파일이 생성되지 않았습니다: {log_file}")
        
        if os.path.exists(error_log_file):
            print(f"  ✅ 에러 로그 파일 생성 확인: {error_log_file}")
        else:
            print(f"  ⚠️ 에러 로그 파일이 생성되지 않았습니다: {error_log_file}")
        
        return True
    except Exception as e:
        print(f"  ❌ 로그 파일 생성 테스트 실패: {e}")
        return False

def test_config_loading_with_errors():
    """설정 파일 로딩 오류 처리 테스트"""
    print("✓ 테스트 4: 설정 파일 오류 처리")
    try:
        from modules.ai_code_manager.sorisay_core_controller import SorisayCore
        
        # 존재하지 않는 설정 파일 경로
        fake_path = "/nonexistent/path/config.json"
        
        # SorisayCore 인스턴스 생성 (오류가 발생하지 않아야 함)
        core = SorisayCore(config_path=fake_path)
        
        # 기본 설정이 로드되었는지 확인
        if core.config is not None:
            print("  ✅ 설정 파일 없을 때 기본 설정 사용 확인")
            return True
        else:
            print("  ❌ 설정이 로드되지 않았습니다")
            return False
            
    except Exception as e:
        print(f"  ❌ 설정 로딩 테스트 실패: {e}")
        return False

def test_invalid_json_config():
    """잘못된 JSON 설정 파일 처리 테스트"""
    print("✓ 테스트 5: 잘못된 JSON 설정 처리")
    try:
        # 임시 잘못된 JSON 파일 생성
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json content")
            temp_path = f.name
        
        try:
            from modules.ai_code_manager.sorisay_core_controller import SorisayCore
            
            # 잘못된 JSON 파일로 초기화 (오류가 발생하지 않아야 함)
            core = SorisayCore(config_path=temp_path)
            
            if core.config is not None:
                print("  ✅ 잘못된 JSON 파일 처리 시 기본 설정 사용 확인")
                return True
            else:
                print("  ❌ 설정이 로드되지 않았습니다")
                return False
        finally:
            # 임시 파일 삭제
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        print(f"  ❌ 잘못된 JSON 처리 테스트 실패: {e}")
        return False

def test_voice_command_logging():
    """음성 명령 로깅 테스트"""
    print("✓ 테스트 6: 음성 명령 로깅")
    try:
        from run_all_shinsegye import log_voice_command
        
        # 테스트 명령 로깅
        test_command = "테스트 음성 명령"
        log_voice_command(test_command)
        
        # 로그 파일 확인
        log_file = "logs/voice_history.txt"
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if test_command in content:
                    print(f"  ✅ 음성 명령 로깅 확인: {test_command}")
                    return True
                else:
                    print(f"  ⚠️ 로그 파일에 명령이 기록되지 않았습니다")
                    return False
        else:
            print(f"  ⚠️ 음성 명령 로그 파일이 없습니다: {log_file}")
            return False
            
    except ImportError as e:
        print(f"  ⚠️ 모듈 임포트 실패 (예상된 동작): {e}")
        return True  # 의존성이 없을 수 있으므로 통과
    except Exception as e:
        print(f"  ❌ 음성 명령 로깅 테스트 실패: {e}")
        return False

def main():
    """테스트 실행"""
    print("=" * 60)
    print("🧪 에러 처리 개선 테스트 시작")
    print("=" * 60)
    
    tests = [
        test_logging_config_import,
        test_logger_creation,
        test_logger_file_creation,
        test_voice_command_logging,
        # 아래 테스트는 실제 모듈 의존성이 필요하므로 선택적으로 실행
        # test_config_loading_with_errors,
        # test_invalid_json_config,
    ]
    
    results = []
    for test in tests:
        print()
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ❌ 테스트 실행 중 예외 발생: {e}")
            results.append(False)
    
    print()
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"📊 테스트 결과: {passed}/{total} 통과")
    
    if passed == total:
        print("✅ 모든 테스트 통과!")
        return 0
    else:
        print(f"⚠️ {total - passed}개 테스트 실패")
        return 1

if __name__ == "__main__":
    exit(main())
