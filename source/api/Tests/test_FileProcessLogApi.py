import json
import re
import uuid
import requests
import pytest
from runtests import config_path, apiBaseUrl, pc_api_base_url,env

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
pcapiBaseUrl= pc_api_base_url
baseUrl = apiBaseUrl
apiVersion = configData["common"]["apiVersion"]
apiVersion2 = configData["common"]["apiVersion2"]
cultureCode = configData["common"]["cultureCode"]
clientId = configData["common"]["testClientId"]
 
# Token from runtests config
token = config["tokenApi"]["token"]
header = {"Authorization": f"Bearer {token}"}
 
# Load configuration data from config.json
def read():
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)
 
# Get ActivityType and ProcessStatus from config.json
activityType = configData.get('activityTypeApi', {}).get('activityType')
processStatus = configData.get('processStatusApi', {}).get('status')


# Prepare processLog data, including the activityType and processStatus
processLog_post_data = configData.get('processLogApi')
processLog_post_data['type'] = activityType
processLog_post_data['status'] = processStatus

# Get fileProcessLogApi and processLogApi values from config.json
fileProcessLogData = configData.get('fileProcessLogApi', {})
processLogId = configData.get('processLogApi', {}).get('processLogId')


# Update the fileProcessLog data with necessary fields
fileProcessLogData['processLogId'] = processLogId
fileProcessLogData['fileProcessLogId'] = fileProcessLogData.get('fileProcessLogId')
fileProcessLogData['updatedBy'] = fileProcessLogData.get('updatedBy')

fileProcessLogDatav2 = configData.get('fileProcessLogApiv2', {})
processLogId = configData.get('processLogApi', {}).get('processLogId')
fileProcessLogDatav2['processLogId'] = processLogId
fileProcessLogDatav2['fileProcessLogId'] = fileProcessLogDatav2.get('fileProcessLogId')
fileProcessLogDatav2['updatedBy'] = fileProcessLogDatav2.get('updatedBy')

# Fetch startTimeStamp and lastUpdatedTimeStamp from config.json, or generate them if not present
start_timestamp = configData.get('processLogApi', {}).get('startTimeStamp')
last_updated_timestamp = configData.get('processLogApi', {}).get('lastUpdatedTimeStamp')

# If timestamps are missing, generate them
if not start_timestamp:
    start_timestamp = datetime.datetime.now().isoformat() + 'Z'
    processLog_post_data['startTimeStamp'] = start_timestamp

if not last_updated_timestamp:
    last_updated_timestamp = datetime.datetime.now().isoformat() + 'Z'
    processLog_post_data['lastUpdatedTimeStamp'] = last_updated_timestamp

print("processLog POST data:", processLog_post_data)
 

 
# Generic method for making requests
def makeRequest(method, endpoint, data=None):
    config  = load_Config()
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
        "api-version": apiVersion,
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
 
# Save processLogId to config.json
def saveProcessLogId(processLog_Id, processLog_Idv2):
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)
 
    configData['fileProcessLogApi']['processLogId'] = processLog_Id
    configData['fileProcessLogApiv2']['processLogId'] = processLog_Idv2
 
    with open(config_path, 'w') as configFile:
        json.dump(configData, configFile, indent=4)
 
    print(f"'processLogId' saved in config.json under fileProcessLogApi: {processLog_Id}")
    print(f"'processLogId' saved in config.json under fileProcessLogApiv2: {processLog_Idv2}")
 
 
# Save fileProcessLogId to config.json
def saveFileProcessLogId(fileProcessLogId):
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)
    configData['fileProcessLogApi']['fileProcessLogId'] = fileProcessLogId
    # Write the updated data back to the file
    with open(config_path, 'w') as configFile:
        json.dump(configData, configFile, indent=4)
    print(f"'fileProcessLogId' saved in config.json under fileProcessLogApi: {fileProcessLogId}")

