import os

def detect_unused_files(directory):
    all_files = []
    referenced_files = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".js") or file.endswith(".ts"):
                path = os.path.join(root, file)
                all_files.append(path)

                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    for other in files:
                        if other in content:
                            referenced_files.add(os.path.join(root, other))

    unused = [f for f in all_files if f not in referenced_files]
    return unused