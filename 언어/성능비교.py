import time

def test_analyzers():
    # 테스트 텍스트
    text = "안녕하세요. 오늘 날씨가 정말 좋네요. 파이썬으로 자연어 처리를 공부하고 있습니다."
    
    results = {}
    
    # Mecab
    try:
        from konlpy.tag import Mecab
        mecab = Mecab()
        start = time.time()
        result = mecab.pos(text)
        end = time.time()
        results['Mecab'] = {'time': end-start, 'count': len(result), 'sample': result[:3]}
    except:
        results['Mecab'] = {'error': 'Not installed'}
    
    # Okt
    try:
        from konlpy.tag import Okt
        okt = Okt()
        start = time.time()
        result = okt.pos(text)
        end = time.time()
        results['Okt'] = {'time': end-start, 'count': len(result), 'sample': result[:3]}
    except:
        results['Okt'] = {'error': 'Not installed'}
    
    # Kkma
    try:
        from konlpy.tag import Kkma
        kkma = Kkma()
        start = time.time()
        result = kkma.pos(text)
        end = time.time()
        results['Kkma'] = {'time': end-start, 'count': len(result), 'sample': result[:3]}
    except:
        results['Kkma'] = {'error': 'Not installed'}
    
    # Hannanum
    try:
        from konlpy.tag import Hannanum
        hannanum = Hannanum()
        start = time.time()
        result = hannanum.pos(text)
        end = time.time()
        results['Hannanum'] = {'time': end-start, 'count': len(result), 'sample': result[:3]}
    except:
        results['Hannanum'] = {'error': 'Not installed'}
    
    # Khaiii
    try:
        from khaiii import KhaiiiApi
        api = KhaiiiApi()
        start = time.time()
        result = []
        for word in api.analyze(text):
            for morph in word.morphs:
                result.append((morph.lex, morph.tag))
        end = time.time()
        results['Khaiii'] = {'time': end-start, 'count': len(result), 'sample': result[:3]}
    except:
        results['Khaiii'] = {'error': 'Not installed'}
    
    # Soynlp
    try:
        from soynlp.word import WordExtractor
        from soynlp.tokenizer import LTokenizer
        word_extractor = WordExtractor()
        word_extractor.train([text])
        words = word_extractor.extract()
        cohesion_score = {word: score.cohesion_forward for word, score in words.items()}
        tokenizer = LTokenizer(scores=cohesion_score)
        start = time.time()
        result = [(token, 'WORD') for token in tokenizer.tokenize(text)]
        end = time.time()
        results['Soynlp'] = {'time': end-start, 'count': len(result), 'sample': result[:3]}
    except:
        results['Soynlp'] = {'error': 'Not installed'}
    
    # 결과 출력
    print("=== 형태소 분석기 성능 비교 ===")
    print(f"테스트 텍스트: {text}")
    print()
    
    print(f"{'분석기':<10} {'시간(초)':<10} {'형태소수':<10} {'샘플결과'}")
    print("-" * 60)
    
    for name, result in results.items():
        if 'error' in result:
            print(f"{name:<10} {'설치안됨':<10} {'':<10} {result['error']}")
        else:
            print(f"{name:<10} {result['time']:.4f}초{'':<3} {result['count']:<10} {result['sample']}")
    
    # 속도 순위
    print("\n=== 속도 순위 ===")
    speed_ranking = [(name, data['time']) for name, data in results.items() if 'time' in data]
    speed_ranking.sort(key=lambda x: x[1])
    
    for i, (name, time_val) in enumerate(speed_ranking, 1):
        print(f"{i}위: {name} ({time_val:.4f}초)")

if __name__ == "__main__":
    test_analyzers()