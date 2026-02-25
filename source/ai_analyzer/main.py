import os
import sys

# Ensure neighbor scripts can be imported
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from static_analyzer import analyze_file
from duplication_detector import detect_duplicates
from dead_code_detector import detect_unused_files

# Use GITHUB_WORKSPACE (root) or local fallback
REPO_ROOT = os.environ.get('GITHUB_WORKSPACE', os.path.abspath(os.path.join(CURRENT_DIR, "..", "..")))
REPORT_DIR = os.path.join(REPO_ROOT, "source", "reports")
REPORT_PATH = os.path.join(REPORT_DIR, "report.md")

def run_pipeline():
    os.makedirs(REPORT_DIR, exist_ok=True)
    report = ["# 🤖 AI Test Maintenance Report\n"]
    
    # 1. AI Analysis
    for root, _, files in os.walk(REPO_ROOT):
        for file in files:
            if file.endswith((".py", ".js", ".ts")) and "ai_analyzer" not in root:
                path = os.path.join(root, file)
                issues = analyze_file(path)
                if "No issues" not in issues:
                    report.append(f"### 📄 {os.path.relpath(path, REPO_ROOT)}\n{issues}\n")

    # 2. Duplicates & Unused (Standard Logic)
    # ... call detect_duplicates(REPO_ROOT) ...
    # ... call detect_unused_files(REPO_ROOT) ...

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print(f"✅ Created report at: {REPORT_PATH}")

if __name__ == "__main__":
    run_pipeline()