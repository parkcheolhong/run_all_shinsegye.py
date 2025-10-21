# Docker 실행 가이드 (Docker Run Guide)

## 🐳 Docker를 사용한 실행

### 전제 조건
- Docker가 설치되어 있어야 합니다
- Docker Compose가 설치되어 있어야 합니다

**참고**: Docker 이미지에는 TTS(Text-to-Speech)를 위한 espeak/espeak-ng가 포함되어 있습니다.

### 실행 방법

#### 1. Docker Compose를 사용한 실행 (권장)

```bash
# 이미지 빌드 및 컨테이너 실행
docker compose up -d

# 로그 확인
docker compose logs -f sorisae

# 중지
docker compose down
```

#### 2. Docker 직접 실행

```bash
# 이미지 빌드
docker build -t parkcheolhong/sorisae:v1 .

# 컨테이너 실행
docker run -d -p 5050:5050 --name sorisae parkcheolhong/sorisae:v1

# 로그 확인
docker logs -f sorisae

# 중지 및 제거
docker stop sorisae
docker rm sorisae
```

### 웹 대시보드 접속

컨테이너가 실행되면 웹 브라우저에서 다음 주소로 접속:
- http://localhost:5050
- http://127.0.0.1:5050

**참고**: 웹 대시보드는 이제 Docker 환경에서 정상적으로 접근 가능합니다. 서버는 `0.0.0.0:5050`에 바인딩되어 호스트 머신에서 접근할 수 있습니다.

### 환경 변수

docker-compose.yml에서 다음 환경 변수가 설정됩니다:
- `PYTHONUNBUFFERED=1`: Python 출력 버퍼링 비활성화

### 주의사항

⚠️ **음성 인식 기능**: Docker 컨테이너 내에서 마이크 접근이 제한될 수 있습니다. 완전한 음성 인식 기능을 사용하려면 호스트 시스템에서 직접 실행하는 것을 권장합니다.

### 문제 해결

#### 웹 대시보드 접속 불가
만약 `http://localhost:5050`으로 접속이 안 되는 경우:
1. Docker 컨테이너가 실행 중인지 확인: `docker ps`
2. 포트가 올바르게 매핑되었는지 확인: `docker port sorisae`
3. 컨테이너 로그 확인: `docker logs sorisae`
4. 방화벽이 5050 포트를 차단하고 있는지 확인

**최근 수정사항**: 웹 대시보드가 `127.0.0.1`이 아닌 `0.0.0.0`에 바인딩되도록 수정되어 Docker 환경에서 정상적으로 접근 가능합니다.

#### 포트 충돌
```bash
# 다른 포트로 실행하려면 docker-compose.yml 수정
ports:
  - "8080:5050"  # 호스트 포트를 8080으로 변경
```

#### 컨테이너 재시작
```bash
docker compose restart sorisae
```

#### 전체 재빌드
```bash
docker compose build --no-cache
docker compose up -d
```
