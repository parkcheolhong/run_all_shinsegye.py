# 테스트 실행 가이드 (Test Execution Guide)

## 🚀 빠른 시작 (Quick Start)

### 전체 테스트 실행
```bash
# 모든 테스트를 한 번에 실행
python run_all_tests.py
```

### pytest 사용
```bash
# pytest로 테스트 실행
pytest tests/ -v

# 특정 테스트만 실행
pytest tests/test_import_paths.py -v

# 커버리지와 함께 실행 (pytest-cov 설치 필요)
pytest tests/ --cov=modules --cov-report=html
```

### 개별 테스트 실행
```bash
# Import 경로 테스트
python tests/test_import_paths.py

# 에러 처리 테스트
python tests/test_error_handling.py

# NLP 테스트
python tests/test_nlp.py

# 감정 NLP 테스트
python tests/test_emotion_nlp.py
```

## 📋 테스트 목록

### ✅ 의존성 없이 실행 가능한 테스트
1. **test_import_paths.py** - 모듈 import 검증
2. **test_error_handling.py** - 로깅 및 에러 핸들링

### ⚠️ 부분 의존성이 필요한 테스트
3. **test_file_check.py** - 파일 및 기능 존재 확인
4. **test_nlp.py** - 자연어 처리
5. **test_emotion_nlp.py** - 감정 분석

### 🔊 TTS 엔진 필요 (espeak)
6. **test_creative_probability.py** - 창조적 확률 테스트
7. **final_system_test.py** - 최종 시스템 테스트

## 🔧 사전 준비사항

### Python 패키지 설치
```bash
pip install -r requirements.txt
```

### 시스템 의존성 (선택사항)
음성 합성(TTS) 기능을 테스트하려면 espeak 설치가 필요합니다:

**Ubuntu/Debian:**
```bash
sudo apt-get install espeak espeak-ng
```

**macOS:**
```bash
brew install espeak
```

**Windows:**
- [eSpeak 다운로드](https://espeak.sourceforge.net/)

## 📊 테스트 결과 확인

### 실행 후 생성되는 파일
- `TEST_RESULTS_REPORT.md` - 상세 테스트 결과 보고서
- `logs/test_file_logger.log` - 테스트 로그 파일
- `logs/test_file_logger_errors.log` - 에러 로그 파일

### 결과 요약
실행이 완료되면 다음과 같은 요약이 표시됩니다:
```
📊 테스트 실행 결과 요약
========================================
⏱️  총 실행 시간: X.XX초
📝 총 테스트 수: 8개
✅ 통과: 5개
❌ 실패: 3개
```

## 🐛 문제 해결

### "ModuleNotFoundError: No module named 'speech_recognition'"
```bash
pip install speechrecognition
```

### "RuntimeError: This means you probably do not have eSpeak or eSpeak-ng installed!"
이 오류는 TTS 엔진이 없을 때 발생합니다. 위의 시스템 의존성 섹션을 참고하세요.

### "AttributeError: 'CreativeSorisayEngine' object has no attribute 'web_search_and_learn'"
이는 알려진 문제로, 해당 메서드가 아직 구현되지 않았습니다.

## 🔄 CI/CD 통합

### GitHub Actions 예시
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y espeak espeak-ng
      - name: Install Python dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python run_all_tests.py
```

## 📝 테스트 작성 가이드

새로운 테스트를 추가할 때는:

1. `tests/` 디렉토리에 `test_*.py` 파일 생성
2. 필요한 경우 `sys.path` 설정:
   ```python
   import sys
   import os
   sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
   ```
3. 테스트 함수 또는 스크립트 작성
4. `run_all_tests.py`의 테스트 목록에 추가

## 🔗 관련 문서
- [README.md](README.md) - 프로젝트 개요
- [TEST_RESULTS_REPORT.md](TEST_RESULTS_REPORT.md) - 최신 테스트 결과
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 문제 해결 가이드

---

**마지막 업데이트**: 2025-10-21  
**테스트 버전**: 1.0.0
