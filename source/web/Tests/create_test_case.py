import os
import requests
import json
import base64
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Azure DevOps organization and project details
organization = 'EclipseInsightsHC'
project = 'Commercialization'

# Retrieve the AccessToken from environment variable
personal_access_token = os.getenv('AccessToken')
if not personal_access_token:
    logging.error("AccessToken environment variable is not set.")
    exit(1)

# Encode the PAT
encoded_pat = base64.b64encode(f':{personal_access_token}'.encode()).decode()

# Headers for the request
headers = {
    'Content-Type': 'application/json-patch+json',
    'Authorization': f'Basic {encoded_pat}'
}

# Headers for the WIQL query
wiql_headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {encoded_pat}'
}


def read_and_format_steps(file_path):
    with open(file_path, 'r') as file:
        test_cases = json.load(file)
        for test_case in test_cases:
            steps = "<steps>"
            for step in test_case['Steps']:
                steps += f"""
                <step id='1' type='ActionStep'>
                    <parameterizedString isformatted='true'>{step['StepName']}</parameterizedString>
                    <parameterizedString isformatted='true'>{step['StepExpectedResult']}</parameterizedString>
                </step>
                """
            steps += "</steps>"
            yield (
                test_case['TestCaseName'],
                steps,
                test_case['Description'],
                test_case['Test Method Name'],
                test_case['Assembly'],
                test_case['Namespace'],
                test_case['Test Class Name'],
                test_case['Test Type'],
                test_case['Test Plans']  # Updated to handle multiple test plans
            )


def search_test_case(title):
    # Escape single quotes in the title by doubling them
    escaped_title = title.replace("'", "''")

    # Construct the WIQL query
    query = {
        "query": f"Select [System.Id] From WorkItems Where [System.WorkItemType] = 'Test Case' AND [System.Title] = '{escaped_title}'"
    }
    url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=6.0'
    response = requests.post(url, headers=wiql_headers, data=json.dumps(query))
    if response.status_code == 200:
        work_items = response.json().get('workItems', [])
        if work_items:
            return work_items[0]['id']
    return None


def create_or_update_test_case(title, steps, description, test_method_name, test_assembly, test_namespace,
                               test_class_name, test_type):
    test_case_id = search_test_case(title)
    if test_case_id:
        logging.info(f"Test case with title '{title}' already exists with ID {test_case_id}. Checking for updates.")

        # Fetch the existing test case details
        existing_test_case = get_test_case_details(test_case_id)

        # Normalize the steps field for comparison (if necessary)
        existing_steps = existing_test_case.get('Microsoft.VSTS.TCM.Steps', '')
        new_steps = steps

        # Compare fields
        if (existing_test_case.get('System.Title') == title and
                existing_steps == new_steps and
                existing_test_case.get('Description') == description and
                existing_test_case.get('Microsoft.VSTS.TCM.AutomatedTestName') == test_method_name and
                existing_test_case.get('Microsoft.VSTS.TCM.AutomatedTestStorage') == test_assembly and
                existing_test_case.get('Microsoft.VSTS.TCM.AutomatedTestType') == test_type and
                existing_test_case.get(
                    'Microsoft.VSTS.TCM.AutomatedTestId') == f"{test_namespace}.{test_class_name}.{test_method_name}"):
            return test_case_id
        else:
            # Prepare the update payload
            data = [
                {
                    "op": "replace",
                    "path": "/fields/System.Title",
                    "value": title
                },
                {
                    "op": "replace",
                    "path": "/fields/Microsoft.VSTS.TCM.Steps",
                    "value": steps
                },
                {
                    "op": "replace",
                    "path": "/fields/Description",
                    "value": description
                },
                {
                    "op": "replace",
                    "path": "/fields/Microsoft.VSTS.TCM.AutomatedTestName",
                    "value": test_method_name
                },
                {
                    "op": "replace",
                    "path": "/fields/Microsoft.VSTS.TCM.AutomatedTestStorage",
                    "value": test_assembly
                },
                {
                    "op": "replace",
                    "path": "/fields/Microsoft.VSTS.TCM.AutomatedTestType",
                    "value": test_type
                },
                {
                    "op": "replace",
                    "path": "/fields/Microsoft.VSTS.TCM.AutomatedTestId",
                    "value": f"{test_namespace}.{test_class_name}.{test_method_name}"
                }
            ]

            # Update the test case
            update_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{test_case_id}?api-version=6.0'
            response = requests.patch(update_url, headers=headers, data=json.dumps(data))

            if response.status_code == 200:
                return test_case_id
            else:
                logging.error("Failed to update test case.")
                logging.error(f"Response: {response.content}")
                return None
    else:
        logging.info(f"No test case with title '{title}' found. Creating a new test case.")
        url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Test%20Case?api-version=6.0'
        data = [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": title
            },
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.TCM.Steps",
                "value": steps
            },
            {
                "op": "add",
                "path": "/fields/Description",
                "value": description
            },
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.TCM.AutomatedTestName",
                "value": test_method_name
            },
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.TCM.AutomatedTestStorage",
                "value": test_assembly
            },
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.TCM.AutomatedTestType",
                "value": test_type
            },
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.TCM.AutomatedTestId",
                "value": f"{test_namespace}.{test_class_name}.{test_method_name}"
            }
        ]
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            logging.info("Test case created successfully.")
            logging.info(f"Test Case ID: {response.json()['id']}")
            return response.json()['id']
        else:
            logging.error("Failed to create test case.")
            logging.error(f"Response: {response.content}")
            return None


