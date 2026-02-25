import json
import requests
import pytest
import uuid
import re
from runtests import config_path, pc_api_base_url

# Load configuration data from config.json
with open(config_path, 'r') as config_file:
    config_data = json.load(config_file)

# Base URL for the API
version_id = config_data.get("common", {}).get("apiVersion3")


# Load configuration from config.json
def loadConfig():
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        return config


# Generic method for making requests
def makeRequest(method, endpoint, data=None, isJsonResponse="true", header=None):
    url = f"{pc_api_base_url}{endpoint}"
    print(f"{method.upper()} URL: {url}")

    # Handle request types
    try:
        if method == 'post':
            response = requests.post(url, json=data, verify=False)
        elif method == 'get':
            if header is None:
                response = requests.get(url, verify=False)
            else:
                response = requests.get(url, verify=False, headers=header)
        elif method == 'put':
            response = requests.put(url, json=data, verify=False)
        else:
            raise ValueError("Invalid method type provided.")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        raise

    # Parse response data
    try:
        if isJsonResponse == "true":
            response_data = response.json()
            print("Response body:", json.dumps(response_data, indent=4))
        else:
            response_data = {"content": response.content}
            print("Response body:", response.content)

    except json.JSONDecodeError:
        print("Response body is not JSON:", response.text)
        response_data = {}

    return response, response_data


# Save client ID to config.json
def saveId(key, value, config_data):
    # Save clientId under the tokenApi section
    config_data['tokenApi'][key] = value

    # Write the updated data back to the file
    with open(config_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)


# Create token

def testgenerate_token(tokenApiPayload=None):
    config = loadConfig()
    if tokenApiPayload is None:
        tokenApiPayload = config['tokenApi']
    mtoken = tokenApiPayload['mtoken']
    idToken = tokenApiPayload['idToken']
    response, response_data = makeRequest('get', f"/api/Authorization/Token?api-version={version_id}", None, "false",
                                          {"Authorization": f"Bearer {mtoken}","X-ID-Token": idToken})
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    token = response_data["content"].decode('UTF-8')
    saveId("token", token, config)


if __name__ == "__main__":
    pytest.main()