import os
import re

def analyze_file(file_path):
    issues = []

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.split("\n")

    # 1️⃣ Missing Assertions
    if "expect(" not in content and "assert" not in content:
        issues.append("❌ No assertions found in file.")

    # 2️⃣ Sleep Usage
    if "sleep(" in content or "wait(" in content:
        issues.append("⚠️ Possible hard wait detected (sleep/wait). Use explicit waits.")

    # 3️⃣ Hardcoded values (basic detection)
    hardcoded_strings = re.findall(r'\"[A-Za-z0-9@#$%^&*()_+=-]{6,}\"', content)
    if hardcoded_strings:
        issues.append(f"⚠️ Hardcoded values detected: {hardcoded_strings[:3]}")

    # 4️⃣ Long Test Method Detection (>40 lines)
    test_blocks = re.findall(r'it\((.*?)\{([\s\S]*?)\}\);', content)
    for block in test_blocks:
        block_lines = block[1].split("\n")
        if len(block_lines) > 40:
            issues.append("⚠️ Long test method detected (>40 lines). Consider refactoring.")

    # 5️⃣ Index-based XPath
    if re.search(r'\(//.*?\)\[\d+\]', content):
        issues.append("⚠️ Index-based XPath detected. Avoid unstable locators.")

    return issues