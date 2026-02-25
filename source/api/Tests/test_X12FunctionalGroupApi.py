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
postBaseUrl = f"{baseurl}/api/X12FunctionalGroup?api-version={apiVersion}"
postProcessLogBaseUrl = f"{baseurl}/api/ProcessLog?api-version={apiVersion}"
postFileProcessLogBaseUrl = f"{baseurl}/api/FileProcessLog?api-version={apiVersion}"
postX12InterchangeBaseUrl = f"{baseurl}/api/X12Interchange?api-version={apiVersion}"
getAllTypeBaseUrl = f"{baseurl}/api/ActivityType?api-version={apiVersion}"
getAllStatusBaseUrl = f"{baseurl}/api/ProcessStatus?api-version={apiVersion}"
getBaseUrl = f"{baseurl}/api/X12FunctionalGroup"
getByX12InterchangeBaseUrl = f"{baseurl}/api/X12FunctionalGroup/X12Interchange"
invalidId = config['common']['invalidId']
processLogPayload = config['processLogApi']
fileProcessLogPayload = config['fileProcessLogApi']
x12InterchangePayload = config['x12InterchangeApi']
x12FunctionalGroupPayload = config['x12FunctionalGroupApi']
putBaseUrl = f"{baseurl}/api/X12FunctionalGroup"

headers = {
    "X-EI-ClientId": clientId,
}

def createprocesslog():
    response = requests.get(getAllTypeBaseUrl, headers=headers, verify=False)
    assert response.status_code == 200, f"Failed to get  type"
    if response.status_code == 200:
        responceDataType = response.json()
        config['processLogApi']['type'] = responceDataType[0].get('type') 
        saveConfig(config)
    response = requests.get(getAllStatusBaseUrl, headers=headers, verify=False)
    assert response.status_code == 200, f"Failed to get  status"
    if response.status_code == 200:
        responceDataStatus = response.json()
        config['processLogApi']['status'] = responceDataStatus[0].get('status') 
        saveConfig(config)
    payload = processLogPayload
    response = requests.post(postProcessLogBaseUrl,json=payload, headers=headers, verify=False)
    assert response.status_code == 201, f"Failed to create process log"
    if response.status_code == 201:
        responceDataPostProcessLog = response.json()
        config['fileProcessLogApi']['processLogId'] = responceDataPostProcessLog.get('id')
        saveConfig(config)
    payload = fileProcessLogPayload
    response = requests.post(postFileProcessLogBaseUrl,json=payload, headers=headers, verify=False)
    assert response.status_code == 201, f"Failed to create file process log"
    if response.status_code == 201:
        responceDataPostProcessLog = response.json()
        config['x12InterchangeApi']['fileProcessLogId'] = responceDataPostProcessLog.get('id')
        saveConfig(config)
    payload = x12InterchangePayload
    response = requests.post(postX12InterchangeBaseUrl,json=payload, headers=headers, verify=False)
    assert response.status_code == 201, f"Failed to create X12Interchage"
    if response.status_code == 201:
        responceDataPostProcessLog = response.json()
        config['x12FunctionalGroupApi']['x12InterchangeId'] = responceDataPostProcessLog.get('id')
        saveConfig(config)
    response = requests.get(postX12InterchangeBaseUrl, headers=headers, verify=False)
    assert response.status_code == 200, f"Failed to get X12 status"
    if response.status_code == 200:
        responceDataPostProcessLog = response.json()
        config['x12FunctionalGroupApi']['status'] = responceDataPostProcessLog[0].get('status')
        saveConfig(config)

createprocesslog()

