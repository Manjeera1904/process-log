import pytest
import os
import xml.etree.ElementTree as ET

test_script_path = os.path.dirname(os.path.abspath(__file__))

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