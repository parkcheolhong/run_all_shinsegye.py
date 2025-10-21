#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
네트워크 연결 테스트 스크립트
Google Speech Recognition API 접근성 진단
"""

import sys
import socket
import urllib.request
import urllib.error

def test_network():
    """네트워크 연결 및 Google API 접근성 테스트"""
    print("=" * 60)
    print("🌐 소리새 AI 네트워크 진단 도구")
    print("=" * 60)
    print()
    
    all_tests_passed = True
    
    # 1. DNS 확인
    print("📋 1단계: DNS 해석 테스트")
    print("-" * 60)
    try:
        ip = socket.gethostbyname("www.google.com")
        print(f"✅ DNS 정상 작동")
        print(f"   www.google.com → {ip}")
        print()
    except socket.gaierror as e:
        print(f"❌ DNS 해석 실패: {e}")
        print("   해결 방법:")
        print("   1. 인터넷 연결 확인")
        print("   2. DNS 서버 설정 확인 (8.8.8.8 또는 1.1.1.1)")
        print("   3. 네트워크 케이블/WiFi 연결 확인")
        print()
        all_tests_passed = False
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        print()
        all_tests_passed = False
    
    # 2. 기본 인터넷 연결 확인
    print("📋 2단계: 기본 인터넷 연결 테스트")
    print("-" * 60)
    try:
        response = urllib.request.urlopen("https://www.google.com", timeout=5)
        status = response.getcode()
        print(f"✅ 인터넷 연결 정상")
        print(f"   상태 코드: {status}")
        print()
    except urllib.error.URLError as e:
        print(f"❌ 인터넷 연결 실패: {e}")
        print("   해결 방법:")
        print("   1. WiFi/이더넷 연결 확인")
        print("   2. 프록시 설정 확인")
        print("   3. 방화벽 설정 확인")
        print()
        all_tests_passed = False
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        print()
        all_tests_passed = False
    
    # 3. Google API 접근 테스트
    print("📋 3단계: Google API 접근 테스트")
    print("-" * 60)
    try:
        # Google Speech API 엔드포인트 확인
        response = urllib.request.urlopen(
            "https://speech.googleapis.com", 
            timeout=5
        )
        print("✅ Google Speech API 접근 가능")
        print(f"   상태 코드: {response.getcode()}")
        print()
    except urllib.error.HTTPError as e:
        # 401/403 오류는 정상 (인증이 필요하지만 접근은 가능)
        if e.code in [401, 403, 404]:
            print("✅ Google Speech API 접근 가능")
            print(f"   상태 코드: {e.code} (정상 - API 엔드포인트 존재)")
            print()
        else:
            print(f"⚠️  예상치 못한 HTTP 오류: {e.code}")
            print("   하지만 API에 접근은 가능할 수 있습니다.")
            print()
    except urllib.error.URLError as e:
        print(f"❌ Google Speech API 접근 불가: {e}")
        print("   해결 방법:")
        print("   1. 방화벽에서 HTTPS(443 포트) 허용")
        print("   2. 프록시 설정 확인")
        print("   3. 회사/학교 네트워크의 경우 IT 부서에 문의")
        print()
        all_tests_passed = False
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        print()
        all_tests_passed = False
    
    # 4. 포트 443 (HTTPS) 확인
    print("📋 4단계: HTTPS 포트(443) 연결 테스트")
    print("-" * 60)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(("www.google.com", 443))
        sock.close()
        
        if result == 0:
            print("✅ HTTPS 포트(443) 연결 가능")
            print()
        else:
            print(f"❌ HTTPS 포트(443) 연결 실패 (코드: {result})")
            print("   해결 방법:")
            print("   1. 방화벽 설정 확인")
            print("   2. 안티바이러스 소프트웨어 예외 추가")
            print("   3. 네트워크 관리자에게 문의")
            print()
            all_tests_passed = False
    except Exception as e:
        print(f"❌ 포트 테스트 실패: {e}")
        print()
        all_tests_passed = False
    
    # 5. 프록시 설정 확인
    print("📋 5단계: 프록시 설정 확인")
    print("-" * 60)
    import os
    http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    
    if http_proxy or https_proxy:
        print("⚠️  프록시 설정이 감지되었습니다:")
        if http_proxy:
            print(f"   HTTP_PROXY: {http_proxy}")
        if https_proxy:
            print(f"   HTTPS_PROXY: {https_proxy}")
        print()
        print("   프록시 환경에서 작동하지 않는 경우:")
        print("   1. 프록시 설정이 올바른지 확인")
        print("   2. 프록시 인증이 필요한지 확인")
        print("   3. 프록시 우회 설정 확인")
        print()
    else:
        print("✅ 프록시 설정 없음 (직접 연결)")
        print()
    
    # 최종 결과
    print("=" * 60)
    if all_tests_passed:
        print("✅ 모든 네트워크 테스트 통과!")
        print("=" * 60)
        print()
        print("🎉 Google Speech Recognition API를 사용할 수 있습니다!")
        print("   소리새 AI의 음성 인식이 정상적으로 작동할 것입니다.")
        print()
    else:
        print("❌ 일부 네트워크 테스트 실패")
        print("=" * 60)
        print()
        print("⚠️  음성 인식에 문제가 발생할 수 있습니다.")
        print("   위의 해결 방법을 따라 문제를 해결하세요.")
        print("   또는 VOICE_TROUBLESHOOTING_GUIDE.md를 참조하세요.")
        print()
    
    return all_tests_passed


def main():
    """메인 함수"""
    try:
        success = test_network()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  테스트가 사용자에 의해 중단되었습니다.")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ 치명적인 오류 발생: {e}")
        print("   VOICE_TROUBLESHOOTING_GUIDE.md를 참조하세요.")
        sys.exit(1)


if __name__ == "__main__":
    main()
