#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
신세계 오토파일럿 (One-File Edition)
- .gitignore 자동 생성/보강
- AI 코드관리 초기화 (git_sync, code_reviewer, auto_refactor, version_tracker)
- RunAllTool 실행기 (명령/스크립트/디렉터리)
- Flask 대시보드 (실시간 로그 + 분석 그래프)
- 음성 명령(선택): "리팩터링", "동기화", "실행", "종료"
"""

import os, sys, argparse, subprocess, threading, time, json
from pathlib import Path
from typing import List
def system_self_check():
    import importlib
    import sys
    import os

    print("[System] 안정화 점검 중...")

    essential_modules = [
        "speech_recognition", "pyttsx3", "flask", 
        "pyaudio", "requests"
    ]

    for module in essential_modules:
        try:
            importlib.import_module(module)
        except ImportError:
            print(f"[경고] '{module}' 모듈이 누락되어 있습니다. 자동 복구 시도 중...")
            os.system(f"{sys.executable} -m pip install {module}")

    print("[System] 모든 핵심 모듈 확인 완료. 시스템 안정화 완료!")

system_self_check()

# ░░░ 공용 실행 로그(분석용) ░░░
EXEC_RESULTS: List[dict] = []  # {'command','success','stderr','exec_time'}

# ░░░ .gitignore 자동 생성/보강 ░░░
def ensure_gitignore():
    gitignore_path = os.path.join(os.getcwd(), ".gitignore")
    base_rules = """# Python cache
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Test files
/tmp/
*.tmp
"""
    try:
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, "w", encoding="utf-8") as f:
                f.write(base_rules)
            print("✅ .gitignore 자동 생성 완료")
        else:
            with open(gitignore_path, "r+", encoding="utf-8") as f:
                existing = f.read()
                if "Python cache" not in existing:
                    f.write("\n" + base_rules)
                    print("🔁 .gitignore 규칙 보강 완료")
                else:
                    print("📁 .gitignore 최신 상태")
    except Exception as e:
        print(f"⚠️ .gitignore 처리 오류: {e}")

# ░░░ AI 코드관리 초기화 ░░░
# 필요한 모듈이 없더라도 전체 실행은 계속되도록 try-import
try:
    from modules.ai_code_manager import auto_refactor, git_sync, code_reviewer, version_tracker
    AI_MODULES_OK = True
except Exception as e:
    AI_MODULES_OK = False
    print("⚠️ AI 코드관리 모듈을 불러오지 못했습니다. (modules/ai_code_manager/* 필요)")
    print(f"   오류: {e}")

def initialize_ai_manager():
    print("🔧 AI 코드관리 모듈 초기화 중...")
    if not AI_MODULES_OK:
        print("⏭️ 모듈 없음: 초기화 스킵 (폴더와 파일 확인)")
        return
    try:
        git_sync.sync_repository()
        code_reviewer.scan_and_review()
        auto_refactor.optimize_code()
        version_tracker.update_version()
        print("✅ 코드관리 및 버전 업데이트 완료\n")
    except Exception as e:
        print(f"⚠️ AI 초기화 중 오류: {e}\n")

# ░░░ 실행기 ░░░
class RunAllTool:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: List[dict] = []

    def log(self, msg: str):
        if self.verbose:
            print(f"[INFO] {msg}")

    def run_command(self, command: str, shell: bool = True) -> dict:
        self.log(f"Running: {command}")
        t0 = time.time()
        try:
            result = subprocess.run(
                command, shell=shell, capture_output=True, text=True, timeout=300
            )
            dt = round(time.time() - t0, 3)
            output = {
                'command': command,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0,
                'exec_time': dt
            }
        except subprocess.TimeoutExpired:
            dt = round(time.time() - t0, 3)
            output = {
                'command': command, 'returncode': -1,
                'stdout': '', 'stderr': 'Command timed out',
                'success': False, 'exec_time': dt
            }
        except Exception as e:
            dt = round(time.time() - t0, 3)
            output = {
                'command': command, 'returncode': -1,
                'stdout': '', 'stderr': str(e),
                'success': False, 'exec_time': dt
            }

        self.results.append(output)
        EXEC_RESULTS.append({'command': output['command'],
                             'success': output['success'],
                             'stderr': output['stderr'],
                             'exec_time': output['exec_time']})
        if output['success']:
            self.log(f"✓ OK ({output['exec_time']}s)")
        else:
            self.log(f"✗ FAIL: {output['stderr'][:120]}")
        return output

    def run_script(self, script_path: str) -> dict:
        if not os.path.exists(script_path):
            self.log(f"✗ Script not found: {script_path}")
            return {'command': f"python {script_path}", 'returncode': -1,
                    'stdout': '', 'stderr': f"Script not found: {script_path}",
                    'success': False, 'exec_time': 0.0}
        return self.run_command(f"python {script_path}")

    def run_all_from_file(self, file_path: str) -> List[dict]:
        results = []
        if not os.path.exists(file_path):
            self.log(f"✗ File not found: {file_path}")
            return results
        with open(file_path, 'r', encoding='utf-8') as f:
            commands = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        for cmd in commands:
            results.append(self.run_command(cmd))
        return results

    def run_all_scripts_in_directory(self, directory: str, pattern: str = "*.py") -> List[dict]:
        results = []
        if not os.path.isdir(directory):
            self.log(f"✗ Directory not found: {directory}")
            return results
        scripts = list(Path(directory).glob(pattern))
        for script in scripts:
            results.append(self.run_script(str(script)))
        return results

    def print_summary(self):
        if not self.results:
            print("\nNo commands were executed.")
            return
        total = len(self.results)
        successful = sum(1 for r in self.results if r['success'])
        failed = total - successful
        print("\n" + "="*60)
        print("EXECUTION SUMMARY")
        print("="*60)
        print(f"Total: {total}  Successful: {successful} ✓  Failed: {failed} ✗")
        print("="*60)
        if failed:
            print("\nFailed list:")
            for r in self.results:
                if not r['success']:
                    print(f"  ✗ {r['command']}")
                    if r['stderr']:
                        print(f"    {r['stderr'][:100]}")
        print()

# ░░░ 분석기(내장) ░░░
class Analyzer:
    def __init__(self, log_data=None):
        self.log_data = log_data or []
        self.summary = {}

    def analyze(self):
        total = len(self.log_data)
        success = sum(1 for r in self.log_data if r.get("success"))
        failed = total - success
        avg_time = round(sum(r.get("exec_time", 0) for r in self.log_data) / (total or 1), 2)
        self.summary = {
            "total": total, "success": success, "failed": failed,
            "avg_time": avg_time,
            "success_rate": round(success / (total or 1) * 100, 2)
        }
        return self.summary

    def save_report(self, path="logs/ai_report.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.summary, f, ensure_ascii=False, indent=2)
        print(f"📊 분석 리포트 저장: {path}")
        return path

# ░░░ 대시보드(Flask + SocketIO) ░░░
FLASK_OK = True
try:
    from flask import Flask, render_template_string
    from flask_socketio import SocketIO, emit
except Exception as e:
    FLASK_OK = False
    print("ℹ️ Flask 대시보드를 건너뜁니다. 설치하려면:")
    print("   pip install flask flask_socketio")
    print(f"   ({e})")

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>🌐 신세계 오토파일럿 대시보드</title>
<style>
body { font-family: 'Malgun Gothic', Arial; background:#111; color:#eee; text-align:center; }
#log { width:86%; margin:18px auto; text-align:left; background:#222; padding:16px; border-radius:8px; height:380px; overflow-y:scroll; }
button { margin:8px; padding:10px 20px; background:#0078ff; color:white; border:none; border-radius:6px; cursor:pointer; }
button:hover { background:#005ecc; }
</style>
</head>
<body>
<h2>🌐 신세계 오토파일럿 대시보드</h2>
<div id="log"></div>
<div>
  <button onclick="sendCommand('리팩터링')">리팩터링</button>
  <button onclick="sendCommand('동기화')">동기화</button>
  <button onclick="sendCommand('실행')">전체 실행</button>
  <button onclick="sendCommand('분석')">분석 실행</button>
  <button onclick="sendCommand('종료')">종료</button>
</div>

<h3>📈 실행 분석 결과</h3>
<canvas id="chart" width="420" height="210"></canvas>

<script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const socket = io();
const logBox = document.getElementById('log');

socket.on('update', data => {
  logBox.innerHTML += `<div>${data}</div>`;
  logBox.scrollTop = logBox.scrollHeight;
});

function sendCommand(cmd){
  if(cmd === '분석'){ socket.emit('analyze'); return; }
  socket.emit('voice_command', cmd);
}

// doughnut chart
let ctx = document.getElementById('chart').getContext('2d');
let chart = new Chart(ctx, {
  type: 'doughnut',
  data: { labels: ['성공', '실패'], datasets: [{ data: [0,0] }] },
  options: { plugins:{ legend:{ labels:{ color:'#fff' }}}}
});
socket.on('report', data => {
  chart.data.datasets[0].data = [data.success, data.failed];
  chart.update();
  logBox.innerHTML += `<div>📊 성공률: ${data.success_rate}% | 평균시간: ${data.avg_time}s</div>`;
  logBox.scrollTop = logBox.scrollHeight;
});
</script>
</body>
</html>
"""

