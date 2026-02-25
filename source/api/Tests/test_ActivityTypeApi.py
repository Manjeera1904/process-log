import json
import requests
import pytest
from runtests import config_path, apiBaseUrl, pc_api_base_url, env


def load_Config():
    with open(config_path) as config_file:
        return json.load(config_file)


# Load configuration data
with open(config_path, 'r') as configFile:
    configData = json.load(configFile)


def saveConfig(configData):
    with open(config_path, 'w') as config_file:
        json.dump(configData, config_file, indent=4)
    print("Config data saved successfully.")


# Config values
config = load_Config()
pcapiBaseUrl = pc_api_base_url
baseUrl = apiBaseUrl
apiVersion = configData["common"]["apiVersion"]
cultureCode = configData["common"]["cultureCode"]
clientId = configData["common"]["testClientId"]

# Token from runtests config
token = config["tokenApi"]["token"]
header = {"Authorization": f"Bearer {token}"}


# Load configuration data from config.json
def read():
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

# Generic method for making requests
def makeRequest(method, endpoint, data=None):
    clientId = config["common"]["testClientId"]
    url = f"{baseUrl}{endpoint}"
    print(f"\n=== {method.upper()} Request ===")
    print(f"URL: {url}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-EI-ClientId": clientId
    }
    print("Request headers:", headers)

    try:
        if method == 'post':
            response = requests.post(url, json=data, verify=False, headers=headers)
        elif method == 'get':
            response = requests.get(url, verify=False, headers=headers)
        elif method == 'put':
            response = requests.put(url, json=data, verify=False, headers=headers)
        else:
            raise ValueError("Invalid method type provided.")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        raise

    # --- Always show raw response ---
    print("\n--- Raw Response Body ---")
    print(response.text)

    # --- Try to parse JSON if possible ---
    try:
        response_data = response.json()
        print("\n--- Parsed JSON Response ---")
        print(json.dumps(response_data, indent=4))
    except json.JSONDecodeError:
        print("\n⚠️ Response body is not valid JSON")
        response_data = {}

    return response, response_data

def test_get_client_id():
    client_name = f"db{env}client"
    url = f"{pcapiBaseUrl}/api/Client/name/{client_name}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    params = {
        "cultureCode": cultureCode,
        "api-version": apiVersion
    }

    response = requests.get(url, headers=headers, params=params)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    if response.status_code == 200:
        data = response.json()
        config["common"]["testClientId"] = data.get("id")
        saveConfig(config)
        print(f"Client ID saved: {data.get('id')}")
    else:
        print(f"Failed to fetch client. Status code: {response.status_code}, Response: {response.text}")
        return None


#  Test to GET all activity types
def testGetAllActivityTypes():
    endpoint = f"/api/ActivityType?cultureCode={cultureCode}&api-version={apiVersion}"
    response, responseData = makeRequest('get', endpoint)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response}"
    # assert isinstance(responseData, list), f"Expected list, got {type(responseData).__name__}: {responseData}"
    assert isinstance(responseData, list), "Expected response to be a list of Activity Types"


# Test to GET all activity types by Id
def testGetActivityTypeById():
    activityTypeId = configData.get("activityTypeApi", {}).get("activityTypeId")
    response, _ = makeRequest('get',
                              f"/api/ActivityType/{activityTypeId}?cultureCode={cultureCode}&api-version={apiVersion}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"


# Test to GET all activity types by type
def testGetActivityTypeByType():
    activityType = configData.get("activityTypeApi", {}).get("activityType")
    response, _ = makeRequest('get',
                              f"/api/ActivityType/type/{activityType}?cultureCode={cultureCode}&api-version={apiVersion}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"


# Parameterized test for GET a specific activity type by ID
@pytest.mark.parametrize("activityTypeId, expectedStatusCode", [
    (configData.get("common", {}).get("nonExistingId"), 404),  # Non-existing ID
    (configData.get("common", {}).get("invalidId"), 404)  # Non-existing ID
])
def test_GetActivityType_ById(activityTypeId, expectedStatusCode):
    response, _ = makeRequest('get',
                              f"/api/ActivityType/{activityTypeId}?cultureCode={cultureCode}&api-version={apiVersion}")
    assert response.status_code == expectedStatusCode, f"Expected status code {expectedStatusCode}, but got {response.status_code}"


# Parameterized test for GET activity type by type
@pytest.mark.parametrize("activityType, expectedStatusCode", [
    (configData.get("common", {}).get("invalidType"), 404)  # Invalid type
])
def test_GetActivityType_ByType(activityType, expectedStatusCode):
    response, _ = makeRequest('get',
                              f"/api/ActivityType/type/{activityType}?cultureCode={cultureCode}&api-version={apiVersion}")
    assert response.status_code == expectedStatusCode, f"Expected status code {expectedStatusCode}, but got {response.status_code}"


if __name__ == "__main__":
    pytest.main()
