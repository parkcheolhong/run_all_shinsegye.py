#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 소리새 AI 보안 시스템 종합 테스트
API 키, 토큰, 권한 시스템의 모든 기능을 테스트합니다.
"""

import requests
import json
import time
from security_key_manager import SecurityKeyManager

class SecurityTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.manager = SecurityKeyManager()
        self.test_results = []
    
    def log_test(self, test_name, success, message):
        """테스트 결과 로깅"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"{status} {test_name}: {message}"
        print(result)
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
    
    def test_api_key_creation(self):
        """API 키 생성 테스트"""
        try:
            # 테스트용 API 키 생성
            test_key = self.manager.add_api_key("test_user", "user")
            self.log_test("API 키 생성", True, f"키 생성 성공: {test_key[:20]}...")
            return test_key
        except Exception as e:
            self.log_test("API 키 생성", False, f"오류: {str(e)}")
            return None
    
    def test_token_creation(self):
        """토큰 생성 테스트"""
        try:
            # 테스트용 토큰 생성
            test_token = self.manager.add_token("test_user", "user")
            self.log_test("토큰 생성", True, f"토큰 생성 성공: {test_token[:20]}...")
            return test_token
        except Exception as e:
            self.log_test("토큰 생성", False, f"오류: {str(e)}")
            return None
    
    def test_dashboard_access(self):
        """대시보드 접근 테스트"""
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code == 200:
                self.log_test("대시보드 접근", True, "대시보드 정상 접근")
            else:
                self.log_test("대시보드 접근", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("대시보드 접근", False, f"연결 오류: {str(e)}")
    
    def test_auth_verification(self, credential):
        """인증 검증 테스트"""
        try:
            headers = {'X-API-Key': credential}
            response = requests.get(f"{self.base_url}/api/auth/verify", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('valid'):
                    permissions = data.get('permissions', [])
                    self.log_test("인증 검증", True, f"인증 성공, 권한: {permissions}")
                    return True
                else:
                    self.log_test("인증 검증", False, "인증 실패")
                    return False
            else:
                self.log_test("인증 검증", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("인증 검증", False, f"오류: {str(e)}")
            return False
    
    def test_invalid_auth(self):
        """잘못된 인증 정보 테스트"""
        try:
            headers = {'X-API-Key': 'invalid_key_123'}
            response = requests.get(f"{self.base_url}/api/auth/verify", headers=headers)
            
            if response.status_code == 401:
                self.log_test("잘못된 인증", True, "잘못된 키 올바르게 거부됨")
            else:
                data = response.json()
                if not data.get('valid'):
                    self.log_test("잘못된 인증", True, "잘못된 키 올바르게 거부됨")
                else:
                    self.log_test("잘못된 인증", False, "잘못된 키가 통과됨 (보안 취약)")
        except Exception as e:
            self.log_test("잘못된 인증", False, f"오류: {str(e)}")
    
    def test_protected_endpoints(self, credential):
        """보호된 엔드포인트 테스트"""
        try:
            headers = {'X-API-Key': credential}
            response = requests.get(f"{self.base_url}/api/stats", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("보호된 엔드포인트", True, f"통계 API 접근 성공: {len(data)} 항목")
            else:
                self.log_test("보호된 엔드포인트", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("보호된 엔드포인트", False, f"오류: {str(e)}")
    
    def test_permission_levels(self):
        """권한 레벨 테스트"""
        try:
            # 다양한 권한 레벨의 키 생성 및 테스트
            test_keys = {
                "guest": self.manager.add_api_key("test_guest", "guest"),
                "user": self.manager.add_api_key("test_user_2", "user"),
                "admin": self.manager.add_api_key("test_admin", "admin")
            }
            
            for level, key in test_keys.items():
                if self.test_auth_verification(key):
                    self.log_test(f"{level.upper()} 권한", True, f"{level} 레벨 인증 성공")
                else:
                    self.log_test(f"{level.upper()} 권한", False, f"{level} 레벨 인증 실패")
                    
        except Exception as e:
            self.log_test("권한 레벨", False, f"오류: {str(e)}")
    
    def test_key_listing(self):
        """키 목록 테스트"""
        try:
            print("\n🔐 현재 등록된 인증 정보:")
            self.manager.list_credentials()
            self.log_test("키 목록", True, "키 목록 출력 성공")
        except Exception as e:
            self.log_test("키 목록", False, f"오류: {str(e)}")
    
    def cleanup_test_keys(self):
        """테스트 키 정리"""
        test_keys = [
            "test_user_key", "test_user_token",
            "test_guest_key", "test_user_2_key", "test_admin_key"
        ]
        
        for key_name in test_keys:
            try:
                self.manager.revoke_key(key_name)
            except:
                pass  # 키가 없어도 무시
        
        self.manager.save_config()
        print("🧹 테스트 키 정리 완료")
    
    def run_all_tests(self):
        """모든 테스트 실행"""
        print("🚀 소리새 AI 보안 시스템 종합 테스트 시작")
        print("=" * 60)
        
        # 1. 키 생성 테스트
        test_api_key = self.test_api_key_creation()
        test_token = self.test_token_creation()
        
        # 2. 대시보드 접근 테스트
        self.test_dashboard_access()
        
        # 3. 인증 테스트
        if test_api_key:
            self.test_auth_verification(test_api_key)
            self.test_protected_endpoints(test_api_key)
        
        # 4. 보안 테스트
        self.test_invalid_auth()
        
        # 5. 권한 레벨 테스트
        self.test_permission_levels()
        
        # 6. 키 목록 테스트
        self.test_key_listing()
        
        # 설정 저장
        self.manager.save_config()
        
        # 결과 요약
        self.print_test_summary()
        
        # 정리 옵션
        cleanup = input("\n🧹 테스트 키를 정리하시겠습니까? (y/N): ")
        if cleanup.lower() == 'y':
            self.cleanup_test_keys()
    
    def print_test_summary(self):
        """테스트 결과 요약"""
        print("\n📊 테스트 결과 요약")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"총 테스트: {total_tests}")
        print(f"✅ 성공: {passed_tests}")
        print(f"❌ 실패: {failed_tests}")
        print(f"📈 성공률: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ 실패한 테스트:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['message']}")
        
        print("\n🔒 보안 상태 평가:")
        if passed_tests >= total_tests * 0.8:
            print("   ✅ 우수 - 보안 시스템이 올바르게 작동합니다")
        elif passed_tests >= total_tests * 0.6:
            print("   ⚠️ 보통 - 일부 개선이 필요합니다")
        else:
            print("   ❌ 취약 - 보안 시스템에 문제가 있습니다")

def main():
    print("🧪 소리새 AI 보안 테스트 도구")
    print("대시보드가 실행 중인지 확인해주세요 (http://localhost:5000)")
    
    input("준비되면 Enter를 누르세요...")
    
    tester = SecurityTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()