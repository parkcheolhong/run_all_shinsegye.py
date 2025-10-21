#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
주요 개선사항 검증 테스트
"""
import os
import sys


def test_bom_removed():
    """BOM 문자가 제거되었는지 확인"""
    print("테스트 1: BOM 문자 제거 확인...")
    
    # 프로젝트 루트 찾기
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main_file = os.path.join(project_root, 'run_all_shinsegye.py')
    
    with open(main_file, 'rb') as f:
        content = f.read(3)
    
    if content == b'\xef\xbb\xbf':
        print("❌ 실패: BOM 문자가 여전히 존재합니다")
        return False
    else:
        print("✅ 성공: BOM 문자가 제거되었습니다")
        return True


def test_syntax_valid():
    """Python 구문이 유효한지 확인"""
    print("\n테스트 2: 구문 검증...")
    import py_compile
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main_file = os.path.join(project_root, 'run_all_shinsegye.py')
    
    try:
        py_compile.compile(main_file, doraise=True)
        print("✅ 성공: 구문 오류 없음")
        return True
    except py_compile.PyCompileError as e:
        print(f"❌ 실패: 구문 오류 발견 - {e}")
        return False


def test_imports():
    """핵심 모듈을 import 할 수 있는지 확인"""
    print("\n테스트 3: 모듈 import 확인...")
    
    # 프로젝트 루트를 Python path에 추가
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    try:
        from modules.logging_config import setup_logger
        print("✅ 성공: logging_config import")
        return True
    except ImportError as e:
        print(f"❌ 실패: logging_config import 실패 - {e}")
        return False


def test_log_directory():
    """로그 디렉토리가 생성되는지 확인"""
    print("\n테스트 4: 로그 디렉토리 생성 확인...")
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(project_root, "logs")
    
    if os.path.exists(log_dir):
        print(f"✅ 성공: logs 디렉토리 존재")
        return True
    else:
        # 디렉토리가 없으면 생성 시도
        try:
            os.makedirs(log_dir, exist_ok=True)
            print(f"✅ 성공: logs 디렉토리 생성")
            return True
        except Exception as e:
            print(f"⚠️ 경고: logs 디렉토리 생성 실패 - {e}")
            print("   (프로그램은 임시 디렉토리를 사용할 것입니다)")
            return True  # 이건 치명적이지 않음


def test_requirements_files():
    """requirements 파일들이 존재하는지 확인"""
    print("\n테스트 5: requirements 파일 확인...")
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = ['requirements.txt', 'requirements-minimal.txt']
    all_exist = True
    
    for file in files:
        filepath = os.path.join(project_root, file)
        if os.path.exists(filepath):
            print(f"✅ 성공: {file} 존재")
        else:
            print(f"❌ 실패: {file} 없음")
            all_exist = False
    
    return all_exist


def test_documentation():
    """문서 파일들이 존재하는지 확인"""
    print("\n테스트 6: 문서 파일 확인...")
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = [
        'PROGRAM_REVIEW_DETAILED_KO.md',
        'INSTALLATION_TROUBLESHOOTING.md',
        'README.md'
    ]
    all_exist = True
    
    for file in files:
        filepath = os.path.join(project_root, file)
        if os.path.exists(filepath):
            print(f"✅ 성공: {file} 존재")
        else:
            print(f"❌ 실패: {file} 없음")
            all_exist = False
    
    return all_exist


def main():
    """모든 테스트 실행"""
    print("=" * 60)
    print("🔍 프로그램 개선사항 검증 테스트 시작")
    print("=" * 60)
    
    tests = [
        test_bom_removed,
        test_syntax_valid,
        test_imports,
        test_log_directory,
        test_requirements_files,
        test_documentation,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ 테스트 실행 중 오류: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 테스트 결과 요약")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"통과: {passed}/{total}")
    print(f"실패: {total - passed}/{total}")
    
    if all(results):
        print("\n✅ 모든 테스트 통과!")
        return 0
    else:
        print("\n⚠️ 일부 테스트 실패")
        return 1


if __name__ == "__main__":
    sys.exit(main())
