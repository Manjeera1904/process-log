import hashlib
import os

def detect_duplicates(directory):
    hashes = {}
    duplicates = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".py", ".js", ".ts")):
                path = os.path.join(root, file)
                with open(path, "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                
                if file_hash in hashes:
                    duplicates.append(f"{path} is a duplicate of {hashes[file_hash]}")
                else:
                    hashes[file_hash] = path
    return duplicates