def saveFileProcessLogIdv2(fileProcessLogId):
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)
    configData['fileProcessLogApiv2']['fileProcessLogId'] = fileProcessLogId
    # Write the updated data back to the file
    with open(config_path, 'w') as configFile:
        json.dump(configData, configFile, indent=4)
    print(f"'fileProcessLogId' saved in config.json under fileProcessLogApiv2: {fileProcessLogId}")
 
# Field validation function
def validateFields(responseData, fieldValidations):
    for field, fieldType, *length in fieldValidations:
        fieldValue = responseData.get(field)
 
        if field == 'id':
            try:
                uuid.UUID(fieldValue)
            except ValueError:
                raise TypeError(f"Field '{field}' is not a valid UUID.")
        elif field == 'rowVersion':
            pattern = r'^[A-Za-z0-9+/]+={0,2}$'
            if not re.match(pattern, fieldValue or ''):
                raise ValueError(f"Field '{field}' is not in the correct format.")
        else:
            if not isinstance(fieldValue, fieldType):
                raise TypeError(f"Field '{field}' must be of type {fieldType}.")
           
 
def testPostRequest():
    print("\n--- Executing POST ProcessLog ---")
    print("POST payload:")
    print(json.dumps(processLog_post_data, indent=4))
 
    # Send POST request
    response, response_data = makeRequest(
        'post',
        f"/api/ProcessLog?api-version={apiVersion}",
        processLog_post_data
    )
 
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(json.dumps(response_data, indent=4))
 
    # Assert creation success
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
 
    # Save processLogId
    processLog_Id = response_data.get('id')
    
    # Send POST request
    response, response_data = makeRequest(
        'post',
        f"/api/ProcessLog?api-version={apiVersion}",
        processLog_post_data
    )
 
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(json.dumps(response_data, indent=4))
 
    # Assert creation success
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    

    processLog_Idv2 = response_data.get('id')
    assert processLog_Id, "No 'id' found in the response for the new process log."
    assert processLog_Idv2, "No 'id' found in the response for the new process log."
    saveProcessLogId(processLog_Id, processLog_Idv2)


 
    # --- 🔍 Verify data was actually stored ---
    get_response, get_data = makeRequest(
        'get',
        f"/api/ProcessLog/{processLog_Id}?api-version={apiVersion}"
    )
 
    print("Fetched Data (GET after POST):")
    print(json.dumps(get_data, indent=4))
 
    assert get_response.status_code == 200, f"Expected 200, got {get_response.status_code}"
 
# Test to POST a new fileProcessLog entry
def testPostFileProcessLog():

    configData = load_Config()
    fileProcessLogData = configData.get('fileProcessLogApi', {})
 
    processLogId = configData.get('fileProcessLogApi', {}).get('processLogId')
 
 
    # Update the fileProcessLog data with necessary fields
    fileProcessLogData['processLogId'] = processLogId
    fileProcessLogData['fileProcessLogId'] = fileProcessLogData.get('fileProcessLogId')
    fileProcessLogData['updatedBy'] = fileProcessLogData.get('updatedBy')

    response, responseData = makeRequest('post', f"/api/FileProcessLog?api-version={apiVersion}", fileProcessLogData)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
 
    if 'id' in responseData:
        # Save the ID immediately after confirming it was created successfully
        saveFileProcessLogId(responseData['id'])
 
    # Field validation
    fieldValidations = [
        ('id', uuid.UUID),            # UUID for the file process log ID
        ('updatedBy', str),           # UpdatedBy field should be a string
        ('rowVersion', str),          # rowVersion should be a string
        ('fileName', str),            # File name
        ('filePath', str),            # File path
        ('fileSize', int),            # File size in bytes
        ('fileHash', str),            # Hash of the file content
        ('processLogId', str),        # Process log ID should be a string
    ]
    validateFields(responseData, fieldValidations)
 