if FLASK_OK:
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="*")

    @app.route('/')
    def index():
        return render_template_string(DASHBOARD_HTML)

    @socketio.on('voice_command')
    def handle_command(cmd):
        emit('update', f"🗣 명령 수신: {cmd}", broadcast=True)
        # 버튼 명령 → 음성 명령 처리기 재사용
        VoiceCommandManager._dispatch_text(cmd)

    @socketio.on('analyze')
    def handle_analyze():
        analyzer = Analyzer(EXEC_RESULTS)
        summary = analyzer.analyze()
        socketio.emit('report', summary, broadcast=True)
        analyzer.save_report()

    def run_dashboard():
        socketio.run(app, host="0.0.0.0", port=5000, debug=False)

# ░░░ 음성 명령(선택) ░░░
VOICE_OK = True
try:
    import speech_recognition as sr
    import pyttsx3
except Exception as e:
    VOICE_OK = False
    print("ℹ️ 음성기능을 건너뜁니다. 설치하려면:")
    print("   pip install SpeechRecognition pyttsx3 pyaudio")
    print(f"   ({e})")

class VoiceCommandManager:
    _engine = None
    _recognizer = None

    def __init__(self):
        if VOICE_OK:
            try:
                self._recognizer = sr.Recognizer()
                self._engine = pyttsx3.init()
            except Exception:
                pass

    def speak(self, text):
        print(f"🎤 {text}")
        if VOICE_OK and self._engine:
            try:
                self._engine.say(text)
                self._engine.runAndWait()
            except Exception:
                pass

    @staticmethod
    def _dispatch_text(text: str):
        text = text or ""
        t = text.replace("시작", "").strip()
        if "종료" in t:
            print("🛑 종료 요청")
            if FLASK_OK: socketio.emit('update', "💤 시스템 종료 요청됨", broadcast=True)
            os._exit(0)
        elif "리팩터링" in t:
            if AI_MODULES_OK:
                auto_refactor.optimize_code()
                msg = "코드 리팩터링 완료"
            else:
                msg = "리팩터링 모듈 없음"
            print("✅", msg)
            if FLASK_OK: socketio.emit('update', f"✅ {msg}", broadcast=True)
        elif "동기화" in t:
            if AI_MODULES_OK:
                git_sync.sync_repository()
                msg = "깃 동기화 완료"
            else:
                msg = "동기화 모듈 없음"
            print("✅", msg)
            if FLASK_OK: socketio.emit('update', f"✅ {msg}", broadcast=True)
        elif "실행" in t:
            tool = RunAllTool(verbose=True)
            tool.run_all_scripts_in_directory("modules")
            tool.print_summary()
            if FLASK_OK: socketio.emit('update', "🏃 전체 스크립트 실행 완료", broadcast=True)
        else:
            if FLASK_OK: socketio.emit('update', "❓ 알 수 없는 명령", broadcast=True)

    def listen_loop(self):
        if not VOICE_OK or not self._recognizer:
            print("🎧 음성 모듈 미설치/비활성 — 대시보드 버튼으로 사용하세요.")
            while True: time.sleep(3600)  # 대시보드만 사용
        self.speak("신세계 오토파일럿이 준비되었습니다.")
        while True:
           try:
    # 시작 시, 배경 소음 조정 및 주변 소음 필터링
    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

    # 너무 오래 기다리거나 한 문장이 너무 길어지는 것 방지
    audio = self.recognizer.listen(
        source,
        timeout=8,              # 8초 안에 말 시작 없으면 타임아웃
        phrase_time_limit=15    # 한 번 말할 때 15초까지만 듣기
    )

    # 음성 → 텍스트 변환
    text = self.recognizer.recognize_google(audio, language="ko-KR")
    print(f"📝 인식: {text}")
    self.dispatch_text(text)

