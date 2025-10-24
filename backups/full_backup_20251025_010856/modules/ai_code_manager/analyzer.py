import json, time

class Analyzer:
    def __init__(self, log_data=None):
        self.log_data = log_data or []
        self.summary = {}

    def analyze(self):
        total = len(self.log_data)
        success = sum(1 for r in self.log_data if r.get("success"))
        failed = total - success
        avg_time = round(sum(r.get("exec_time", 0) for r in self.log_data) / (total or 1), 2)

        self.summary = {
            "total": total,
            "success": success,
            "failed": failed,
            "avg_time": avg_time,
            "success_rate": round(success / (total or 1) * 100, 2)
        }
        return self.summary

    def save_report(self, path="logs/ai_report.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.summary, f, ensure_ascii=False, indent=2)
        print(f"📊 분석 리포트 저장 완료: {path}")
        return path