# # Test to GET all fileProcessLog entries
def testGetAllFileProcessLogs():
    response, responseData = makeRequest('get', f"/api/FileProcessLog?api-version={apiVersion}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert isinstance(responseData, list), "Expected response to be a list of fileProcessLog entries"
 
 
def testGetFileProcessLogById():
    # Load the configuration to get the fileProcessLogId
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)
    file_process_log_id = configData.get("fileProcessLogApi", {}).get('fileProcessLogId')
    assert file_process_log_id, "fileProcessLogId not found in config.json"
    print(f"Using fileProcessLog ID: {file_process_log_id}")
 
    # Make the GET request
    response, response_data = makeRequest('get', f"/api/FileProcessLog/{file_process_log_id}?api-version={apiVersion}")
 
    # Check if the response status is 200 (OK)
    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code} and response: {response.text}"
    )
 
    # Check if response data is a JSON object with expected keys
    expected_keys = ["id", "updatedBy", "rowVersion", "processLogId", "fileName", "filePath", "fileSize", "fileHash"]
    for key in expected_keys:
        assert key in response_data, f"Expected key '{key}' in response, but it was missing."
 
    # Additional validation for each field based on FileProcessLogV1 model requirements
    assert isinstance(response_data["id"], str) or response_data["id"] is None, "id should be a string or None"
    assert isinstance(response_data["updatedBy"], str) or response_data[
        "updatedBy"] is None, "updatedBy should be a string or None"
    assert isinstance(response_data["rowVersion"], str) or response_data[
        "rowVersion"] is None, "rowVersion should be a string or None"
    assert isinstance(response_data["processLogId"], str), "processLogId should be a string (UUID format)"
    assert isinstance(response_data["fileName"], str) and 1 <= len(
        response_data["fileName"]) <= 1000, "fileName should be a string with length between 1 and 1000"
    assert isinstance(response_data["filePath"], str) and 1 <= len(
        response_data["filePath"]) <= 1000, "filePath should be a string with length between 1 and 1000"
    assert isinstance(response_data["fileSize"], int) or response_data[
        "fileSize"] is None, "fileSize should be an integer or None"
    assert isinstance(response_data["fileHash"], str) or response_data[
        "fileHash"] is None, "fileHash should be a string or None"
 
def testGetProcessLogById():
    configData = load_Config()
    # Load the configuration to get the processLogId
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)
    process_log_id = configData.get("fileProcessLogApi", {}).get('processLogId')
    assert process_log_id, "processLogId not found in config.json"
    print(f"Using processLog ID: {process_log_id}")
 
    # Make the GET request
    response, response_data = makeRequest('get', f"/api/FileProcessLog/ProcessLog/{process_log_id}?api-version={apiVersion}")
 
    # Check if the response status is 200 (OK)
    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code} and response: {response.text}"
    )
 
    # Ensure response data is a list
    assert isinstance(response_data, list), f"Expected response data to be a list, but got {type(response_data)}"
 
    # Define the expected keys based on the FileProcessLogV1 model
    expected_keys = ["id", "updatedBy", "rowVersion", "processLogId", "fileName", "filePath", "fileSize", "fileHash"]
 
    # Iterate over each item in the response data and validate keys and field types
    for item in response_data:
        for key in expected_keys:
            assert key in item, f"Expected key '{key}' in response item, but it was missing."
 
        # Additional validation for each field based on FileProcessLogV1 model requirements
        assert isinstance(item["id"], str) or item["id"] is None, "id should be a string or None"
        assert isinstance(item["updatedBy"], str) or item["updatedBy"] is None, "updatedBy should be a string or None"
        assert isinstance(item["rowVersion"], str) or item["rowVersion"] is None, "rowVersion should be a string or None"
        assert isinstance(item["processLogId"], str), "processLogId should be a string (UUID format)"
        assert isinstance(item["fileName"], str) and 1 <= len(item["fileName"]) <= 1000, "fileName should be a string with length between 1 and 1000"
        assert isinstance(item["filePath"], str) and 1 <= len(item["filePath"]) <= 1000, "filePath should be a string with length between 1 and 1000"
        assert isinstance(item["fileSize"], int) or item["fileSize"] is None, "fileSize should be an integer or None"
        assert isinstance(item["fileHash"], str) or item["fileHash"] is None, "fileHash should be a string or None"
 
