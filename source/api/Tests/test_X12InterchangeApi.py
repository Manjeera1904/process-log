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
baseurl = apiBaseUrl
postBaseUrl = f"{baseurl}/api/X12Interchange?api-version={apiVersion}"
clientId = config['common']['testClientId']
postProcessLogBaseUrl = f"{baseurl}/api/ProcessLog?api-version={apiVersion}"
postFileProcessLogBaseUrl = f"{baseurl}/api/FileProcessLog?api-version={apiVersion}"
postX12InterchangeBaseUrl = f"{baseurl}/api/X12Interchange?api-version={apiVersion}"
getAllTypeBaseUrl = f"{baseurl}/api/ActivityType?api-version={apiVersion}"
getAllStatusBaseUrl = f"{baseurl}/api/ProcessStatus?api-version={apiVersion}"
getBaseUrl = f"{baseurl}/api/X12Interchange"
getProcessLogBaseUrl = f"{baseurl}/api/X12Interchange/ProcessLog"
getFileProcessLogBaseUrl = f"{baseurl}/api/X12Interchange/FileProcessLog"
invalidId = config['common']['invalidId']
processLogPayload = config['processLogApi']
fileProcessLogPayload = config['fileProcessLogApi']
x12InterchangePayload = config['x12InterchangeApi']
x12FunctionalGroupPayload = config['x12InterchangeApi']
putBaseUrl = f"{baseurl}/api/X12Interchange"

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

createprocesslog()

