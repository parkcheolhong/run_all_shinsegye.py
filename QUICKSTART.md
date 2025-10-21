# Quick Reference - run_all_shinsegye.py

## 🆘 접속 문제? 빠른 해결

**프로그램에 접속할 수 없나요?**

```bash
# 접속키 빠르게 확인
python show_access_keys.py

# 또는
python security_key_manager.py show-all
```

**빠른 접속 링크:**
```
http://localhost:5050?api_key=sorisay_user_2025_key_ijkl9012
```

📖 **자세한 안내**: [ACCESS_KEYS.md](./ACCESS_KEYS.md)

---

## 빠른 시작 (Quick Start)

### 설치 (Installation)
```bash
git clone https://github.com/parkcheolhong/run_all_shinsegye.py.git
cd run_all_shinsegye.py

# 시스템 의존성 설치 (Text-to-Speech 엔진)
# Ubuntu/Debian:
sudo apt-get install espeak espeak-ng

# macOS:
brew install espeak

# Windows: https://espeak.sourceforge.net/ 에서 다운로드

# Python 의존성 설치
pip install -r requirements.txt
```

### 기본 사용법 (Basic Usage)

```bash
# 단일 명령어 실행
python run_all_shinsegye.py -c "ls -la"

# Python 스크립트 실행
python run_all_shinsegye.py -s my_script.py

# 파일에서 명령어 실행
python run_all_shinsegye.py -f commands.txt

# 디렉토리의 모든 스크립트 실행
python run_all_shinsegye.py -d ./scripts

# 상세 모드
python run_all_shinsegye.py -f commands.txt -v
```

## 명령어 옵션 (Command Options)

| Short | Long | Description |
|-------|------|-------------|
| `-c` | `--command` | 단일 명령어 실행 |
| `-s` | `--script` | Python 스크립트 실행 |
| `-f` | `--file` | 파일에서 명령어 읽기 |
| `-d` | `--directory` | 디렉토리 스크립트 실행 |
| `-p` | `--pattern` | 파일 패턴 (기본: *.py) |
| `-v` | `--verbose` | 상세 출력 |
| | `--no-summary` | 요약 비활성화 |

## 예제 (Examples)

### 1. 여러 명령어 실행 (Multiple Commands)

**commands.txt:**
```bash
echo "Starting..."
date
ls -la
echo "Done!"
```

**실행:**
```bash
python run_all_shinsegye.py --file commands.txt
```

### 2. Python 스크립트 배치 실행 (Batch Python Scripts)

```bash
# scripts 폴더의 모든 .py 파일 실행
python run_all_shinsegye.py --directory scripts

# test_로 시작하는 파일만 실행
python run_all_shinsegye.py --directory scripts --pattern "test_*.py"
```

### 3. 상세 로그 (Verbose Logging)

```bash
python run_all_shinsegye.py --file commands.txt --verbose
```

**출력:**
```
[INFO] Found 4 commands to execute
[INFO] Executing command 1/4
[INFO] Running command: echo "Starting..."
[INFO] ✓ Command succeeded: echo "Starting..."
...
```

## 팁 (Tips)

1. **명령어 파일에서 주석 사용**
   ```bash
   # 이것은 주석입니다
   echo "실행됩니다"
   # 또 다른 주석
   ls -la
   ```

2. **에러 핸들링**
   - 실패한 명령어가 있어도 다음 명령어 계속 실행
   - 최종 요약에서 성공/실패 확인 가능

3. **타임아웃**
   - 각 명령어는 기본 5분 타임아웃
   - 긴 작업의 경우 여러 단계로 나누기 권장

## 문제 해결 (Troubleshooting)

### espeak 설치 관련 오류
**오류**: `RuntimeError: This means you probably do not have eSpeak or eSpeak-ng installed!`

**해결 방법**:
```bash
# Ubuntu/Debian
sudo apt-get install espeak espeak-ng

# macOS
brew install espeak

# Windows
# https://espeak.sourceforge.net/ 에서 설치
```

### Python 스크립트가 실행되지 않을 때
```bash
# Python 경로 확인
which python
python --version

# 스크립트 권한 확인
ls -la my_script.py
chmod +x my_script.py
```

### 명령어가 찾을 수 없을 때
```bash
# 절대 경로 사용
python run_all_shinsegye.py --command "/usr/bin/ls -la"

# PATH 확인
echo $PATH
```

## 더 많은 정보 (More Information)

자세한 내용은 README.md를 참조하세요.
See README.md for detailed information.