@pytest.mark.parametrize("invalid_data", [
    # Test cases for 'id'
    {"id": "invalid-uuid"},
    {"id": ""},
    {"id": 123434},
 
    # Test cases for 'updatedBy'
    {"updatedBy": "a" * 121},
    {"updatedBy": 1231},
 
    # Test cases for 'rowVersion'
    {"rowVersion": 12343},
    {"rowVersion": "!!@qeq"},
 
    # Test cases for 'processLogId'
    {"processLogId": "invalid-uuid"},
    {"processLogId": ""},
    {"processLogId": 123434},
 
    # Test cases for 'fileName'
    {"fileName": ""},
    {"fileName": "a" * 1001},
    {"fileName": 1234},
    {"fileName": None},
 
    # Test cases for 'filePath'
    {"filePath": ""},
    {"filePath": "a" * 1001},
    {"filePath": 1234},
    {"filePath": None},
 
    # Test cases for 'fileSize'
    {"fileSize": "not-a-number"},
    {"fileSize": "-99ab"},
    {"fileSize": 2**31},
 
    # Test cases for 'fileHash'
    {"fileHash": "a" * 501},
    {"fileHash": 1234},
    {"fileHash": -1}
])
def testPostInvalidFileProcessLogData(invalid_data):
    data_to_send = fileProcessLogData.copy()  # Use the existing valid data
    data_to_send.update(invalid_data)
    response, response_data = makeRequest('post', f"/api/FileProcessLog?api-version={apiVersion}", data_to_send)
 
    # Check if the response status is 400 (Bad Request) for invalid inputs
    assert response.status_code == 400, f"Expected 400 Bad Request for invalid data: {invalid_data}, but got: {response.status_code}"
 
# Test to update a FileProcessLog
def testPutFileProcessLog():
    # Load the latest config data to get the updated fileProcessLogId
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile) # Load the updated config data
    file_process_log_id = configData.get("fileProcessLogApi", {}).get('fileProcessLogId')
    assert file_process_log_id, "fileProcessLogId not found in config.json"
 
    # Fetch current FileProcessLog data
    _, current_file_process_log_data = makeRequest('get',
                                                   f"/api/FileProcessLog/{file_process_log_id}?api-version={apiVersion}")
 
    # Modify the data as needed for the update
    current_file_process_log_data["updatedBy"] = "lavan"  # Example modification
    print(f"Payload being sent: {current_file_process_log_data}")
 
    response, _ = makeRequest('put', f"/api/FileProcessLog/{file_process_log_id}?api-version={apiVersion}",
                               current_file_process_log_data)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} and response: {response.text}"
 
