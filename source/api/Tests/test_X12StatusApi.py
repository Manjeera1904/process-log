import pytest
import requests
import json
from runtests import apiBaseUrl

# Load configuration from config.json
def loadConfig():
    with open('source/api/Tests/config.json') as config_file:
        return json.load(config_file)

# Save configuration to config.json
def saveConfig(config_data):
    with open('source/api/Tests/config.json', 'w') as config_file:
        json.dump(config_data, config_file, indent=4)

# Load config at the start
config = loadConfig()
apiVersion = config['common']['apiVersion']
clientId = config['common']['testClientId']
baseurl = apiBaseUrl
getByStatusBaseUrl = f"{baseurl}/api/X12Status/status"
getByIdBaseUrl = f"{baseurl}/api/X12Status"
getBaseUrl = f"{baseurl}/api/X12Status?api-version={apiVersion}"
invalidId = config['common']['invalidId']

headers = {
    "X-EI-ClientId": clientId,
}

# Test the GETALL method
def testGetAllX12Status():
    # {{baseUrl}}/api/X12Status?api-version=1.0
    response = requests.get(getBaseUrl, headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    if response.status_code == 200:
        responceData = response.json()
        config['x12StatusApi']['id'] = responceData[0].get('id') 
        config['x12StatusApi']['status'] = responceData[0].get('status') 
        saveConfig(config)

    # Check that the response is a list
    data = response.json()
    assert isinstance(data, list), "Expected a list of data sources"

# Test the GET by ID method
def testGetX12StatusByInvalidId():
    response = requests.get(f"{getByIdBaseUrl}/{invalidId}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 404, f"Expected status code 404 for invalid ID, got {response.status_code}"

def testGetX12StatusByValidId():
    # {{baseUrl}}/api/X12Status/bc5f9d9b-a344-4251-8ed8-067840e72777?api-version=1.0
    response = requests.get(f"{getByIdBaseUrl}/{config['x12StatusApi']['id']}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200 for valid ID, got {response.status_code}"
    responceDataPost = response.json()
    assert "status" in responceDataPost, "X12Status status not found in the retrieved data for valid ID"
    assert "name" in responceDataPost, "X12Status name not found in the retrieved data for valid ID"
    assert "description" in responceDataPost, "X12Status description not found in the retrieved data for valid ID"
    assert "cultureCode" in responceDataPost, "X12Status cultureCode not found in the retrieved data for valid ID"
    assert "translationUpdatedBy" in responceDataPost, "X12Status translationUpdatedBy not found in the retrieved data for valid ID"
    assert "translationRowVersion" in responceDataPost, "X12Status translationRowVersion not found in the retrieved data for valid ID"
    assert "id" in responceDataPost, "X12Status id not found in the retrieved data for valid ID"
    assert "updatedBy" in responceDataPost, "X12Status updatedBy not found in the retrieved data for valid ID"
    assert "rowVersion" in responceDataPost, "X12Status rowVersion not found in the retrieved data for valid ID"

# Test the GET by status method
def testGetX12StatusByInvalidstatus():
    response = requests.get(f"{getByStatusBaseUrl}/{invalidId}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 404, f"Expected status code 404 for invalid ID, got {response.status_code}"

def testGetX12StatusByValidId():
    # {{baseUrl}}/api/X12Status/bc5f9d9b-a344-4251-8ed8-067840e72777?api-version=1.0
    response = requests.get(f"{getByStatusBaseUrl}/{config['x12StatusApi']['status']}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200 for valid ID, got {response.status_code}"
    responceDataPost = response.json()
    assert "status" in responceDataPost, "X12Status status not found in the retrieved data for valid ID"
    assert "name" in responceDataPost, "X12Status name not found in the retrieved data for valid ID"
    assert "description" in responceDataPost, "X12Status description not found in the retrieved data for valid ID"
    assert "cultureCode" in responceDataPost, "X12Status cultureCode not found in the retrieved data for valid ID"
    assert "translationUpdatedBy" in responceDataPost, "X12Status translationUpdatedBy not found in the retrieved data for valid ID"
    assert "translationRowVersion" in responceDataPost, "X12Status translationRowVersion not found in the retrieved data for valid ID"
    assert "id" in responceDataPost, "X12Status id not found in the retrieved data for valid ID"
    assert "updatedBy" in responceDataPost, "X12Status updatedBy not found in the retrieved data for valid ID"
    assert "rowVersion" in responceDataPost, "X12Status rowVersion not found in the retrieved data for valid ID"

if __name__ == "__main__":
    pytest.main()