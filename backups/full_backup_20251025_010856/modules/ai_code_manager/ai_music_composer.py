"""
🎵 AI 음악 작곡가 시스템 (AI Music Composer)
코드 패턴을 음악으로 변환하고 감정 기반 작곡을 수행하는 혁신적인 AI 시스템

주요 기능:
- 프로그래밍 코드를 음악 패턴으로 변환
- 감정 상태에 따른 맞춤형 작곡
- ASCII 텍스트 기반 악보 생성
- 12가지 감정별 음악 스타일 지원
"""
import json
import random
import re
from typing import Dict, List, Any, Tuple
from datetime import datetime

class AIMusicComposer:
    """
    AI 음악 작곡가 클래스
    
    이 클래스는 프로그래밍 코드를 분석하여 음악으로 변환하거나
    사용자의 감정 상태를 기반으로 맞춤형 음악을 작곡합니다.
    """
    
    def __init__(self):
        """AI 음악 작곡가 초기화"""
        
        # 기본 음계 정의 (12음계)
        self.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        # 음계별 음정 패턴 정의
        # 음계별 음정 패턴 정의
        self.scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],      # 장조 (밝고 행복한 느낌)
            'minor': [0, 2, 3, 5, 7, 8, 10],      # 단조 (슬프고 서정적인 느낌)
            'pentatonic': [0, 2, 4, 7, 9],        # 5음계 (평온하고 동양적인 느낌)
            'blues': [0, 3, 5, 6, 7, 10]          # 블루스 (재즈적이고 감성적인 느낌)
        }
        
        # 감정별 음악 스타일 정의
        # 각 감정에 맞는 음계, 템포, 리듬, 조성을 매핑
        self.emotion_styles = {
            'happy': {      # 기쁜 감정
                'scale': 'major',        # 장조 사용
                'tempo': 'fast',         # 빠른 템포
                'rhythm': 'upbeat',      # 경쾌한 리듬
                'key': 'C'              # C 장조
            },
            'sad': {        # 슬픈 감정
                'scale': 'minor',        # 단조 사용
                'tempo': 'slow',         # 느린 템포
                'rhythm': 'melancholy',  # 우울한 리듬
                'key': 'Am'             # A 단조
            },
            'excited': {    # 흥분된 감정
                'scale': 'major',        # 장조 사용
                'tempo': 'very_fast',    # 매우 빠른 템포
                'rhythm': 'energetic',   # 에너지틱한 리듬
                'key': 'G'              # G 장조
            },
            'calm': {       # 평온한 감정
                'scale': 'pentatonic',   # 5음계 사용
                'tempo': 'moderate',     # 적당한 템포
                'rhythm': 'flowing',     # 흐르는 듯한 리듬
                'key': 'F'              # F 장조
            },
            'creative': {   # 창의적인 감정
                'scale': 'blues',        # 블루스 음계
                'tempo': 'varied',       # 다양한 템포
                'rhythm': 'jazz',        # 재즈 리듬
                'key': 'Bb'            # Bb 장조
            }
        }
        
        # 프로그래밍 코드 패턴을 음악 요소로 매핑
        # 각 프로그래밍 구문을 특정 음악적 표현으로 변환
        self.code_music_mapping = {
            'for': '반복 리듬 패턴',          # 반복문 → 반복적인 리듬
            'if': '조건부 화음 변화',         # 조건문 → 화음의 변화
            'function': '메인 멜로디 라인',   # 함수 → 주선율
            'class': '전체 곡 구조',         # 클래스 → 곡의 전체 구조
            'return': '마무리 코다',         # 반환문 → 곡의 마무리
            'print': '악센트 노트',          # 출력문 → 강조 음표
            'while': '지속적인 베이스 라인', # 무한루프 → 지속되는 베이스
            'try': '실험적 불협화음',        # 예외처리 → 실험적 화음
            'except': '해결 화음'           # 예외처리 → 불협화음의 해결
        }
        
        # 작곡된 음악들을 저장하는 리스트
        self.compositions = []
    
    def analyze_code_pattern(self, code: str) -> Dict[str, Any]:
        """
        프로그래밍 코드 패턴을 음악적 요소로 분석
        
        Args:
            code (str): 분석할 프로그래밍 코드
            
        Returns:
            Dict[str, Any]: 음악적 요소로 변환된 분석 결과
                - complexity: 코드 복잡도 (1-10)
                - rhythm_pattern: 리듬 패턴
                - melodic_structure: 멜로디 구조
                - harmonic_elements: 화성 요소
        """
        analysis = {
            'complexity': self.calculate_complexity(code),
            'rhythm_pattern': self.extract_rhythm_pattern(code),
            'melodic_structure': self.extract_melodic_structure(code),
            'harmonic_elements': self.extract_harmonic_elements(code)
        }
        
        return analysis
    
    def calculate_complexity(self, code: str) -> int:
        """
        코드 복잡도를 음악 복잡도로 변환
        
        Args:
            code (str): 분석할 코드
            
        Returns:
            int: 음악 복잡도 (1-10 스케일)
        """
        # 코드의 여러 요소를 분석하여 복잡도 계산
        lines = len(code.split('\n'))                    # 총 라인 수
        functions = len(re.findall(r'def\s+\w+', code))  # 함수 개수
        loops = len(re.findall(r'(for|while)', code))    # 반복문 개수
        conditionals = len(re.findall(r'if\s+', code))   # 조건문 개수
        
        # 가중치를 적용하여 복잡도 계산
        complexity = (lines * 0.1) + (functions * 2) + (loops * 1.5) + (conditionals * 1)
        return min(int(complexity), 10)  # 1-10 스케일로 제한
    
    def extract_rhythm_pattern(self, code: str) -> List[str]:
        """
        코드에서 리듬 패턴 추출
        
        Args:
            code (str): 분석할 코드
            
        Returns:
            List[str]: 추출된 리듬 패턴 리스트
        """
        patterns = []
        
        # 들여쓰기 레벨을 기반으로 리듬 패턴 생성
        lines = code.split('\n')
        for line in lines:
            if line.strip():
                indent_level = (len(line) - len(line.lstrip())) // 4
                if indent_level == 0:
                    patterns.append('강박')
                elif indent_level == 1:
                    patterns.append('약박')
                else:
                    patterns.append('오프비트')
        
        return patterns[:16]  # 최대 16박자
    
    def extract_melodic_structure(self, code: str) -> List[int]:
        """코드에서 멜로디 구조 추출"""
        melody = []
        
        # 함수명과 변수명의 길이를 음높이로 변환
        words = re.findall(r'\b[a-zA-Z_]\w*\b', code)
        for word in words[:12]:  # 12음 한 옥타브
            note_index = len(word) % 12
            melody.append(note_index)
        
        return melody
    
    def extract_harmonic_elements(self, code: str) -> Dict[str, int]:
        """코드에서 화음 요소 추출"""
        harmonics = {}
        
        for keyword, description in self.code_music_mapping.items():
            count = len(re.findall(keyword, code, re.IGNORECASE))
            if count > 0:
                harmonics[keyword] = count
        
        return harmonics
    
    def compose_from_code(self, code: str, emotion: str = "neutral") -> Dict[str, Any]:
        """코드를 기반으로 음악 작곡"""
        analysis = self.analyze_code_pattern(code)
        
        # 감정 스타일 결정
        if emotion not in self.emotion_styles:
            emotion = "calm"
        
        style = self.emotion_styles[emotion]
        
        # 멜로디 생성
        melody = self.generate_melody(analysis['melodic_structure'], style['scale'], style['key'])
        
        # 리듬 패턴 생성
        rhythm = self.generate_rhythm(analysis['rhythm_pattern'], style['tempo'])
        
        # 화음 진행 생성
        chords = self.generate_chord_progression(analysis['harmonic_elements'], style['key'])
        
        composition = {
            'title': f"Code Symphony in {style['key']}",
            'composer': 'AI Music Bot',
            'timestamp': datetime.now().isoformat(),
            'emotion': emotion,
            'style': style,
            'melody': melody,
            'rhythm': rhythm,
            'chords': chords,
            'code_analysis': analysis,
            'ascii_notation': self.create_ascii_notation(melody, rhythm)
        }
        
        self.compositions.append(composition)
        return composition
    
    def generate_melody(self, structure: List[int], scale: str, key: str) -> List[str]:
        """멜로디 라인 생성"""
        scale_notes = self.scales[scale]
        key_index = self.notes.index(key) if key in self.notes else 0
        
        melody = []
        for note_num in structure:
            scale_degree = note_num % len(scale_notes)
            note_index = (key_index + scale_notes[scale_degree]) % 12
            melody.append(self.notes[note_index])
        
        return melody
    
    def generate_rhythm(self, pattern: List[str], tempo: str) -> List[str]:
        """리듬 패턴 생성"""
        tempo_mapping = {
            'slow': ['♩', '♩', '𝅗𝅥', '♩'],
            'moderate': ['♪', '♪', '♩', '♪', '♪'],
            'fast': ['♬', '♬', '♬', '♬', '♪', '♪'],
            'very_fast': ['♬', '♬', '♬', '♬', '♬', '♬', '♬', '♬'],
            'varied': ['♩', '♪', '♬', '𝅗𝅥', '♪']
        }
        
        base_rhythm = tempo_mapping.get(tempo, tempo_mapping['moderate'])
        
        # 패턴에 따라 리듬 조정
        rhythm = []
        for i, beat_type in enumerate(pattern):
            if i < len(base_rhythm):
                if beat_type == '강박':
                    rhythm.append('♩')  # 4분음표
                elif beat_type == '약박':
                    rhythm.append('♪')  # 8분음표
                else:
                    rhythm.append('♬')  # 16분음표
            else:
                rhythm.append(random.choice(base_rhythm))
        
        return rhythm[:16]
    
    def generate_chord_progression(self, harmonics: Dict[str, int], key: str) -> List[str]:
        """화음 진행 생성"""
        # 기본 코드 진행 (I-V-vi-IV)
        if key.endswith('m'):  # 단조
            progressions = [
                ['Am', 'F', 'C', 'G'],
                ['Am', 'Dm', 'G', 'C'],
                ['Am', 'F', 'G', 'Am']
            ]
        else:  # 장조
            progressions = [
                ['C', 'G', 'Am', 'F'],
                ['C', 'F', 'G', 'C'],
                ['C', 'Am', 'F', 'G']
            ]
        
        # harmonics에 따라 진행 선택
        total_elements = sum(harmonics.values()) if harmonics else 1
        progression_index = total_elements % len(progressions)
        
        return progressions[progression_index]
    
    def create_ascii_notation(self, melody: List[str], rhythm: List[str]) -> str:
        """ASCII 악보 표기법 생성"""
        notation = "🎵 ASCII 음악 표기:\n"
        notation += "=" * 40 + "\n"
        
        # 멜로디 라인
        melody_line = "Melody: "
        for i, note in enumerate(melody):
            rhythm_symbol = rhythm[i] if i < len(rhythm) else '♩'
            melody_line += f"{note}{rhythm_symbol} "
        
        notation += melody_line + "\n"
        
        # 시각적 표현
        notation += "\nVisual:\n"
        for note in melody[:8]:  # 처음 8음만
            height = self.notes.index(note) if note in self.notes else 0
            spaces = " " * (height // 2)
            notation += f"{spaces}●\n"
        
        return notation
    
    def compose_by_emotion(self, emotion: str, length: int = 8) -> Dict[str, Any]:
        """감정 기반 순수 작곡"""
        if emotion not in self.emotion_styles:
            emotion = "calm"
        
        style = self.emotion_styles[emotion]
        
        # 감정에 맞는 멜로디 생성
        melody = []
        scale_notes = self.scales[style['scale']]
        key_index = self.notes.index(style['key']) if style['key'] in self.notes else 0
        
        for i in range(length):
            if emotion == "happy":
                # 상승하는 멜로디
                scale_degree = (i + random.randint(0, 2)) % len(scale_notes)
            elif emotion == "sad":
                # 하강하는 멜로디
                scale_degree = (len(scale_notes) - 1 - i + random.randint(-1, 1)) % len(scale_notes)
            else:
                # 무작위 하지만 스케일 내에서
                scale_degree = random.choice(range(len(scale_notes)))
            
            note_index = (key_index + scale_notes[scale_degree]) % 12
            melody.append(self.notes[note_index])
        
        # 리듬 생성
        rhythm = self.generate_rhythm(['강박'] * length, style['tempo'])
        
        # 화음 생성
        chords = self.generate_chord_progression({}, style['key'])
        
        composition = {
            'title': f"{emotion.capitalize()} Mood in {style['key']}",
            'composer': 'AI Emotion Composer',
            'timestamp': datetime.now().isoformat(),
            'emotion': emotion,
            'style': style,
            'melody': melody,
            'rhythm': rhythm,
            'chords': chords,
            'ascii_notation': self.create_ascii_notation(melody, rhythm)
        }
        
        self.compositions.append(composition)
        return composition
    
    def get_composition_summary(self) -> str:
        """작곡 목록 요약"""
        if not self.compositions:
            return "🎵 아직 작곡된 곡이 없습니다."
        
        summary = f"🎼 **작곡 목록** ({len(self.compositions)}곡):\n\n"
        
        for i, comp in enumerate(self.compositions, 1):
            summary += f"{i}. **{comp['title']}**\n"
            summary += f"   감정: {comp['emotion']} | 조성: {comp['style']['key']}\n"
            summary += f"   작곡 시간: {comp['timestamp'][:16]}\n\n"
        
        return summary
    
    def play_composition_text(self, composition: Dict[str, Any]) -> str:
        """작곡을 텍스트로 "연주" """
        result = f"🎵 **{composition['title']}** 연주 중...\n\n"
        result += f"🎭 감정: {composition['emotion']}\n"
        result += f"🎹 조성: {composition['style']['key']} {composition['style']['scale']}\n"
        result += f"🥁 템포: {composition['style']['tempo']}\n\n"
        
        result += composition['ascii_notation'] + "\n"
        
        result += "🎶 화음 진행:\n"
        chord_line = " → ".join(composition['chords'])
        result += f"   {chord_line}\n\n"
        
        result += "✨ 이 음악이 마음에 드시나요? 다른 감정으로도 작곡해드릴 수 있어요!"
        
        return result

class AILyricsWriter:
    """
    AI 작사가 클래스
    
    감정과 테마를 기반으로 자동으로 가사를 생성하는 시스템
    """
    
    def __init__(self):
        """AI 작사가 초기화"""
        
        # 감정별 기본 단어 데이터베이스
        self.emotion_words = {
            'happy': {
                '형용사': ['행복한', '즐거운', '밝은', '웃는', '기쁜', '환한', '빛나는', '따뜻한'],
                '명사': ['웃음', '햇빛', '꿈', '희망', '사랑', '봄', '꽃', '하늘', '별'],
                '동사': ['웃다', '노래하다', '춤추다', '달리다', '날아가다', '빛나다', '피어나다']
            },
            'sad': {
                '형용사': ['슬픈', '외로운', '쓸쓸한', '아픈', '그리운', '차가운', '어두운', '무거운'],
                '명사': ['눈물', '비', '이별', '그리움', '밤', '달', '바람', '기억', '아픔'],
                '동사': ['울다', '그리워하다', '떠나다', '사라지다', '기다리다', '흘러가다', '잊다']
            },
            'romantic': {
                '형용사': ['사랑스러운', '로맨틱한', '달콤한', '부드러운', '포근한', '따스한', '예쁜'],
                '명사': ['사랑', '연인', '마음', '키스', '포옹', '약속', '데이트', '꽃', '하트'],
                '동사': ['사랑하다', '안다', '키스하다', '약속하다', '만나다', '걷다', '속삭이다']
            },
            'energetic': {
                '형용사': ['역동적인', '강한', '뜨거운', '활기찬', '파워풀한', '멋진', '자유로운'],
                '명사': ['힘', '에너지', '열정', '도전', '승리', '자유', '꿈', '미래', '무대'],
                '동사': ['달리다', '뛰다', '싸우다', '도전하다', '이기다', '외치다', '넘어서다']
            }
        }
        
        # 가사 구조 템플릿
        self.lyric_templates = {
            'verse': [
                "{형용사} {명사}가 {동사}",
                "{명사} 속에서 {동사}는",
                "언제나 {형용사} {명사}를",
                "{동사}면서 {명사}를 생각해"
            ],
            'chorus': [
                "{명사}야, {명사}야",
                "{형용사} {명사}처럼",
                "우리 함께 {동사}자",
                "{명사}가 {형용사} 세상에서"
            ],
            'bridge': [
                "이제는 {동사} 시간",
                "{형용사} {명사}들이",
                "모든 {명사}를 넘어서",
                "{동사}는 그 순간"
            ]
        }
        
        # 운율 패턴
        self.rhyme_patterns = ['AABA', 'ABAB', 'AABB', 'ABCB']
        
        # 생성된 가사 저장
        self.lyrics_history = []
    
    def generate_lyrics(self, emotion: str = 'happy', theme: str = None, lines: int = 8) -> Dict[str, Any]:
        """
        감정과 테마를 기반으로 가사 생성
        
        Args:
            emotion (str): 감정 ('happy', 'sad', 'romantic', 'energetic')
            theme (str): 가사 주제 (선택사항)
            lines (int): 생성할 가사 줄 수
            
        Returns:
            Dict[str, Any]: 생성된 가사 정보
        """
        if emotion not in self.emotion_words:
            emotion = 'happy'
        
        # 가사 구조 결정
        structure = self._determine_structure(lines)
        
        # 가사 생성
        lyrics_lines = []
        for section_type, section_lines in structure.items():
            section_lyrics = self._generate_section(emotion, section_type, section_lines)
            lyrics_lines.extend(section_lyrics)
        
        # 가사 정보 구성
        lyrics_info = {
            'emotion': emotion,
            'theme': theme,
            'lines': lyrics_lines,
            'structure': structure,
            'rhyme_pattern': random.choice(self.rhyme_patterns),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'title': self._generate_title(emotion, theme)
        }
        
        # 히스토리에 추가
        self.lyrics_history.append(lyrics_info)
        
        return lyrics_info
    
    def _determine_structure(self, total_lines: int) -> Dict[str, int]:
        """가사 구조 결정"""
        if total_lines <= 4:
            return {'verse': total_lines}
        elif total_lines <= 8:
            return {'verse': total_lines // 2, 'chorus': total_lines // 2}
        else:
            verse_lines = total_lines // 3
            chorus_lines = total_lines // 3
            bridge_lines = total_lines - verse_lines - chorus_lines
            return {'verse': verse_lines, 'chorus': chorus_lines, 'bridge': bridge_lines}
    
    def _generate_section(self, emotion: str, section_type: str, num_lines: int) -> List[str]:
        """특정 섹션의 가사 생성"""
        words = self.emotion_words[emotion]
        templates = self.lyric_templates.get(section_type, self.lyric_templates['verse'])
        
        section_lines = []
        for _ in range(num_lines):
            template = random.choice(templates)
            
            # 템플릿에 단어 대입
            line = template
            if '{형용사}' in line:
                line = line.replace('{형용사}', random.choice(words['형용사']))
            if '{명사}' in line:
                line = line.replace('{명사}', random.choice(words['명사']))
            if '{동사}' in line:
                line = line.replace('{동사}', random.choice(words['동사']))
            
            section_lines.append(line)
        
        return section_lines
    
    def _generate_title(self, emotion: str, theme: str = None) -> str:
        """가사 제목 생성"""
        if theme:
            return f"{theme}의 노래"
        
        emotion_titles = {
            'happy': ['행복한 하루', '웃음의 노래', '밝은 세상', '기쁨의 춤'],
            'sad': ['슬픈 이별', '그리운 사람', '눈물의 기억', '외로운 밤'],
            'romantic': ['사랑의 고백', '달콤한 약속', '로맨틱한 밤', '첫사랑'],
            'energetic': ['열정의 노래', '힘찬 도전', '꿈을 향해', '승리의 함성']
        }
        
        return random.choice(emotion_titles.get(emotion, emotion_titles['happy']))
    
    def format_lyrics_display(self, lyrics_info: Dict[str, Any]) -> str:
        """가사를 보기 좋게 포맷팅"""
        result = f"🎤 **{lyrics_info['title']}**\n"
        result += f"📝 감정: {lyrics_info['emotion']} | 운율: {lyrics_info['rhyme_pattern']}\n"
        result += f"⏰ 작성시간: {lyrics_info['created_at']}\n\n"
        
        result += "📜 **가사:**\n"
        result += "=" * 40 + "\n\n"
        
        for i, line in enumerate(lyrics_info['lines'], 1):
            result += f"{i:2d}. {line}\n"
        
        result += "\n" + "=" * 40 + "\n"
        result += "✨ 이 가사가 마음에 드시나요? 다른 감정으로도 작사해드릴 수 있어요!"
        
        return result
    
    def get_lyrics_history(self) -> str:
        """작사 히스토리 조회"""
        if not self.lyrics_history:
            return "📝 아직 작성된 가사가 없습니다."
        
        result = f"📚 **작사 히스토리** ({len(self.lyrics_history)}곡):\n\n"
        
        for i, lyrics in enumerate(self.lyrics_history, 1):
            result += f"{i}. **{lyrics['title']}**\n"
            result += f"   감정: {lyrics['emotion']} | 줄수: {len(lyrics['lines'])}줄\n"
            result += f"   작성: {lyrics['created_at'][:16]}\n\n"
        
        return result

class AIMusicLyricsStudio:
    """
    AI 음악 작곡 & 작사 통합 스튜디오
    
    작곡과 작사를 함께 수행하는 통합 시스템
    """
    
    def __init__(self):
        """AI 음악 스튜디오 초기화"""
        self.composer = AIMusicComposer()
        self.lyricist = AILyricsWriter()
        self.complete_songs = []
    
    def create_complete_song(self, emotion: str = 'happy', theme: str = None, 
                           code: str = None) -> Dict[str, Any]:
        """
        완전한 노래 (작곡 + 작사) 생성
        
        Args:
            emotion (str): 감정
            theme (str): 주제
            code (str): 작곡에 사용할 코드 (선택사항)
            
        Returns:
            Dict[str, Any]: 완성된 노래 정보
        """
        # 작곡 생성
        if code:
            composition = self.composer.compose_from_code(code, emotion)
        else:
            composition = self.composer.compose_by_emotion(emotion)
        
        # 작사 생성  
        lyrics = self.lyricist.generate_lyrics(emotion, theme, lines=8)
        
        # 완성된 노래 정보
        complete_song = {
            'title': theme or f"{emotion.title()} Song",
            'emotion': emotion,
            'theme': theme,
            'composition': composition,
            'lyrics': lyrics,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'song_id': len(self.complete_songs) + 1
        }
        
        # 완성된 노래 목록에 추가
        self.complete_songs.append(complete_song)
        
        return complete_song
    
    def display_complete_song(self, song: Dict[str, Any]) -> str:
        """완성된 노래를 보기 좋게 표시"""
        result = f"🎼🎤 **{song['title']}**\n"
        result += f"🎭 감정: {song['emotion']} | 테마: {song.get('theme', 'None')}\n"
        result += f"⏰ 작성: {song['created_at']}\n\n"
        
        result += "🎵 **작곡 정보:**\n"
        result += f"   조성: {song['composition']['style']['key']} {song['composition']['style']['scale']}\n"
        result += f"   템포: {song['composition']['style']['tempo']}\n\n"
        
        result += "🎼 **악보:**\n"
        result += song['composition']['ascii_notation'] + "\n\n"
        
        result += "🎤 **가사:**\n"
        result += "=" * 40 + "\n"
        for i, line in enumerate(song['lyrics']['lines'], 1):
            result += f"{i:2d}. {line}\n"
        result += "=" * 40 + "\n\n"
        
        result += "🎶 **화음 진행:**\n"
        chord_line = " → ".join(song['composition']['chords'])
        result += f"   {chord_line}\n\n"
        
        result += "✨ 완성된 노래입니다! 다른 감정이나 테마로도 만들어드릴 수 있어요!"
        
        return result
    
    def get_song_catalog(self) -> str:
        """완성된 노래 카탈로그 조회"""
        if not self.complete_songs:
            return "🎼 아직 완성된 노래가 없습니다."
        
        result = f"📻 **완성된 노래 목록** ({len(self.complete_songs)}곡):\n\n"
        
        for song in self.complete_songs:
            result += f"🎵 **{song['title']}**\n"
            result += f"   감정: {song['emotion']} | ID: {song['song_id']}\n"
            result += f"   작성: {song['created_at'][:16]}\n\n"
        
        return result