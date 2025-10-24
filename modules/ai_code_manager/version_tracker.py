"""
버전 추적 시스템
"""
import json
import os
from datetime import datetime

VERSION_FILE = "version.json"

def get_current_version():
    """현재 버전 정보 가져오기"""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"version": "1.0.0", "updated": ""}

def update_version():
    """버전 정보 업데이트"""
    version_info = get_current_version()
    version_info["updated"] = datetime.now().isoformat()
    
    with open(VERSION_FILE, 'w', encoding='utf-8') as f:
        json.dump(version_info, f, ensure_ascii=False, indent=2)
    
    return version_info

if __name__ == "__main__":
    update_version()
