# run_all_shinsegye.py

신비로운 가방 - 편리한 나의 도구 (My Convenient Tool)

## 소개 (Introduction)

`run_all_shinsegye.py`는 신비로운 가방처럼 다양한 작업을 실행할 수 있는 편리한 Python 유틸리티 도구입니다.
여러 개의 명령어나 스크립트를 자동으로 실행하고 결과를 요약해주는 강력한 도구입니다.

A convenient Python utility tool like a mysterious bag that can execute various tasks.
It's a powerful tool that can automatically run multiple commands or scripts and summarize the results.

## 주요 기능 (Features)

- ✨ 단일 명령어 실행 (Execute single commands)
- 🐍 Python 스크립트 실행 (Run Python scripts)
- 📄 파일에서 여러 명령어 일괄 실행 (Batch execute commands from a file)
- 📁 디렉토리의 모든 스크립트 실행 (Run all scripts in a directory)
- 📊 실행 결과 요약 (Execution summary)
- 🔍 상세한 로그 출력 옵션 (Verbose logging option)

## 설치 (Installation)

```bash
# 저장소 클론 (Clone the repository)
git clone https://github.com/parkcheolhong/run_all_shinsegye.py.git
cd run_all_shinsegye.py

# 실행 권한 부여 (Make executable)
chmod +x run_all_shinsegye.py
```

## 사용법 (Usage)

### 기본 사용 예제 (Basic Examples)

#### 1. 단일 명령어 실행 (Run a single command)

```bash
python run_all_shinsegye.py --command "echo Hello World"
```

#### 2. Python 스크립트 실행 (Run a Python script)

```bash
python run_all_shinsegye.py --script example_script1.py
```

#### 3. 파일에서 명령어 일괄 실행 (Run commands from a file)

```bash
"python" run_all_shinsegye.py --file example_commands.txt --verbose
```

#### 4. 디렉토리의 모든 Python 스크립트 실행 (Run all Python scripts in a directory)

```bash
python run_all_shinsegye.py --directory ./scripts
```

#

### 고급 옵션 (Advanced Options)

```bash
# 특정 패턴의 파일만 실행 (Run files matching a specific pattern)
python run_all_shinsegye.py --directory ./scripts --pattern "test_*.py"

# 요약 출력 비활성화 (Disable summary output)
python run_all_shinsegye.py --file commands.txt --no-summary

# 상세 로그와 함께 실행 (Run with verbose logging)
python run_all_shinsegye.py --directory ./scripts --verbose
```

### 명령어 파일 형식 (Command File Format)

명령어 파일은 각 줄에 하나의 명령어를 작성하며, `#`로 시작하는 줄은 주석으로 처리됩니다.

Command files have one command per line, and lines starting with `#` are treated as comments.

**example_commands.txt:**

```bash
# This is a comment
echo "Hello World"
ls -la
date
python my_script.py
```

## 명령줄 옵션 (Command-Line Options)

| 옵션 | 설명 (Description) |
|------|-------------------|
| `-c, --command` | 단일 명령어 실행 (Run a single command) |
| `-s, --script` | Python 스크립트 실행 (Run a Python script) |
| `-f, --file` | 파일에서 명령어 읽어서 실행 (Run commands from a file) |
| `-d, --directory` | 디렉토리의 모든 스크립트 실행 (Run all scripts in a directory) |
| `-p, --pattern` | 디렉토리 모드에서 파일 패턴 지정 (File pattern for directory mode, default: *.py) |
| `-v, --verbose` | 상세 출력 활성화 (Enable verbose output) |
| `--no-summary` | 요약 출력 비활성화 (Disable summary output) |

## 예제 파일 (Example Files)

저장소에는 다음 예제 파일들이 포함되어 있습니다:

The repository includes the following example files:

- `example_commands.txt` - 명령어 일괄 실행 예제 (Example command batch file)
- `example_script1.py` - 간단한 Python 스크립트 예제 (Simple Python script example)
- `example_script2.py` - 파일 작업 Python 스크립트 예제 (File operations Python script example)

## 실행 예제 (Execution Examples)

### 예제 명령어 파일 실행

```bash
python run_all_shinsegye.py --file example_commands.txt --verbose
```

출력 예시:

``
[INFO] Found 6 commands to execute
[INFO] Executing command 1/6
[INFO] Running command: echo "Hello from 신비로운 가방!"
[INFO] ✓ Command succeeded: echo "Hello from 신비로운 가방!"
...

============================================================
EXECUTION SUMMARY
============================================================

Total commands: 6
Successful: 6 ✓
Failed: 0 ✗
============================================================

``

## 개발 (Development)

### 요구사항 (Requirements)

- Python 3.6 이상 (Python 3.6 or higher)

### 테스트 (Testing)

```bash
# 예제 스크립트 테스트 (Test example scripts)
python run_all_shinsegye.py --script example_script1.py
python run_all_shinsegye.py --script example_script2.py

# 예제 명령어 파일 테스트 (Test example command file)
python run_all_shinsegye.py --file example_commands.txt
```

## 기여 (Contributing)

이슈 등록과 풀 리퀘스트를 환영합니다!

Issues and pull requests are welcome!

## 라이선스 (License)

MIT License

## 작성자 (Author)

parkcheolhong
