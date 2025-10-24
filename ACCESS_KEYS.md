# 🔑 소리새 AI 접속키 안내 (Access Keys Guide)

## 📌 빠른 접속 방법

프로그램에 접속할 수 없다면, 아래 명령어로 접속키를 확인하세요:

```bash
python security_key_manager.py show-all
```

## 🌐 웹 대시보드 접속 방법

### 방법 1: URL에 API 키 포함 (추천)

브라우저에서 다음과 같이 접속하세요:

```
http://localhost:5050?api_key=YOUR_API_KEY
```

**예시 (사용자 키 사용):**
```
http://localhost:5050?api_key=sorisay_user_2025_key_ijkl9012
```

### 방법 2: 대시보드에서 직접 입력

1. 브라우저에서 `http://localhost:5050` 접속
2. 우측 상단 "🔑 인증" 버튼 클릭
3. API 키 입력 후 "✅ 인증" 버튼 클릭

## 🔐 기본 제공 접속키

### 🔴 마스터 키 (Master Key)
- **키**: `sorisay_master_2025_secure_key_abcd1234`
- **권한**: 모든 기능 접근 가능
- **사용 용도**: 시스템 관리자

### 🟡 관리자 키 (Admin Key)
- **키**: `sorisay_admin_2025_key_efgh5678`
- **권한**: 대시보드, 명령, 설정, 로그
- **사용 용도**: 일반 관리 작업

### 🟢 사용자 키 (User Key)
- **키**: `sorisay_user_2025_key_ijkl9012`
- **권한**: 대시보드, 명령
- **사용 용도**: 일반 사용자 (추천)

### 🔵 게스트 키 (Guest Key)
- **키**: `sorisay_guest_2025_key_mnop3456`
- **권한**: 대시보드 읽기 전용
- **사용 용도**: 관람 모드

## 🎫 액세스 토큰 사용

API 키 대신 토큰을 사용할 수도 있습니다:

```
http://localhost:5050?token=YOUR_TOKEN
```

**예시 (사용자 토큰 사용):**
```
http://localhost:5050?token=USR_tok_2025_ghi012jkl345mno678
```

## 🛠️ 키 관리 명령어

### 모든 키 목록 보기 (짧게)
```bash
python security_key_manager.py list
```

### 모든 키 전체 값 보기
```bash
python security_key_manager.py show-all
```

### 새 사용자 키 생성
```bash
python security_key_manager.py add-key --name myuser --type user
```

### 새 관리자 키 생성
```bash
python security_key_manager.py add-key --name myadmin --type admin
```

### 키 검증
```bash
python security_key_manager.py verify --credential "sorisay_user_2025_key_ijkl9012"
```

### 키 폐기
```bash
python security_key_manager.py revoke --name user_key
```

## ❓ 문제 해결

### Q1: "프로그램에 접속할 수 없어요"

**해결 방법:**
1. 프로그램이 실행 중인지 확인
   ```bash
   python run_all_shinsegye.py
   ```
2. 브라우저에서 접속키와 함께 접속
   ```
   http://localhost:5050?api_key=sorisay_user_2025_key_ijkl9012
   ```

### Q2: "접속키가 없어진 것 같아요"

**해결 방법:**
접속키는 `config/security_config.json` 파일에 저장되어 있습니다. 다음 명령으로 확인하세요:
```bash
python security_key_manager.py show-all
```

### Q3: "접속키가 바뀐 것 같아요"

**해결 방법:**
기본 키는 변경되지 않습니다. 위의 `show-all` 명령으로 현재 등록된 모든 키를 확인할 수 있습니다.

### Q4: "새 키를 만들고 싶어요"

**해결 방법:**
```bash
# 사용자 키 생성
python security_key_manager.py add-key --name mynewuser --type user

# 생성된 키는 자동으로 표시됩니다
```

## 🔒 보안 주의사항

⚠️ **중요**: 접속키는 비밀번호와 같습니다!

- ❌ 공개 저장소에 키를 올리지 마세요
- ❌ 다른 사람과 키를 공유하지 마세요
- ✅ 필요 시 새 키를 생성하여 사용하세요
- ✅ 사용하지 않는 키는 폐기하세요

## 📞 추가 지원

더 자세한 보안 가이드는 [SECURITY_GUIDE.md](./SECURITY_GUIDE.md)를 참고하세요.

---

**마지막 업데이트**: 2025-10-21
