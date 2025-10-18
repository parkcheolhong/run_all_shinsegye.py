from modules.ai_code_manager.nlp_processor import NLPProcessor

nlp = NLPProcessor()

# 테스트 문장들
test_sentences = [
    '테스트 해줘',
    '코드를 정리해줘',
    '깃허브와 동기화해줘',
    '시스템 상태 확인해줘',
    '도움말 보여줘',
    '안녕하세요',
    '종료해줘'
]

for sentence in test_sentences:
    result = nlp.process_natural_language(sentence)
    print(f'입력: {sentence}')
    print(f'의도: {result["intent"]}, 신뢰도: {result["confidence"]:.2f}')
    print(f'응답: {result["response"]}')
    print('-' * 50)