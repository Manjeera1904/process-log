import os
import re

def detect_unused_files(directory):
    all_files = []
    all_content = ""
    
    # 1. Map all files and read all content
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".py", ".js", ".ts")):
                full_path = os.path.abspath(os.path.join(root, file))
                all_files.append(full_path)
                with open(full_path, "r", errors="ignore") as f:
                    all_content += f.read()

    unused = []
    for file_path in all_files:
        file_name = os.path.basename(file_path).split('.')[0]
        # Check if the filename is mentioned (imported) anywhere in the codebase
        if file_name not in all_content:
            # Avoid flagging main or config files
            if "main" not in file_name and "config" not in file_name:
                unused.append(file_path)
                
    return unused