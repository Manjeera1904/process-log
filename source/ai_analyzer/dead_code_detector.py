import os

def detect_dead_code():
    # Define the directory to scan (usually your source or tests folder)
    directory = "source" 
    all_files_data = {}
    
    # 1. Read all files into a dictionary {path: content}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".py", ".js", ".ts")):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", errors="ignore", encoding="utf-8") as f:
                        all_files_data[full_path] = f.read()
                except Exception as e:
                    print(f"Could not read {full_path}: {e}")

    unused = []
    all_paths = list(all_files_data.keys())

    # 2. Check if file_name appears in any OTHER file's content
    for target_path in all_paths:
        file_name = os.path.basename(target_path).split('.')[0]
        
        # Skip main/config as they are entry points
        if "main" in file_name.lower() or "config" in file_name.lower():
            continue

        is_used = False
        for other_path, content in all_files_data.items():
            if target_path == other_path:
                continue # Don't look at yourself
            
            if file_name in content:
                is_used = True
                break
        
        if not is_used:
            unused.append(target_path)
                
    return f"Unused Files detected: {unused}" if unused else "No unused files detected."