# Test: Check for data type validation and length validation
@pytest.mark.parametrize("field, value, expectedStatusCode", [
    # Testing FunctionalIdentifierCode (nvarchar)
    ("functionalIdentifierCode","St",201), # Valid length, Valid datatype and not nullable
    ("functionalIdentifierCode", None, 201),  # Not null field
    ("functionalIdentifierCode", 12345, 400),  # Invalid data type (int instead of string)
    ("functionalIdentifierCode","A"*3,400), # InValid length

    # Testing ApplicationSenderCode (nvarchar)
    ("applicationSenderCode", "PlatformConfig", 201), # Valid length, Valid datatype and not nullable
    ("applicationSenderCode", None, 201),  # Not null field
    ("applicationSenderCode", True, 400),  # Invalid data type (bool instead of string)    
    ("applicationSenderCode","A"*16,400), # InValid length

    # Testing ApplicationReceiverCode (nvarchar, null allowed)
    ("applicationReceiverCode", "PlatformConfig", 201),  # Valid length, Valid datatype and not nullable
    ("applicationReceiverCode", 12345, 400),  # Invalid data type (int instead of string)
    ("applicationReceiverCode", None, 201),  # InValid, not null
    ("applicationReceiverCode","A"*16,400), # InValid length

    # Testing date (nvarchar, null allowed)
    ("date", "date", 201),  # Valid length, Valid datatype and not nullable
    ("date", 12345, 400),  # Invalid data type (int instead of string)
    ("date", None, 201),  # InValid, not null
    ("date","A"*9,400), # InValid length

    # Testing time (nvarchar, null allowed)
    ("time", "time", 201),  # Valid length, Valid datatype and not nullable
    ("time", 12345, 400),  # Invalid data type (int instead of string)
    ("time", None, 201),  # InValid, not null
    ("time","A"*9,400), # InValid length

    # Testing GroupControlNumber (nvarchar, null allowed)
    ("groupControlNumber", "time", 201),  # Valid length, Valid datatype and not nullable
    ("groupControlNumber", 12345, 400),  # Invalid data type (int instead of string)
    ("groupControlNumber", None, 201),  # InValid, not null
    ("groupControlNumber","A"*10,400), # InValid length

    # Testing ResponsibleAgencyCode (nvarchar, null allowed)
    ("responsibleAgencyCode", "st", 201),  # Valid length, Valid datatype and not nullable
    ("responsibleAgencyCode", 12345, 400),  # Invalid data type (int instead of string)
    ("responsibleAgencyCode", None, 201),  # InValid, not null
    ("responsibleAgencyCode","A"*3,400), # InValid length

    # Testing VersionReleaseIndustryIdentifierCode (nvarchar, null allowed)
    ("versionReleaseIndustryIdentifierCode", "st", 201),  # Valid length, Valid datatype and not nullable
    ("versionReleaseIndustryIdentifierCode", 12345, 400),  # Invalid data type (int instead of string)
    ("versionReleaseIndustryIdentifierCode", None, 201),  # InValid, not null
    ("versionReleaseIndustryIdentifierCode","A"*13,400), # InValid length

    # Testing updatedBy (nvarchar, not null)
    ("updatedBy", "Rahul", 201),  # Valid length, Valid datatype and not nullable
    ("updatedBy", None, 400),  # Not null field
    ("updatedBy", 12345, 400),  # Invalid data type (int instead of string)
    ("updatedBy","A"*121,400), # InValid length
])
    
