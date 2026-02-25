import re
import json
import os
import pytest

@pytest.fixture
def paths():
    """Fixture to provide important project paths."""
    test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
    repo_root = os.path.dirname(test_script_path)

    return {
        "test_script_path": test_script_path,
        "repo_root": repo_root,
        "config_path": os.path.join(test_script_path, "config.json").replace('\\', '/'),
        "theme_path": os.path.join(repo_root, "src/theme.ts").replace('\\', '/'),
               
    }

def get_theme_code(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# 2. Dedicated function for the JSON config
def update_json_file(path, new_values):
    # Read
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Modify
    if "common" not in data:
        data["common"] = {}
    data["common"].update(new_values)
    
    # Write
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def test_sync_theme_to_config(paths):
    # STEP 1: Get the TS code as a string
    theme_text = get_theme_code(paths["theme_path"])
    
    # STEP 2: Extraction logic (Regex)
    size_match = re.search(r"typography:\s*\{.*?fontSize:\s*(\d+)", theme_text, re.DOTALL)
    font_match = re.search(r"fontFamily:\s*['\"]+([^'\"]+)['\"]+", theme_text, re.DOTALL)
    
    if size_match and font_match:
        extracted = {
            "expected_font_size": f"{size_match.group(1)}px",
            "expected_font_family": font_match.group(1).split(',')[0].strip().replace('"', '').replace("'", "")
        }
        
        # STEP 3: Put it in the JSON
        update_json_file(paths["config_path"], extracted)
        print(f" Success! Synced: {extracted}")