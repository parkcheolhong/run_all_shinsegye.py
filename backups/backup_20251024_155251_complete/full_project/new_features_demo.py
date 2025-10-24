"""
🚀 소리새 AI 새로운 기능 데모
2번: 개인 맞춤 AI 튜터
4번: AI 기반 실시간 게임 생성기
"""

from modules.ai_code_manager.personal_ai_tutor import PersonalAITutor, create_ai_tutor_response
from modules.ai_code_manager.realtime_game_generator import RealTimeGameGenerator, create_game_response

def demo_ai_tutor():
    """🎓 AI 튜터 데모"""
    print("🎓 개인 맞춤 AI 튜터 데모")
    print("="*50)
    
    tutor = PersonalAITutor()
    
    # 1. 학습 계획 생성
    print("📚 1. 개인 맞춤 학습 계획:")
    learning_path = tutor.suggest_learning_path()
    for i, step in enumerate(learning_path, 1):
        print(f"   {i}. {step}")
    
    # 2. 도전 과제 생성
    print(f"\n🎯 2. 오늘의 도전 과제:")
    challenge = tutor.generate_personalized_challenge()
    print(f"   {challenge}")
    
    # 3. 격려 메시지
    print(f"\n💪 3. 격려 메시지:")
    encouragement = tutor.get_personalized_encouragement()
    print(f"   {encouragement}")
    
    # 4. 코딩 패턴 분석
    print(f"\n🔍 4. 코딩 스타일 피드백:")
    sample_code = '''
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
'''
    feedback = tutor.analyze_coding_pattern(sample_code, "python")
    for fb in feedback[:3]:
        print(f"   • {fb}")
    
    # 5. 음성 명령 응답 테스트
    print(f"\n🎤 5. 음성 명령 테스트:")
    commands = [
        "학습 계획 세워줘",
        "도전 과제 주세요",
        "격려해주세요",
        "코딩 실력 평가해줘"
    ]
    
    for cmd in commands:
        response = create_ai_tutor_response(cmd)
        print(f"   명령: '{cmd}'")
        print(f"   응답: {response[:60]}...")
        print()

def demo_game_generator():
    """🎮 게임 생성기 데모"""
    print("\n🎮 AI 기반 실시간 게임 생성기 데모")
    print("="*50)
    
    generator = RealTimeGameGenerator()
    
    # 1. 다양한 게임 생성
    game_requests = [
        "간단한 수학 퍼즐 만들어줘",
        "어려운 코딩 퀴즈 만들어줘", 
        "타이핑 게임 만들어줘",
        "단어 퍼즐 만들어줘"
    ]
    
    games = []
    for i, request in enumerate(game_requests, 1):
        print(f"🎲 {i}. 게임 생성 테스트:")
        print(f"   요청: {request}")
        
        game = generator.create_game(request)
        games.append(game)
        
        print(f"   게임명: {game['data']['name']}")
        print(f"   문제: {game['data']['question']}")
        print(f"   정답: {game['data']['answer']}")
        print(f"   타입: {game['request']['type']} ({game['request']['difficulty']})")
        print()
    
    # 2. 게임 플레이 시뮬레이션
    print("🕹️ 게임 플레이 시뮬레이션:")
    if games:
        test_game = games[0]  # 첫 번째 게임으로 테스트
        print(f"   게임: {test_game['data']['name']}")
        print(f"   문제: {test_game['data']['question']}")
        
        # 정답 입력
        correct_answer = test_game['data']['answer']
        result = generator.play_game(test_game, correct_answer)
        
        print(f"   입력: {correct_answer}")
        print(f"   결과: {result['message']}")
        print(f"   점수: {test_game.get('score', 0)}점")
    
    # 3. 음성 명령 응답 테스트
    print(f"\n🎤 음성 명령 테스트:")
    commands = [
        "퍼즐 게임 만들어줘",
        "코딩 퀴즈 만들어줘",
        "재미있는 게임하자",
        "어려운 액션 게임 만들어줘"
    ]
    
    for cmd in commands:
        response = create_game_response(cmd)
        print(f"   명령: '{cmd}'")
        print(f"   응답: {response[:80]}...")
        print()

def demo_integration():
    """🔗 소리새 통합 데모"""
    print("\n🔗 소리새 AI 통합 시스템 데모")
    print("="*50)
    
    print("🎯 새로 추가된 기능들:")
    print("   1. 🎓 개인 맞춤 AI 튜터")
    print("      - 개인별 학습 패턴 분석")
    print("      - 맞춤형 커리큘럼 생성") 
    print("      - 실시간 코딩 스타일 피드백")
    print("      - 격려 및 동기부여 시스템")
    
    print("\n   2. 🎮 AI 기반 실시간 게임 생성")
    print("      - 음성 명령으로 즉석 게임 생성")
    print("      - 다양한 장르 지원 (퍼즐, 액션, 학습, 전략)")
    print("      - 난이도 자동 조정")
    print("      - 실시간 플레이 및 채점")
    
    print("\n🎤 사용 예시:")
    print("   '소리새야, 파이썬 학습 계획 세워줘'")
    print("   '코딩 실력을 평가해줘'")  
    print("   '격려해줘, 힘들어'")
    print("   '간단한 퍼즐 게임 만들어줘'")
    print("   '어려운 코딕 퀴즈 도전하고 싶어'")
    
    print(f"\n✨ 이제 소리새가 더욱 스마트해졌습니다!")
    print(f"   - 🧠 개인화된 학습 지원")
    print(f"   - 🎮 즐거운 게임 경험")  
    print(f"   - 🚀 실시간 콘텐츠 생성")

if __name__ == "__main__":
    print("🌟 2025년 핫 트렌드 기능 추가 완료! 🌟")
    print("소리새 AI가 더욱 똑똑하고 재미있어졌습니다!")
    print()
    
    # AI 튜터 데모
    demo_ai_tutor()
    
    # 게임 생성기 데모  
    demo_game_generator()
    
    # 통합 시스템 데모
    demo_integration()
    
    print("\n🎉 새로운 기능들이 소리새에 성공적으로 추가되었습니다!")
    print("이제 'python run_all_shinsegye.py'로 실행해서 체험해보세요! 🚀")