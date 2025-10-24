"""
Import 경로 테스트 - 의존성 없이 실행 가능
"""
import sys
import os

# 프로젝트 루트를 PYTHONPATH에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🔍 Import 경로 테스트")
print("=" * 50)

# 1. 모듈 존재 확인
test_results = []

try:
    import modules
    test_results.append(("modules 패키지", True, ""))
except ImportError as e:
    test_results.append(("modules 패키지", False, str(e)))

try:
    import modules.ai_code_manager
    test_results.append(("modules.ai_code_manager 패키지", True, ""))
except ImportError as e:
    test_results.append(("modules.ai_code_manager 패키지", False, str(e)))

# 2. 주요 모듈 파일 존재 확인
module_files = [
    "modules/ai_code_manager/sorisay_core_controller.py",
    "modules/ai_code_manager/nlp_processor.py",
    "modules/ai_code_manager/creative_sorisay_engine.py",
    "modules/ai_code_manager/persona_system.py",
    "modules/ai_code_manager/memory_palace.py",
]

for module_file in module_files:
    exists = os.path.exists(module_file)
    test_results.append((module_file, exists, "" if exists else "파일이 존재하지 않음"))

# 3. 중복 파일 제거 확인
duplicate_files = [
    "sorisay_core_controller.py",
    "nlp_processor.py",
    "config/sorisay_core_controller.py",
    "config/nlp_processor.py",
    "modules/nlp_processor.py",
]

for dup_file in duplicate_files:
    exists = os.path.exists(dup_file)
    test_results.append((f"중복 제거: {dup_file}", not exists, "아직 존재함" if exists else ""))

# 결과 출력
passed = 0
failed = 0

for test_name, success, error_msg in test_results:
    if success:
        print(f"✅ {test_name}")
        passed += 1
    else:
        print(f"❌ {test_name}: {error_msg}")
        failed += 1

print("\n" + "=" * 50)
print(f"📊 결과: {passed}개 성공, {failed}개 실패")

if failed == 0:
    print("🎉 모든 테스트 통과!")
else:
    print(f"⚠️ {failed}개 테스트 실패")
    sys.exit(1)