@pytest.mark.parametrize("invalid_data", [
    # Test cases for 'id'
    {"id": "invalid-uuid"},
    {"id": ""},
    {"id": 123434},
 
    # Test cases for 'updatedBy'
 
    {"updatedBy": "a" * 121},
    {"updatedBy": 1231},
 
 
    # Test cases for 'rowVersion'
    {"rowVersion": 12343},
    {"rowVersion": "!!@qeq"},
    {"rowVersion":None},
 
    # Test cases for 'processLogId'
    {"processLogId": "invalid-uuid"},
    {"processLogId": ""},
    {"processLogId": 123434},
 
    # Test cases for 'fileName'
    {"fileName": ""},
    {"fileName": "a" * 1001},
    {"fileName": 1234},
    {"fileName": None},
 
    # Test cases for 'filePath'
    {"filePath": ""},
    {"filePath": "a" * 1001},
    {"filePath": 1234},
    {"filePath": None},
 
    # Test cases for 'fileSize'
    {"fileSize": "not-a-number"},
    {"fileSize": "-99ab"},
    {"fileSize": 2 ** 31},
 
    # Test cases for 'fileHash'
    {"fileHash": "a" * 501},
    {"fileHash": 1234},
    {"fileHash": -1},
])
def testPutInvalidFileProcessLogData(invalid_data):
    # Load the latest config data to get the updated fileProcessLogId
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)  # Load the updated config data
    file_process_log_id = configData.get("fileProcessLogApi", {}).get('fileProcessLogId')
    assert file_process_log_id, "fileProcessLogId not found in config.json"
 
    # Fetch current FileProcessLog data
    _, current_file_process_log_data = makeRequest('get',
                                                   f"/api/FileProcessLog/{file_process_log_id}?api-version={apiVersion}")
 
    # Use the existing valid data and update it with invalid data
    data_to_send = current_file_process_log_data.copy()
    data_to_send.update(invalid_data)
 
    response, _ = makeRequest('put', f"/api/FileProcessLog/{file_process_log_id}?api-version={apiVersion}",
                               data_to_send)
 
    # Check if the response status is 400 (Bad Request) for invalid inputs
    assert response.status_code == 400, f"Expected 400 Bad Request for invalid data: {invalid_data}, but got: {response.status_code}"
 
# Parameterized test for GET FileProcessLog by Process log ID
@pytest.mark.parametrize("process_log_id, expected_status_code", [
    (configData.get("common", {}).get("nonExistingId"), 404),  # Non-existing ID
    (configData.get("common", {}).get("invalidId"), 404)  # Invalid ID
])
def test_GetFileProcessLog_ById(process_log_id, expected_status_code):
    # Make the GET request with the process_log_id
    response, _ = makeRequest('get', f"/api/FileProcessLog/ProcessLog/{process_log_id}?api-version={apiVersion}")
 
    # Assert that the response status code matches the expected status code
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code} and response: {response.text}"
 
# Parameterized test for GET FileProcessLog by ID
@pytest.mark.parametrize("id", [
    configData.get("common", {}).get("nonExistingId"),  # Non-existing ID
    configData.get("common", {}).get("invalidId")  # Invalid ID
])
def test_GetFileProcessLog_ById(id):
    # Make the GET request with the process_log_id
    response, _ = makeRequest('get', f"/api/FileProcessLog/{id}?api-version={apiVersion}")
 
    # Assert that the response status code is 404
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code} and response: {response.text}"
 
 
 
# Testing apiversion - 2.0
# Test to POST a new fileProcessLog entry
def testPostFileProcessLogV2():
    configData = load_Config()
    fileProcessLogDatav2 = configData.get('fileProcessLogApiv2', {})
    processLogId = configData.get('fileProcessLogApiv2', {}).get('processLogId')
    
 
 
    # Update the fileProcessLog data with necessary fields
    fileProcessLogDatav2['processLogId'] = processLogId
    fileProcessLogDatav2['fileProcessLogId'] = fileProcessLogDatav2.get('fileProcessLogId')
    fileProcessLogDatav2['updatedBy'] = fileProcessLogDatav2.get('updatedBy')
    response, responseData = makeRequest('post', f"/api/FileProcessLog?api-version={apiVersion2}", fileProcessLogDatav2)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
 
    if 'id' in responseData:
        # Save the ID immediately after confirming it was created successfully
        saveFileProcessLogIdv2(responseData['id'])
 
    # Field validation
    fieldValidations = [
        ('id', uuid.UUID),            # UUID for the file process log ID
        ('updatedBy', str),           # UpdatedBy field should be a string
        ('rowVersion', str),          # rowVersion should be a string
        ('fileName', str),            # File name
        ('filePath', str),            # File path
        ('fileSize', int),            # File size in bytes
        ('fileHash', str),            # Hash of the file content
        ('processLogId', str),        # Process log ID should be a string
        ('purposeName', str),  # purposeName should be a string
        ('processStatus', str)        # processStatus should be a string
    ]
    validateFields(responseData, fieldValidations)
 
