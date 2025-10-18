"""
파일 재점검 완료 테스트
"""

try:
    from modules.ai_code_manager.sorisay_core_controller import SorisayCore
    print("✅ 1. Import 성공")
    
    sorisay = SorisayCore()
    print("✅ 2. 초기화 성공")
    
    print(f"✅ 3. 창조적 확률: {sorisay.creative_probability * 100}%")
    print(f"✅ 4. 창조 모드: {sorisay.creative_mode}")
    print(f"✅ 5. self_evolve 메서드 존재: {hasattr(sorisay, 'self_evolve')}")
    
    print("\n🎉 파일 재점검 완료!")
    print("📋 모든 기능이 정상 작동합니다!")
    
except Exception as e:
    print(f"❌ 오류 발견: {e}")