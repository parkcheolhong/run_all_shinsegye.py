#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 소리새 AI 전체 테스트 실행기
모든 테스트를 실행하고 결과를 요약합니다.
"""

import sys
import os
import subprocess
import time
from datetime import datetime

# 프로젝트 루트를 PYTHONPATH에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

class TestRunner:
    def __init__(self):
        self.results = []
        self.start_time = time.time()
        
    def run_test(self, test_path, test_name):
        """개별 테스트 실행"""
        print(f"\n{'='*60}")
        print(f"🧪 실행 중: {test_name}")
        print(f"{'='*60}")
        
        try:
            # PYTHONPATH 설정하여 테스트 실행
            env = os.environ.copy()
            env['PYTHONPATH'] = project_root
            
            result = subprocess.run(
                [sys.executable, test_path],
                capture_output=True,
                text=True,
                cwd=project_root,
                env=env,
                timeout=60
            )
            
            # 출력 표시
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            
            success = result.returncode == 0
            self.results.append({
                'name': test_name,
                'path': test_path,
                'success': success,
                'returncode': result.returncode
            })
            
            status = "✅ 통과" if success else "❌ 실패"
            print(f"\n{status}: {test_name}")
            return success
            
        except subprocess.TimeoutExpired:
            print(f"⏱️ 타임아웃: {test_name}")
            self.results.append({
                'name': test_name,
                'path': test_path,
                'success': False,
                'returncode': -1,
                'error': 'timeout'
            })
            return False
        except Exception as e:
            print(f"❌ 오류: {test_name} - {str(e)}")
            self.results.append({
                'name': test_name,
                'path': test_path,
                'success': False,
                'returncode': -1,
                'error': str(e)
            })
            return False
    
    def print_summary(self):
        """테스트 결과 요약 출력"""
        elapsed = time.time() - self.start_time
        
        print("\n\n")
        print("="*70)
        print("📊 테스트 실행 결과 요약")
        print("="*70)
        print(f"⏱️  총 실행 시간: {elapsed:.2f}초")
        print(f"📝 총 테스트 수: {len(self.results)}개")
        
        passed = sum(1 for r in self.results if r['success'])
        failed = len(self.results) - passed
        
        print(f"✅ 통과: {passed}개")
        print(f"❌ 실패: {failed}개")
        print()
        
        if failed > 0:
            print("실패한 테스트:")
            for result in self.results:
                if not result['success']:
                    error_info = result.get('error', f"exit code {result['returncode']}")
                    print(f"  ❌ {result['name']} - {error_info}")
            print()
        
        print("테스트 상세 결과:")
        for i, result in enumerate(self.results, 1):
            status = "✅" if result['success'] else "❌"
            print(f"{i}. {status} {result['name']}")
        
        print("="*70)
        
        if failed == 0:
            print("🎉 모든 테스트가 통과했습니다!")
            return 0
        else:
            print(f"⚠️  {failed}개의 테스트가 실패했습니다.")
            return 1

def main():
    """메인 테스트 실행 함수"""
    print("🌟 소리새 AI 전체 테스트 스위트 실행")
    print(f"📅 실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python 버전: {sys.version}")
    print()
    
    runner = TestRunner()
    
    # 실행할 테스트 목록
    tests = [
        ('tests/test_import_paths.py', '1. Import 경로 테스트'),
        ('tests/test_error_handling.py', '2. 에러 처리 테스트'),
    ]
    
    # TTS 의존성이 필요한 테스트들 (선택적)
    optional_tests = [
        ('test_creative_probability.py', '3. 창조적 확률 테스트'),
        ('tests/test_file_check.py', '4. 파일 체크 테스트'),
        ('tests/test_nlp.py', '5. NLP 처리 테스트'),
        ('tests/test_emotion_nlp.py', '6. 감정 NLP 테스트'),
        ('tests/test_creative_sorisay.py', '7. 창조형 소리새 테스트'),
        ('tests/final_system_test.py', '8. 최종 시스템 테스트'),
    ]
    
    # 필수 테스트 실행
    print("📋 필수 테스트 실행 중...")
    for test_path, test_name in tests:
        full_path = os.path.join(project_root, test_path)
        if os.path.exists(full_path):
            runner.run_test(full_path, test_name)
        else:
            print(f"⚠️  테스트 파일을 찾을 수 없습니다: {test_path}")
    
    # 선택적 테스트 실행
    print("\n📋 선택적 테스트 실행 중 (의존성 필요)...")
    print("⚠️  일부 테스트는 시스템 의존성(예: espeak)이 필요하여 실패할 수 있습니다.")
    for test_path, test_name in optional_tests:
        full_path = os.path.join(project_root, test_path)
        if os.path.exists(full_path):
            runner.run_test(full_path, test_name)
        else:
            print(f"⚠️  테스트 파일을 찾을 수 없습니다: {test_path}")
    
    # 결과 요약
    return runner.print_summary()

if __name__ == "__main__":
    sys.exit(main())
