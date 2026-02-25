import json
import requests
import pytest
from runtests import config_path, apiBaseUrl, pc_api_base_url

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
pcapiBaseUrl= pc_api_base_url
baseUrl = apiBaseUrl
apiVersion = configData["common"]["apiVersion"]
cultureCode = configData["common"]["cultureCode"]
clientId = configData["common"]["testClientId"]

# Token from runtests config
token = configData["tokenApi"]["token"]
header = {"Authorization": f"Bearer {token}"}

# Generic method for making requests
def makeRequest(method, endpoint, data=None):
    url = f"{baseUrl}{endpoint}"
    print(f"{method.upper()} URL: {url}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-EI-ClientId": clientId
    }
    print("Request headers:", headers)
    if method == 'post':
        response = requests.post(url, headers=headers, json=data, verify=False)
    elif method == 'get':
        response = requests.get(url, headers=headers, verify=False)
    elif method == 'put':
        response = requests.put(url, headers=headers, json=data, verify=False)
    else:
        raise ValueError("Invalid method type provided.")

    try:
        responseData = response.json()
        print("Response body:", json.dumps(responseData, indent=4))
    except json.JSONDecodeError:
        print("Response body is not JSON:", response.text)
        responseData = {}

    return response, responseData


def testGetAllProcessStatuses():
    response, responseData = makeRequest('get', f"/api/ProcessStatus?cultureCode={cultureCode}&api-version={apiVersion}")
    assert response.status_code == 200
    assert isinstance(responseData, list)
    expected_statuses = configData["processStatusApi"]["validStatuses"]
    actual_statuses = [item["status"] for item in responseData]
    for status in expected_statuses:
        assert status in actual_statuses, f"{status} not found in API response"


@pytest.mark.parametrize("processStatusId", [
    configData["processStatusApi"]["newId"],
    configData["processStatusApi"]["inProgressId"],
    configData["processStatusApi"]["pausedId"],
    configData["processStatusApi"]["completedId"],
    configData["processStatusApi"]["failedId"],
    configData["processStatusApi"]["cancelledId"],
    configData["processStatusApi"]["duplicateId"]
])
def testGetProcessStatusById(processStatusId):
    response, data = makeRequest('get', f"/api/ProcessStatus/{processStatusId}?cultureCode={cultureCode}&api-version={apiVersion}")
    assert response.status_code == 200
    assert data["id"].lower() == processStatusId.lower()


@pytest.mark.parametrize("status", configData["processStatusApi"]["validStatuses"])
def testGetProcessStatusByStatus(status):
    response, data = makeRequest('get', f"/api/ProcessStatus/status/{status}?cultureCode={cultureCode}&api-version={apiVersion}")
    assert response.status_code == 200
    assert data["status"] == status


# ---- NEGATIVE TESTS ---- #

@pytest.mark.parametrize("invalidId", [
    configData["common"].get("nonExistingId", "00000000-0000-0000-0000-000000000000"),
    configData["common"].get("invalidId", "not-a-guid")
])
def test_GetProcessStatus_ByInvalidId(invalidId):
    response, _ = makeRequest('get', f"/api/ProcessStatus/{invalidId}?cultureCode={cultureCode}&api-version={apiVersion}")
    assert response.status_code == 404


@pytest.mark.parametrize("invalidStatus", [
    configData["common"].get("invalidType", "InvalidStatus")
])
def test_GetProcessStatus_ByInvalidStatus(invalidStatus):
    response, _ = makeRequest('get', f"/api/ProcessStatus/status/{invalidStatus}?cultureCode={cultureCode}&api-version={apiVersion}")
    assert response.status_code == 404

if __name__ == "__main__":
    pytest.main()
