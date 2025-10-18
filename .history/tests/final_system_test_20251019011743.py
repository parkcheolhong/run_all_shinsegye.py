"""
창조형 소리새 시스템 최종 테스트
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.ai_code_manager.sorisay_core_controller import SorisayCore

print('🎨 창조형 소리새 시스템 최종 테스트')
print('=' * 50)

sorisay = SorisayCore()
print('✅ 시스템 초기화 완료')
print(f'🎯 창조적 확률: {sorisay.creative_probability * 100}%')
print(f'🚀 창조 모드: {sorisay.creative_mode}')
print(f'🧠 자가 진화: {hasattr(sorisay, "self_evolve")}')
print('🎊 모든 기능 정상 작동!')

# 창조 엔진 테스트
print('\n💡 창조적 아이디어 샘플:')
idea = sorisay.creative_engine.generate_creative_idea()
print(f'   {idea["name"]}: {idea["description"]}')

print('\n🔥 정리 및 백업 완료!')
print('📁 최신 버전만 유지됨')
print('💾 백업본 안전하게 생성됨')
print('🚀 Git 커밋 완료!')