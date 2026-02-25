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
    
    print(f"🚀 Starting scan at REPO_ROOT: {REPO_ROOT}")
    
    # 1. AI Analysis
    for root, dirs, files in os.walk(REPO_ROOT):
        # SKIP unnecessary folders to speed up the scan and clean up logs
        if any(ignored in root for ignored in [".git", "__pycache__", "node_modules", "ai_analyzer", "reports"]):
            continue
            
        # THIS IS THE LINE: It prints the current folder being scanned
        print(f"📂 Scanning folder: {root}")

        for file in files:
            if file.endswith((".py", ".js", ".ts")):
                path = os.path.join(root, file)
                print(f"   📄 Analyzing file: {file}") # Track progress per file
                
                try:
                    issues = analyze_file(path)
                    if "No issues" not in issues and issues.strip():
                        report.append(f"### 📄 {os.path.relpath(path, REPO_ROOT)}\n{issues}\n")
                except Exception as e:
                    print(f"   ❌ Error analyzing {file}: {e}")

    # 2. Add Duplicates and Unused to the report
    duplicates = detect_duplicates(REPO_ROOT)
    if duplicates:
        report.append("## 🔁 Duplicate Files\n" + "\n".join([f"- {d}" for d in duplicates]))

    unused = detect_unused_files(REPO_ROOT)
    if unused:
        report.append("## 🗑️ Unused Files\n" + "\n".join([f"- {u}" for u in unused]))

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
        
    print(f"✅ Created report at: {REPORT_PATH}")