#Test the POST request
def testDataTypeValidation(field, value, expectedStatusCode):
    # Copy the valid payload and modify the field under test
    payload = x12FunctionalGroupPayload.copy()
    payload[field] = value

    # {{baseUrl}}/api/X12FunctionalGroup?api-version=1.0
    response = requests.post(postBaseUrl, headers=headers, json=payload, verify=False)

    # Check the status code matches the expected result
    assert response.status_code == expectedStatusCode, f"Failed for {field} with value {value} | Expected: {expectedStatusCode}, Got: {response.status_code}"
    
    # If status is 201 (Created), extract the X12FunctionalGroupId and save it to config.json
    if response.status_code == 201:
        responceDataPost = response.json()
        config['x12FunctionalGroupApi']['X12FunctionalGroupId'] = responceDataPost.get('id')
        saveConfig(config)  # Save the updated config back to the file
        # Validate the response data
        responceDataPost = response.json()
        assert "x12InterchangeId" in responceDataPost, "X12FunctionalGroup x12InterchangeId not found in the retrieved data for valid ID"
        assert "status" in responceDataPost, "X12FunctionalGroup status not found in the retrieved data for valid ID"
        assert "functionalIdentifierCode" in responceDataPost, "X12FunctionalGroup functionalIdentifierCode not found in the retrieved data for valid ID"
        assert "applicationSenderCode" in responceDataPost, "X12FunctionalGroup applicationSenderCode not found in the retrieved data for valid ID"
        assert "applicationReceiverCode" in responceDataPost, "X12FunctionalGroup applicationReceiverCode not found in the retrieved data for valid ID"
        assert "date" in responceDataPost, "X12FunctionalGroup date not found in the retrieved data for valid ID"
        assert "time" in responceDataPost, "X12FunctionalGroup time not found in the retrieved data for valid ID"
        assert "groupControlNumber" in responceDataPost, "X12FunctionalGroup groupControlNumber not found in the retrieved data for valid ID"
        assert "responsibleAgencyCode" in responceDataPost, "X12FunctionalGroup responsibleAgencyCode not found in the retrieved data for valid ID"
        assert "versionReleaseIndustryIdentifierCode" in responceDataPost, "X12FunctionalGroup versionReleaseIndustryIdentifierCode not found in the retrieved data for valid ID"
        assert "id" in responceDataPost, "X12FunctionalGroup id not found in the retrieved data for valid ID"
        assert "updatedBy" in responceDataPost, "X12FunctionalGroup updatedBy not found in the retrieved data for valid ID"
        assert "rowVersion" in responceDataPost, "X12FunctionalGroup rowVersion not found in the retrieved data for valid ID"

