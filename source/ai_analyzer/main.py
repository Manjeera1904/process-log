import os
import sys

# 1. Setup paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from static_analyzer import analyze_file
from duplication_detector import detect_duplicates
from dead_code_detector import detect_unused_files

# Ensure we are at the root
REPO_ROOT = os.environ.get('GITHUB_WORKSPACE', os.path.abspath(os.path.join(CURRENT_DIR, "../../")))
REPORT_DIR = os.path.join(REPO_ROOT, "source", "reports")
REPORT_PATH = os.path.join(REPORT_DIR, "report.md")

def run_pipeline():
    os.makedirs(REPORT_DIR, exist_ok=True)
    report = ["# 🤖 AI Test Maintenance Report\n"]
    report.append("## 🔍 Files Scanned\n")
    
    print(f"🚀 Starting scan at: {REPO_ROOT}")
    
    found_any_files = False

    # 2. AI Analysis Loop
    for root, dirs, files in os.walk(REPO_ROOT):
        # Skip system folders
        if any(ignored in root for ignored in [".git", "__pycache__", "node_modules", "ai_analyzer", "reports"]):
            continue
            
        for file in files:
            # Check for Python, JS, TS (Add others if needed)
            if file.endswith((".py", ".js", ".ts")):
                found_any_files = True
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, REPO_ROOT)
                
                print(f"📄 Found file: {rel_path} - Sending to AI...")
                
                try:
                    issues = analyze_file(path)
                    if "No issues" in issues or not issues.strip():
                        report.append(f"### ✅ {rel_path}\n* Status: Clean\n")
                    else:
                        report.append(f"### ❌ {rel_path}\n{issues}\n")
                except Exception as e:
                    print(f"   ⚠️ Error: {e}")

    if not found_any_files:
        print("❌ No test files found! Check your folder structure.")
        report.append("> ⚠️ No supported files (.py, .js, .ts) were found in the repository.")

    # 3. Standard Detectors
    report.append("\n---\n## ⚙️ Maintenance Checks")
    
    dupes = detect_duplicates(REPO_ROOT)
    report.append(f"\n### 🔁 Duplicates\n" + ("\n".join([f"- {d}" for d in dupes]) if dupes else "No duplicates found."))

    unused = detect_unused_files(REPO_ROOT)
    report.append(f"\n### 🗑️ Unused Code\n" + ("\n".join([f"- {u}" for u in unused]) if unused else "No unused files found."))

    # 4. Save
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print(f"✅ Report saved to: {REPORT_PATH}")

if __name__ == "__main__":
    run_pipeline()