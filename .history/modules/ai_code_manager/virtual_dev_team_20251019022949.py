# -*- coding: utf-8 -*-
"""
🤖 가상 개발팀 시스템 (Virtual Development Team)
AI 기반 다중 역할 개발팀 시뮬레이션 및 협업 관리
"""

import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging
from dataclasses import dataclass
from enum import Enum

class DeveloperRole(Enum):
    """개발자 역할 정의"""
    FRONTEND = "프론트엔드"
    BACKEND = "백엔드"
    FULLSTACK = "풀스택"
    DEVOPS = "데브옵스"
    QA = "QA"
    PM = "프로젝트매니저"
    DESIGNER = "디자이너"
    ARCHITECT = "아키텍트"

class TaskPriority(Enum):
    """작업 우선순위"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Task:
    """작업 정보"""
    id: str
    title: str
    description: str
    role: DeveloperRole
    priority: TaskPriority
    estimated_hours: int
    status: str = "대기중"
    assignee: str = ""
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class TeamMember:
    """팀 멤버 정보"""
    name: str
    role: DeveloperRole
    skill_level: int  # 1-10
    personality: str
    availability: float  # 0.0-1.0
    current_tasks: List[str] = None
    
    def __post_init__(self):
        if self.current_tasks is None:
            self.current_tasks = []

class VirtualDevelopmentTeam:
    """가상 개발팀 시스템"""
    
    def __init__(self):
        self.setup_logging()
        
        # 팀 멤버 초기화
        self.team_members = self._create_default_team()
        
        # 작업 관리
        self.tasks = {}
        self.task_counter = 0
        
        # 프로젝트 상태
        self.current_projects = {}
        self.project_counter = 0
        
        # 팀 성격 및 문화
        self.team_culture = {
            "agile_maturity": random.uniform(0.6, 0.9),
            "communication_openness": random.uniform(0.7, 0.9),
            "innovation_level": random.uniform(0.7, 1.0),
            "quality_focus": random.uniform(0.6, 0.95)
        }
        
        # 회의 및 이벤트
        self.meetings = []
        self.team_events = []

    def setup_logging(self):
        """로깅 설정"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _create_default_team(self) -> Dict[str, TeamMember]:
        """기본 팀 생성"""
        team = {}
        
        # 팀 구성원 정의
        members_data = [
            {"name": "김코딩", "role": DeveloperRole.FRONTEND, "skill": 8, "personality": "창의적", "availability": 0.9},
            {"name": "이백엔드", "role": DeveloperRole.BACKEND, "skill": 9, "personality": "분석적", "availability": 0.85},
            {"name": "박풀스택", "role": DeveloperRole.FULLSTACK, "skill": 7, "personality": "다재다능", "availability": 0.8},
            {"name": "최데브옵스", "role": DeveloperRole.DEVOPS, "skill": 8, "personality": "체계적", "availability": 0.75},
            {"name": "정QA", "role": DeveloperRole.QA, "skill": 7, "personality": "꼼꼼함", "availability": 0.9},
            {"name": "한PM", "role": DeveloperRole.PM, "skill": 8, "personality": "리더십", "availability": 0.95},
            {"name": "유디자이너", "role": DeveloperRole.DESIGNER, "skill": 8, "personality": "감성적", "availability": 0.8},
            {"name": "서아키텍트", "role": DeveloperRole.ARCHITECT, "skill": 9, "personality": "전략적", "availability": 0.7}
        ]
        
        for member_data in members_data:
            member = TeamMember(
                name=member_data["name"],
                role=member_data["role"],
                skill_level=member_data["skill"],
                personality=member_data["personality"],
                availability=member_data["availability"]
            )
            team[member.name] = member
            
        return team

    def create_project(self, project_name: str, description: str, 
                      duration_weeks: int = 4) -> Dict:
        """새 프로젝트 생성"""
        self.project_counter += 1
        project_id = f"PRJ-{self.project_counter:03d}"
        
        # 프로젝트 기본 작업 생성
        tasks = self._generate_project_tasks(project_name, description)
        
        project = {
            "id": project_id,
            "name": project_name,
            "description": description,
            "duration_weeks": duration_weeks,
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(weeks=duration_weeks),
            "status": "계획중",
            "tasks": [task.id for task in tasks],
            "assigned_team": self._auto_assign_team(tasks),
            "progress": 0,
            "budget": self._estimate_project_budget(tasks, duration_weeks),
            "risks": self._assess_project_risks(tasks, duration_weeks)
        }
        
        self.current_projects[project_id] = project
        
        # 작업들을 태스크 딕셔너리에 추가
        for task in tasks:
            self.tasks[task.id] = task
        
        self.logger.info(f"프로젝트 생성: {project_name} ({project_id})")
        return project

    def _generate_project_tasks(self, project_name: str, description: str) -> List[Task]:
        """프로젝트에 필요한 작업들 생성"""
        tasks = []
        
        # 기본 개발 작업들
        base_tasks = [
            {"title": "요구사항 분석", "role": DeveloperRole.PM, "hours": 16, "priority": TaskPriority.HIGH},
            {"title": "시스템 아키텍처 설계", "role": DeveloperRole.ARCHITECT, "hours": 24, "priority": TaskPriority.HIGH},
            {"title": "UI/UX 디자인", "role": DeveloperRole.DESIGNER, "hours": 32, "priority": TaskPriority.MEDIUM},
            {"title": "데이터베이스 설계", "role": DeveloperRole.BACKEND, "hours": 20, "priority": TaskPriority.HIGH},
            {"title": "API 개발", "role": DeveloperRole.BACKEND, "hours": 40, "priority": TaskPriority.HIGH},
            {"title": "프론트엔드 개발", "role": DeveloperRole.FRONTEND, "hours": 50, "priority": TaskPriority.HIGH},
            {"title": "인프라 구축", "role": DeveloperRole.DEVOPS, "hours": 30, "priority": TaskPriority.MEDIUM},
            {"title": "테스트 계획 수립", "role": DeveloperRole.QA, "hours": 16, "priority": TaskPriority.MEDIUM},
            {"title": "통합 테스트", "role": DeveloperRole.QA, "hours": 24, "priority": TaskPriority.HIGH},
            {"title": "배포 준비", "role": DeveloperRole.DEVOPS, "hours": 16, "priority": TaskPriority.MEDIUM}
        ]
        
        for i, task_data in enumerate(base_tasks):
            self.task_counter += 1
            task = Task(
                id=f"TSK-{self.task_counter:03d}",
                title=f"{project_name}: {task_data['title']}",
                description=f"{description} - {task_data['title']} 작업",
                role=task_data["role"],
                priority=task_data["priority"],
                estimated_hours=task_data["hours"]
            )
            tasks.append(task)
            
        return tasks

    def _auto_assign_team(self, tasks: List[Task]) -> Dict[str, List[str]]:
        """작업에 따라 자동으로 팀 배정"""
        assignments = {}
        
        for task in tasks:
            # 해당 역할의 가장 적합한 멤버 찾기
            suitable_members = [
                member for member in self.team_members.values()
                if member.role == task.role and member.availability > 0.5
            ]
            
            if suitable_members:
                # 스킬 레벨과 가용성을 고려하여 최적 멤버 선택
                best_member = max(suitable_members, 
                                key=lambda m: m.skill_level * m.availability)
                
                task.assignee = best_member.name
                
                if best_member.name not in assignments:
                    assignments[best_member.name] = []
                assignments[best_member.name].append(task.id)
                
                # 해당 멤버의 현재 작업에 추가
                best_member.current_tasks.append(task.id)
                
                # 가용성 조정 (작업량에 따라)
                workload_impact = task.estimated_hours / 160  # 월 160시간 기준
                best_member.availability = max(0.1, 
                    best_member.availability - workload_impact)
        
        return assignments

    def simulate_daily_progress(self, project_id: str) -> Dict:
        """일일 프로젝트 진행 상황 시뮬레이션"""
        if project_id not in self.current_projects:
            return {"error": "프로젝트를 찾을 수 없습니다"}
        
        project = self.current_projects[project_id]
        progress_report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "project_id": project_id,
            "team_activities": [],
            "completed_tasks": [],
            "new_issues": [],
            "team_status": {},
            "overall_progress": 0
        }
        
        # 각 팀 멤버의 작업 진행 시뮬레이션
        for member_name, member in self.team_members.items():
            if member.current_tasks:
                member_activity = self._simulate_member_work(member)
                progress_report["team_activities"].append(member_activity)
                
                # 작업 완료 체크
                for task_id in member.current_tasks[:]:
                    if task_id in self.tasks:
                        task = self.tasks[task_id]
                        completion_chance = member.skill_level * member.availability * 0.1
                        
                        if random.random() < completion_chance:
                            task.status = "완료"
                            member.current_tasks.remove(task_id)
                            progress_report["completed_tasks"].append({
                                "task_id": task_id,
                                "task_title": task.title,
                                "completed_by": member_name
                            })
                
                # 멤버 상태 업데이트
                progress_report["team_status"][member_name] = {
                    "active_tasks": len(member.current_tasks),
                    "availability": member.availability,
                    "mood": self._calculate_member_mood(member)
                }
        
        # 새로운 이슈 생성 (확률적)
        if random.random() < 0.2:  # 20% 확률로 이슈 발생
            new_issue = self._generate_random_issue()
            progress_report["new_issues"].append(new_issue)
        
        # 전체 프로젝트 진행률 계산
        total_tasks = len(project["tasks"])
        completed_tasks = len([task for task in self.tasks.values() 
                             if task.id in project["tasks"] and task.status == "완료"])
        
        progress_report["overall_progress"] = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        project["progress"] = progress_report["overall_progress"]
        
        return progress_report

    def _simulate_member_work(self, member: TeamMember) -> Dict:
        """개별 멤버 작업 시뮬레이션"""
        productivity = member.skill_level * member.availability * random.uniform(0.7, 1.3)
        
        activities = []
        if member.current_tasks:
            # 작업 중인 태스크에서 랜덤하게 선택
            current_task_id = random.choice(member.current_tasks)
            if current_task_id in self.tasks:
                task = self.tasks[current_task_id]
                
                if member.role == DeveloperRole.FRONTEND:
                    activities = ["컴포넌트 개발", "스타일링", "반응형 디자인", "사용자 테스트"]
                elif member.role == DeveloperRole.BACKEND:
                    activities = ["API 엔드포인트 개발", "데이터베이스 쿼리 최적화", "보안 강화", "성능 개선"]
                elif member.role == DeveloperRole.QA:
                    activities = ["테스트 케이스 작성", "버그 검증", "자동화 테스트", "성능 테스트"]
                elif member.role == DeveloperRole.PM:
                    activities = ["일정 조정", "팀 미팅 진행", "클라이언트 커뮤니케이션", "리스크 관리"]
        
        selected_activity = random.choice(activities) if activities else "일반 업무"
        
        return {
            "member": member.name,
            "role": member.role.value,
            "activity": selected_activity,
            "productivity_score": round(productivity, 2),
            "mood": self._calculate_member_mood(member),
            "notes": self._generate_work_notes(member, selected_activity)
        }

    def _calculate_member_mood(self, member: TeamMember) -> str:
        """멤버의 현재 기분 계산"""
        workload = len(member.current_tasks)
        availability = member.availability
        
        mood_score = (availability * 2) - (workload * 0.1)
        
        if mood_score > 1.5:
            return "매우 좋음"
        elif mood_score > 1.0:
            return "좋음"
        elif mood_score > 0.5:
            return "보통"
        elif mood_score > 0:
            return "피곤함"
        else:
            return "스트레스"

    def _generate_work_notes(self, member: TeamMember, activity: str) -> str:
        """작업 노트 생성"""
        notes_templates = {
            DeveloperRole.FRONTEND: [
                f"{activity} 진행 중, UI 개선사항 발견",
                f"{activity} 완료, 브라우저 호환성 확인 필요",
                f"{activity} 중 성능 이슈 발견, 최적화 계획 수립"
            ],
            DeveloperRole.BACKEND: [
                f"{activity} 진행, 데이터베이스 성능 모니터링",
                f"{activity} 완료, 추가 보안 검토 필요",
                f"{activity} 중 확장성 고려사항 발견"
            ],
            DeveloperRole.QA: [
                f"{activity} 완료, 추가 테스트 케이스 필요",
                f"{activity} 진행 중, 버그 재현성 확인",
                f"{activity} 완료, 테스트 커버리지 향상"
            ]
        }
        
        role_notes = notes_templates.get(member.role, [f"{activity} 진행 중"])
        return random.choice(role_notes)

    def _generate_random_issue(self) -> Dict:
        """랜덤 이슈 생성"""
        issue_types = [
            {"type": "버그", "severity": "중간", "description": "UI 렌더링 문제 발생"},
            {"type": "성능", "severity": "높음", "description": "API 응답 시간 지연"},
            {"type": "보안", "severity": "높음", "description": "잠재적 보안 취약점 발견"},
            {"type": "호환성", "severity": "낮음", "description": "구형 브라우저 호환성 이슈"},
            {"type": "기능", "severity": "중간", "description": "사용자 피드백 기반 기능 개선 요청"}
        ]
        
        issue = random.choice(issue_types)
        issue["id"] = f"ISS-{random.randint(1000, 9999)}"
        issue["reported_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        return issue

    def conduct_team_meeting(self, meeting_type: str = "일일스탠드업") -> Dict:
        """팀 미팅 진행"""
        meeting = {
            "type": meeting_type,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "attendees": list(self.team_members.keys()),
            "agenda": self._generate_meeting_agenda(meeting_type),
            "discussions": [],
            "decisions": [],
            "action_items": []
        }
        
        # 각 멤버의 발언 시뮬레이션
        for member_name, member in self.team_members.items():
            discussion = self._simulate_member_discussion(member, meeting_type)
            meeting["discussions"].append(discussion)
        
        # 미팅 결과 생성
        meeting["decisions"] = self._generate_meeting_decisions(meeting_type)
        meeting["action_items"] = self._generate_action_items()
        
        self.meetings.append(meeting)
        return meeting

    def _generate_meeting_agenda(self, meeting_type: str) -> List[str]:
        """미팅 안건 생성"""
        agendas = {
            "일일스탠드업": [
                "어제 완료한 작업 공유",
                "오늘 계획한 작업 발표", 
                "블로커 및 이슈 논의"
            ],
            "스프린트계획": [
                "이전 스프린트 리뷰",
                "다음 스프린트 목표 설정",
                "작업 분배 및 일정 논의"
            ],
            "회고": [
                "잘된 점 공유",
                "개선점 논의",
                "액션 아이템 도출"
            ]
        }
        return agendas.get(meeting_type, ["일반 논의사항"])

    def _simulate_member_discussion(self, member: TeamMember, meeting_type: str) -> Dict:
        """멤버의 미팅 발언 시뮬레이션"""
        discussions = {
            DeveloperRole.FRONTEND: [
                "사용자 피드백을 반영한 UI 개선 작업을 진행했습니다",
                "반응형 디자인 이슈를 해결했고, 성능 최적화가 필요해 보입니다",
                "디자인 시스템 구축을 제안하고 싶습니다"
            ],
            DeveloperRole.BACKEND: [
                "API 성능 개선을 완료했고, 데이터베이스 최적화가 필요합니다",
                "새로운 보안 패치를 적용했습니다",
                "마이크로서비스 아키텍처 도입을 고려해볼 시점입니다"
            ],
            DeveloperRole.QA: [
                "테스트 커버리지를 85%까지 향상시켰습니다",
                "자동화 테스트 환경 구축이 완료되었습니다",
                "성능 테스트에서 몇 가지 이슈를 발견했습니다"
            ]
        }
        
        role_discussions = discussions.get(member.role, ["일반적인 진행 상황을 공유했습니다"])
        
        return {
            "speaker": member.name,
            "role": member.role.value,
            "comment": random.choice(role_discussions),
            "mood": self._calculate_member_mood(member)
        }

    def _generate_meeting_decisions(self, meeting_type: str) -> List[str]:
        """미팅 결정사항 생성"""
        decisions = [
            "다음 스프린트 목표를 성능 최적화로 설정",
            "주간 코드 리뷰 세션을 금요일에 진행",
            "새로운 개발 툴 도입을 검토하기로 결정"
        ]
        return random.sample(decisions, 2)

    def _generate_action_items(self) -> List[Dict]:
        """액션 아이템 생성"""
        items = [
            {"task": "성능 테스트 환경 구축", "assignee": "최데브옵스", "due_date": "2024-10-25"},
            {"task": "코드 리뷰 가이드라인 작성", "assignee": "서아키텍트", "due_date": "2024-10-23"},
            {"task": "사용자 피드백 분석 보고서 작성", "assignee": "한PM", "due_date": "2024-10-24"}
        ]
        return random.sample(items, 2)

    def get_team_analytics(self) -> Dict:
        """팀 분석 리포트 생성"""
        analytics = {
            "team_overview": {
                "total_members": len(self.team_members),
                "avg_skill_level": sum(m.skill_level for m in self.team_members.values()) / len(self.team_members),
                "avg_availability": sum(m.availability for m in self.team_members.values()) / len(self.team_members),
                "team_culture_score": sum(self.team_culture.values()) / len(self.team_culture)
            },
            "project_status": {
                "active_projects": len(self.current_projects),
                "total_tasks": len(self.tasks),
                "completed_tasks": len([t for t in self.tasks.values() if t.status == "완료"]),
                "avg_progress": sum(p.get("progress", 0) for p in self.current_projects.values()) / len(self.current_projects) if self.current_projects else 0
            },
            "productivity_metrics": self._calculate_productivity_metrics(),
            "team_health": self._assess_team_health(),
            "recommendations": self._generate_team_recommendations()
        }
        
        return analytics

    def _calculate_productivity_metrics(self) -> Dict:
        """생산성 메트릭 계산"""
        total_estimated_hours = sum(task.estimated_hours for task in self.tasks.values())
        completed_hours = sum(task.estimated_hours for task in self.tasks.values() if task.status == "완료")
        
        return {
            "velocity": completed_hours / max(len(self.meetings) or 1, 1),  # 미팅당 완료 시간
            "completion_rate": (completed_hours / total_estimated_hours * 100) if total_estimated_hours > 0 else 0,
            "avg_task_completion_time": "3.2일",  # 시뮬레이션 데이터
            "team_efficiency": random.uniform(75, 95)  # 효율성 점수
        }

    def _assess_team_health(self) -> Dict:
        """팀 건강도 평가"""
        stress_levels = [1 if self._calculate_member_mood(member) in ["스트레스", "피곤함"] else 0 
                        for member in self.team_members.values()]
        
        return {
            "overall_mood": "좋음" if sum(stress_levels) < len(self.team_members) * 0.3 else "보통",
            "stress_level": sum(stress_levels) / len(self.team_members) * 100,
            "collaboration_score": self.team_culture["communication_style"] == "개방적" and 85 or 70,
            "satisfaction_index": random.uniform(75, 90)
        }

    def _generate_team_recommendations(self) -> List[str]:
        """팀 개선 권장사항 생성"""
        recommendations = []
        
        # 가용성이 낮은 멤버 체크
        overloaded_members = [m.name for m in self.team_members.values() if m.availability < 0.5]
        if overloaded_members:
            recommendations.append(f"업무 과부하 멤버들({', '.join(overloaded_members)})의 작업 재분배 필요")
        
        # 프로젝트 진행률 체크
        slow_projects = [p["name"] for p in self.current_projects.values() if p["progress"] < 30]
        if slow_projects:
            recommendations.append(f"진행 지연 프로젝트({', '.join(slow_projects)}) 리스크 관리 강화 필요")
        
        # 팀 문화 개선
        if self.team_culture["innovation_level"] < 0.8:
            recommendations.append("혁신적 아이디어 도출을 위한 브레인스토밍 세션 증대")
        
        if not recommendations:
            recommendations.append("현재 팀 상태가 양호합니다. 지속적인 모니터링을 권장합니다.")
        
        return recommendations

    def simulate_sprint_planning(self, sprint_duration: int = 2) -> Dict:
        """스프린트 계획 시뮬레이션"""
        sprint = {
            "sprint_id": f"SPR-{random.randint(100, 999)}",
            "duration_weeks": sprint_duration,
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(weeks=sprint_duration),
            "goals": [],
            "selected_tasks": [],
            "team_capacity": {},
            "risks": [],
            "success_criteria": []
        }
        
        # 스프린트 목표 설정
        sprint["goals"] = [
            "사용자 인증 기능 완성",
            "API 성능 30% 향상",
            "모바일 반응형 UI 구현"
        ]
        
        # 팀 용량 계산
        for member in self.team_members.values():
            weekly_capacity = 40 * member.availability  # 주 40시간 * 가용성
            sprint["team_capacity"][member.name] = {
                "weekly_hours": weekly_capacity,
                "total_capacity": weekly_capacity * sprint_duration,
                "current_utilization": len(member.current_tasks) * 10  # 태스크당 10시간 추정
            }
        
        # 작업 선택 (우선순위 기반)
        available_tasks = [task for task in self.tasks.values() if task.status == "대기중"]
        high_priority_tasks = [task for task in available_tasks if task.priority == TaskPriority.HIGH]
        
        sprint["selected_tasks"] = [
            {"id": task.id, "title": task.title, "estimated_hours": task.estimated_hours}
            for task in high_priority_tasks[:5]  # 상위 5개 작업 선택
        ]
        
        # 리스크 식별
        sprint["risks"] = [
            "외부 API 의존성으로 인한 지연 가능성",
            "신규 기술 스택 학습 시간 필요",
            "클라이언트 요구사항 변경 가능성"
        ]
        
        # 성공 기준
        sprint["success_criteria"] = [
            "계획된 작업의 80% 이상 완료",
            "버그 발생률 5% 이하 유지",
            "코드 리뷰 100% 완료"
        ]
        
        return sprint

    def generate_team_report(self) -> str:
        """팀 상태 보고서 생성"""
        analytics = self.get_team_analytics()
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("🤖 가상 개발팀 상태 보고서")
        report_lines.append("=" * 60)
        report_lines.append(f"보고서 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # 팀 개요
        overview = analytics["team_overview"]
        report_lines.append("👥 팀 개요")
        report_lines.append(f"  총 팀원 수: {overview['total_members']}명")
        report_lines.append(f"  평균 스킬 레벨: {overview['avg_skill_level']:.1f}/10")
        report_lines.append(f"  평균 가용성: {overview['avg_availability']:.1%}")
        report_lines.append("")
        
        # 프로젝트 상태
        project_status = analytics["project_status"]
        report_lines.append("📊 프로젝트 상태")
        report_lines.append(f"  진행 중인 프로젝트: {project_status['active_projects']}개")
        report_lines.append(f"  전체 작업: {project_status['total_tasks']}개")
        report_lines.append(f"  완료 작업: {project_status['completed_tasks']}개")
        report_lines.append(f"  평균 진행률: {project_status['avg_progress']:.1f}%")
        report_lines.append("")
        
        # 생산성
        productivity = analytics["productivity_metrics"]
        report_lines.append("⚡ 생산성 지표")
        report_lines.append(f"  작업 완료율: {productivity['completion_rate']:.1f}%")
        report_lines.append(f"  팀 효율성: {productivity['team_efficiency']:.1f}%")
        report_lines.append("")
        
        # 팀 건강도
        health = analytics["team_health"]
        report_lines.append("💚 팀 건강도")
        report_lines.append(f"  전체 분위기: {health['overall_mood']}")
        report_lines.append(f"  스트레스 레벨: {health['stress_level']:.1f}%")
        report_lines.append(f"  만족도 지수: {health['satisfaction_index']:.1f}%")
        report_lines.append("")
        
        # 권장사항
        recommendations = analytics["recommendations"]
        report_lines.append("💡 권장사항")
        for i, rec in enumerate(recommendations, 1):
            report_lines.append(f"  {i}. {rec}")
        
        report_lines.append("=" * 60)
        return "\n".join(report_lines)

    def _estimate_project_budget(self, tasks: List[Task], duration_weeks: int) -> Dict:
        """프로젝트 예산 추정"""
        total_hours = sum(task.estimated_hours for task in tasks)
        
        # 시간당 비용 (역할별)
        hourly_rates = {
            DeveloperRole.ARCHITECT: 100,
            DeveloperRole.FULLSTACK: 80,
            DeveloperRole.BACKEND: 75,
            DeveloperRole.FRONTEND: 70,
            DeveloperRole.DEVOPS: 85,
            DeveloperRole.PM: 90,
            DeveloperRole.QA: 65,
            DeveloperRole.DESIGNER: 70
        }
        
        labor_cost = sum(task.estimated_hours * hourly_rates.get(task.role, 70) 
                        for task in tasks)
        
        return {
            "labor_cost": labor_cost,
            "infrastructure_cost": duration_weeks * 500,  # 주당 인프라 비용
            "tools_and_licenses": 2000,  # 도구 및 라이센스
            "contingency": labor_cost * 0.15,  # 15% 여유분
            "total": labor_cost + (duration_weeks * 500) + 2000 + (labor_cost * 0.15)
        }

    def _assess_project_risks(self, tasks: List[Task], duration_weeks: int) -> List[Dict]:
        """프로젝트 리스크 평가"""
        risks = []
        
        # 작업 복잡도 기반 리스크
        high_complexity_tasks = len([task for task in tasks if task.estimated_hours > 30])
        if high_complexity_tasks > 3:
            risks.append({
                "type": "기술적 복잡성",
                "probability": "높음",
                "impact": "높음",
                "mitigation": "추가 기술 검토 및 프로토타이핑"
            })
        
        # 일정 리스크
        if duration_weeks < 6:
            risks.append({
                "type": "일정 압박",
                "probability": "중간",
                "impact": "높음", 
                "mitigation": "우선순위 조정 및 범위 축소"
            })
        
        # 팀 가용성 리스크
        low_availability_members = len([m for m in self.team_members.values() if m.availability < 0.7])
        if low_availability_members > 2:
            risks.append({
                "type": "인력 부족",
                "probability": "중간",
                "impact": "중간",
                "mitigation": "외부 리소스 투입 또는 일정 조정"
            })
        
        return risks

if __name__ == "__main__":
    # 테스트 코드
    team = VirtualDevelopmentTeam()
    
    print("🤖 가상 개발팀 시스템 테스트")
    print("=" * 50)
    
    # 프로젝트 생성 테스트
    project = team.create_project(
        "온라인 쇼핑몰", 
        "모던한 전자상거래 플랫폼 개발",
        duration_weeks=6
    )
    print(f"✅ 프로젝트 생성: {project['name']} ({project['id']})")
    print(f"   작업 수: {len(project['tasks'])}개")
    print(f"   예상 예산: ${project['budget']['total']:,.0f}")
    
    # 일일 진행 시뮬레이션
    progress = team.simulate_daily_progress(project['id'])
    print(f"\n📅 일일 진행 상황:")
    print(f"   전체 진행률: {progress['overall_progress']:.1f}%")
    print(f"   완료된 작업: {len(progress['completed_tasks'])}개")
    print(f"   팀 활동: {len(progress['team_activities'])}건")
    
    # 팀 미팅
    meeting = team.conduct_team_meeting("일일스탠드업")
    print(f"\n👥 {meeting['type']} 미팅:")
    print(f"   참석자: {len(meeting['attendees'])}명")
    print(f"   결정사항: {len(meeting['decisions'])}건")
    
    # 스프린트 계획
    sprint = team.simulate_sprint_planning()
    print(f"\n🏃 스프린트 계획:")
    print(f"   스프린트 ID: {sprint['sprint_id']}")
    print(f"   선택된 작업: {len(sprint['selected_tasks'])}개")
    
    # 팀 분석
    analytics = team.get_team_analytics()
    print(f"\n📊 팀 분석:")
    print(f"   팀 효율성: {analytics['productivity_metrics']['team_efficiency']:.1f}%")
    print(f"   팀 만족도: {analytics['team_health']['satisfaction_index']:.1f}%")
    
    print("\n🎯 가상 개발팀 시스템 테스트 완료!")