# Test: Check for data type validation and length validation
@pytest.mark.parametrize("field, value, expectedStatusCode", [
    # Testing interchangeSenderIdQualifier (nvarchar)
    ("interchangeSenderIdQualifier","Test",201), # Valid length, Valid datatype and not nullable
    ("interchangeSenderIdQualifier", None, 201),  # Not null field
    ("interchangeSenderIdQualifier", 12345, 400),  # Invalid data type (int instead of string)
    ("interchangeSenderIdQualifier","A"*11,400), # InValid length

    # Testing interchangeSenderId (nvarchar)
    ("interchangeSenderId", "PlatformConfig", 201), # Valid length, Valid datatype and not nullable
    ("interchangeSenderId", None, 201),  # Not null field
    ("interchangeSenderId", True, 400),  # Invalid data type (bool instead of string)    
    ("interchangeSenderId","A"*16,400), # InValid length

    # Testing interchangeReceiverIdQualifier (nvarchar, null allowed)
    ("interchangeReceiverIdQualifier", "Testing", 201),  # Valid length, Valid datatype and not nullable
    ("interchangeReceiverIdQualifier", 12345, 400),  # Invalid data type (int instead of string)
    ("interchangeReceiverIdQualifier", None, 201),  # InValid, not null
    ("interchangeReceiverIdQualifier","A"*11,400), # InValid length

    # Testing interchangeReceiverId (nvarchar, null allowed)
    ("interchangeReceiverId", "Testing", 201),  # Valid length, Valid datatype and not nullable
    ("interchangeReceiverId", 12345, 400),  # Invalid data type (int instead of string)
    ("interchangeReceiverId", None, 201),  # InValid, not null
    ("interchangeReceiverId","A"*16,400), # InValid length

    # Testing interchangeDate (nvarchar, null allowed)
    ("interchangeDate", "date", 201),  # Valid length, Valid datatype and not nullable
    ("interchangeDate", 12345, 400),  # Invalid data type (int instead of string)
    ("interchangeDate", None, 201),  # InValid, not null
    ("interchangeDate","A"*7,400), # InValid length

    # Testing interchangeTime (nvarchar, null allowed)
    ("interchangeTime", "time", 201),  # Valid length, Valid datatype and not nullable
    ("interchangeTime", 12345, 400),  # Invalid data type (int instead of string)
    ("interchangeTime", None, 201),  # InValid, not null
    ("interchangeTime","A"*5,400), # InValid length

    # Testing repetitionSeparator (nvarchar, null allowed)
    ("repetitionSeparator", "test", 201),  # Valid length, Valid datatype and not nullable
    ("repetitionSeparator", 12345, 400),  # Invalid data type (int instead of string)
    ("repetitionSeparator", None, 201),  # InValid, not null
    ("repetitionSeparator","A"*5,400), # InValid length

    # Testing interchangeControlVersionNumber (nvarchar, null allowed)
    ("interchangeControlVersionNumber", "Test", 201),  # Valid length, Valid datatype and not nullable
    ("interchangeControlVersionNumber", 12345, 400),  # Invalid data type (int instead of string)
    ("interchangeControlVersionNumber", None, 201),  # InValid, not null
    ("interchangeControlVersionNumber","A"*6,400), # InValid length

    # Testing interchangeControlNumber (nvarchar, null allowed)
    ("interchangeControlNumber", "Test", 201),  # Valid length, Valid datatype and not nullable
    ("interchangeControlNumber", 12345, 400),  # Invalid data type (int instead of string)
    ("interchangeControlNumber", None, 201),  # InValid, not null
    ("interchangeControlNumber","A"*10,400), # InValid length

    # Testing acknowledgementRequested (nvarchar, null allowed)
    ("acknowledgementRequested", "s", 201),  # Valid length, Valid datatype and not nullable
    ("acknowledgementRequested", 12345, 400),  # Invalid data type (int instead of string)
    ("acknowledgementRequested", None, 201),  # InValid, not null
    ("acknowledgementRequested","A"*2,400), # InValid length

    # Testing usageIndicator (nvarchar, null allowed)
    ("usageIndicator", "s", 201),  # Valid length, Valid datatype and not nullable
    ("usageIndicator", 12345, 400),  # Invalid data type (int instead of string)
    ("usageIndicator", None, 201),  # InValid, not null
    ("usageIndicator","A"*2,400), # InValid length

    # Testing componentElementSeparator (nvarchar, null allowed)
    ("componentElementSeparator", "s", 201),  # Valid length, Valid datatype and not nullable
    ("componentElementSeparator", 12345, 400),  # Invalid data type (int instead of string)
    ("componentElementSeparator", None, 201),  # InValid, not null
    ("componentElementSeparator","A"*2,400), # InValid length

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

    # {{baseUrl}}/api/X12Interchange?api-version=1.0
    response = requests.post(postBaseUrl, headers=headers, json=payload, verify=False)

    # Check the status code matches the expected result
    assert response.status_code == expectedStatusCode, f"Failed for {field} with value {value} | Expected: {expectedStatusCode}, Got: {response.status_code}"
    
    # If status is 201 (Created), extract the X12InterchangeId and save it to config.json
    if response.status_code == 201:
        responceDataPost = response.json()
        config['x12InterchangeApi']['x12InterchangeId'] = responceDataPost.get('id')
        saveConfig(config)  # Save the updated config back to the file
        # Validate the response data
        responceDataPost = response.json()
        assert "fileProcessLogId" in responceDataPost, "X12Interchange fileProcessLogId not found in the retrieved data for valid ID"
        assert "status" in responceDataPost, "X12Interchange status not found in the retrieved data for valid ID"
        assert "interchangeSenderIdQualifier" in responceDataPost, "X12Interchange interchangeSenderIdQualifier not found in the retrieved data for valid ID"
        assert "interchangeSenderId" in responceDataPost, "X12Interchange interchangeSenderId not found in the retrieved data for valid ID"
        assert "interchangeReceiverIdQualifier" in responceDataPost, "X12Interchange interchangeReceiverIdQualifier not found in the retrieved data for valid ID"
        assert "interchangeReceiverId" in responceDataPost, "X12Interchange interchangeReceiverId not found in the retrieved data for valid ID"
        assert "interchangeDate" in responceDataPost, "X12Interchange interchangeDate not found in the retrieved data for valid ID"
        assert "interchangeTime" in responceDataPost, "X12Interchange interchangeTime not found in the retrieved data for valid ID"
        assert "repetitionSeparator" in responceDataPost, "X12Interchange repetitionSeparator not found in the retrieved data for valid ID"
        assert "interchangeControlVersionNumber" in responceDataPost, "X12Interchange interchangeControlVersionNumber not found in the retrieved data for valid ID"
        assert "interchangeControlNumber" in responceDataPost, "X12Interchange interchangeControlNumber not found in the retrieved data for valid ID"
        assert "acknowledgementRequested" in responceDataPost, "X12Interchange acknowledgementRequested not found in the retrieved data for valid ID"
        assert "usageIndicator" in responceDataPost, "X12Interchange usageIndicator not found in the retrieved data for valid ID"
        assert "componentElementSeparator" in responceDataPost, "X12Interchange componentElementSeparator not found in the retrieved data for valid ID"
        assert "id" in responceDataPost, "X12Interchange id not found in the retrieved data for valid ID"
        assert "updatedBy" in responceDataPost, "X12Interchange updatedBy not found in the retrieved data for valid ID"
        assert "rowVersion" in responceDataPost, "X12Interchange rowVersion not found in the retrieved data for valid ID"

# Test the GETALL method
def testGetAllX12Interchanges():
    # {{baseUrl}}/api/X12Interchange?api-version=1.0
    response = requests.get(postBaseUrl, headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Check that the response is a list
    data = response.json()
    assert isinstance(data, list), "Expected a list of data sources"

# Test the GET by ID method
def testGetX12InterchangeByInvalidId():
    response = requests.get(f"{getBaseUrl}/{invalidId}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 404, f"Expected status code 404 for invalid ID, got {response.status_code}"

def testGetX12InterchangeByValidId():
    # {{baseUrl}}/api/X12Interchange/bc5f9d9b-a344-4251-8ed8-067840e72777?api-version=1.0
    response = requests.get(f"{getBaseUrl}/{config['x12InterchangeApi']['x12InterchangeId']}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200 for valid ID, got {response.status_code}"
    responceDataPost = response.json()
    assert "fileProcessLogId" in responceDataPost, "X12Interchange fileProcessLogId not found in the retrieved data for valid ID"
    assert "status" in responceDataPost, "X12Interchange status not found in the retrieved data for valid ID"
    assert "interchangeSenderIdQualifier" in responceDataPost, "X12Interchange interchangeSenderIdQualifier not found in the retrieved data for valid ID"
    assert "interchangeSenderId" in responceDataPost, "X12Interchange interchangeSenderId not found in the retrieved data for valid ID"
    assert "interchangeReceiverIdQualifier" in responceDataPost, "X12Interchange interchangeReceiverIdQualifier not found in the retrieved data for valid ID"
    assert "interchangeReceiverId" in responceDataPost, "X12Interchange interchangeReceiverId not found in the retrieved data for valid ID"
    assert "interchangeDate" in responceDataPost, "X12Interchange interchangeDate not found in the retrieved data for valid ID"
    assert "interchangeTime" in responceDataPost, "X12Interchange interchangeTime not found in the retrieved data for valid ID"
    assert "repetitionSeparator" in responceDataPost, "X12Interchange repetitionSeparator not found in the retrieved data for valid ID"
    assert "interchangeControlVersionNumber" in responceDataPost, "X12Interchange interchangeControlVersionNumber not found in the retrieved data for valid ID"
    assert "interchangeControlNumber" in responceDataPost, "X12Interchange interchangeControlNumber not found in the retrieved data for valid ID"
    assert "acknowledgementRequested" in responceDataPost, "X12Interchange acknowledgementRequested not found in the retrieved data for valid ID"
    assert "usageIndicator" in responceDataPost, "X12Interchange usageIndicator not found in the retrieved data for valid ID"
    assert "componentElementSeparator" in responceDataPost, "X12Interchange componentElementSeparator not found in the retrieved data for valid ID"
    assert "id" in responceDataPost, "X12Interchange id not found in the retrieved data for valid ID"
    assert "updatedBy" in responceDataPost, "X12Interchange updatedBy not found in the retrieved data for valid ID"
    assert "rowVersion" in responceDataPost, "X12Interchange rowVersion not found in the retrieved data for valid ID"

    # If status is 200 , extract the details for put and save it to config.json
    if response.status_code == 200:
        response_data = response.json()
        config['x12InterchangeApi']['fileProcessLogId'] = response_data.get('fileProcessLogId')
        config['x12InterchangeApi']['status'] = response_data.get('status')
        config['x12InterchangeApi']['interchangeSenderIdQualifier'] = response_data.get('interchangeSenderIdQualifier')
        config['x12InterchangeApi']['interchangeSenderId'] = response_data.get('interchangeSenderId')
        config['x12InterchangeApi']['interchangeReceiverIdQualifier'] = response_data.get('interchangeReceiverIdQualifier')
        config['x12InterchangeApi']['interchangeReceiverId'] = response_data.get('interchangeReceiverId')
        config['x12InterchangeApi']['interchangeDate'] = response_data.get('interchangeDate')
        config['x12InterchangeApi']['interchangeTime'] = response_data.get('interchangeTime')
        config['x12InterchangeApi']['repetitionSeparator'] = response_data.get('repetitionSeparator')
        config['x12InterchangeApi']['interchangeControlVersionNumber'] = response_data.get('interchangeControlVersionNumber')
        config['x12InterchangeApi']['interchangeControlNumber'] = response_data.get('interchangeControlNumber')
        config['x12InterchangeApi']['acknowledgementRequested'] = response_data.get('acknowledgementRequested')
        config['x12InterchangeApi']['usageIndicator'] = response_data.get('usageIndicator')
        config['x12InterchangeApi']['componentElementSeparator'] = response_data.get('componentElementSeparator')
        config['x12InterchangeApi']['x12InterchangeId'] = response_data.get('id')
        config['x12InterchangeApi']['updatedBy'] = response_data.get('updatedBy')
        config['x12InterchangeApi']['rowVersion'] = response_data.get('rowVersion')
        saveConfig(config)  # Save the updated config back to the file

# Test the GET by ProcessLog ID method
def testGetX12InterchangeByInvalidProcessLogId():
    response = requests.get(f"{getProcessLogBaseUrl}/{invalidId}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 404, f"Expected status code 404 for invalid ID, got {response.status_code}"

def testGetX12InterchangeByValidProcessLogId():
    # {{baseUrl}}/api/X12Interchange/bc5f9d9b-a344-4251-8ed8-067840e72777?api-version=1.0
    response = requests.get(f"{getProcessLogBaseUrl}/{config['fileProcessLogApi']['processLogId']}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200 for valid ID, got {response.status_code}"

# Test the GET by File ProcessLog ID method
def testGetX12InterchangeByInvalidFileProcessLogId():
    response = requests.get(f"{getFileProcessLogBaseUrl}/{invalidId}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 404, f"Expected status code 404 for invalid ID, got {response.status_code}"

def testGetX12InterchangeByValidFileProcessLogId():
    # {{baseUrl}}/api/X12Interchange/bc5f9d9b-a344-4251-8ed8-067840e72777?api-version=1.0
    response = requests.get(f"{getFileProcessLogBaseUrl}/{config['x12InterchangeApi']['fileProcessLogId']}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200 for valid ID, got {response.status_code}"

# Test: Check for data type validation and length validation
@pytest.mark.parametrize("field, value, expectedStatusCode", [
    # Testing interchangeSenderIdQualifier (nvarchar)
    ("interchangeSenderIdQualifier","Test",200), # Valid length, Valid datatype and not nullable
    ("interchangeSenderIdQualifier", None, 200),  # Not null field
    ("interchangeSenderIdQualifier", 12345, 400),  # Invalid data type (int instead of string)
    ("interchangeSenderIdQualifier","A"*11,400), # InValid length

    # Testing interchangeSenderId (nvarchar)
    ("interchangeSenderId", "PlatformConfig", 200), # Valid length, Valid datatype and not nullable
    ("interchangeSenderId", None, 200),  # Not null field
    ("interchangeSenderId", True, 400),  # Invalid data type (bool instead of string)    
    ("interchangeSenderId","A"*16,400), # InValid length

    # Testing interchangeReceiverIdQualifier (nvarchar, null allowed)
    ("interchangeReceiverIdQualifier", "Testing", 200),  # Valid length, Valid datatype and not nullable
    ("interchangeReceiverIdQualifier", 12345, 400),  # Invalid data type (int instead of string)
    ("interchangeReceiverIdQualifier", None, 200),  # InValid, not null
    ("interchangeReceiverIdQualifier","A"*11,400), # InValid length

    # Testing interchangeReceiverId (nvarchar, null allowed)
    ("interchangeReceiverId", "Testing", 200),  # Valid length, Valid datatype and not nullable
    ("interchangeReceiverId", 12345, 400),  # Invalid data type (int instead of string)
    ("interchangeReceiverId", None, 200),  # InValid, not null
    ("interchangeReceiverId","A"*16,400), # InValid length

    # Testing interchangeDate (nvarchar, null allowed)
    ("interchangeDate", "date", 200),  # Valid length, Valid datatype and not nullable
    ("interchangeDate", 12345, 400),  # Invalid data type (int instead of string)
    ("interchangeDate", None, 200),  # InValid, not null
    ("interchangeDate","A"*7,400), # InValid length

    # Testing interchangeTime (nvarchar, null allowed)
    ("interchangeTime", "time", 200),  # Valid length, Valid datatype and not nullable
    ("interchangeTime", 12345, 400),  # Invalid data type (int instead of string)
    ("interchangeTime", None, 200),  # InValid, not null
    ("interchangeTime","A"*5,400), # InValid length

    # Testing repetitionSeparator (nvarchar, null allowed)
    ("repetitionSeparator", "test", 200),  # Valid length, Valid datatype and not nullable
    ("repetitionSeparator", 12345, 400),  # Invalid data type (int instead of string)
    ("repetitionSeparator", None, 200),  # InValid, not null
    ("repetitionSeparator","A"*5,400), # InValid length

    # Testing interchangeControlVersionNumber (nvarchar, null allowed)
    ("interchangeControlVersionNumber", "Test", 200),  # Valid length, Valid datatype and not nullable
    ("interchangeControlVersionNumber", 12345, 400),  # Invalid data type (int instead of string)
    ("interchangeControlVersionNumber", None, 200),  # InValid, not null
    ("interchangeControlVersionNumber","A"*6,400), # InValid length

    # Testing interchangeControlNumber (nvarchar, null allowed)
    ("interchangeControlNumber", "Test", 200),  # Valid length, Valid datatype and not nullable
    ("interchangeControlNumber", 12345, 400),  # Invalid data type (int instead of string)
    ("interchangeControlNumber", None, 200),  # InValid, not null
    ("interchangeControlNumber","A"*10,400), # InValid length

    # Testing acknowledgementRequested (nvarchar, null allowed)
    ("acknowledgementRequested", "s", 200),  # Valid length, Valid datatype and not nullable
    ("acknowledgementRequested", 12345, 400),  # Invalid data type (int instead of string)
    ("acknowledgementRequested", None, 200),  # InValid, not null
    ("acknowledgementRequested","A"*2,400), # InValid length

    # Testing usageIndicator (nvarchar, null allowed)
    ("usageIndicator", "s", 200),  # Valid length, Valid datatype and not nullable
    ("usageIndicator", 12345, 400),  # Invalid data type (int instead of string)
    ("usageIndicator", None, 200),  # InValid, not null
    ("usageIndicator","A"*2,400), # InValid length

    # Testing componentElementSeparator (nvarchar, null allowed)
    ("componentElementSeparator", "s", 200),  # Valid length, Valid datatype and not nullable
    ("componentElementSeparator", 12345, 400),  # Invalid data type (int instead of string)
    ("componentElementSeparator", None, 200),  # InValid, not null
    ("componentElementSeparator","A"*2,400), # InValid length

    # Testing updatedBy (nvarchar, not null)
    ("updatedBy", "Rahul", 200),  # Valid length, Valid datatype and not nullable
    ("updatedBy", None, 400),  # Not null field
    ("updatedBy", 12345, 400),  # Invalid data type (int instead of string)
    ("updatedBy","A"*121,400), # InValid length
])

#Test the PUT method
def testUpdateX12Interchange(field, value, expectedStatusCode):
    testGetX12InterchangeByValidId()
    # Create the updated data from the config
    updatedData = config["x12InterchangeApi"].copy()
    updatedData[field] = value
    updatedData["id"] = config['x12InterchangeApi']['x12InterchangeId']
    
    # {{baseUrl}}/api/X12Interchange/bc5f9d9b-a344-4251-8ed8-067840e72777?api-version=1.0
    response = requests.put(f"{putBaseUrl}/{config['x12InterchangeApi']['x12InterchangeId']}?api-version={apiVersion}", headers=headers, json=updatedData,verify=False)
    # Check the status code matches the expected result
    assert response.status_code == expectedStatusCode, f"Failed for {field} with value {value} | Expected: {expectedStatusCode}, Got: {response.status_code}"

    if response.status_code == 200:
        # Validate the response data
        responseDataPut = response.json()
        assert "fileProcessLogId" in responseDataPut, "X12Interchange fileProcessLogId not found in the retrieved data for valid ID"
        assert "status" in responseDataPut, "X12Interchange status not found in the retrieved data for valid ID"
        assert "interchangeSenderIdQualifier" in responseDataPut, "X12Interchange interchangeSenderIdQualifier not found in the retrieved data for valid ID"
        assert "interchangeSenderId" in responseDataPut, "X12Interchange interchangeSenderId not found in the retrieved data for valid ID"
        assert "interchangeReceiverIdQualifier" in responseDataPut, "X12Interchange interchangeReceiverIdQualifier not found in the retrieved data for valid ID"
        assert "interchangeReceiverId" in responseDataPut, "X12Interchange interchangeReceiverId not found in the retrieved data for valid ID"
        assert "interchangeDate" in responseDataPut, "X12Interchange interchangeDate not found in the retrieved data for valid ID"
        assert "interchangeTime" in responseDataPut, "X12Interchange interchangeTime not found in the retrieved data for valid ID"
        assert "repetitionSeparator" in responseDataPut, "X12Interchange repetitionSeparator not found in the retrieved data for valid ID"
        assert "interchangeControlVersionNumber" in responseDataPut, "X12Interchange interchangeControlVersionNumber not found in the retrieved data for valid ID"
        assert "interchangeControlNumber" in responseDataPut, "X12Interchange interchangeControlNumber not found in the retrieved data for valid ID"
        assert "acknowledgementRequested" in responseDataPut, "X12Interchange acknowledgementRequested not found in the retrieved data for valid ID"
        assert "usageIndicator" in responseDataPut, "X12Interchange usageIndicator not found in the retrieved data for valid ID"
        assert "componentElementSeparator" in responseDataPut, "X12Interchange componentElementSeparator not found in the retrieved data for valid ID"
        assert "id" in responseDataPut, "X12Interchange id not found in the retrieved data for valid ID"
        assert "updatedBy" in responseDataPut, "X12Interchange updatedBy not found in the retrieved data for valid ID"
        assert "rowVersion" in responseDataPut, "X12Interchange rowVersion not found in the retrieved data for valid ID"

if __name__ == "__main__":
    pytest.main()