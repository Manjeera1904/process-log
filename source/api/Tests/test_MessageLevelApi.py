import json
import requests
import pytest
from runtests import config_path, apiBaseUrl, pc_api_base_url, env

def load_Config():
    with open(config_path) as config_file:
        return json.load(config_file)

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

# Generic method for making requests
def makeRequest(method, endpoint, data=None):
    clientId = config["common"]["testClientId"]
    url = f"{baseUrl}{endpoint}"
    print(f"{method.upper()} URL: {url}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-EI-ClientId": clientId
    }
    print("Request headers:", headers)
    try:
        if method == 'post':
            response = requests.post(url, headers=headers, json=data, verify=False)
        elif method == 'get':
            response = requests.get(url, headers=headers, verify=False)
        elif method == 'put':
            response = requests.put(url, headers=headers, json=data, verify=False)
        else:
            raise ValueError("Invalid method type provided.")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        raise


    try:
        responseData = response.json()
        print("Response body:", json.dumps(responseData, indent=4))
    except json.JSONDecodeError:
        print("Response body is not JSON:", response.text)
        responseData = {}

    return response, responseData

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


# Test to GET all message levels
def testGetAllMessageLevel():
    response, responseData = makeRequest(
        'get',
        f"/api/MessageLevel?cultureCode={cultureCode}&api-version={apiVersion}"
    )
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("API returned levels:", [item["level"] for item in responseData])  # 👈 Debug

    assert isinstance(responseData, list), "Expected response to be a list of message levels"
    returned_levels = [item["level"] for item in responseData]
    for expected in configData["messageLevelApi"]["validLevels"]:
        assert expected in returned_levels, f"Missing expected level: {expected}"

# Parametrized test: GET each message level by valid Id
@pytest.mark.parametrize("messageLevelId", [
    configData["messageLevelApi"]["infoId"],
    configData["messageLevelApi"]["statusId"],
    configData["messageLevelApi"]["warnId"],
    configData["messageLevelApi"]["errorId"],
    configData["messageLevelApi"]["fatalId"],
])
def testGetMessageLevelById(messageLevelId):
    response, responseData = makeRequest(
        'get',
        f"/api/MessageLevel/{messageLevelId}?cultureCode={cultureCode}&api-version={apiVersion}"
    )
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert responseData["id"].lower() == messageLevelId.lower()


# Parametrized test: GET each message level by valid Level
@pytest.mark.parametrize("level", configData["messageLevelApi"]["validLevels"])
def testGetMessageLevelByLevel(level):
    response, responseData = makeRequest(
        'get',
        f"/api/MessageLevel/level/{level}?cultureCode={cultureCode}&api-version={apiVersion}"
    )
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert responseData["level"].lower() == level.lower()


# Negative test: invalid IDs
@pytest.mark.parametrize("messageLevelId, expectedStatusCode", [
    (configData["common"]["nonExistingId"], 404),
    (configData["common"]["invalidId"], 404),
])
def test_GetMessageLevel_ById_Invalid(messageLevelId, expectedStatusCode):
    response, _ = makeRequest(
        'get',
        f"/api/MessageLevel/{messageLevelId}?cultureCode={cultureCode}&api-version={apiVersion}"
    )
    assert response.status_code == expectedStatusCode, \
        f"Expected status code {expectedStatusCode}, but got {response.status_code}"


@pytest.mark.parametrize("level, expectedStatusCode", [
    (configData["common"]["invalidLevel"], 404),
])
def test_GetMessageLevel_ByLevel_Invalid(level, expectedStatusCode):
    response, _ = makeRequest(
        'get',
        f"/api/MessageLevel/level/{level}?cultureCode={cultureCode}&api-version={apiVersion}"
    )
    assert response.status_code == expectedStatusCode, \
        f"Expected status code {expectedStatusCode}, but got {response.status_code}"


if __name__ == "__main__":
    pytest.main()
