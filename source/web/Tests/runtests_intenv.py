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

# smoke tests
smoke_tests = [
    os.path.join(test_script_path, 'test_ComponentMetadata.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_CreateTokenApi.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_ClientConfiguration.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_UserClientConfiguration.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_NonProdHelperApi.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_ImportValuesFromTS.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_SmokeTests.py').replace('\\', '/'),
]

# Full test suite
test_files = [
    os.path.join(test_script_path, 'test_processMonitoringUI.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_verifySignalRUI.py').replace('\\', '/'),
    os.path.join(test_script_path, 'test_GridComponentAndTableBehivour.py').replace('\\', '/')
]
if __name__ == "__main__":
    # Run smoke tests first
    print("\n=== Running Smoke Tests ===")
    smoke_result = pytest.main([
        *smoke_tests,
        f'--junitxml={os.path.join(test_script_path, "test-results-smoke.xml")}',
        '--tb=short',
        '--disable-warnings'
    ])

    if smoke_result != 0:
        print("\n Smoke tests failed. Skipping full test suite.")
        exit(smoke_result)

    # Run full test suite if smoke tests passed
    print("\n Smoke tests passed. Running full test suite...")
    exit(pytest.main([
        *test_files,
        f'--junitxml={os.path.join(test_script_path, "test-results-intenv.xml")}',
        '--tb=short',
        '--disable-warnings'
    ]))
