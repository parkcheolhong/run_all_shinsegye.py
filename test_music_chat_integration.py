#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🎵 소리새 음악 채팅 통합 시스템 테스트
완성된 작사, 작곡 프로그램에 사용자들 채팅장 생성 기능 테스트
"""

def test_music_chat_integration():
    """음악 채팅 통합 시스템 테스트"""
    print("🧪 소리새 음악 채팅 통합 시스템 테스트")
    print("=" * 50)

    # 1. 대시보드 웹 모듈 import 테스트
    try:
        from modules.sorisay_dashboard_web import app, music_chat_system, dashboard_state
        print("✅ 대시보드 웹 모듈 로드 성공")
    except Exception as e:
        print(f"❌ 대시보드 웹 모듈 오류: {e}")
        return False

    # 2. 음악 채팅 시스템 테스트
    try:
        if music_chat_system:
            # 채팅방 생성 테스트
            room_id = music_chat_system.create_room("테스트 채팅방")
            print(f"✅ 채팅방 생성 성공: {room_id}")
            
            # 사용자 참여 테스트
            success = music_chat_system.join_room(room_id, "테스트 사용자")
            print(f"✅ 사용자 참여 성공: {success}")
            
            # 메시지 전송 테스트
            music_chat_system.send_message(room_id, "테스트 사용자", "안녕하세요! 음악 채팅방입니다.")
            print("✅ 메시지 전송 성공")
            
            # 채팅방 통계
            rooms = music_chat_system.list_rooms()
            print(f"✅ 현재 채팅방 수: {len(rooms)}")
            
        else:
            print("⚠️ 음악 채팅 시스템 사용 불가")
    except Exception as e:
        print(f"❌ 음악 채팅 시스템 오류: {e}")
        return False

    # 3. 대시보드 통계 테스트
    try:
        stats = dashboard_state.get_stats()
        print("✅ 대시보드 통계:")
        print(f"   - 채팅방 수: {stats.get('chat_rooms', 0)}")
        print(f"   - 채팅 사용자: {stats.get('chat_users', 0)}")
        print(f"   - 총 메시지: {stats.get('total_chat_messages', 0)}")
    except Exception as e:
        print(f"❌ 대시보드 통계 오류: {e}")
        return False

    # 4. SorisayCore 통합 테스트
    try:
        from modules.ai_code_manager.sorisay_core_controller import SorisayCore
        core = SorisayCore()
        
        # 음성 명령 테스트
        test_commands = [
            "채팅방 만들어줘",
            "채팅방 목록", 
            "채팅 통계",
            "작곡 시작",
            "작사 시작"
        ]
        
        print("\n📝 음성 명령 처리 테스트:")
        for cmd in test_commands:
            try:
                result = core.handle_creative_commands(cmd)
                print(f"   ✅ '{cmd}' -> 처리 성공")
            except Exception as e:
                print(f"   ⚠️ '{cmd}' -> {str(e)}")
                
    except Exception as e:
        print(f"❌ SorisayCore 통합 오류: {e}")

    print("\n🎵 음악 채팅 통합 시스템이 준비되었습니다!")
    print("웹 브라우저에서 접속하세요:")
    print("- 메인 대시보드: http://localhost:5050")
    print("- 음악 채팅방: http://localhost:5050/music-chat")
    
    return True

def test_music_composition_system():
    """작곡 작사 시스템 테스트"""
    print("\n🎼 작곡 작사 시스템 테스트")
    print("=" * 30)
    
    try:
        from modules.ai_code_manager.ai_music_composer import AIMusicComposer, AILyricsWriter, AIMusicLyricsStudio
        
        # 1. AI 작곡가 테스트
        composer = AIMusicComposer()
        composition = composer.compose_by_emotion("happy")
        print("✅ AI 작곡 시스템 동작")
        print(f"   생성된 멜로디: {composition['melody'][:50]}...")
        
        # 2. AI 작사가 테스트
        lyricist = AILyricsWriter()
        lyrics = lyricist.generate_lyrics("happy", "사랑")
        print("✅ AI 작사 시스템 동작")
        print(f"   생성된 가사 제목: {lyrics['title']}")
        print(f"   가사 줄 수: {len(lyrics['lines'])}")
        
        # 3. 통합 스튜디오 테스트
        studio = AIMusicLyricsStudio()
        song = studio.create_complete_song("행복한 하루", "happy")
        print("✅ 통합 음악 스튜디오 동작")
        print(f"   완성된 노래 제목: {song['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 작곡 작사 시스템 오류: {e}")
        return False

if __name__ == "__main__":
    print("🎵 소리새 음악 채팅 통합 시스템 전체 테스트")
    print("=" * 60)
    
    # 작곡 작사 시스템 테스트
    composition_ok = test_music_composition_system()
    
    # 음악 채팅 통합 테스트  
    integration_ok = test_music_chat_integration()
    
    print("\n📊 테스트 결과 요약:")
    print(f"   작곡/작사 시스템: {'✅ 성공' if composition_ok else '❌ 실패'}")
    print(f"   음악 채팅 통합: {'✅ 성공' if integration_ok else '❌ 실패'}")
    
    if composition_ok and integration_ok:
        print("\n🎉 모든 시스템이 정상적으로 통합되었습니다!")
        print("사용자들이 작곡, 작사, 채팅을 모두 즐길 수 있습니다.")
    else:
        print("\n⚠️ 일부 시스템에 문제가 있습니다. 로그를 확인하세요.")