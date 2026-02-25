import os
from collections import defaultdict

def detect_duplicates(directory):
    content_map = defaultdict(list)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".js") or file.endswith(".ts"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    normalized = content.replace(" ", "").replace("\n", "")
                    content_map[normalized[:300]].append(path)

    duplicates = []
    for key, files in content_map.items():
        if len(files) > 1:
            duplicates.append(files)

    return duplicates