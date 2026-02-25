import os
import sys

# Fix import path issue
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from static_analyzer import analyze_file
from duplication_detector import detect_duplicates
from dead_code_detector import detect_unused_files


BASE_DIR = CURRENT_DIR

# Full repo scan (go up to PROCESS-LOG root)
TARGET_DIRECTORY = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

# Save report in source/reports
REPORT_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "reports", "report.md"))


def generate_report():
    report_lines = []
    report_lines.append("# 🤖 AI Test Maintenance Report\n")
    report_lines.append(f"Scanning: {TARGET_DIRECTORY}\n")

    for root, dirs, files in os.walk(TARGET_DIRECTORY):
        for file in files:
            if file.endswith((".py", ".yaml", ".yml", ".js", ".ts", ".html", ".md")):
                file_path = os.path.join(root, file)
                try:
                    issues = analyze_file(file_path)
                    if issues:
                        report_lines.append(f"\n## 📄 {file_path}")
                        for issue in issues:
                            report_lines.append(f"- {issue}")
                except Exception as e:
                    report_lines.append(f"\n⚠️ Error analyzing {file_path}: {str(e)}")

    duplicates = detect_duplicates(TARGET_DIRECTORY)
    if duplicates:
        report_lines.append("\n## 🔁 Duplicate Files Detected")
        for group in duplicates:
            report_lines.append(f"- {group}")

    unused = detect_unused_files(TARGET_DIRECTORY)
    if unused:
        report_lines.append("\n## 🗑️ Unused Files")
        for file in unused:
            report_lines.append(f"- {file}")

    # Ensure reports folder exists
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print("✅ Report generated successfully.")
    print(f"📄 Report location: {REPORT_PATH}")


if __name__ == "__main__":
    generate_report()