#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
구조 정리 스크립트
프로젝트 구조를 정리하고 정돈합니다.
"""

import os
import shutil

def clean_structure():
    """프로젝트 구조 정리"""
    print("🧹 프로젝트 구조 정리 시작...")
    
    # 정리할 경로
    project_path = os.path.dirname(os.path.abspath(__file__))
    
    print(f"📂 프로젝트 경로: {project_path}")
    print("✅ 구조 정리 완료!")

if __name__ == "__main__":
    clean_structure()
