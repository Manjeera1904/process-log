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
postBaseUrl = f"{baseurl}/api/X12Message?api-version={apiVersion}"
postProcessLogBaseUrl = f"{baseurl}/api/ProcessLog?api-version={apiVersion}"
postFileProcessLogBaseUrl = f"{baseurl}/api/FileProcessLog?api-version={apiVersion}"
postX12InterchangeBaseUrl = f"{baseurl}/api/X12Interchange?api-version={apiVersion}"
postX12StatusBaseUrl = f"{baseurl}/api/X12Status?api-version={apiVersion}"
postX12MessageLevelBaseUrl = f"{baseurl}/api/MessageLevel?api-version={apiVersion}"
postX12FunctionalGroupBaseUrl = f"{baseurl}/api/X12FunctionalGroup?api-version={apiVersion}"
postX12TransactionSetBaseUrl = f"{baseurl}/api/X12TransactionSet?api-version={apiVersion}"
getAllTypeBaseUrl = f"{baseurl}/api/ActivityType?api-version={apiVersion}"
getAllStatusBaseUrl = f"{baseurl}/api/ProcessStatus?api-version={apiVersion}"
getBaseUrl = f"{baseurl}/api/X12Message"
getByX12InterchangeBaseUrl = f"{baseurl}/api/X12Message/X12Interchange"
getByX12FunctionalGroupBaseUrl = f"{baseurl}/api/X12Message/X12FunctionalGroup"
getByX12TransactionSetBaseUrl = f"{baseurl}/api/X12Message/X12TransactionSet"
invalidId = config['common']['invalidId']
processLogPayload = config['processLogApi']
fileProcessLogPayload = config['fileProcessLogApi']
x12InterchangePayload = config['x12InterchangeApi']
x12FunctionalGroupPayload = config['x12FunctionalGroupApi']
x12TransactionSetPayload = config['x12TransactionSetApi']
x12MessagePayload = config['x12MessageApi']
putBaseUrl = f"{baseurl}/api/X12Message"

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
        config['x12MessageApi']['x12InterchangeId'] = responceDataPostProcessLog.get('id')
        saveConfig(config)
    response = requests.get(postX12StatusBaseUrl, headers=headers, verify=False)
    assert response.status_code == 200, f"Failed to get X12 status"
    if response.status_code == 200:
        responceDataPostProcessLog = response.json()
        config['x12FunctionalGroupApi']['status'] = responceDataPostProcessLog[0].get('status')
        saveConfig(config)
    payload = x12FunctionalGroupPayload
    response = requests.post(postX12FunctionalGroupBaseUrl, headers=headers, json=payload, verify=False)
    assert response.status_code == 201, f"Failed to create X12Functional Group"
    if response.status_code == 201:
        responceDataPostProcessLog = response.json()
        config['x12MessageApi']['x12FunctionalGroupId'] = responceDataPostProcessLog.get('id')
        saveConfig(config)
    response = requests.get(postX12MessageLevelBaseUrl, headers=headers, verify=False)
    assert response.status_code == 200, f"Failed to get X12 Message level"
    if response.status_code == 200:
        responceDataPostProcessLog = response.json()
        config['x12MessageApi']['level'] = responceDataPostProcessLog[0].get('level')
        saveConfig(config)
    payload = x12TransactionSetPayload
    response = requests.post(postX12TransactionSetBaseUrl, headers=headers, json=payload, verify=False)
    assert response.status_code == 201, f"Failed to create X12 TransactionSet"
    if response.status_code == 201:
        responceDataPostProcessLog = response.json()
        config['x12MessageApi']['x12TransactionSetId'] = responceDataPostProcessLog.get('id')
        saveConfig(config)

createprocesslog()

# Test: Check for data type validation and length validation
@pytest.mark.parametrize("field, value, expectedStatusCode", [
    # Testing Message (nvarchar)
    ("message","Testing",201), # Valid length, Valid datatype and not nullable
    ("message", None, 400),  # Not null field
    ("message", 12345, 400),  # Invalid data type (int instead of string)

    # Testing X12Status (nvarchar, null allowed)
    ("level", 12345, 400),  # Invalid data type (int instead of string)
    ("level", None, 400),  # InValid, not null
    ("level","A"*51,400), # InValid length

    # Testing updatedBy (nvarchar, not null)
    ("updatedBy", "Rahul", 201),  # Valid length, Valid datatype and not nullable
    ("updatedBy", None, 400),  # Not null field
    ("updatedBy", 12345, 400),  # Invalid data type (int instead of string)
    ("updatedBy","A"*121,400), # InValid length
])
    