except sr.WaitTimeoutError:
    # 조용하면 그냥 다음 루프로 넘어가기
    pass

except sr.UnknownValueError:
    # 인식 실패 시 음성 출력
    self.speak("음성을 인식하지 못했습니다.")

except sr.RequestError:
    # API 또는 네트워크 오류
    self.speak("네트워크 오류가 발생했습니다.")

except Exception as e:
    # 예기치 못한 오류 로깅
    print(e)


# ░░░ CLI 파서 구성 ░░░
def parse_args():
    parser = argparse.ArgumentParser(
        description='run_all_shinsegye_project.py - 신세계 오토파일럿',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="예) python run_all_shinsegye_project.py --directory ./modules"
    )

    parser.add_argument('-c', '--command', help='단일 쉘 명령 실행')
    parser.add_argument('-s', '--script', help='파이썬 스크립트 실행')
    parser.add_argument('-f', '--file', help='파일의 명령들 일괄 실행')
    parser.add_argument('-d', '--directory', help='디렉터리 내 스크립트 일괄 실행')
    parser.add_argument('-p', '--pattern', default='*.py', help='디렉터리 실행 패턴 (기본: *.py)')
    parser.add_argument('-v', '--verbose', action='store_true', help='자세히 출력')
    parser.add_argument('--no-summary', action='store_true', help='요약 출력 끔')
    parser.add_argument('--headless', action='store_true', help='대시보드/음성 비활성(순수 CLI 모드)')

    return parser.parse_args()