# Test to GET all fileProcessLog entries
def testGetAllFileProcessLogsV2():
    response, responseData = makeRequest('get', f"/api/FileProcessLog?api-version={apiVersion2}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert isinstance(responseData, list), "Expected response to be a list of fileProcessLog entries"
 
 
def testGetFileProcessLogByIdV2():
    # Load the configuration to get the fileProcessLogId
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)
    file_process_log_id = configData.get("fileProcessLogApiv2", {}).get('fileProcessLogId')
    assert file_process_log_id, "fileProcessLogId not found in config.json"
    print(f"Using fileProcessLog ID: {file_process_log_id}")
 
    # Make the GET request
    response, response_data = makeRequest('get', f"/api/FileProcessLog/{file_process_log_id}?api-version={apiVersion2}")
 
    # Check if the response status is 200 (OK)
    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code} and response: {response.text}"
    )
 
    # Check if response data is a JSON object with expected keys
    expected_keys = ["id", "updatedBy", "rowVersion", "processLogId", "fileName", "filePath", "fileSize", "fileHash", "purposeName", "processStatus"]
    for key in expected_keys:
        assert key in response_data, f"Expected key '{key}' in response, but it was missing."
 
    # Additional validation for each field based on FileProcessLogV1 model requirements
    assert isinstance(response_data["id"], str) or response_data["id"] is None, "id should be a string or None"
    assert isinstance(response_data["updatedBy"], str) or response_data[
        "updatedBy"] is None, "updatedBy should be a string or None"
    assert isinstance(response_data["rowVersion"], str) or response_data[
        "rowVersion"] is None, "rowVersion should be a string or None"
    assert isinstance(response_data["processLogId"], str), "processLogId should be a string (UUID format)"
    assert isinstance(response_data["fileName"], str) and 1 <= len(
        response_data["fileName"]) <= 1000, "fileName should be a string with length between 1 and 1000"
    assert isinstance(response_data["filePath"], str) and 1 <= len(
        response_data["filePath"]) <= 1000, "filePath should be a string with length between 1 and 1000"
    assert isinstance(response_data["fileSize"], int) or response_data[
        "fileSize"] is None, "fileSize should be an integer or None"
    assert isinstance(response_data["fileHash"], str) or response_data[
        "fileHash"] is None, "fileHash should be a string or None"
    assert isinstance(response_data["purposeName"], str) or response_data[
        "purposeName"] is None, "purposeName should be a string or None"
    assert isinstance(response_data["processStatus"], str) or response_data[
        "processStatus"] is None, "processStatus should be a string or None"
 
def testGetProcessLogByIdV2():
    # Load the configuration to get the processLogId
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)
    process_log_id = configData.get("fileProcessLogApiv2", {}).get('processLogId')
    assert process_log_id, "processLogId not found in config.json"
    print(f"Using processLog ID: {process_log_id}")
 
    # Make the GET request
    response, response_data = makeRequest('get', f"/api/FileProcessLog/ProcessLog/{process_log_id}?api-version={apiVersion2}")
 
    # Check if the response status is 200 (OK)
    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code} and response: {response.text}"
    )
 
    # Ensure response data is a list
    assert isinstance(response_data, list), f"Expected response data to be a list, but got {type(response_data)}"
 
    # Define the expected keys based on the FileProcessLogV1 model
    expected_keys = ["id", "updatedBy", "rowVersion", "processLogId", "fileName", "filePath", "fileSize", "fileHash", "purposeName", "processStatus"]
 
    # Iterate over each item in the response data and validate keys and field types
    for item in response_data:
        for key in expected_keys:
            assert key in item, f"Expected key '{key}' in response item, but it was missing."
 
        # Additional validation for each field based on FileProcessLogV1 model requirements
        assert isinstance(item["id"], str) or item["id"] is None, "id should be a string or None"
        assert isinstance(item["updatedBy"], str) or item["updatedBy"] is None, "updatedBy should be a string or None"
        assert isinstance(item["rowVersion"], str) or item["rowVersion"] is None, "rowVersion should be a string or None"
        assert isinstance(item["processLogId"], str), "processLogId should be a string (UUID format)"
        assert isinstance(item["fileName"], str) and 1 <= len(item["fileName"]) <= 1000, "fileName should be a string with length between 1 and 1000"
        assert isinstance(item["filePath"], str) and 1 <= len(item["filePath"]) <= 1000, "filePath should be a string with length between 1 and 1000"
        assert isinstance(item["fileSize"], int) or item["fileSize"] is None, "fileSize should be an integer or None"
        assert isinstance(item["fileHash"], str) or item["fileHash"] is None, "fileHash should be a string or None"
        assert isinstance(item["purposeName"], str) or item["purposeName"] is None, "purposeName should be a string or None"
        assert isinstance(item["processStatus"], str) or item["processStatus"] is None, "processStatus should be a string or None"
 
