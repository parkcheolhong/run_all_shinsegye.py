#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 소리새 AI 보안 시스템 데모
키 생성, 검증, 권한 확인 기능을 시연합니다.
"""

import json
import os
from security_key_manager import SecurityKeyManager

def demo_security_system():
    print("🔐 소리새 AI 보안 시스템 데모")
    print("=" * 50)
    
    # 키 매니저 초기화
    manager = SecurityKeyManager()
    
    print("\n1️⃣ 현재 보안 설정 상태:")
    print("-" * 30)
    
    # 현재 설정 확인
    manager.list_credentials()
    
    print("\n2️⃣ 새 사용자 키 생성 데모:")
    print("-" * 30)
    
    # 새 사용자 키 생성
    demo_key = manager.add_api_key("demo_user", "user")
    
    print("\n3️⃣ 키 검증 테스트:")
    print("-" * 30)
    
    # 키 검증
    if manager.verify_credential(demo_key):
        print("✅ 키 검증 성공!")
    else:
        print("❌ 키 검증 실패!")
    
    # 잘못된 키 테스트
    print("\n4️⃣ 잘못된 키 테스트:")
    print("-" * 30)
    if manager.verify_credential("wrong_key_123"):
        print("❌ 보안 취약점 발견!")
    else:
        print("✅ 잘못된 키 올바르게 거부됨")
    
    print("\n5️⃣ 권한 시스템 테스트:")
    print("-" * 30)
    
    # 다양한 권한 레벨 키 생성
    permission_keys = {}
    for level in ['guest', 'user', 'admin']:
        key = manager.add_api_key(f"demo_{level}", level)
        permission_keys[level] = key
    
    # 권한 확인
    for level, key in permission_keys.items():
        permissions = manager.config["security"]["permissions"].get(f"demo_{level}_key", [])
        print(f"📋 {level.upper()} 권한: {permissions}")
    
    print("\n6️⃣ 보안 통계:")
    print("-" * 30)
    
    total_keys = len(manager.config["security"]["api_keys"])
    total_tokens = len(manager.config["security"]["access_tokens"])
    
    print(f"🔑 총 API 키: {total_keys}개")
    print(f"🎫 총 토큰: {total_tokens}개")
    print(f"🛡️ 보안 수준: {'높음' if total_keys >= 4 else '보통'}")
    
    # 설정 저장
    manager.save_config()
    
    print("\n7️⃣ 정리 옵션:")
    print("-" * 30)
    cleanup = input("데모 키들을 정리하시겠습니까? (y/N): ")
    if cleanup.lower() == 'y':
        demo_keys = ["demo_user_key", "demo_guest_key", "demo_user_key", "demo_admin_key"]
        for key_name in demo_keys:
            try:
                manager.revoke_key(key_name)
            except:
                pass
        manager.save_config()
        print("🧹 데모 키 정리 완료")
    
    print("\n✅ 보안 시스템 데모 완료!")
    print("\n📚 더 자세한 사용법은 SECURITY_GUIDE.md를 참고하세요.")

if __name__ == "__main__":
    demo_security_system()