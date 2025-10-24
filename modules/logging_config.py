# -*- coding: utf-8 -*-
"""
🔍 로깅 설정 모듈 (Logging Configuration)
소리새 AI 시스템의 통합 로깅 설정
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# 로그 디렉토리 생성
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 로그 포맷 정의
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DETAILED_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'

# 로그 레벨 매핑
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

def setup_logger(name, log_file=None, level='INFO', detailed=False):
    """
    로거 설정
    
    Args:
        name: 로거 이름
        log_file: 로그 파일 경로 (None이면 기본 경로 사용)
        level: 로그 레벨 ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        detailed: 상세 로깅 여부
    
    Returns:
        logging.Logger: 설정된 로거 객체
    """
    logger = logging.getLogger(name)
    
    # 이미 핸들러가 설정되어 있으면 반환
    if logger.handlers:
        return logger
    
    logger.setLevel(LOG_LEVELS.get(level, logging.INFO))
    
    # 로그 포맷 선택
    formatter = logging.Formatter(DETAILED_FORMAT if detailed else LOG_FORMAT)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 파일 핸들러 (로테이션 지원)
    if log_file is None:
        log_file = os.path.join(LOG_DIR, f"{name.replace('.', '_')}.log")
    
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 에러 전용 파일 핸들러
    error_log_file = log_file.replace('.log', '_errors.log')
    error_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(DETAILED_FORMAT))
    logger.addHandler(error_handler)
    
    return logger

def get_logger(name):
    """
    기존 로거 가져오기 또는 새로 생성
    
    Args:
        name: 로거 이름
    
    Returns:
        logging.Logger: 로거 객체
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger

def log_exception(logger, exc_info=True):
    """
    예외 정보를 상세하게 로깅하는 데코레이터
    
    Args:
        logger: 로거 객체
        exc_info: 스택 트레이스 포함 여부
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    f"함수 {func.__name__}에서 예외 발생: {type(e).__name__}: {str(e)}",
                    exc_info=exc_info
                )
                raise
        return wrapper
    return decorator

# 기본 로거 설정
def setup_default_logging(level='INFO'):
    """
    기본 로깅 설정 (애플리케이션 시작 시 호출)
    
    Args:
        level: 기본 로그 레벨
    """
    # 루트 로거 설정
    logging.basicConfig(
        level=LOG_LEVELS.get(level, logging.INFO),
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                os.path.join(LOG_DIR, 'sorisay.log'),
                maxBytes=10*1024*1024,
                backupCount=5,
                encoding='utf-8'
            )
        ]
    )
    
    # 외부 라이브러리 로그 레벨 조정
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('socketio').setLevel(logging.WARNING)
    logging.getLogger('engineio').setLevel(logging.WARNING)

if __name__ == "__main__":
    # 테스트 코드
    setup_default_logging()
    logger = get_logger(__name__)
    
    logger.debug("디버그 메시지 테스트")
    logger.info("정보 메시지 테스트")
    logger.warning("경고 메시지 테스트")
    logger.error("에러 메시지 테스트")
    logger.critical("심각한 에러 메시지 테스트")
    
    print(f"✅ 로그 파일 생성됨: {LOG_DIR}/")