# ░░░ 엔트리 ░░░
import time
import speech_recognition as sr
import pyttsx3

def speak(text):
    """소리새가 말하기"""
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()

def listen():
    """사용자 음성 듣기"""
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("🎧 [소리새] 듣는 중입니다... 말씀해 주세요.")
        speak("소리새가 듣고 있습니다. 지금 말씀하세요.")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="ko-KR")
        print("🗣 인식된 음성:", text)
        return text
    except sr.UnknownValueError:
        speak("잘 못 들었어요. 다시 말씀해 주세요.")
        return None
    except sr.RequestError:
        speak("음성 인식 서버에 연결할 수 없습니다.")
        return None

def main():
    speak("안녕하세요. 저는 소리새입니다. 무엇을 도와드릴까요?")
    while True:
        command = listen()
        if not command:
            continue

        if "소리새" not in command:
            print("⚙️ [소리새] 호출어가 감지되지 않았습니다.")
            continue

        command = command.replace("소리새", "").strip()

        if "끝" in command or "종료" in command:
            speak("소리새를 종료합니다. 다음에 또 뵐게요.")
            break
        elif "시간" in command:
            now = time.strftime("%Y년 %m월 %d일 %H시 %M분")
            speak(f"현재 시간은 {now}입니다.")
        else:
            speak(f"{command} 명령을 인식했습니다. 아직 학습 중입니다.")
        time.sleep(1)

if __name__ == "__main__":
    main()

