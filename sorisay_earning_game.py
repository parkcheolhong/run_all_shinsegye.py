#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💰 소리새 AI 파트너 수익 게임 시스템
게임하며 실제 돈을 벌 수 있는 혁신적인 P2E 플랫폼
"""

import sys
import os
import time
import random
import json
from datetime import datetime
from typing import Dict, List

sys.path.append(os.getcwd())

class SorisayEarningGame:
    """소리새와 함께하는 수익 게임 시스템"""
    
    def __init__(self):
        self.player_level = 1
        self.earned_money = 0.0
        self.ai_partner_level = 1
        self.available_services = []
        self.completed_missions = []
        
    def initialize_earning_game(self):
        """수익 게임 시스템 초기화"""
        print("💰 소리새 AI 파트너 수익 게임 초기화...")
        
        welcome_message = """
🎉 소리새 AI 파트너 수익 게임에 오신 것을 환영합니다!

💡 게임 컨셉:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AI 파트너와 협업하여 실제 서비스 제공
🎮 재미있는 게임 형태로 가치 있는 일 수행
💰 플레이하며 실제 돈을 벌 수 있는 시스템
🌟 상대성 게임: 놀면서 일하고, 일하면서 놀기
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 시작 가능한 수익 활동들:
• 📝 AI 협업 콘텐츠 제작 (블로그, 기사)
• 🎨 디지털 아트 창작 및 NFT 판매  
• 📊 데이터 분석 서비스 제공
• 🎵 AI 음악 작곡 및 라이센싱
• 💬 다국어 번역 서비스
• 🏫 온라인 과외 및 강의
• 🛒 AI 쇼핑몰 운영 도우미
        """
        
        print(welcome_message)
        self.setup_available_services()
        
    def setup_available_services(self):
        """이용 가능한 수익 서비스 설정"""
        self.available_services = [
            {
                'id': 'content_creation',
                'name': '🤖 AI 협업 콘텐츠 제작',
                'description': 'AI와 함께 고품질 블로그/기사 작성',
                'base_reward': 50.0,
                'difficulty': 'easy',
                'time_required': '30분',
                'skill_required': 'writing'
            },
            {
                'id': 'digital_art',
                'name': '🎨 디지털 아트 NFT 제작',
                'description': 'AI 도구로 독창적인 디지털 아트 창작',
                'base_reward': 100.0,
                'difficulty': 'medium',
                'time_required': '1시간',
                'skill_required': 'creativity'
            },
            {
                'id': 'data_analysis',
                'name': '📊 AI 데이터 분석 서비스',
                'description': 'AI와 협업하여 기업 데이터 분석',
                'base_reward': 200.0,
                'difficulty': 'hard',
                'time_required': '2시간',
                'skill_required': 'analysis'
            },
            {
                'id': 'music_creation',
                'name': '🎵 AI 음악 작곡 스튜디오',
                'description': 'AI와 함께 음악 작곡하고 라이센싱',
                'base_reward': 150.0,
                'difficulty': 'medium',
                'time_required': '1.5시간',
                'skill_required': 'music'
            },
            {
                'id': 'translation',
                'name': '💬 AI 번역 서비스',
                'description': 'AI 도움으로 고품질 번역 서비스',
                'base_reward': 80.0,
                'difficulty': 'easy',
                'time_required': '45분',
                'skill_required': 'language'
            },
            {
                'id': 'tutoring',
                'name': '🏫 AI 온라인 과외',
                'description': 'AI 교육 도구로 맞춤형 과외',
                'base_reward': 120.0,
                'difficulty': 'medium',
                'time_required': '1시간',
                'skill_required': 'teaching'
            }
        ]
    
    def show_available_missions(self):
        """이용 가능한 수익 미션 표시"""
        print("\n🎯 현재 이용 가능한 수익 미션들:")
        print("=" * 70)
        
        for i, service in enumerate(self.available_services, 1):
            difficulty_icon = {'easy': '⭐', 'medium': '⭐⭐', 'hard': '⭐⭐⭐'}[service['difficulty']]
            
            print(f"""
{i}. {service['name']}
   💰 예상 수익: ${service['base_reward']:.0f}
   ⏰ 소요 시간: {service['time_required']}
   {difficulty_icon} 난이도: {service['difficulty'].title()}
   📝 설명: {service['description']}
            """)
    
    def start_earning_mission(self, mission_id: int):
        """수익 미션 시작"""
        if mission_id < 1 or mission_id > len(self.available_services):
            print("❌ 잘못된 미션 번호입니다.")
            return
        
        selected_service = self.available_services[mission_id - 1]
        print(f"\n🚀 '{selected_service['name']}' 미션 시작!")
        print("=" * 50)
        
        # 미션 진행 시뮬레이션
        mission_result = self.execute_mission(selected_service)
        
        # 수익 계산 및 지급
        earned_amount = self.calculate_earnings(selected_service, mission_result)
        self.earned_money += earned_amount
        
        # 결과 출력
        self.show_mission_result(selected_service, mission_result, earned_amount)
        
        # 완료된 미션에 추가
        self.completed_missions.append({
            'service': selected_service['name'],
            'earned': earned_amount,
            'completion_time': datetime.now(),
            'quality_score': mission_result['quality_score']
        })
        
    def execute_mission(self, service: Dict) -> Dict:
        """미션 실행 및 결과 생성"""
        print(f"\n🤖 AI 파트너와 '{service['name']}' 작업 중...")
        
        # 작업 진행 시뮬레이션
        progress_steps = [
            "🔍 작업 요구사항 분석 중...",
            "🧠 AI와 협업 전략 수립 중...",
            "⚡ 실제 작업 진행 중...",
            "✨ 품질 검토 및 개선 중...",
            "🎯 최종 결과물 완성!"
        ]
        
        for step in progress_steps:
            print(f"   {step}")
            time.sleep(0.8)
        
        # 품질 점수 계산 (레벨과 AI 파트너 수준에 따라)
        base_quality = 70
        level_bonus = self.player_level * 2
        ai_bonus = self.ai_partner_level * 3
        random_factor = random.randint(-10, 15)
        
        quality_score = min(100, base_quality + level_bonus + ai_bonus + random_factor)
        
        # 특별 보너스 이벤트
        bonus_events = []
        if random.random() < 0.3:  # 30% 확률
            bonus_events.append("🌟 완벽한 협업 보너스!")
        if random.random() < 0.2:  # 20% 확률
            bonus_events.append("🔥 창의성 폭발 보너스!")
        
        return {
            'quality_score': quality_score,
            'bonus_events': bonus_events,
            'completion_time': datetime.now(),
            'ai_contribution': random.randint(40, 70)
        }
    
    def calculate_earnings(self, service: Dict, result: Dict) -> float:
        """수익 계산"""
        base_reward = service['base_reward']
        
        # 품질에 따른 수익 조정
        quality_multiplier = result['quality_score'] / 100.0
        
        # 레벨 보너스
        level_multiplier = 1.0 + (self.player_level - 1) * 0.1
        
        # 보너스 이벤트 추가 수익
        bonus_multiplier = 1.0 + len(result['bonus_events']) * 0.2
        
        final_earning = base_reward * quality_multiplier * level_multiplier * bonus_multiplier
        
        return round(final_earning, 2)
    
    def show_mission_result(self, service: Dict, result: Dict, earned: float):
        """미션 결과 표시"""
        print(f"\n🎉 '{service['name']}' 미션 완료!")
        print("=" * 60)
        print(f"📊 작업 품질: {result['quality_score']}점")
        print(f"🤖 AI 기여도: {result['ai_contribution']}%")
        print(f"💰 획득 수익: ${earned:.2f}")
        
        if result['bonus_events']:
            print("\n🎁 특별 보너스:")
            for bonus in result['bonus_events']:
                print(f"   {bonus}")
        
        # 레벨업 체크
        if len(self.completed_missions) % 3 == 0:
            self.player_level += 1
            print(f"\n🆙 레벨업! 현재 레벨: {self.player_level}")
        
        if len(self.completed_missions) % 5 == 0:
            self.ai_partner_level += 1
            print(f"🤖 AI 파트너도 성장! AI 레벨: {self.ai_partner_level}")
    
    def show_earning_statistics(self):
        """수익 통계 표시"""
        total_missions = len(self.completed_missions)
        avg_earning = self.earned_money / max(1, total_missions)
        
        print(f"\n📈 수익 통계 대시보드")
        print("=" * 50)
        print(f"💰 총 누적 수익: ${self.earned_money:.2f}")
        print(f"🎯 완료한 미션: {total_missions}개")
        print(f"📊 미션당 평균 수익: ${avg_earning:.2f}")
        print(f"🆙 플레이어 레벨: {self.player_level}")
        print(f"🤖 AI 파트너 레벨: {self.ai_partner_level}")
        
        if total_missions > 0:
            print(f"\n📋 최근 완료 미션:")
            for mission in self.completed_missions[-3:]:
                print(f"   • {mission['service']}: ${mission['earned']:.2f}")
    
    def show_earning_projections(self):
        """수익 예측 표시"""
        daily_potential = 0
        for service in self.available_services:
            # 하루에 각 서비스를 몇 번 할 수 있는지 계산
            time_per_service = {'30분': 0.5, '45분': 0.75, '1시간': 1, '1.5시간': 1.5, '2시간': 2}
            service_time = time_per_service.get(service['time_required'], 1)
            daily_possible = 8 / service_time  # 하루 8시간 기준
            daily_earning = service['base_reward'] * daily_possible * (self.player_level * 0.1 + 0.9)
            daily_potential += daily_earning / len(self.available_services)  # 평균화
        
        monthly_potential = daily_potential * 22  # 주 5일, 월 22일 기준
        yearly_potential = monthly_potential * 12
        
        print(f"\n🔮 수익 예측 (현재 레벨 기준)")
        print("=" * 50)
        print(f"📅 일 예상 수익: ${daily_potential:.0f}")
        print(f"📅 월 예상 수익: ${monthly_potential:.0f}")
        print(f"📅 연 예상 수익: ${yearly_potential:.0f}")
        print(f"\n💡 레벨업할수록 수익이 더 증가합니다!")

def main():
    """메인 게임 실행"""
    print("💰 소리새 AI 파트너 수익 게임 시작!")
    print("=" * 70)
    
    game = SorisayEarningGame()
    game.initialize_earning_game()
    
    while True:
        print(f"\n🎮 현재 상태: 레벨 {game.player_level} | 누적 수익: ${game.earned_money:.2f}")
        print("\n📋 메뉴:")
        print("1. 🎯 수익 미션 보기")
        print("2. 🚀 미션 시작하기")  
        print("3. 📈 수익 통계 보기")
        print("4. 🔮 수익 예측 보기")
        print("5. ❌ 게임 종료")
        
        try:
            choice = input("\n선택하세요 (1-5): ").strip()
            
            if choice == '1':
                game.show_available_missions()
                
            elif choice == '2':
                game.show_available_missions()
                mission_num = int(input("\n미션 번호를 선택하세요: "))
                game.start_earning_mission(mission_num)
                
            elif choice == '3':
                game.show_earning_statistics()
                
            elif choice == '4':
                game.show_earning_projections()
                
            elif choice == '5':
                print("\n🎉 게임을 종료합니다!")
                print(f"💰 총 획득 수익: ${game.earned_money:.2f}")
                print("🌟 실제 돈을 벌며 즐거운 게임이었습니다!")
                break
                
            else:
                print("❌ 1-5 사이의 숫자를 입력해주세요.")
                
        except ValueError:
            print("❌ 올바른 숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n\n🛑 게임이 중단되었습니다.")
            break

if __name__ == "__main__":
    main()