"""
🎵💬 AI 음악 작사/작곡 채팅장 시스템
사용자들이 실시간으로 음악을 공유하고 협업할 수 있는 채팅 시스템

주요 기능:
- 실시간 채팅
- 음악/가사 공유
- 협업 작곡/작사
- 음악 방 생성
- 사용자 프로필
"""

import json
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import uuid

@dataclass
class ChatUser:
    """채팅 사용자 정보"""
    user_id: str
    username: str
    avatar: str = "🎤"
    join_time: str = ""
    is_online: bool = True
    favorite_genre: str = "팝"
    instruments: List[str] = None
    
    def __post_init__(self):
        if not self.join_time:
            self.join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if self.instruments is None:
            self.instruments = []

@dataclass
class ChatMessage:
    """채팅 메시지"""
    message_id: str
    user_id: str
    username: str
    content: str
    message_type: str  # 'text', 'music', 'lyrics', 'collaboration'
    timestamp: str
    room_id: str
    music_data: Dict[str, Any] = None  # 음악/가사 데이터
    
    def __post_init__(self):
        if not self.message_id:
            self.message_id = str(uuid.uuid4())[:8]
        if not self.timestamp:
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@dataclass
@dataclass
class MusicRoom:
    """음악 채팅 방"""
    room_id: str
    room_name: str
    description: str = ""
    creator_id: str = "system"
    created_at: str = ""
    max_users: int = 10
    current_users: List[str] = None
    room_type: str = "general"  # 'general', 'collaboration', 'jam_session'
    genre: str = "pop"
    is_private: bool = False
    password: Optional[str] = None
    
    def __post_init__(self):
        if self.current_users is None:
            self.current_users = []
        if not self.created_at:
            self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class MusicChatSystem:
    """
    AI 음악 채팅 시스템
    
    사용자들이 실시간으로 음악과 가사를 공유하고 협업할 수 있는 플랫폼
    """
    
    def __init__(self):
        """음악 채팅 시스템 초기화"""
        
        # 데이터 저장소
        self.users: Dict[str, ChatUser] = {}
        self.rooms: Dict[str, MusicRoom] = {}
        self.messages: Dict[str, List[ChatMessage]] = {}  # room_id -> messages
        self.active_collaborations: Dict[str, Dict] = {}
        
        # 스레드 안전성을 위한 락
        self.lock = threading.Lock()
        
        # 기본 방 생성
        self._create_default_rooms()
        
        # 채팅 히스토리 저장 경로
        self.chat_history_file = "data/music_chat_history.json"
        self._load_chat_history()
    
    def _create_default_rooms(self):
        """기본 채팅방들 생성"""
        default_rooms = [
            {
                "room_name": "🎵 일반 음악 채팅",
                "description": "자유로운 음악 이야기를 나누는 공간",
                "room_type": "general",
                "genre": "pop"
            },
            {
                "room_name": "🎼 작곡 협업실",
                "description": "함께 작곡하고 아이디어를 나누는 공간",
                "room_type": "collaboration", 
                "genre": "all"
            },
            {
                "room_name": "📝 작사 워크샵",
                "description": "가사 창작과 시 쓰기를 위한 공간",
                "room_type": "collaboration",
                "genre": "lyrics"
            },
            {
                "room_name": "🎸 잼 세션",
                "description": "실시간 음악 잼 세션을 위한 공간",
                "room_type": "jam_session",
                "genre": "rock"
            }
        ]
        
        for room_data in default_rooms:
            room_id = f"default_{len(self.rooms)}"
            room = MusicRoom(
                room_id=room_id,
                creator_id="system",
                **room_data
            )
            self.rooms[room_id] = room
            self.messages[room_id] = []
    
    def create_user(self, username: str, favorite_genre: str = "팝", 
                   instruments: List[str] = None) -> ChatUser:
        """새 사용자 생성"""
        user_id = str(uuid.uuid4())[:8]
        
        user = ChatUser(
            user_id=user_id,
            username=username,
            favorite_genre=favorite_genre,
            instruments=instruments or []
        )
        
        with self.lock:
            self.users[user_id] = user
        
        return user
    
    def create_room(self, creator_id: str, room_name: str, description: str,
                   room_type: str = "general", genre: str = "pop",
                   max_users: int = 10, is_private: bool = False,
                   password: Optional[str] = None) -> MusicRoom:
        """새 채팅방 생성"""
        room_id = str(uuid.uuid4())[:8]
        
        room = MusicRoom(
            room_id=room_id,
            room_name=room_name,
            description=description,
            creator_id=creator_id,
            room_type=room_type,
            genre=genre,
            max_users=max_users,
            is_private=is_private,
            password=password
        )
        
        with self.lock:
            self.rooms[room_id] = room
            self.messages[room_id] = []
            
        return room
    
    def join_room(self, user_id: str, room_id: str, password: Optional[str] = None) -> bool:
        """사용자가 방에 참가"""
        if room_id not in self.rooms or user_id not in self.users:
            return False
        
        room = self.rooms[room_id]
        
        # 비밀번호 확인
        if room.is_private and room.password != password:
            return False
        
        # 방 인원 제한 확인
        if len(room.current_users) >= room.max_users:
            return False
        
        with self.lock:
            if user_id not in room.current_users:
                room.current_users.append(user_id)
                
                # 입장 메시지 추가
                username = self.users[user_id].username
                join_message = ChatMessage(
                    message_id=str(uuid.uuid4())[:8],
                    user_id="system",
                    username="시스템",
                    content=f"{username}님이 입장하셨습니다.",
                    message_type="system",
                    timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    room_id=room_id
                )
                self.messages[room_id].append(join_message)
        
        return True
    
    def leave_room(self, user_id: str, room_id: str) -> bool:
        """사용자가 방에서 나감"""
        if room_id not in self.rooms or user_id not in self.users:
            return False
        
        room = self.rooms[room_id]
        
        with self.lock:
            if user_id in room.current_users:
                room.current_users.remove(user_id)
                
                # 퇴장 메시지 추가
                username = self.users[user_id].username
                leave_message = ChatMessage(
                    message_id=str(uuid.uuid4())[:8],
                    user_id="system",
                    username="시스템", 
                    content=f"{username}님이 퇴장하셨습니다.",
                    message_type="system",
                    timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    room_id=room_id
                )
                self.messages[room_id].append(leave_message)
        
        return True
    
    def send_message(self, user_id: str, room_id: str, content: str, 
                    message_type: str = "text", music_data: Dict[str, Any] = None) -> bool:
        """메시지 전송"""
        if user_id not in self.users or room_id not in self.rooms:
            return False
        
        user = self.users[user_id]
        room = self.rooms[room_id]
        
        # 사용자가 방에 있는지 확인
        if user_id not in room.current_users:
            return False
        
        message = ChatMessage(
            message_id=str(uuid.uuid4())[:8],
            user_id=user_id,
            username=user.username,
            content=content,
            message_type=message_type,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            room_id=room_id,
            music_data=music_data
        )
        
        with self.lock:
            self.messages[room_id].append(message)
        
        return True
    
    def share_music(self, user_id: str, room_id: str, music_data: Dict[str, Any]) -> bool:
        """음악 작품 공유"""
        music_content = f"🎵 {music_data.get('title', '무제')} 음악을 공유했습니다."
        
        return self.send_message(
            user_id=user_id,
            room_id=room_id,
            content=music_content,
            message_type="music",
            music_data=music_data
        )
    
    def share_lyrics(self, user_id: str, room_id: str, lyrics_data: Dict[str, Any]) -> bool:
        """가사 작품 공유"""
        lyrics_content = f"📝 '{lyrics_data.get('title', '무제')}' 가사를 공유했습니다."
        
        return self.send_message(
            user_id=user_id,
            room_id=room_id,
            content=lyrics_content,
            message_type="lyrics",
            music_data=lyrics_data
        )
    
    def start_collaboration(self, creator_id: str, room_id: str, 
                          collab_type: str, title: str) -> str:
        """협업 프로젝트 시작"""
        collab_id = str(uuid.uuid4())[:8]
        
        collaboration = {
            "collab_id": collab_id,
            "creator_id": creator_id,
            "room_id": room_id,
            "type": collab_type,  # "music", "lyrics", "complete_song"
            "title": title,
            "participants": [creator_id],
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "status": "active",
            "contributions": []
        }
        
        with self.lock:
            self.active_collaborations[collab_id] = collaboration
        
        # 협업 시작 알림 메시지
        creator_name = self.users[creator_id].username
        collab_message = f"🤝 {creator_name}님이 '{title}' {collab_type} 협업을 시작했습니다!"
        
        self.send_message(
            user_id="system",
            room_id=room_id,
            content=collab_message,
            message_type="collaboration",
            music_data={"collaboration_id": collab_id, "action": "start"}
        )
        
        return collab_id
    
    def join_collaboration(self, user_id: str, collab_id: str) -> bool:
        """협업에 참가"""
        if collab_id not in self.active_collaborations:
            return False
        
        collab = self.active_collaborations[collab_id]
        
        with self.lock:
            if user_id not in collab["participants"]:
                collab["participants"].append(user_id)
        
        # 참가 알림
        username = self.users[user_id].username
        join_msg = f"🎼 {username}님이 협업에 참가했습니다!"
        
        self.send_message(
            user_id="system",
            room_id=collab["room_id"],
            content=join_msg,
            message_type="collaboration",
            music_data={"collaboration_id": collab_id, "action": "join"}
        )
        
        return True
    
    def get_room_messages(self, room_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """방의 메시지 목록 조회"""
        if room_id not in self.messages:
            return []
        
        messages = self.messages[room_id][-limit:]
        return [asdict(msg) for msg in messages]
    
    def get_room_list(self) -> List[Dict[str, Any]]:
        """채팅방 목록 조회"""
        return [
            {
                "room_id": room.room_id,
                "room_name": room.room_name,
                "description": room.description,
                "room_type": room.room_type,
                "genre": room.genre,
                "current_users": len(room.current_users),
                "max_users": room.max_users,
                "is_private": room.is_private
            }
            for room in self.rooms.values()
        ]
    
    def get_room_users(self, room_id: str) -> List[Dict[str, Any]]:
        """방의 사용자 목록 조회"""
        if room_id not in self.rooms:
            return []
        
        room = self.rooms[room_id]
        return [
            {
                "user_id": user_id,
                "username": self.users[user_id].username,
                "avatar": self.users[user_id].avatar,
                "favorite_genre": self.users[user_id].favorite_genre,
                "instruments": self.users[user_id].instruments
            }
            for user_id in room.current_users
            if user_id in self.users
        ]
    
    def get_active_collaborations(self, room_id: str) -> List[Dict[str, Any]]:
        """진행 중인 협업 프로젝트 목록"""
        return [
            collab for collab in self.active_collaborations.values()
            if collab["room_id"] == room_id and collab["status"] == "active"
        ]
    
    def _load_chat_history(self):
        """채팅 히스토리 로드"""
        try:
            if os.path.exists(self.chat_history_file):
                with open(self.chat_history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 필요시 히스토리 복원 로직 추가
        except Exception as e:
            print(f"채팅 히스토리 로드 실패: {e}")
    
    def save_chat_history(self):
        """채팅 히스토리 저장"""
        try:
            os.makedirs(os.path.dirname(self.chat_history_file), exist_ok=True)
            
            # 저장할 데이터 준비
            save_data = {
                "rooms": {k: asdict(v) for k, v in self.rooms.items()},
                "recent_messages": {
                    room_id: [asdict(msg) for msg in messages[-100:]]  # 최근 100개만 저장
                    for room_id, messages in self.messages.items()
                },
                "collaborations": self.active_collaborations,
                "saved_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open(self.chat_history_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"채팅 히스토리 저장 실패: {e}")
    
    def get_chat_statistics(self) -> Dict[str, Any]:
        """채팅 시스템 통계"""
        total_messages = sum(len(messages) for messages in self.messages.values())
        
        return {
            "total_users": len(self.users),
            "total_rooms": len(self.rooms),
            "total_messages": total_messages,
            "active_collaborations": len(self.active_collaborations),
            "online_users": len([u for u in self.users.values() if u.is_online])
        }

# 전역 채팅 시스템 인스턴스
music_chat_system = MusicChatSystem()

def get_chat_system():
    """채팅 시스템 인스턴스 반환"""
    return music_chat_system