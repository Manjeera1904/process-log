import pytest
import os
import xml.etree.ElementTree as ET
import os
import json
import shutil

test_script_path = os.path.dirname(os.path.abspath(__file__))

shutil.copy(os.path.join(test_script_path, 'config_Template.json').replace('\\', '/'),
            os.path.join(test_script_path, 'config.json').replace('\\', '/'))

config_path = os.path.join(test_script_path, 'config.json').replace('\\', '/')

with open(config_path, 'r') as config_file:
    config_data = json.load(config_file)

env = os.environ.get('ENVIRONMENT').lower()

baseUrl = f'https://{env}.eclipsevantage.com'
platformUrl = f'{baseUrl}/platform-core'
apiUrl = f'https://platform-core-api.{env}.eclipsevantage.com'

if isinstance(config_data, list):
    config_data = {
        "baseUrl": baseUrl,
        "apiBaseUrl": apiUrl,
        "platformUrl": platformUrl,
        "components": config_data,
        "env": env
    }
else:
    config_data["baseUrl"] = baseUrl
    config_data["apiBaseUrl"] = apiUrl
    config_data["platformUrl"] = platformUrl
    config_data["processLogUrl"] = platformUrl
    config_data["env"] = env
with open(config_path, 'w') as config_file:
    json.dump(config_data, config_file, indent=4)

test_files = [
    os.path.join(test_script_path, 'test_get_msal_from_UI_user1.py').replace('\\', '/')
]


def merge_xml_reports(output_file, append=False):
    if append and os.path.exists(output_file):
        merged_tree = ET.parse(output_file)
        merged_root = merged_tree.getroot()
    else:
        merged_root = ET.Element("testsuites")

    for test_file in test_files:
        temp_file = os.path.join(test_script_path, f"{os.path.basename(test_file)}.xml")
        if os.path.exists(temp_file):
            print(f"Merging: {temp_file}")
            tree = ET.parse(temp_file)
            root = tree.getroot()
            for testsuite in root.findall('testsuite'):
                merged_root.append(testsuite)
            os.remove(temp_file)
        else:
            print(f"File not found: {temp_file}")

    tree = ET.ElementTree(merged_root)
    tree.write(output_file)


if __name__ == "__main__":
    for test_file in test_files:
        junitxml_path = os.path.join(test_script_path, f"{os.path.basename(test_file)}.xml")
        pytest.main([test_file, f'--junitxml={junitxml_path}'])