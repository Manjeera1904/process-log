import base64
import os
import json
import xml.etree.ElementTree as ET
import requests

# Mapping of environments to Test Suite IDs
TEST_SUITE_IDS = {
    'int': 1474,
    'test': 1324,
    'demo': 1363
}


# Function to read the JSON file and filter test cases based on the environment
def read_and_filter_test_cases(file_path):
    with open(file_path, 'r') as file:
        test_cases = json.load(file)
        for test_case in test_cases:
            test_case_title = test_case['TestCaseName']
            test_method_name = test_case['Test Method Name']
            for test_plan in test_case['Test Plans']:
                yield test_case_title, test_method_name, test_plan['Test Plan ID'], test_plan['Test Suite ID']


# Function to parse the test results XML file and get the outcome of the specific test method
def get_test_outcome_from_xml(test_results_file, test_method_name):
    tree = ET.parse(test_results_file)
    root = tree.getroot()
    for testsuite in root.iter('testsuite'):
        for testcase in testsuite.iter('testcase'):
            if testcase.get('name') == test_method_name:
                if testcase.find('failure') is None and testcase.find('error') is None:
                    outcome = "Passed"
                else:
                    outcome = "Failed"
                print(f"Test outcome for {test_method_name}: {outcome}")
                return outcome
    return "Failed"


# Function to get the test case ID from the test suite by comparing the test case title
def get_test_case_id_by_title(test_plan_id, test_suite_id, test_case_title, headers):
    organization = 'EclipseInsightsHC'
    project = 'Commercialization'
    url = f"https://dev.azure.com/{organization}/{project}/_apis/testplan/Plans/{test_plan_id}/Suites/{test_suite_id}/TestCase?api-version=6.0"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        test_cases = response.json()['value']
        for test_case in test_cases:
            if test_case['workItem']['name'] == test_case_title:
                return test_case['workItem']['id']
    else:
        print(f"Failed to get test cases: {response.status_code} - {response.text}")
    return None


# Function to get the test point ID from the test plan by comparing the test case ID
def get_test_point_id(test_plan_id, test_suite_id, test_case_id, headers):
    organization = 'EclipseInsightsHC'
    project = 'Commercialization'
    url = f"https://dev.azure.com/{organization}/{project}/_apis/testplan/Plans/{test_plan_id}/Suites/{test_suite_id}/TestPoint?api-version=6.0"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        test_points = response.json()['value']
        for test_point in test_points:
            if 'testCaseReference' in test_point and test_point['testCaseReference']['id'] == test_case_id:
                return test_point['id']
    else:
        print(f"Failed to get test points: {response.status_code} - {response.text}")
    return None


# Function to update the test case result in Azure DevOps
def update_test_case_result(test_plan_id, test_suite_id, test_case_id, outcome, headers):
    test_point_id = get_test_point_id(test_plan_id, test_suite_id, test_case_id, headers)
    if test_point_id is None:
        print(f"Test point ID not found for test case ID {test_case_id} in Test Suite ID {test_suite_id}")
        return

    organization = 'EclipseInsightsHC'
    project = 'Commercialization'
    url = f"https://dev.azure.com/{organization}/{project}/_apis/testplan/Plans/{test_plan_id}/Suites/{test_suite_id}/TestPoint?api-version=6.0"
    data = [
        {
            "id": test_point_id,
            "results":
                {
                    "outcome": 2 if outcome == "Passed" else 3
                }
        }
    ]
    response = requests.patch(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"Successfully updated test case result for test case ID {test_case_id} in Test Suite ID {test_suite_id}")
    else:
        print(
            f"Failed to update test case result for test case ID {test_case_id} in Test Suite ID {test_suite_id}: {response.status_code} - {response.text}")


# Main function to run all steps
def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'config_testcase.json')

    # Retrieve the Environment from environment variable
    environment = os.getenv('Environment')
    if not environment:
        print("Environment variable is not set.")
        return

    # Get the Test Suite ID based on the environment
    test_suite_id = TEST_SUITE_IDS.get(environment)
    if not test_suite_id:
        print(f"Test Suite ID not found for environment {environment}")
        return

    # Process test cases for the specified Test Suite ID
    for test_case_title, test_method_name, plan_id, suite_ids in read_and_filter_test_cases(file_path):

        # Check if the Test Suite ID matches the environment's Test Suite ID
        if str(test_suite_id) not in map(str, suite_ids):
            print(
                f"Skipping test case '{test_case_title}' as it does not belong to the environment's Test Suite ID {test_suite_id}")
            continue

        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_results_file = os.path.join(current_dir, f'test-results-{environment}env.xml')

        outcome = get_test_outcome_from_xml(test_results_file, test_method_name)
        print(f"Outcome for test case '{test_case_title}' in Test Suite ID {test_suite_id}: {outcome}")

        # Retrieve the AccessToken from environment variable
        personal_access_token = os.getenv('AccessToken')
        if not personal_access_token:
            print("AccessToken environment variable is not set.")
            return

        # Encode the personal access token
        encoded_pat = base64.b64encode(f':{personal_access_token}'.encode()).decode()

        # Headers for the request
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {encoded_pat}'
        }

        # Process each test suite ID for the test case
        for suite_id in suite_ids:
            if str(suite_id) == str(test_suite_id):  # Ensure only the correct test suite is processed
                test_case_id = get_test_case_id_by_title(plan_id, suite_id, test_case_title, headers)
                if test_case_id is None:
                    print(f"Test case ID not found for test case title '{test_case_title}' in Test Suite ID {suite_id}")
                    continue  # Skip to the next test suite if the test case ID is not found

                update_test_case_result(plan_id, suite_id, test_case_id, outcome, headers)


if __name__ == "__main__":
    main()