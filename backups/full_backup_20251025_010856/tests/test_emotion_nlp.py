from modules.ai_code_manager.nlp_processor import NLPProcessor

nlp = NLPProcessor()

# 감정 분석 테스트 문장들
test_sentences = [
    '와! 코드를 빨리 정리해줘!!',
    '고마워, 테스트 해줘',
    '음... 문제가 있는 것 같아',
    '급해! 지금 당장 동기화해줘!',
    '오류가 발생했어 ㅠㅠ',
    '상태를 확인해줘',
    '안녕하세요! 도움말 보여주세요',
    '시스템을 종료해줘'
]

print("🧠 감정 분석 테스트 결과:")
print("=" * 60)

for sentence in test_sentences:
    result = nlp.process_natural_language(sentence)
    print(f"입력: {sentence}")
    print(f"의도: {result['intent']}")
    print(f"감정: {result['emotion']}")
    print(f"신뢰도: {result['confidence']:.2f}")
    print(f"응답: {result['response']}")
    print("-" * 50)