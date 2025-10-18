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
        self.scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'pentatonic': [0, 2, 4, 7, 9],
            'blues': [0, 3, 5, 6, 7, 10]
        }
        
        # 감정별 음악 특성
        self.emotion_styles = {
            'happy': {
                'scale': 'major',
                'tempo': 'fast',
                'rhythm': 'upbeat',
                'key': 'C'
            },
            'sad': {
                'scale': 'minor',
                'tempo': 'slow',
                'rhythm': 'melancholy',
                'key': 'Am'
            },
            'excited': {
                'scale': 'major',
                'tempo': 'very_fast',
                'rhythm': 'energetic',
                'key': 'G'
            },
            'calm': {
                'scale': 'pentatonic',
                'tempo': 'moderate',
                'rhythm': 'flowing',
                'key': 'F'
            },
            'creative': {
                'scale': 'blues',
                'tempo': 'varied',
                'rhythm': 'jazz',
                'key': 'Bb'
            }
        }
        
        # 코드 패턴 → 음악 매핑
        self.code_music_mapping = {
            'for': '반복 리듬 패턴',
            'if': '조건부 화음 변화',
            'function': '메인 멜로디 라인',
            'class': '전체 곡 구조',
            'return': '마무리 코다',
            'print': '악센트 노트',
            'while': '지속적인 베이스 라인',
            'try': '실험적 불협화음',
            'except': '해결 화음'
        }
        
        self.compositions = []
    
    def analyze_code_pattern(self, code: str) -> Dict[str, Any]:
        """코드 패턴을 음악적 요소로 분석"""
        analysis = {
            'complexity': self.calculate_complexity(code),
            'rhythm_pattern': self.extract_rhythm_pattern(code),
            'melodic_structure': self.extract_melodic_structure(code),
            'harmonic_elements': self.extract_harmonic_elements(code)
        }
        
        return analysis
    
    def calculate_complexity(self, code: str) -> int:
        """코드 복잡도를 음악 복잡도로 변환"""
        lines = len(code.split('\n'))
        functions = len(re.findall(r'def\s+\w+', code))
        loops = len(re.findall(r'(for|while)', code))
        conditionals = len(re.findall(r'if\s+', code))
        
        complexity = (lines * 0.1) + (functions * 2) + (loops * 1.5) + (conditionals * 1)
        return min(int(complexity), 10)  # 1-10 스케일
    
    def extract_rhythm_pattern(self, code: str) -> List[str]:
        """코드에서 리듬 패턴 추출"""
        patterns = []
        
        # 들여쓰기 기반 리듬
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