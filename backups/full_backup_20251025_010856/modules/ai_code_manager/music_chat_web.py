"""
🎵💬 음악 채팅장 웹 인터페이스
Flask 기반의 실시간 음악 채팅 웹 서비스

주요 기능:
- 실시간 채팅 인터페이스
- 음악/가사 공유 UI
- 방 생성/관리
- 협업 프로젝트 관리
"""

from flask import Flask, render_template_string, jsonify, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import os
from datetime import datetime

# 음악 채팅 시스템 import
from modules.ai_code_manager.music_chat_system import get_chat_system
from modules.ai_code_manager.ai_music_composer import AIMusicComposer, AILyricsWriter, AIMusicLyricsStudio

class MusicChatWebInterface:
    """음악 채팅 웹 인터페이스"""
    
    def __init__(self, app: Flask, socketio: SocketIO):
        self.app = app
        self.socketio = socketio
        self.chat_system = get_chat_system()
        self.music_studio = AIMusicLyricsStudio()
        
        # 라우트 등록
        self._register_routes()
        self._register_socketio_events()
    
    def _register_routes(self):
        """웹 라우트 등록"""
        
        @self.app.route('/music-chat')
        def music_chat_main():
            """메인 채팅 페이지"""
            return render_template_string(MUSIC_CHAT_HTML_TEMPLATE)
        
        @self.app.route('/api/chat/rooms')
        def get_rooms():
            """채팅방 목록 API"""
            rooms = self.chat_system.get_room_list()
            return jsonify({
                'success': True,
                'rooms': rooms
            })
        
        @self.app.route('/api/chat/room/<room_id>/messages')
        def get_room_messages(room_id):
            """방 메시지 조회 API"""
            limit = request.args.get('limit', 50, type=int)
            messages = self.chat_system.get_room_messages(room_id, limit)
            return jsonify({
                'success': True,
                'messages': messages
            })
        
        @self.app.route('/api/chat/room/<room_id>/users')
        def get_room_users(room_id):
            """방 사용자 조회 API"""
            users = self.chat_system.get_room_users(room_id)
            return jsonify({
                'success': True,
                'users': users
            })
        
        @self.app.route('/api/chat/create-user', methods=['POST'])
        def create_user():
            """사용자 생성 API"""
            data = request.get_json()
            username = data.get('username', '')
            favorite_genre = data.get('favorite_genre', '팝')
            instruments = data.get('instruments', [])
            
            if not username:
                return jsonify({'success': False, 'error': '사용자명이 필요합니다'})
            
            user = self.chat_system.create_user(username, favorite_genre, instruments)
            session['user_id'] = user.user_id
            
            return jsonify({
                'success': True,
                'user': {
                    'user_id': user.user_id,
                    'username': user.username,
                    'favorite_genre': user.favorite_genre,
                    'instruments': user.instruments
                }
            })
        
        @self.app.route('/api/chat/create-room', methods=['POST'])
        def create_room():
            """채팅방 생성 API"""
            data = request.get_json()
            user_id = session.get('user_id')
            
            if not user_id:
                return jsonify({'success': False, 'error': '로그인이 필요합니다'})
            
            room = self.chat_system.create_room(
                creator_id=user_id,
                room_name=data.get('room_name', ''),
                description=data.get('description', ''),
                room_type=data.get('room_type', 'general'),
                genre=data.get('genre', 'pop'),
                max_users=data.get('max_users', 10),
                is_private=data.get('is_private', False),
                password=data.get('password')
            )
            
            return jsonify({
                'success': True,
                'room_id': room.room_id
            })
        
        @self.app.route('/api/music/create-song', methods=['POST'])
        def create_song():
            """AI 음악 생성 API"""
            data = request.get_json()
            emotion = data.get('emotion', 'happy')
            theme = data.get('theme', None)
            song_type = data.get('type', 'complete')  # 'music', 'lyrics', 'complete'
            
            try:
                if song_type == 'music':
                    # 작곡만
                    composer = AIMusicComposer()
                    result = composer.compose_by_emotion(emotion)
                elif song_type == 'lyrics':
                    # 작사만
                    lyricist = AILyricsWriter()
                    result = lyricist.generate_lyrics(emotion, theme, lines=8)
                else:
                    # 완전한 노래
                    result = self.music_studio.create_complete_song(emotion, theme)
                
                return jsonify({
                    'success': True,
                    'song_data': result
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.app.route('/api/chat/statistics')
        def get_chat_statistics():
            """채팅 시스템 통계 API"""
            stats = self.chat_system.get_chat_statistics()
            return jsonify({
                'success': True,
                'statistics': stats
            })
    
    def _register_socketio_events(self):
        """SocketIO 이벤트 등록"""
        
        @self.socketio.on('join_room')
        def handle_join_room(data):
            """방 참가 이벤트"""
            user_id = session.get('user_id')
            room_id = data.get('room_id')
            password = data.get('password')
            
            if not user_id or not room_id:
                emit('error', {'message': '잘못된 요청입니다'})
                return
            
            success = self.chat_system.join_room(user_id, room_id, password)
            
            if success:
                join_room(room_id)
                emit('joined_room', {'room_id': room_id})
                
                # 방의 다른 사용자들에게 알림
                self.socketio.emit('user_joined', {
                    'user_id': user_id,
                    'username': self.chat_system.users[user_id].username
                }, room=room_id)
            else:
                emit('error', {'message': '방 참가에 실패했습니다'})
        
        @self.socketio.on('leave_room')
        def handle_leave_room(data):
            """방 나가기 이벤트"""
            user_id = session.get('user_id')
            room_id = data.get('room_id')
            
            if user_id and room_id:
                self.chat_system.leave_room(user_id, room_id)
                leave_room(room_id)
                
                # 방의 다른 사용자들에게 알림
                self.socketio.emit('user_left', {
                    'user_id': user_id,
                    'username': self.chat_system.users[user_id].username
                }, room=room_id)
        
        @self.socketio.on('send_message')
        def handle_send_message(data):
            """메시지 전송 이벤트"""
            user_id = session.get('user_id')
            room_id = data.get('room_id')
            content = data.get('content', '')
            message_type = data.get('type', 'text')
            music_data = data.get('music_data')
            
            if not user_id or not room_id or not content:
                emit('error', {'message': '필수 정보가 누락되었습니다'})
                return
            
            success = self.chat_system.send_message(
                user_id, room_id, content, message_type, music_data
            )
            
            if success:
                # 방의 모든 사용자에게 메시지 브로드캐스트
                message_data = {
                    'user_id': user_id,
                    'username': self.chat_system.users[user_id].username,
                    'content': content,
                    'type': message_type,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'music_data': music_data
                }
                
                self.socketio.emit('new_message', message_data, room=room_id)
            else:
                emit('error', {'message': '메시지 전송에 실패했습니다'})
        
        @self.socketio.on('share_music')
        def handle_share_music(data):
            """음악 공유 이벤트"""
            user_id = session.get('user_id')
            room_id = data.get('room_id')
            music_data = data.get('music_data')
            
            if not user_id or not room_id or not music_data:
                emit('error', {'message': '음악 데이터가 필요합니다'})
                return
            
            success = self.chat_system.share_music(user_id, room_id, music_data)
            
            if success:
                # 음악 공유 알림
                share_data = {
                    'user_id': user_id,
                    'username': self.chat_system.users[user_id].username,
                    'music_data': music_data,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                self.socketio.emit('music_shared', share_data, room=room_id)
        
        @self.socketio.on('start_collaboration')
        def handle_start_collaboration(data):
            """협업 시작 이벤트"""
            user_id = session.get('user_id')
            room_id = data.get('room_id')
            collab_type = data.get('collab_type', 'complete_song')
            title = data.get('title', '무제')
            
            if not user_id or not room_id:
                emit('error', {'message': '필수 정보가 누락되었습니다'})
                return
            
            collab_id = self.chat_system.start_collaboration(
                user_id, room_id, collab_type, title
            )
            
            # 협업 시작 알림
            collab_data = {
                'collaboration_id': collab_id,
                'creator_id': user_id,
                'creator_name': self.chat_system.users[user_id].username,
                'type': collab_type,
                'title': title
            }
            
            self.socketio.emit('collaboration_started', collab_data, room=room_id)

# HTML 템플릿
MUSIC_CHAT_HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎵 AI 음악 채팅장</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
        }
        
        .sidebar {
            width: 300px;
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 15px 0 0 15px;
            overflow-y: auto;
        }
        
        .main-chat {
            flex: 1;
            background: rgba(255,255,255,0.9);
            display: flex;
            flex-direction: column;
            border-radius: 0 15px 15px 0;
        }
        
        .chat-header {
            padding: 20px;
            background: rgba(0,0,0,0.1);
            border-bottom: 1px solid #eee;
        }
        
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            max-height: calc(100vh - 200px);
        }
        
        .chat-input {
            padding: 20px;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .message.music {
            border-left-color: #ff6b6b;
            background: #fff5f5;
        }
        
        .message.lyrics {
            border-left-color: #4ecdc4;
            background: #f0fdfc;
        }
        
        .message.collaboration {
            border-left-color: #ffe66d;
            background: #fffbf0;
        }
        
        .room-item {
            padding: 10px;
            margin: 5px 0;
            background: #f8f9fa;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .room-item:hover {
            background: #e9ecef;
            transform: translateY(-2px);
        }
        
        .room-item.active {
            background: #667eea;
            color: white;
        }
        
        .btn {
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5a6fd8;
        }
        
        .btn-music {
            background: #ff6b6b;
            color: white;
        }
        
        .btn-lyrics {
            background: #4ecdc4;
            color: white;
        }
        
        .music-controls {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        
        .user-setup {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .collaboration-panel {
            background: #fffbf0;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            border: 2px solid #ffe66d;
        }
        
        input, select, textarea {
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin: 5px 0;
        }
        
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>🎵 음악 채팅장</h2>
        
        <div id="userSetup" class="user-setup">
            <h3>사용자 설정</h3>
            <input type="text" id="username" placeholder="사용자명" />
            <select id="favoriteGenre">
                <option value="팝">팝</option>
                <option value="록">록</option>
                <option value="재즈">재즈</option>
                <option value="클래식">클래식</option>
                <option value="힙합">힙합</option>
            </select>
            <button class="btn btn-primary" onclick="createUser()">입장하기</button>
        </div>
        
        <div id="roomList" class="hidden">
            <h3>채팅방 목록</h3>
            <div id="rooms"></div>
            
            <div style="margin-top: 20px;">
                <button class="btn btn-primary" onclick="showCreateRoom()">방 만들기</button>
            </div>
            
            <div id="createRoomPanel" class="hidden" style="margin-top: 15px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                <input type="text" id="roomName" placeholder="방 이름" />
                <textarea id="roomDescription" placeholder="방 설명"></textarea>
                <select id="roomType">
                    <option value="general">일반 채팅</option>
                    <option value="collaboration">협업실</option>
                    <option value="jam_session">잼 세션</option>
                </select>
                <select id="roomGenre">
                    <option value="pop">팝</option>
                    <option value="rock">록</option>
                    <option value="jazz">재즈</option>
                    <option value="all">모든 장르</option>
                </select>
                <button class="btn btn-primary" onclick="createRoom()">방 만들기</button>
                <button class="btn" onclick="hideCreateRoom()">취소</button>
            </div>
        </div>
        
        <div id="musicControls" class="music-controls hidden">
            <button class="btn btn-music" onclick="createMusic()">🎵 작곡</button>
            <button class="btn btn-lyrics" onclick="createLyrics()">📝 작사</button>
            <button class="btn btn-primary" onclick="createCompleteSong()">🎼 완전한 노래</button>
        </div>
    </div>
    
    <div class="main-chat">
        <div class="chat-header">
            <h2 id="currentRoomName">채팅방을 선택해주세요</h2>
            <div id="roomUsers"></div>
        </div>
        
        <div id="chatMessages" class="chat-messages"></div>
        
        <div class="chat-input hidden" id="chatInputPanel">
            <input type="text" id="messageInput" placeholder="메시지를 입력하세요..." style="flex: 1;" />
            <button class="btn btn-primary" onclick="sendMessage()">전송</button>
        </div>
        
        <div id="collaborationPanel" class="collaboration-panel hidden">
            <h4>🤝 협업 프로젝트</h4>
            <input type="text" id="collabTitle" placeholder="프로젝트 제목" />
            <select id="collabType">
                <option value="music">작곡 협업</option>
                <option value="lyrics">작사 협업</option>
                <option value="complete_song">완전한 노래 협업</option>
            </select>
            <button class="btn btn-primary" onclick="startCollaboration()">협업 시작</button>
        </div>
    </div>

    <script>
        let socket = io();
        let currentUser = null;
        let currentRoom = null;
        
        // 소켓 이벤트 리스너
        socket.on('joined_room', (data) => {
            currentRoom = data.room_id;
            loadRoomMessages();
            loadRoomUsers();
            document.getElementById('chatInputPanel').classList.remove('hidden');
            document.getElementById('musicControls').classList.remove('hidden');
        });
        
        socket.on('new_message', (data) => {
            displayMessage(data);
        });
        
        socket.on('music_shared', (data) => {
            displayMusicShare(data);
        });
        
        socket.on('collaboration_started', (data) => {
            displayCollaborationStart(data);
        });
        
        socket.on('user_joined', (data) => {
            loadRoomUsers();
            displaySystemMessage(data.username + '님이 입장했습니다.');
        });
        
        socket.on('user_left', (data) => {
            loadRoomUsers();
            displaySystemMessage(data.username + '님이 퇴장했습니다.');
        });
        
        // 사용자 생성
        function createUser() {
            const username = document.getElementById('username').value;
            const favoriteGenre = document.getElementById('favoriteGenre').value;
            
            if (!username) {
                alert('사용자명을 입력해주세요');
                return;
            }
            
            fetch('/api/chat/create-user', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    username: username,
                    favorite_genre: favoriteGenre
                })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    currentUser = data.user;
                    document.getElementById('userSetup').classList.add('hidden');
                    document.getElementById('roomList').classList.remove('hidden');
                    loadRooms();
                }
            });
        }
        
        // 채팅방 목록 로드
        function loadRooms() {
            fetch('/api/chat/rooms')
            .then(r => r.json())
            .then(data => {
                const roomsDiv = document.getElementById('rooms');
                roomsDiv.innerHTML = '';
                
                data.rooms.forEach(room => {
                    const roomDiv = document.createElement('div');
                    roomDiv.className = 'room-item';
                    roomDiv.innerHTML = `
                        <strong>${room.room_name}</strong><br>
                        <small>${room.description}</small><br>
                        <span>👥 ${room.current_users}/${room.max_users} | 🎵 ${room.genre}</span>
                    `;
                    roomDiv.onclick = () => joinRoom(room.room_id);
                    roomsDiv.appendChild(roomDiv);
                });
            });
        }
        
        // 방 참가
        function joinRoom(roomId) {
            socket.emit('join_room', {room_id: roomId});
            
            // 활성화된 방 표시
            document.querySelectorAll('.room-item').forEach(item => {
                item.classList.remove('active');
            });
            event.target.classList.add('active');
        }
        
        // 메시지 전송
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const content = input.value.trim();
            
            if (!content || !currentRoom) return;
            
            socket.emit('send_message', {
                room_id: currentRoom,
                content: content,
                type: 'text'
            });
            
            input.value = '';
        }
        
        // Enter 키로 메시지 전송
        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('messageInput').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        });
        
        // 메시지 표시
        function displayMessage(data) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${data.type}`;
            
            let content = `
                <strong>${data.username}</strong> 
                <small>${data.timestamp}</small><br>
                ${data.content}
            `;
            
            if (data.music_data) {
                content += `<div style="margin-top: 10px; padding: 10px; background: rgba(0,0,0,0.1); border-radius: 5px;">
                    <strong>🎵 ${data.music_data.title || '음악 작품'}</strong>
                </div>`;
            }
            
            messageDiv.innerHTML = content;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        // AI 음악 생성
        function createMusic() {
            createAIContent('music');
        }
        
        function createLyrics() {
            createAIContent('lyrics');
        }
        
        function createCompleteSong() {
            createAIContent('complete');
        }
        
        function createAIContent(type) {
            const emotion = prompt('감정을 선택하세요 (happy, sad, romantic, energetic)', 'happy');
            const theme = prompt('테마를 입력하세요 (선택사항)', '');
            
            if (!emotion) return;
            
            fetch('/api/music/create-song', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: type,
                    emotion: emotion,
                    theme: theme
                })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    socket.emit('share_music', {
                        room_id: currentRoom,
                        music_data: data.song_data
                    });
                }
            });
        }
        
        // 협업 시작
        function startCollaboration() {
            const title = document.getElementById('collabTitle').value;
            const type = document.getElementById('collabType').value;
            
            if (!title) {
                alert('프로젝트 제목을 입력해주세요');
                return;
            }
            
            socket.emit('start_collaboration', {
                room_id: currentRoom,
                collab_type: type,
                title: title
            });
            
            document.getElementById('collabTitle').value = '';
        }
        
        // 방 만들기 패널 표시/숨기기
        function showCreateRoom() {
            document.getElementById('createRoomPanel').classList.remove('hidden');
        }
        
        function hideCreateRoom() {
            document.getElementById('createRoomPanel').classList.add('hidden');
        }
        
        // 방 생성
        function createRoom() {
            const roomName = document.getElementById('roomName').value;
            const description = document.getElementById('roomDescription').value;
            const roomType = document.getElementById('roomType').value;
            const genre = document.getElementById('roomGenre').value;
            
            if (!roomName) {
                alert('방 이름을 입력해주세요');
                return;
            }
            
            fetch('/api/chat/create-room', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    room_name: roomName,
                    description: description,
                    room_type: roomType,
                    genre: genre
                })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    loadRooms();
                    hideCreateRoom();
                    // 새로 만든 방에 자동 참가
                    joinRoom(data.room_id);
                }
            });
        }
        
        // 방 메시지 로드
        function loadRoomMessages() {
            if (!currentRoom) return;
            
            fetch(`/api/chat/room/${currentRoom}/messages`)
            .then(r => r.json())
            .then(data => {
                const messagesDiv = document.getElementById('chatMessages');
                messagesDiv.innerHTML = '';
                
                data.messages.forEach(msg => {
                    displayMessage(msg);
                });
            });
        }
        
        // 방 사용자 로드
        function loadRoomUsers() {
            if (!currentRoom) return;
            
            fetch(`/api/chat/room/${currentRoom}/users`)
            .then(r => r.json())
            .then(data => {
                const usersDiv = document.getElementById('roomUsers');
                const userList = data.users.map(u => 
                    `${u.avatar} ${u.username}`
                ).join(' ');
                usersDiv.innerHTML = `온라인: ${userList}`;
            });
        }
        
        // 시스템 메시지 표시
        function displaySystemMessage(message) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message';
            messageDiv.style.background = '#e9ecef';
            messageDiv.innerHTML = `<em>${message}</em>`;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
    </script>
</body>
</html>
'''

def setup_music_chat_interface(app: Flask, socketio: SocketIO):
    """음악 채팅 인터페이스 설정"""
    return MusicChatWebInterface(app, socketio)