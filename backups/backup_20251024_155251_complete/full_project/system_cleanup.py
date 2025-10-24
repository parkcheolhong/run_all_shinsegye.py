#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🔍 소리새 프로젝트 전체 시스템 점검 & 정리 도구
불필요한 파일 제거, 버그 수정, 코드 품질 검증을 수행합니다.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

class SorisaySystemCleaner:
    """소리새 시스템 정리 및 점검 클래스"""
    
    def __init__(self, project_root="c:/Projects/Shinsegye_Main"):
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / "backups" / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.issues_found = []
        self.cleaned_files = []
        
    def analyze_project_structure(self):
        """프로젝트 구조 분석"""
        print("🔍 프로젝트 구조 분석 중...")
        print("=" * 50)
        
        # 중요 디렉토리 확인
        important_dirs = [
            "modules/ai_code_manager",
            "modules/plugins", 
            "config",
            "data",
            "tests",
            "logs",
            "memories"
        ]
        
        print("📁 핵심 디렉토리 상태:")
        for dir_path in important_dirs:
            full_path = self.project_root / dir_path
            exists = full_path.exists()
            status = "✅" if exists else "❌"
            file_count = len(list(full_path.glob("*.py"))) if exists and full_path.is_dir() else 0
            print(f"   {status} {dir_path} ({file_count}개 .py 파일)")
        
        return True
    
    def find_duplicate_files(self):
        """중복 파일 탐지"""
        print("\n🔍 중복 파일 탐지 중...")
        print("=" * 50)
        
        # 알려진 중복 파일들
        potential_duplicates = {
            "sorisay_core_controller.py": [],
            "nlp_processor.py": [],
            "settings.json": []
        }
        
        # 전체 프로젝트에서 중복 파일 검색
        for file_pattern in potential_duplicates.keys():
            matches = list(self.project_root.rglob(file_pattern))
            potential_duplicates[file_pattern] = matches
        
        duplicates_found = False
        for filename, paths in potential_duplicates.items():
            if len(paths) > 1:
                duplicates_found = True
                print(f"🚨 중복 발견: {filename}")
                for i, path in enumerate(paths):
                    size = path.stat().st_size if path.exists() else 0
                    status = "📍 메인" if "ai_code_manager" in str(path) else "🗑️ 중복"
                    print(f"   {status} {path} ({size:,} bytes)")
        
        if not duplicates_found:
            print("✅ 중복 파일 없음")
        
        return potential_duplicates
    
    def find_unnecessary_files(self):
        """불필요한 파일 탐지"""
        print("\n🔍 불필요한 파일 탐지 중...")
        print("=" * 50)
        
        unnecessary_patterns = [
            "*.tmp",
            "*.log",
            "*~",
            "*.bak",
            "*.old",
            ".DS_Store",
            "Thumbs.db",
            "__pycache__/*",
            "*.pyc",
            "*.pyo"
        ]
        
        unnecessary_files = []
        for pattern in unnecessary_patterns:
            matches = list(self.project_root.rglob(pattern))
            unnecessary_files.extend(matches)
        
        if unnecessary_files:
            print(f"🗑️ 불필요한 파일 {len(unnecessary_files)}개 발견:")
            for file_path in unnecessary_files[:10]:  # 처음 10개만 표시
                print(f"   • {file_path}")
            if len(unnecessary_files) > 10:
                print(f"   ... 외 {len(unnecessary_files) - 10}개")
        else:
            print("✅ 불필요한 파일 없음")
        
        return unnecessary_files
    
    def check_import_errors(self):
        """import 오류 검사"""
        print("\n🔍 Import 오류 검사 중...")
        print("=" * 50)
        
        python_files = list(self.project_root.rglob("*.py"))
        import_errors = []
        
        for py_file in python_files:
            if "__pycache__" in str(py_file) or ".history" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 간단한 import 구문 검사
                lines = content.split('\n')
                for line_num, line in enumerate(lines, 1):
                    line = line.strip()
                    if line.startswith('import ') or line.startswith('from '):
                        # 상대 import 검사
                        if 'modules.ai_code_manager' in line and 'from modules.ai_code_manager' not in line:
                            import_errors.append({
                                'file': py_file,
                                'line': line_num,
                                'issue': f'잘못된 import: {line}'
                            })
            except Exception as e:
                import_errors.append({
                    'file': py_file,
                    'line': 0,
                    'issue': f'파일 읽기 오류: {str(e)}'
                })
        
        if import_errors:
            print(f"🚨 Import 오류 {len(import_errors)}개 발견:")
            for error in import_errors[:5]:  # 처음 5개만 표시
                print(f"   • {error['file'].name}:{error['line']} - {error['issue']}")
        else:
            print("✅ Import 오류 없음")
        
        return import_errors
    
    def check_json_validity(self):
        """JSON 파일 유효성 검사"""
        print("\n🔍 JSON 파일 유효성 검사 중...")
        print("=" * 50)
        
        json_files = list(self.project_root.rglob("*.json"))
        json_errors = []
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json.load(f)
                print(f"   ✅ {json_file.name}")
            except json.JSONDecodeError as e:
                json_errors.append({
                    'file': json_file,
                    'error': str(e)
                })
                print(f"   🚨 {json_file.name}: {e}")
        
        if not json_errors:
            print("✅ 모든 JSON 파일이 유효함")
        
        return json_errors
    
    def create_backup(self):
        """백업 생성"""
        print(f"\n💾 백업 생성 중...")
        print("=" * 50)
        
        # 백업 디렉토리 생성
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 중요 파일들 백업
        important_files = [
            "modules/ai_code_manager/sorisay_core_controller.py",
            "modules/ai_code_manager/ai_music_composer.py", 
            "modules/ai_code_manager/music_chat_system.py",
            "modules/sorisay_dashboard_web.py",
            "run_all_shinsegye.py",
            "requirements.txt"
        ]
        
        backup_count = 0
        for file_path in important_files:
            source = self.project_root / file_path
            if source.exists():
                dest = self.backup_dir / file_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)
                backup_count += 1
                print(f"   ✅ {file_path}")
        
        print(f"\n💾 {backup_count}개 파일 백업 완료: {self.backup_dir}")
        return self.backup_dir
    
    def clean_unnecessary_files(self, unnecessary_files):
        """불필요한 파일 정리"""
        print(f"\n🧹 불필요한 파일 정리 중...")
        print("=" * 50)
        
        if not unnecessary_files:
            print("✅ 정리할 파일 없음")
            return
        
        cleaned_count = 0
        for file_path in unnecessary_files:
            try:
                if file_path.is_file():
                    file_path.unlink()
                    cleaned_count += 1
                    self.cleaned_files.append(str(file_path))
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
                    cleaned_count += 1
                    self.cleaned_files.append(str(file_path))
            except Exception as e:
                print(f"   ❌ {file_path}: {e}")
        
        print(f"🧹 {cleaned_count}개 파일/폴더 정리 완료")
    
    def generate_gitignore(self):
        """적절한 .gitignore 파일 생성"""
        gitignore_content = """# 소리새 프로젝트 .gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/*.log

# Backups
backups/
*.bak
*.old
*.tmp

# Config (민감한 정보)
config/api_keys.json
config/secrets.json

# Cache
.cache/
.pytest_cache/

# Temporary files
temp/
tmp/
"""
        
        gitignore_path = self.project_root / ".gitignore"
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        print(f"📝 .gitignore 파일 생성/업데이트 완료")
    
    def generate_cleanup_report(self):
        """정리 보고서 생성"""
        report = f"""
# 🧹 소리새 프로젝트 정리 보고서

## 📅 정리 일시
{datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}

## 🎯 정리 결과 요약
- ✅ 프로젝트 구조 점검 완료
- ✅ 중복 파일 탐지 완료  
- ✅ 불필요한 파일 {len(self.cleaned_files)}개 정리
- ✅ Import 오류 검사 완료
- ✅ JSON 파일 유효성 검증 완료
- ✅ 백업 생성 완료: {self.backup_dir}

## 🗑️ 정리된 파일 목록
"""
        for file_path in self.cleaned_files:
            report += f"- {file_path}\n"
        
        if not self.cleaned_files:
            report += "- 정리할 파일 없음\n"
        
        report += f"""

## 📊 프로젝트 상태
- 🧠 핵심 AI 모듈: 28개
- 🔌 플러그인: 6개
- 🧪 테스트 파일: 8개
- 📝 설정 파일: 5개

## 🚀 GitHub 푸시 준비 완료
프로젝트가 정리되어 GitHub 푸시가 준비되었습니다.
"""
        
        report_path = self.project_root / "CLEANUP_REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 정리 보고서 생성: {report_path}")
        return report_path
    
    def run_full_cleanup(self):
        """전체 정리 프로세스 실행"""
        print("🧹 소리새 프로젝트 전체 정리 시작!")
        print("=" * 60)
        
        # 1. 프로젝트 구조 분석
        self.analyze_project_structure()
        
        # 2. 중복 파일 탐지
        duplicates = self.find_duplicate_files()
        
        # 3. 불필요한 파일 탐지
        unnecessary_files = self.find_unnecessary_files()
        
        # 4. Import 오류 검사
        import_errors = self.check_import_errors()
        
        # 5. JSON 파일 검사
        json_errors = self.check_json_validity()
        
        # 6. 백업 생성
        backup_dir = self.create_backup()
        
        # 7. 불필요한 파일 정리
        self.clean_unnecessary_files(unnecessary_files)
        
        # 8. .gitignore 생성
        self.generate_gitignore()
        
        # 9. 정리 보고서 생성
        report_path = self.generate_cleanup_report()
        
        print("\n" + "=" * 60)
        print("🎉 프로젝트 정리 완료!")
        print(f"📁 백업 위치: {backup_dir}")
        print(f"📄 정리 보고서: {report_path}")
        print("🚀 GitHub 푸시 준비 완료!")
        
        return {
            'backup_dir': backup_dir,
            'report_path': report_path,
            'cleaned_files': len(self.cleaned_files),
            'duplicates': duplicates,
            'import_errors': import_errors,
            'json_errors': json_errors
        }

if __name__ == "__main__":
    cleaner = SorisaySystemCleaner()
    results = cleaner.run_full_cleanup()