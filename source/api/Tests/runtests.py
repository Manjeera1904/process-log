import pytest
import xml.etree.ElementTree as ET
import os
import json
import shutil

test_script_path = os.path.dirname(os.path.abspath(__file__))

shutil.copy(os.path.join(test_script_path, 'config_Template.json').replace('\\', '/'),
            os.path.join(test_script_path, 'config.json'))

config_path = os.path.join(test_script_path, 'config.json').replace('\\', '/')

with open(config_path, 'r') as config_file:
    config_data = json.load(config_file)

env = os.environ.get('ENVIRONMENT').lower()

pc_base_url = f'https://{env}.eclipsevantage.com/platform-core'

ui_base_url = f'https://{env}.eclipsevantage.com'

platform_url = f'https://{env}.eclipsevantage.com/platform-core'

apiBaseUrl = f'https://process-logging-api.{env}.eclipsevantage.com'

pc_api_base_url = f'https://platform-core-api.{env}.eclipsevantage.com'

test_files = [
    os.path.join(test_script_path, 'test_CreateTokenApi.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_ActivityTypeApi.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_ProcessLogApi.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_ProcessStatusApi.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_FileProcessLogApi.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_MessageLevelApi.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_ProcessLogMessageApi.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_message_handling.py').replace('\\', '/'),
    # os.path.join(test_script_path, 'test_process_log_to_application_events.py').replace('\\', '/'),
    # os.path.join(test_script_path, 'test_X12InterchangeApi.py').replace('\\', '/'),
    # os.path.join(test_script_path, 'test_X12StatusApi.py').replace('\\', '/'),
    # os.path.join(test_script_path, 'test_X12FunctionalGroupApi.py').replace('\\', '/'),
    # os.path.join(test_script_path, 'test_X12TransactionSetApi.py').replace('\\', '/'),
    # os.path.join(test_script_path, 'test_X12MessageApi.py').replace('\\', '/'),

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

    merge_xml_reports(os.path.join(test_script_path, 'test-results.xml'), append=True)
    os.remove(os.path.join(test_script_path, 'config.json').replace('\\', '/'))
