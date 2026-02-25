import argparse
import json
import os
import xml.etree.ElementTree as ET
import shutil
import pytest

test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config_path = os.path.join(test_script_path, 'config.json').replace('\\', '/')

shutil.copy(os.path.join(test_script_path, 'config_Template.json').replace('\\', '/'),
            os.path.join(test_script_path, 'config.json').replace('\\', '/'))

with open(config_path, 'r') as config_file:
    config_data = json.load(config_file)

test_files = [
    os.path.join(test_script_path, 'test_ComponentMetadata.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_CreateTokenApi.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_CreateRoleRBAC.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_NonProdHelperApi.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_processMonitoringUI.py').replace('\\', '/')
]

if __name__ == "__main__":
    # Run pytest directly
    pytest.main([
        *test_files,
        f'--junitxml={os.path.join(test_script_path, "test-results-devenv.xml")}',
        '--tb=short',
        '--disable-warnings'
    ])


