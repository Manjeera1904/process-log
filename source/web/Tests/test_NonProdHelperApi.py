import json
import os
import requests
import pytest
from requests import RequestException

test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config_path = os.path.join(test_script_path, 'config.json').replace('\\', '/')

# Load configuration data from config.json
with open(config_path, 'r') as config_file:
    config_data = json.load(config_file)

# Get API URL from config (set by runtests.py)
base_url = config_data['apiBaseUrl']

version_id = config_data.get("common", {}).get("versionId")
nonProdHelper_post_data = config_data.get('nonProdHelperApi')

def read():
    with open(config_path, 'r') as config_file:
        config_data = json.load(config_file)

# Set the token in the header
token = config_data.get("tokenApi", {}).get("token")

def makeRequest(method, endpoint, data=None):
    # Re-read the config to get latest token
    with open(config_path, 'r') as config_file:
        config_data = json.load(config_file)

    token = config_data.get("tokenApi", {}).get("token")

    url = f"{base_url}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        if method == 'delete':
            response = requests.delete(url, json=data, headers=headers, verify=False)
        else:
            raise ValueError(f"Invalid method type provided: {method}")
    except RequestException as e:
        print(f"Request exception occurred: {e}")
        raise

    try:
        response_json = response.json()
    except json.JSONDecodeError:
        response_json = {}

    if response.status_code != 200:
        print("\n======= DEBUG INFO =======")
        print(f"URL: {url}")
        print("Request Headers:", json.dumps(headers, indent=2))
        print("Request Payload:", json.dumps(data, indent=2))
        print(f"Status Code: {response.status_code}")
        print("Response Text:", response.text or "[EMPTY RESPONSE BODY]")
        print("==========================\n")

    return response, response_json

@pytest.mark.parametrize("valid_data", [({})])
def testDeleteRequest(valid_data):
    data_to_send = nonProdHelper_post_data.copy()
    data_to_send.update(valid_data)
    response, response_data = makeRequest('delete', f"/api/NonProdHelper?api-version={version_id}", data_to_send)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"