@pytest.mark.parametrize("invalid_data", [
    # Test cases for 'id'
    {"id": "invalid-uuid"},
    {"id": ""},
    {"id": 123434},
 
    # Test cases for 'updatedBy'
    {"updatedBy": "a" * 121},
    {"updatedBy": 1231},
 
    # Test cases for 'rowVersion'
    {"rowVersion": 12343},
    {"rowVersion": "!!@qeq"},
 
    # Test cases for 'processLogId'
    {"processLogId": "invalid-uuid"},
    {"processLogId": ""},
    {"processLogId": 123434},
 
    # Test cases for 'fileName'
    {"fileName": ""},
    {"fileName": "a" * 1001},
    {"fileName": 1234},
    {"fileName": None},
 
    # Test cases for 'filePath'
    {"filePath": ""},
    {"filePath": "a" * 1001},
    {"filePath": 1234},
    {"filePath": None},
 
    # Test cases for 'fileSize'
    {"fileSize": "not-a-number"},
    {"fileSize": "-99ab"},
    {"fileSize": 2**31},
 
    # Test cases for 'fileHash'
    {"fileHash": "a" * 501},
    {"fileHash": 1234},
    {"fileHash": -1},
 
    # Test cases for 'purposeName'
    {"purposeName": ""},
    {"purposeName": 1234},
    {"purposeName": None},
    {"purposeName": "a" * 51},
 
    # Test cases for 'processStatus'
    {"processStatus": ""},
    {"processStatus": 5678},
    {"processStatus": None},
    {"processStatus": "a" * 51}
])
def testPostInvalidFileProcessLogDataV2(invalid_data):
    data_to_send = fileProcessLogDatav2.copy()  # Use the existing valid data
    data_to_send.update(invalid_data)
    response, response_data = makeRequest('post', f"/api/FileProcessLog?api-version={apiVersion2}", data_to_send)
 
    # Check if the response status is 400 (Bad Request) for invalid inputs
    assert response.status_code == 400, f"Expected 400 Bad Request for invalid data: {invalid_data}, but got: {response.status_code}"
 
# Test to update a FileProcessLog
def testPutFileProcessLogV2():
    # Load the latest config data to get the updated fileProcessLogId
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile) # Load the updated config data
    file_process_log_id = configData.get("fileProcessLogApiv2", {}).get('fileProcessLogId')
    assert file_process_log_id, "fileProcessLogId not found in config.json"
 
    # Fetch current FileProcessLog data
    _, current_file_process_log_data = makeRequest('get',
                                                   f"/api/FileProcessLog/{file_process_log_id}?api-version={apiVersion2}")
 
    # Modify the data as needed for the update
    current_file_process_log_data["updatedBy"] = "lavan"  # Example modification
    print(f"Payload being sent: {current_file_process_log_data}")
 
    response, _ = makeRequest('put', f"/api/FileProcessLog/{file_process_log_id}?api-version={apiVersion2}",
                               current_file_process_log_data)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} and response: {response.text}"
 
