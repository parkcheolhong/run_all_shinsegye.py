from modules.ai_code_manager.nlp_processor import NLPProcessor

nlp = NLPProcessor()

# 차분한 응답 테스트
test_sentences = [
    '안녕하세요',
    '코드를 정리해주세요',
    '테스트해주세요',
    '동기화해주세요',
    '도움말 보여주세요'
]

print("🧠 차분한 응답 테스트:")
print("=" * 50)

for sentence in test_sentences:
    result = nlp.process_natural_language(sentence)
    print(f"입력: {sentence}")
    print(f"응답: {result['response']}")
    print("-" * 30)