def get_test_case_details(test_case_id):
    url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{test_case_id}?api-version=6.0'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['fields']
    else:
        logging.error(f"Failed to fetch test case details for ID {test_case_id}.")
        return None


def update_test_case_state(test_case_id, state):
    url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{test_case_id}?api-version=6.0'
    data = [
        {
            "op": "replace",
            "path": "/fields/System.State",
            "value": state
        }
    ]
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        logging.info("Test case state updated successfully.")
    else:
        logging.error("Failed to update test case state.")
        logging.error(f"Response: {response.content}")


def is_test_case_in_suite(test_plan_id, test_suite_id, test_case_id):
    url = f'https://dev.azure.com/{organization}/{project}/_apis/testplan/Plans/{test_plan_id}/suites/{test_suite_id}/testcase?api-version=6.0'
    response = requests.get(url, headers=wiql_headers)
    if response.status_code == 200:
        test_cases = response.json().get('value', [])
        for test_case in test_cases:
            if test_case['workItem']['id'] == test_case_id:
                return True
    return False


def add_test_case_to_suite(test_plan_id, test_suite_id, test_case_id):
    if not is_test_case_in_suite(test_plan_id, test_suite_id, test_case_id):
        url = f'https://dev.azure.com/{organization}/{project}/_apis/testplan/Plans/{test_plan_id}/suites/{test_suite_id}/testcase?api-version=6.0'
        data = [
            {
                "pointAssignments": [],
                "workItem": {
                    "id": test_case_id
                }
            }
        ]
        response = requests.post(url, headers=wiql_headers, data=json.dumps(data))
        if response.status_code == 200:
            logging.info(
                f"Test case {test_case_id} added to test suite {test_suite_id} in test plan {test_plan_id} successfully.")
        else:
            logging.error(
                f"Failed to add test case {test_case_id} to test suite {test_suite_id} in test plan {test_plan_id}.")
            logging.error(f"Response: {response.content}")
    else:
        logging.info(f"Test case {test_case_id} is already in test suite {test_suite_id} in test plan {test_plan_id}.")


# Example usage
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'config_testcase.json')
for title, steps, description, test_method_name, test_assembly, test_namespace, test_class_name, test_type, test_plans in read_and_format_steps(
        file_path):
    test_case_id = create_or_update_test_case(title, steps, description, test_method_name, test_assembly,
                                              test_namespace, test_class_name, test_type)
    if test_case_id:
        update_test_case_state(test_case_id, "Ready")
        for test_plan in test_plans:
            test_plan_id = test_plan['Test Plan ID']
            for test_suite_id in test_plan['Test Suite ID']:
                add_test_case_to_suite(test_plan_id, test_suite_id, test_case_id)