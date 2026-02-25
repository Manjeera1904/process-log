import json
import os
import requests
import pytest
import uuid
import re
import shutil

test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config_path = os.path.join(test_script_path, 'config.json').replace('\\', '/')

shutil.copy(os.path.join(test_script_path, 'config_Template.json').replace('\\', '/'),
            os.path.join(test_script_path, 'config.json').replace('\\', '/'))

# Load configuration data from config.json
with open(config_path, 'r') as config_file:
    config_data = json.load(config_file)

# Base URL for the API
versionId3 = config_data.get("common", {}).get("versionId3")
apiBaseUrl = config_data.get("apiBaseUrl")


# Load configuration from config.json
def loadConfig():
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        return config


# Generic method for making requests
def makeRequest(method, endpoint, data=None, isJsonResponse="true", header=None):
    url = f"{apiBaseUrl}{endpoint}"
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
def generate_token():
    config = loadConfig()
    tokenApiPayload = config['tokenApi']
    mtoken = tokenApiPayload['mtoken']
    idToken = tokenApiPayload['idToken']
    response, response_data = makeRequest('get', f"/api/Authorization/Token?api-version={versionId3}", None, "false",
                                          {"Authorization": f"Bearer {mtoken}","X-ID-Token": idToken})
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response_data != {}, f"Expected token, but got empty"
    assert response_data["content"].decode('UTF-8') != "", f"Expected token, but got empty"

    token = response_data["content"].decode('UTF-8')
    saveId("token", token, config)
    return token


def test_generate_token():
    token = generate_token()
    assert token != "", "Token should not be empty"


if __name__ == "__main__":
    pytest.main([__file__])