#Test the POST request
def testDataTypeValidation(field, value, expectedStatusCode):
    # Copy the valid payload and modify the field under test
    payload = x12MessagePayload.copy()
    payload[field] = value

    # {{baseUrl}}/api/X12Message?api-version=1.0
    response = requests.post(postBaseUrl, headers=headers, json=payload, verify=False)

    # Check the status code matches the expected result
    assert response.status_code == expectedStatusCode, f"Failed for {field} with value {value} | Expected: {expectedStatusCode}, Got: {response.status_code}"
    
    # If status is 201 (Created), extract the X12MessageId and save it to config.json
    if response.status_code == 201:
        responceDataPost = response.json()
        config['x12MessageApi']['x12MessageId'] = responceDataPost.get('id')
        saveConfig(config)  # Save the updated config back to the file
        # Validate the response data
        responceDataPost = response.json()
        assert "x12InterchangeId" in responceDataPost, "X12Message x12InterchangeId not found in the retrieved data for valid ID"
        assert "x12FunctionalGroupId" in responceDataPost, "X12Message x12FunctionalGroupId not found in the retrieved data for valid ID"
        assert "x12TransactionSetId" in responceDataPost, "X12Message x12TransactionSetId not found in the retrieved data for valid ID"
        assert "level" in responceDataPost, "X12Message level not found in the retrieved data for valid ID"
        assert "message" in responceDataPost, "X12Message message not found in the retrieved data for valid ID"
        assert "messageTimestamp" in responceDataPost, "X12Message messageTimestamp not found in the retrieved data for valid ID"
        assert "id" in responceDataPost, "X12Message id not found in the retrieved data for valid ID"
        assert "updatedBy" in responceDataPost, "X12Message updatedBy not found in the retrieved data for valid ID"
        assert "rowVersion" in responceDataPost, "X12Message rowVersion not found in the retrieved data for valid ID"

