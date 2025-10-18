#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 소리새 AI 보안 시스템 최적화 데모
빠른 보안 테스트와 API 키 관리
"""

import json
import secrets
import string
from datetime import datetime
import hashlib

class OptimizedSecurityDemo:
    def __init__(self):
        self.api_keys = {}
        self.permissions = {}
        self.session_tokens = {}
        
    def generate_secure_key(self, key_type="user", length=32):
        """최적화된 보안 키 생성"""
        # 암호학적으로 안전한 랜덤 생성
        random_part = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
        timestamp = datetime.now().strftime("%Y%m%d")
        
        # 해시 기반 체크섬 추가
        raw_key = f"sorisay_{key_type}_{timestamp}_{random_part}"
        checksum = hashlib.sha256(raw_key.encode()).hexdigest()[:8]
        
        return f"{raw_key}_{checksum}"
    
    def setup_optimized_security(self):
        """최적화된 보안 설정"""
        print("🚀 최적화된 보안 시스템 초기화...")
        
        # 강화된 API 키 생성
        self.api_keys = {
            "master": self.generate_secure_key("master", 40),
            "admin": self.generate_secure_key("admin", 32),
            "user": self.generate_secure_key("user", 24),
            "guest": self.generate_secure_key("guest", 16)
        }
        
        # 세분화된 권한 시스템
        self.permissions = {
            "master": ["all", "system", "security", "admin"],
            "admin": ["dashboard", "commands", "config", "logs", "users"],
            "user": ["dashboard", "commands", "basic"],
            "guest": ["dashboard", "readonly"]
        }
        
        # 세션 토큰 생성
        for role in self.api_keys.keys():
            token = secrets.token_urlsafe(32)
            self.session_tokens[f"{role}_session"] = token
        
        print("✅ 보안 시스템 초기화 완료!")
        return True
    
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