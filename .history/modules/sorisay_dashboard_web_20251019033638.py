from flask import Flask, render_template_string, jsonify, request
from flask_socketio import SocketIO, emit
import json
import os
from datetime import datetime
from threading import Lock
import threading
import time

app = Flask(__name__)
app.secret_key = "sorisay_secure_key_2025"  # 보안키 추가
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:5050", "http://127.0.0.1:5050"])  # CORS 제한

# 실시간 상태 관리
class DashboardState:
    def __init__(self):
        self.lock = Lock()
        self.voice_commands = []
        self.system_status = "대기 중"
        self.active_plugins = []
        self.last_command = None
        self.command_count = 0
        self.is_listening = False
        self.error_count = 0
        # 🎨 새로운 창의적 기능 상태
        self.current_persona = "friendly"
        self.creative_activities = []
        self.ai_collaborations = 0
        self.memory_count = 0
        self.generated_plugins = 0
    
    def add_voice_command(self, command, status="성공", plugin_name=None):
        with self.lock:
            command_data = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "command": command,
                "status": status,
                "plugin": plugin_name or "시스템"
            }
            self.voice_commands.append(command_data)
            self.last_command = command
            self.command_count += 1
            
            if status == "실패":
                self.error_count += 1
                
            # 최근 20개만 유지
            if len(self.voice_commands) > 20:
                self.voice_commands.pop(0)
                
        # 클라이언트에 실시간 업데이트 전송
        socketio.emit('command_update', command_data)
        socketio.emit('stats_update', self.get_stats())
    
    def set_system_status(self, status):
        with self.lock:
            self.system_status = status
        socketio.emit('status_update', {"status": status})
    
    def set_listening_status(self, is_listening):
        with self.lock:
            self.is_listening = is_listening
        socketio.emit('listening_update', {"is_listening": is_listening})
    
    def get_stats(self):
        with self.lock:
            return {
                "total_commands": self.command_count,
                "recent_commands": len(self.voice_commands),
                "last_command": self.last_command,
                "system_status": self.system_status,
                "active_plugins": self.active_plugins,
                "is_listening": self.is_listening,
                "error_count": self.error_count,
                "success_rate": ((self.command_count - self.error_count) / max(1, self.command_count)) * 100,
                # 🎨 창의적 기능 통계
                "current_persona": self.current_persona,
                "ai_collaborations": self.ai_collaborations,
                "memory_count": self.memory_count,
                "generated_plugins": self.generated_plugins,
                "creative_activities": len(self.creative_activities)
            }
    
    def update_persona(self, persona):
        """🎭 페르소나 업데이트"""
        with self.lock:
            self.current_persona = persona
        socketio.emit('persona_update', {"current_persona": persona})
    
    def add_creative_activity(self, activity_type, description):
        """🎨 창의적 활동 추가"""
        with self.lock:
            activity = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "type": activity_type,
                "description": description
            }
            self.creative_activities.append(activity)
            
            # 활동 유형별 카운터 증가
            if activity_type == "collaboration":
                self.ai_collaborations += 1
            elif activity_type == "plugin_generation":
                self.generated_plugins += 1
            elif activity_type == "memory_save":
                self.memory_count += 1
            
            # 최근 10개만 유지
            if len(self.creative_activities) > 10:
                self.creative_activities.pop(0)
                
        socketio.emit('creative_update', activity)
        socketio.emit('stats_update', self.get_stats())

dashboard_state = DashboardState()

HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🌐 소리새 대시보드</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { 
    background: linear-gradient(135deg, #1e3c72, #2a5298); 
    color: #eee; 
    font-family: 'Malgun Gothic', sans-serif;
    min-height: 100vh;
}
.container { max-width: 1200px; margin: 0 auto; padding: 20px; }
.header { text-align: center; margin-bottom: 30px; }
.header h1 { font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
.status-bar { 
    background: rgba(255,255,255,0.1); 
    border-radius: 10px; 
    padding: 15px; 
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.card { 
    background: rgba(255,255,255,0.1); 
    border-radius: 15px; 
    padding: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
}
.card h3 { margin-bottom: 15px; color: #00bcd4; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }
.stat-item { text-align: center; padding: 15px; background: rgba(0,0,0,0.2); border-radius: 10px; }
.stat-number { font-size: 2em; font-weight: bold; color: #4caf50; }
.command-log { 
    height: 300px; 
    overflow-y: auto; 
    background: rgba(0,0,0,0.3); 
    border-radius: 10px; 
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.1);
}
.command-item { 
    padding: 8px 12px; 
    margin: 5px 0; 
    background: rgba(255,255,255,0.1); 
    border-radius: 8px;
    border-left: 4px solid #4caf50;
}
.command-item.failed { border-left-color: #f44336; }
.controls { text-align: center; margin-top: 20px; }
button { 
    background: linear-gradient(45deg, #00bcd4, #0097a7); 
    border: none; 
    color: white; 
    padding: 12px 24px; 
    margin: 8px; 
    border-radius: 25px; 
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,188,212,0.3);
}
button:hover { 
    transform: translateY(-2px); 
    box-shadow: 0 6px 20px rgba(0,188,212,0.4);
}
.system-status { 
    display: inline-block; 
    padding: 6px 12px; 
    border-radius: 15px; 
    font-weight: bold;
}
.status-active { background: #4caf50; }
.status-waiting { background: #ff9800; }
.status-error { background: #f44336; }
@media (max-width: 768px) {
    .grid { grid-template-columns: 1fr; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🎤 소리새 AI 대시보드</h1>
        <div class="status-bar">
            <span>시스템 상태: </span>
            <span id="system-status" class="system-status status-waiting">대기 중</span>
            <span style="margin-left: 20px;">마지막 명령: </span>
            <span id="last-command">없음</span>
        </div>
    </div>
    
    <div class="grid">
        <div class="card">
            <h3>📊 실시간 통계</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number" id="total-commands">0</div>
                    <div>총 명령 수</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="recent-commands">0</div>
                    <div>최근 명령</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="active-plugins">0</div>
                    <div>활성 플러그인</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="uptime">00:00</div>
                    <div>가동 시간</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>🎭 창의적 AI 상태</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number" id="current-persona">😊</div>
                    <div>현재 페르소나</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="ai-collaborations">0</div>
                    <div>AI 협업 횟수</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="memory-count">0</div>
                    <div>저장된 기억</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="generated-plugins">0</div>
                    <div>생성된 플러그인</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>🎙️ 음성 명령 로그</h3>
            <div id="command-log" class="command-log">
                <div style="text-align: center; color: #888; margin-top: 50px;">
                    음성 명령을 기다리는 중...
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>🎨 창의적 활동 로그</h3>
            <div id="creative-log" class="command-log">
                <div style="text-align: center; color: #888; margin-top: 50px;">
                    창의적 활동을 기다리는 중...
                </div>
            </div>
        </div>
    </div>
    
    <div class="card">
        <h3>🎮 원격 제어</h3>
        <div class="controls">
            <button onclick="sendCommand('리팩터링')">🔧 리팩터링</button>
            <button onclick="sendCommand('동기화')">🔄 동기화</button>
            <button onclick="sendCommand('상태')">📋 상태 확인</button>
            <button onclick="sendCommand('테스트')">🧪 테스트 실행</button>
            <button onclick="sendCommand('정리')">🧹 프로젝트 정리</button>
            <button onclick="sendCommand('도움말')">❓ 도움말</button>
        </div>
    </div>
</div>

<script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
<script>
const socket = io();
let startTime = Date.now();

// 소켓 이벤트 리스너
socket.on('voice_command', function(data) {
    addCommandToLog(data.command, data.status);
    updateStats();
});

socket.on('system_status', function(data) {
    updateSystemStatus(data.status);
});

socket.on('stats_update', function(data) {
    document.getElementById('total-commands').textContent = data.total_commands;
    document.getElementById('recent-commands').textContent = data.recent_commands;
    document.getElementById('active-plugins').textContent = data.active_plugins.length;
    document.getElementById('last-command').textContent = data.last_command || '없음';
    
    // 🎨 창의적 기능 통계 업데이트
    if (data.current_persona) {
        const personaEmoji = {
            'friendly': '😊', 'genius': '🤓', 'creative': '🎨', 
            'coach': '💪', 'philosopher': '🧐'
        };
        document.getElementById('current-persona').textContent = 
            personaEmoji[data.current_persona] || '🤖';
    }
    if (data.ai_collaborations !== undefined) {
        document.getElementById('ai-collaborations').textContent = data.ai_collaborations;
    }
    if (data.memory_count !== undefined) {
        document.getElementById('memory-count').textContent = data.memory_count;
    }
    if (data.generated_plugins !== undefined) {
        document.getElementById('generated-plugins').textContent = data.generated_plugins;
    }
});

// 🎭 페르소나 업데이트 이벤트
socket.on('persona_update', function(data) {
    console.log('페르소나 변경:', data.current_persona);
});

// 🎨 창의적 활동 업데이트 이벤트
socket.on('creative_update', function(data) {
    addCreativeActivityToLog(data);
});

// 명령어 로그에 추가
function addCommandToLog(command, status = 'success') {
    const log = document.getElementById('command-log');
    const item = document.createElement('div');
    item.className = `command-item ${status === 'failed' ? 'failed' : ''}`;
    
    const now = new Date();
    const time = now.toLocaleTimeString();
    const statusIcon = status === 'failed' ? '❌' : '✅';
    
    item.innerHTML = `
        <span style="color: #888;">[${time}]</span>
        <span>${statusIcon} ${command}</span>
    `;
    
    log.appendChild(item);
    log.scrollTop = log.scrollHeight;
    
    // 빈 메시지 제거
    const emptyMsg = log.querySelector('div[style*="text-align: center"]');
    if (emptyMsg) emptyMsg.remove();
}

// 시스템 상태 업데이트
function updateSystemStatus(status) {
    const statusEl = document.getElementById('system-status');
    statusEl.textContent = status;
    statusEl.className = 'system-status ' + 
        (status.includes('실행') ? 'status-active' : 
         status.includes('오류') ? 'status-error' : 'status-waiting');
}

// 원격 명령 전송
function sendCommand(command) {
    socket.emit('remote_command', {command: command});
    addCommandToLog(`[원격] ${command}`, 'success');
}

// 🎨 창의적 활동 로그에 추가
function addCreativeActivityToLog(activity) {
    const log = document.getElementById('creative-log');
    const item = document.createElement('div');
    item.className = 'command-item';
    
    const activityIcons = {
        'collaboration': '🤝',
        'plugin_generation': '🧩',
        'memory_save': '🧠',
        'persona_switch': '🎭',
        'code_analysis': '🎨'
    };
    
    const icon = activityIcons[activity.type] || '✨';
    
    item.innerHTML = `
        <span style="color: #888;">[${activity.timestamp}]</span>
        <span>${icon} ${activity.description}</span>
    `;
    
    log.appendChild(item);
    log.scrollTop = log.scrollHeight;
    
    // 빈 메시지 제거
    const emptyMsg = log.querySelector('div[style*="text-align: center"]');
    if (emptyMsg) emptyMsg.remove();
}

// 통계 업데이트 요청
function updateStats() {
    socket.emit('get_stats');
}

// 가동 시간 업데이트
function updateUptime() {
    const uptime = Math.floor((Date.now() - startTime) / 1000);
    const minutes = Math.floor(uptime / 60);
    const seconds = uptime % 60;
    document.getElementById('uptime').textContent = 
        `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

// 초기화 및 주기적 업데이트
setInterval(updateUptime, 1000);
setInterval(updateStats, 5000);
updateStats();
</script>
</body>
</html>"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/stats")
def api_stats():
    return jsonify(dashboard_state.get_stats())

@socketio.on("remote_command")
def handle_remote_command(data):
    command = data.get('command', '')
    print(f"📡 웹에서 원격 명령 수신: {command}")
    dashboard_state.add_voice_command(f"[원격] {command}")
    emit("voice_command", {"command": f"[원격] {command}", "status": "success"}, broadcast=True)

@socketio.on("get_stats")
def handle_get_stats():
    stats = dashboard_state.get_stats()
    emit("stats_update", stats)

def broadcast_voice_command(command, status="success"):
    """음성 명령을 대시보드에 브로드캐스트"""
    dashboard_state.add_voice_command(command, status)
    socketio.emit("voice_command", {"command": command, "status": status})

def broadcast_system_status(status):
    """시스템 상태를 대시보드에 브로드캐스트"""
    dashboard_state.set_system_status(status)
    socketio.emit("system_status", {"status": status})

def broadcast_persona_change(persona):
    """🎭 페르소나 변경을 대시보드에 브로드캐스트"""
    dashboard_state.update_persona(persona)

def broadcast_creative_activity(activity_type, description):
    """🎨 창의적 활동을 대시보드에 브로드캐스트"""
    dashboard_state.add_creative_activity(activity_type, description)

def run_dashboard():
    print("🌍 웹 대시보드 실행 중... (http://localhost:5050)")
    socketio.run(app, host="0.0.0.0", port=5050, debug=False)
