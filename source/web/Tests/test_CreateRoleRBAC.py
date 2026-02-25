import os
import pytest
import requests
import json
from datetime import datetime, timedelta
from test_CreateTokenApi import generate_token

test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config_path = os.path.join(test_script_path, 'config.json').replace('\\', '/')


def read():
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        return config


# Save configuration to config.json
def saveConfig(config_data):
    with open(config_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print("Config data saved successfully.")


# Load config at the start
config = read()
apiBaseUrl = config.get("apiBaseUrl")
apiVersion = config['common']['versionId']


# Set the token in the header
def token():
    token = generate_token()
    if not token or not isinstance(token, str) or "<!doctype html>" in token.lower():
        raise ValueError(f"Invalid token generated: {token}")
    print(f"Generated token: {token}")
    header = {"Authorization": f"Bearer {token}"}
    return header


# Generic method for making requests
def makeRequest(method, endpoint, data=None, header=None):
    if header is None:
        header = token()
    url = f"{apiBaseUrl}{endpoint}"

    # Handle request types
    try:
        if method == 'post':
            response = requests.post(url, json=data, verify=False, headers=header)
        elif method == 'get':
            response = requests.get(url, verify=False, headers=header)
        elif method == 'put':
            response = requests.put(url, json=data, verify=False, headers=header)
        else:
            raise ValueError("Invalid method type provided.")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        raise

    # Check if the response is JSON
    try:
        if 'application/json' in response.headers.get('Content-Type', ''):
            response_data = response.json()
            print("Response body:", json.dumps(response_data, indent=4))
        else:
            response_data = response.text
            print("Response body is not JSON:", response_data)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        raise

    if response.status_code == 401:
        print("Unauthorized access - possibly invalid token")

    return response, response_data


def test_user_client_initial():
    config = read()
    payloaduser = "TestAutomation02@EclipseDevelopmentTest.onmicrosoft.com"
    # Fetch all users and find the specific user by email
    response, response_data_users = makeRequest('get', f"/api/User?api-version={apiVersion}")
    assert response.status_code == 200, f"Failed to fetch users. Status code: {response.status_code}"
    assert isinstance(response_data_users, list), "Expected response data to be a list of users"
    user_id = None
    for user in response_data_users:
        if not isinstance(user, dict):
            print(f"Unexpected user data format: {user}")
            continue
        if user.get('userName') == payloaduser:
            config['userApi']['userId'] = user.get('id')
            saveConfig(config)

    if user_id:
        print(f"User found with ID: {user_id}")
    else:
        print(f"User with email {payloaduser} not found.")
        return


def test_user_client_connect():
    config = read()
    payloadclient = "Eclipse_Insights_Automation"
    response, response_data_client = makeRequest('get', f"/api/Client/name/{payloadclient}?api-version={apiVersion}")

    assert response.status_code == 200, f"Failed to fetch client. Status code: {response.status_code}"
    print("Client response:", response_data_client)

    payload = config['userClientApi']
    payload["userId"] = config['userApi']['userId']
    if isinstance(response_data_client, list) and response_data_client:
        payload["clientId"] = response_data_client[0].get('id')  # Assuming the first item is the desired client
    elif isinstance(response_data_client, dict):
        payload["clientId"] = response_data_client.get('id')
    else:
        raise ValueError("Unexpected response format for client data")
    payload["isDefault"] = True
    response, response_data_userclient = makeRequest('post', f"/api/UserClient?api-version={apiVersion}", payload)
    assert response.status_code in [201, 409], f"Failed to create UserClient. Status code: {response.status_code}"
    config['userClientApi']['userClientId'] = response_data_userclient[0].get('id')
    config['userClientApi']['rowVersion'] = response_data_userclient[0].get('rowVersion')
    saveConfig(config)

    config = read()
    payload = config['userClientApi']
    user_client_id = config['userClientApi']['userClientId']
    payload["isDefault"] = True
    payload["id"] = user_client_id
    response, response_data_userclientconnect = makeRequest('put',
                                                            f"/api/UserClient/{user_client_id}?api-version={apiVersion}",
                                                            payload)
    assert response.status_code in [200, 409], f"Failed to create UserClient. Status code: {response.status_code}"
