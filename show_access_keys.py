#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔑 접속키 빠른 확인 도구
프로그램 접속에 필요한 키를 빠르게 확인할 수 있습니다.
"""

import json
import os
import sys

def display_access_info():
    """접속 정보 표시"""
    print("=" * 60)
    print("🔑 소리새 AI 접속 정보")
    print("=" * 60)
    
    config_path = "config/security_config.json"
    
    if not os.path.exists(config_path):
        print("❌ 보안 설정 파일을 찾을 수 없습니다.")
        print(f"   경로: {config_path}")
        return False
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # 대시보드 URL
        network = config.get("network", {})
        port = network.get("port", 5050)
        bind_addr = network.get("bind_address", "127.0.0.1")
        
        print(f"\n🌐 웹 대시보드 주소:")
        print(f"   http://{bind_addr}:{port}")
        
        # 추천 접속키
        api_keys = config.get("security", {}).get("api_keys", {})
        
        print(f"\n✨ 추천 접속키 (일반 사용자):")
        if "user_key" in api_keys:
            user_key = api_keys["user_key"]
            print(f"   http://{bind_addr}:{port}?api_key={user_key}")
        
        print(f"\n📋 사용 가능한 접속키:")
        
        # 사용자 키
        print("\n   🟢 일반 사용자 키 (추천):")
        for key_name, key_value in api_keys.items():
            if "user" in key_name.lower() and "guest" not in key_name.lower():
                print(f"      • {key_name}: {key_value}")
        
        # 관리자 키
        print("\n   🟡 관리자 키:")
        for key_name, key_value in api_keys.items():
            if "admin" in key_name.lower():
                print(f"      • {key_name}: {key_value}")
        
        # 마스터 키
        print("\n   🔴 마스터 키 (시스템 관리자):")
        for key_name, key_value in api_keys.items():
            if "master" in key_name.lower():
                print(f"      • {key_name}: {key_value}")
        
        # 게스트 키
        print("\n   🔵 게스트 키 (읽기 전용):")
        for key_name, key_value in api_keys.items():
            if "guest" in key_name.lower():
                print(f"      • {key_name}: {key_value}")
        
        # 토큰
        tokens = config.get("security", {}).get("access_tokens", {})
        if tokens:
            print(f"\n🎫 액세스 토큰:")
            for token_name, token_value in tokens.items():
                print(f"      • {token_name}: {token_value}")
        
        print("\n" + "=" * 60)
        print("💡 사용 방법:")
        print("   1. 위의 접속키 중 하나를 복사하세요")
        print("   2. 브라우저에서 접속 URL을 열거나")
        print("   3. 대시보드에서 '🔑 인증' 버튼을 클릭하여 키를 입력하세요")
        print("=" * 60)
        
        print("\n📖 자세한 정보: ACCESS_KEYS.md 파일을 참고하세요")
        print("🔧 키 관리: python security_key_manager.py --help")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ 설정 파일 형식 오류: {e}")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = display_access_info()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 종료합니다.")
        sys.exit(0)