# Test the GETALL method
def testGetAllX12Messages():
    # {{baseUrl}}/api/X12Message?api-version=1.0
    response = requests.get(postBaseUrl, headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Check that the response is a list
    data = response.json()
    assert isinstance(data, list), "Expected a list of data sources"

# Test the GET by ID method
def testGetX12MessageByInvalidId():
    response = requests.get(f"{getBaseUrl}/{invalidId}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 404, f"Expected status code 404 for invalid ID, got {response.status_code}"

def testGetX12MessageByValidId():
    # {{baseUrl}}/api/X12Message/bc5f9d9b-a344-4251-8ed8-067840e72777?api-version=1.0
    response = requests.get(f"{getBaseUrl}/{config['x12MessageApi']['x12MessageId']}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200 for valid ID, got {response.status_code}"
    responceDataPost = response.json()
    assert "x12InterchangeId" in responceDataPost, "X12Message x12InterchangeId not found in the retrieved data for valid ID"
    assert "x12FunctionalGroupId" in responceDataPost, "X12Message x12FunctionalGroupId not found in the retrieved data for valid ID"
    assert "x12TransactionSetId" in responceDataPost, "X12Message x12TransactionSetId not found in the retrieved data for valid ID"
    assert "level" in responceDataPost, "X12Message level not found in the retrieved data for valid ID"
    assert "message" in responceDataPost, "X12Message message not found in the retrieved data for valid ID"
    assert "messageTimestamp" in responceDataPost, "X12Message messageTimestamp not found in the retrieved data for valid ID"
    assert "id" in responceDataPost, "X12Message id not found in the retrieved data for valid ID"
    assert "updatedBy" in responceDataPost, "X12Message updatedBy not found in the retrieved data for valid ID"
    assert "rowVersion" in responceDataPost, "X12Message rowVersion not found in the retrieved data for valid ID"

#     # If status is 200 , extract the details for put and save it to config.json
#     if response.status_code == 200:
#         response_data = response.json()
#         config['x12MessageApi']['x12FunctionalGroupId'] = response_data.get('x12FunctionalGroupId')
#         config['x12MessageApi']['status'] = response_data.get('status')
#         config['x12MessageApi']['transactionSetIdentifierCode'] = response_data.get('transactionSetIdentifierCode')
#         config['x12MessageApi']['transactionSetControlNumber'] = response_data.get('transactionSetControlNumber')
#         config['x12MessageApi']['X12MessageId'] = response_data.get('id')
#         config['x12MessageApi']['updatedBy'] = response_data.get('updatedBy')
#         config['x12MessageApi']['rowVersion'] = response_data.get('rowVersion')
#         saveConfig(config)  # Save the updated config back to the file

def testGetX12MessageByInvalidX12InterchangeId():
    response = requests.get(f"{getByX12InterchangeBaseUrl}/{invalidId}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 404, f"Expected status code 404 for invalid ID, got {response.status_code}"

def testGetX12MessageByValidX12InterchangeId():
    # {{baseUrl}}/api/X12Message/bc5f9d9b-a344-4251-8ed8-067840e72777?api-version=1.0
    response = requests.get(f"{getByX12InterchangeBaseUrl}/{config['x12MessageApi']['x12InterchangeId']}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200 for valid ID, got {response.status_code}"

def testGetX12MessageByInvalidX12FunctionalGroupId():
    response = requests.get(f"{getByX12FunctionalGroupBaseUrl}/{invalidId}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 404, f"Expected status code 404 for invalid ID, got {response.status_code}"

def testGetX12MessageByValidX12FunctionalGroupId():
    # {{baseUrl}}/api/X12Message/bc5f9d9b-a344-4251-8ed8-067840e72777?api-version=1.0
    response = requests.get(f"{getByX12FunctionalGroupBaseUrl}/{config['x12MessageApi']['x12FunctionalGroupId']}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200 for valid ID, got {response.status_code}"

def testGetX12MessageByInvalidX12TransactionSetId():
    response = requests.get(f"{getByX12TransactionSetBaseUrl}/{invalidId}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 404, f"Expected status code 404 for invalid ID, got {response.status_code}"

def testGetX12MessageByValidX12TransactionSetId():
    # {{baseUrl}}/api/X12Message/bc5f9d9b-a344-4251-8ed8-067840e72777?api-version=1.0
    response = requests.get(f"{getByX12TransactionSetBaseUrl}/{config['x12MessageApi']['x12TransactionSetId']}?api-version={apiVersion}", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200 for valid ID, got {response.status_code}"

# # Test: Check for data type validation and length validation
# @pytest.mark.parametrize("field, value, expectedStatusCode", [
#     # Testing TransactionSetIdentifierCode (nvarchar)
#     ("transactionSetIdentifierCode","St",200), # Valid length, Valid datatype and not nullable
#     ("transactionSetIdentifierCode", None, 400),  # Not null field
#     ("transactionSetIdentifierCode", 12345, 400),  # Invalid data type (int instead of string)
#     ("transactionSetIdentifierCode","A"*4,400), # InValid length

#     # Testing transactionSetControlNumber (nvarchar)
#     ("transactionSetControlNumber", "Testing", 200), # Valid length, Valid datatype and not nullable
#     ("transactionSetControlNumber", None, 400),  # Not null field
#     ("transactionSetControlNumber", True, 400),  # Invalid data type (bool instead of string)    
#     ("transactionSetControlNumber","A"*10,400), # InValid length

#     # Testing X12Status (nvarchar, null allowed)
#     ("status", 12345, 400),  # Invalid data type (int instead of string)
#     ("status", None, 400),  # InValid, not null
#     ("status","A"*51,400), # InValid length

#     # Testing updatedBy (nvarchar, not null)
#     ("updatedBy", "Rahul", 200),  # Valid length, Valid datatype and not nullable
#     ("updatedBy", None, 400),  # Not null field
#     ("updatedBy", 12345, 400),  # Invalid data type (int instead of string)
#     ("updatedBy","A"*121,400), # InValid length
# ])

# #Test the PUT method
# def testUpdateX12Message(field, value, expectedStatusCode):
#     testGetX12MessageByValidId()
#     # Create the updated data from the config
#     updatedData = config["x12MessageApi"].copy()
#     updatedData[field] = value
#     updatedData["id"] = config['x12MessageApi']['X12MessageId']
    
#     # {{baseUrl}}/api/X12Message/bc5f9d9b-a344-4251-8ed8-067840e72777?api-version=1.0
#     response = requests.put(f"{putBaseUrl}/{config['x12MessageApi']['X12MessageId']}?api-version={apiVersion}", headers=headers, json=updatedData,verify=False)
#     # Check the status code matches the expected result
#     assert response.status_code == expectedStatusCode, f"Failed for {field} with value {value} | Expected: {expectedStatusCode}, Got: {response.status_code}"

#     if response.status_code == 200:
#         # Validate the response data
#         responseDataPut = response.json()
#         assert "x12FunctionalGroupId" in responseDataPut, "X12Message x12FunctionalGroupId not found in the retrieved data for valid ID"
#         assert "status" in responseDataPut, "X12Message status not found in the retrieved data for valid ID"
#         assert "transactionSetIdentifierCode" in responseDataPut, "X12Message transactionSetIdentifierCode not found in the retrieved data for valid ID"
#         assert "transactionSetControlNumber" in responseDataPut, "X12Message transactionSetControlNumber not found in the retrieved data for valid ID"
#         assert "id" in responseDataPut, "X12Message id not found in the retrieved data for valid ID"
#         assert "updatedBy" in responseDataPut, "X12Message updatedBy not found in the retrieved data for valid ID"
#         assert "rowVersion" in responseDataPut, "X12Message rowVersion not found in the retrieved data for valid ID"

if __name__ == "__main__":
    pytest.main()