@pytest.mark.parametrize("invalid_data", [
    # Test cases for 'id'
    {"id": "invalid-uuid"},
    {"id": ""},
    {"id": 123434},
 
    # Test cases for 'updatedBy'
 
    {"updatedBy": "a" * 121},
    {"updatedBy": 1231},
 
 
    # Test cases for 'rowVersion'
    {"rowVersion": 12343},
    {"rowVersion": "!!@qeq"},
    {"rowVersion":None},
 
    # Test cases for 'processLogId'
    {"processLogId": "invalid-uuid"},
    {"processLogId": ""},
    {"processLogId": 123434},
 
    # Test cases for 'fileName'
    {"fileName": ""},
    {"fileName": "a" * 1001},
    {"fileName": 1234},
    {"fileName": None},
 
    # Test cases for 'filePath'
    {"filePath": ""},
    {"filePath": "a" * 1001},
    {"filePath": 1234},
    {"filePath": None},
 
    # Test cases for 'fileSize'
    {"fileSize": "not-a-number"},
    {"fileSize": "-99ab"},
    {"fileSize": 2 ** 31},
 
    # Test cases for 'fileHash'
    {"fileHash": "a" * 501},
    {"fileHash": 1234},
    {"fileHash": -1},
 
    # Test cases for 'purposeName'
    {"purposeName": ""},
    {"purposeName": 1234},
    {"purposeName": None},
    {"purposeName": "a" * 51},
 
    # Test cases for 'processStatus'
    {"processStatus": ""},
    {"processStatus": 5678},
    {"processStatus": None},
    {"processStatus": "a" * 51}
])
 
def testPutInvalidFileProcessLogDataV2(invalid_data):
    
    # Load the latest config data to get the updated fileProcessLogId
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)  # Load the updated config data
        
    file_process_log_id = configData.get("fileProcessLogApiv2", {}).get('fileProcessLogId')
    assert file_process_log_id, "fileProcessLogId not found in config.json"
    
 
    # Fetch current FileProcessLog data
    _, current_file_process_log_data = makeRequest('get',
                                                   f"/api/FileProcessLog/{file_process_log_id}?api-version={apiVersion2}")
 
    # Use the existing valid data and update it with invalid data
    data_to_send = current_file_process_log_data.copy()
    data_to_send.update(invalid_data)
 
    response, _ = makeRequest('put', f"/api/FileProcessLog/{file_process_log_id}?api-version={apiVersion2}",
                               data_to_send)
 
    # Check if the response status is 400 (Bad Request) for invalid inputs
    assert response.status_code == 400, f"Expected 400 Bad Request for invalid data: {invalid_data}, but got: {response.status_code}"
 
# Parameterized test for GET FileProcessLog by Process log ID
@pytest.mark.parametrize("process_log_id, expected_status_code", [
    (configData.get("common", {}).get("nonExistingId"), 404),  # Non-existing ID
    (configData.get("common", {}).get("invalidId"), 404)  # Invalid ID
])
def test_GetFileProcessLog_ByIdV2(process_log_id, expected_status_code):
    # Make the GET request with the process_log_id
    response, _ = makeRequest('get', f"/api/FileProcessLog/ProcessLog/{process_log_id}?api-version={apiVersion2}")
 
    # Assert that the response status code matches the expected status code
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code} and response: {response.text}"
 
# Parameterized test for GET FileProcessLog by ID
@pytest.mark.parametrize("id", [
    configData.get("common", {}).get("nonExistingId"),  # Non-existing ID
    configData.get("common", {}).get("invalidId")  # Invalid ID
])
def test_GetFileProcessLog_ByIdV2(id):
    # Make the GET request with the process_log_id
    response, _ = makeRequest('get', f"/api/FileProcessLog/{id}?api-version={apiVersion2}")
 
    # Assert that the response status code is 404
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code} and response: {response.text}"
 
# Run the tests if this script is executed directly
if __name__ == "__main__":
    pytest.main()
 
 