# Test the GETALL method
def testGetAllX12FunctionalGroups():
    # {{baseUrl}}/api/X12FunctionalGroup?api-version=1.0
    response = requests.get(postBaseUrl, headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Check that the response is a list
    data = response.json()
    assert isinstance(data, list), "Expected a list of data sources"

# Test the GET by ID method
def testGetX12FunctionalGroupByInvalidId():
    response = requests.get(f"{getBaseUrl}/{invalidId}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 404, f"Expected status code 404 for invalid ID, got {response.status_code}"

def testGetX12FunctionalGroupByValidId():
    # {{baseUrl}}/api/X12FunctionalGroup/bc5f9d9b-a344-4251-8ed8-067840e72777?api-version=1.0
    response = requests.get(f"{getBaseUrl}/{config['x12FunctionalGroupApi']['X12FunctionalGroupId']}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200 for valid ID, got {response.status_code}"
    responceDataPost = response.json()
    assert "x12InterchangeId" in responceDataPost, "X12FunctionalGroup x12InterchangeId not found in the retrieved data for valid ID"
    assert "status" in responceDataPost, "X12FunctionalGroup status not found in the retrieved data for valid ID"
    assert "functionalIdentifierCode" in responceDataPost, "X12FunctionalGroup functionalIdentifierCode not found in the retrieved data for valid ID"
    assert "applicationSenderCode" in responceDataPost, "X12FunctionalGroup applicationSenderCode not found in the retrieved data for valid ID"
    assert "applicationReceiverCode" in responceDataPost, "X12FunctionalGroup applicationReceiverCode not found in the retrieved data for valid ID"
    assert "date" in responceDataPost, "X12FunctionalGroup date not found in the retrieved data for valid ID"
    assert "time" in responceDataPost, "X12FunctionalGroup time not found in the retrieved data for valid ID"
    assert "groupControlNumber" in responceDataPost, "X12FunctionalGroup groupControlNumber not found in the retrieved data for valid ID"
    assert "responsibleAgencyCode" in responceDataPost, "X12FunctionalGroup responsibleAgencyCode not found in the retrieved data for valid ID"
    assert "versionReleaseIndustryIdentifierCode" in responceDataPost, "X12FunctionalGroup versionReleaseIndustryIdentifierCode not found in the retrieved data for valid ID"
    assert "id" in responceDataPost, "X12FunctionalGroup id not found in the retrieved data for valid ID"
    assert "updatedBy" in responceDataPost, "X12FunctionalGroup updatedBy not found in the retrieved data for valid ID"
    assert "rowVersion" in responceDataPost, "X12FunctionalGroup rowVersion not found in the retrieved data for valid ID"

    # If status is 200 , extract the details for put and save it to config.json
    if response.status_code == 200:
        response_data = response.json()
        config['x12FunctionalGroupApi']['x12InterchangeId'] = response_data.get('x12InterchangeId')
        config['x12FunctionalGroupApi']['status'] = response_data.get('status')
        config['x12FunctionalGroupApi']['functionalIdentifierCode'] = response_data.get('functionalIdentifierCode')
        config['x12FunctionalGroupApi']['applicationSenderCode'] = response_data.get('applicationSenderCode')
        config['x12FunctionalGroupApi']['applicationReceiverCode'] = response_data.get('applicationReceiverCode')
        config['x12FunctionalGroupApi']['date'] = response_data.get('date')
        config['x12FunctionalGroupApi']['time'] = response_data.get('time')
        config['x12FunctionalGroupApi']['groupControlNumber'] = response_data.get('groupControlNumber')
        config['x12FunctionalGroupApi']['responsibleAgencyCode'] = response_data.get('responsibleAgencyCode')
        config['x12FunctionalGroupApi']['versionReleaseIndustryIdentifierCode'] = response_data.get('versionReleaseIndustryIdentifierCode')
        config['x12FunctionalGroupApi']['updatedBy'] = response_data.get('updatedBy')
        config['x12FunctionalGroupApi']['rowVersion'] = response_data.get('rowVersion')
        saveConfig(config)  # Save the updated config back to the file

def testGetX12FunctionalGroupByInvalidX12InterchangeId():
    response = requests.get(f"{getByX12InterchangeBaseUrl}/{invalidId}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 404, f"Expected status code 404 for invalid ID, got {response.status_code}"

def testGetX12FunctionalGroupByValidX12InterchangeId():
    # {{baseUrl}}/api/X12FunctionalGroup/bc5f9d9b-a344-4251-8ed8-067840e72777?api-version=1.0
    response = requests.get(f"{getByX12InterchangeBaseUrl}/{config['x12FunctionalGroupApi']['x12InterchangeId']}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200 for valid ID, got {response.status_code}"

# Test: Check for data type validation and length validation
@pytest.mark.parametrize("field, value, expectedStatusCode", [
    # Testing FunctionalIdentifierCode (nvarchar)
    ("functionalIdentifierCode","St",200), # Valid length, Valid datatype and not nullable
    ("functionalIdentifierCode", None, 200),  # Not null field
    ("functionalIdentifierCode", 12345, 400),  # Invalid data type (int instead of string)
    ("functionalIdentifierCode","A"*3,400), # InValid length

    # Testing ApplicationSenderCode (nvarchar)
    ("applicationSenderCode", "PlatformConfig", 200), # Valid length, Valid datatype and not nullable
    ("applicationSenderCode", None, 200),  # Not null field
    ("applicationSenderCode", True, 400),  # Invalid data type (bool instead of string)    
    ("applicationSenderCode","A"*16,400), # InValid length

    # Testing ApplicationReceiverCode (nvarchar, null allowed)
    ("applicationReceiverCode", "PlatformConfig", 200),  # Valid length, Valid datatype and not nullable
    ("applicationReceiverCode", 12345, 400),  # Invalid data type (int instead of string)
    ("applicationReceiverCode", None, 200),  # InValid, not null
    ("applicationReceiverCode","A"*16,400), # InValid length

    # Testing date (nvarchar, null allowed)
    ("date", "date", 200),  # Valid length, Valid datatype and not nullable
    ("date", 12345, 400),  # Invalid data type (int instead of string)
    ("date", None, 200),  # InValid, not null
    ("date","A"*9,400), # InValid length

    # Testing time (nvarchar, null allowed)
    ("time", "time", 200),  # Valid length, Valid datatype and not nullable
    ("time", 12345, 400),  # Invalid data type (int instead of string)
    ("time", None, 200),  # InValid, not null
    ("time","A"*9,400), # InValid length

    # Testing GroupControlNumber (nvarchar, null allowed)
    ("groupControlNumber", "time", 200),  # Valid length, Valid datatype and not nullable
    ("groupControlNumber", 12345, 400),  # Invalid data type (int instead of string)
    ("groupControlNumber", None, 200),  # InValid, not null
    ("groupControlNumber","A"*10,400), # InValid length

    # Testing ResponsibleAgencyCode (nvarchar, null allowed)
    ("responsibleAgencyCode", "st", 200),  # Valid length, Valid datatype and not nullable
    ("responsibleAgencyCode", 12345, 400),  # Invalid data type (int instead of string)
    ("responsibleAgencyCode", None, 200),  # InValid, not null
    ("responsibleAgencyCode","A"*3,400), # InValid length

    # Testing VersionReleaseIndustryIdentifierCode (nvarchar, null allowed)
    ("versionReleaseIndustryIdentifierCode", "st", 200),  # Valid length, Valid datatype and not nullable
    ("versionReleaseIndustryIdentifierCode", 12345, 400),  # Invalid data type (int instead of string)
    ("versionReleaseIndustryIdentifierCode", None, 200),  # InValid, not null
    ("versionReleaseIndustryIdentifierCode","A"*13,400), # InValid length

    # Testing updatedBy (nvarchar, not null)
    ("updatedBy", "Rahul", 200),  # Valid length, Valid datatype and not nullable
    ("updatedBy", None, 400),  # Not null field
    ("updatedBy", 12345, 400),  # Invalid data type (int instead of string)
    ("updatedBy","A"*121,400), # InValid length
])

#Test the PUT method
def testUpdateX12FunctionalGroup(field, value, expectedStatusCode):
    testGetX12FunctionalGroupByValidId()
    # Create the updated data from the config
    updatedData = config["x12FunctionalGroupApi"].copy()
    updatedData[field] = value
    updatedData["id"] = config['x12FunctionalGroupApi']['X12FunctionalGroupId']
    
    # {{baseUrl}}/api/X12FunctionalGroup/bc5f9d9b-a344-4251-8ed8-067840e72777?api-version=1.0
    response = requests.put(f"{putBaseUrl}/{config['x12FunctionalGroupApi']['X12FunctionalGroupId']}?api-version={apiVersion}", headers=headers, json=updatedData,verify=False)
    # Check the status code matches the expected result
    assert response.status_code == expectedStatusCode, f"Failed for {field} with value {value} | Expected: {expectedStatusCode}, Got: {response.status_code}"

    if response.status_code == 200:
        # Validate the response data
        responseDataPut = response.json()
        assert "x12InterchangeId" in responseDataPut, "X12FunctionalGroup x12InterchangeId not found in the retrieved data for valid ID"
        assert "status" in responseDataPut, "X12FunctionalGroup status not found in the retrieved data for valid ID"
        assert "functionalIdentifierCode" in responseDataPut, "X12FunctionalGroup functionalIdentifierCode not found in the retrieved data for valid ID"
        assert "applicationSenderCode" in responseDataPut, "X12FunctionalGroup applicationSenderCode not found in the retrieved data for valid ID"
        assert "applicationReceiverCode" in responseDataPut, "X12FunctionalGroup applicationReceiverCode not found in the retrieved data for valid ID"
        assert "date" in responseDataPut, "X12FunctionalGroup date not found in the retrieved data for valid ID"
        assert "time" in responseDataPut, "X12FunctionalGroup time not found in the retrieved data for valid ID"
        assert "groupControlNumber" in responseDataPut, "X12FunctionalGroup groupControlNumber not found in the retrieved data for valid ID"
        assert "responsibleAgencyCode" in responseDataPut, "X12FunctionalGroup responsibleAgencyCode not found in the retrieved data for valid ID"
        assert "versionReleaseIndustryIdentifierCode" in responseDataPut, "X12FunctionalGroup versionReleaseIndustryIdentifierCode not found in the retrieved data for valid ID"
        assert "id" in responseDataPut, "X12FunctionalGroup id not found in the retrieved data for valid ID"
        assert "updatedBy" in responseDataPut, "X12FunctionalGroup updatedBy not found in the retrieved data for valid ID"
        assert "rowVersion" in responseDataPut, "X12FunctionalGroup rowVersion not found in the retrieved data for valid ID"

if __name__ == "__main__":
    pytest.main()