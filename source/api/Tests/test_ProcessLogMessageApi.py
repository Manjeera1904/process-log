import datetime
import json
import re
import uuid
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
# Get level, processLogId from config.json
processLog_id = configData.get('processLogApi', {}).get('processLogId')
fileProcessLog_id = configData.get('fileProcessLogApi', {}).get('fileProcessLogId')
message_level = configData.get('messageLevelApi', {}).get('level')

# Prepare processLogMessageApi data, including the processLogId and level
processLogMessage_post_data= configData.get('processLogMessageApi')
processLogMessage_post_data['processLogId'] = processLog_id
processLogMessage_post_data['fileProcessLogId'] = fileProcessLog_id
processLogMessage_post_data['level']= message_level



# Fetch messageTimeStamp  from config.json, or generate them if not present
message_timestamp = configData.get('processLogMessageApi', {}).get('messageTimeStamp')
last_message_timestamp = configData.get('processLogMessageApi', {}).get('lastMessageTimeStamp')


# If timestamps are missing, generate them
if not message_timestamp:
    message_timestamp = datetime.datetime.now().isoformat() + 'Z'
    processLogMessage_post_data['messageTimeStamp'] = message_timestamp
# Now processLogMessage_post_data contains the correct processLogId and level

if not last_message_timestamp:
    last_message_timestamp = datetime.datetime.now().isoformat() + 'Z'
    processLogMessage_post_data['lastMessageTimeStamp'] = last_message_timestamp
print("processLogMessage POST data:", processLogMessage_post_data)


## Generic method for making requests
def makeRequest(method, endpoint, data=None):

    clientId = config["common"]["testClientId"]
    url = f"{baseUrl}{endpoint}"
    print(f"\n=== [{method.upper()}] {url} ===")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-EI-ClientId": clientId
    }
    print("Request headers:", json.dumps(headers, indent=4))
    if data:
        print("Request body:", json.dumps(data, indent=4))

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

    # Parse response data
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        response_data = response.text

    print(f"Response status: {response.status_code}")
    print("Response body:", json.dumps(response_data, indent=4) if isinstance(response_data, dict) else response_data)

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


# Save updated timestamps to config.json
def saveTimestamps(messageTime,lastMessageTime):
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    configData['processLogMessageApi']['messageTimeStamp'] = messageTime
    configData['processLogMessageApi']['last_message_timestamp'] = lastMessageTime


    with open(config_path, 'w') as configFile:
        json.dump(configData, configFile, indent=4)

    print(f"Timestamps saved in config.json: messageTimeStamp={messageTime}, last_message_timestamp={lastMessageTime} ")

# Save processLogMessage ID to config.json
def saveProcessLogMessageId(processLogMessage_Id):
    # Open the config (or processLogMessage) JSON file
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    # Save ProcessLogMessageId under the processLogMessageAPI section
    configData['processLogMessageApi']['processLogMessageId'] = processLogMessage_Id

    # Write the updated data back to the file
    with open(config_path, 'w') as configFile:
        json.dump(configData, configFile, indent=4)

    print(f"'processLogMessageId' saved in config.json under processLogMessageApi: {processLogMessage_Id}")

# validate the fields
def validateFields(response_data, field_validations):
    for field, field_type, *length in field_validations:
        field_value = response_data.get(field)

        if field == 'id' or field == 'processLogMessageId':
            try:
                if isinstance(field_value, str):
                    uuid_value = uuid.UUID(field_value)
                else:
                    uuid_value = field_value
            except ValueError:
                raise TypeError(f"Field '{field}' is not a valid UUID.")
        elif field == 'rowVersion':
            pattern = r'^[A-Za-z0-9+/]+={0,2}$'
            if not re.match(pattern, field_value or ''):
                raise ValueError(f"Field '{field}' is not in the correct format.")
        else:
            if not isinstance(field_type, tuple):
                field_type = (field_type,)

from datetime import datetime
# Test to POST userClient
def testPostRequest():


    response, response_data = makeRequest('post', f"/api/ProcessLogMessage?api-version={apiVersion}",
                                          processLogMessage_post_data)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
    # Save userClientId if the POST is successful
    if 'id' in response_data:
        saveProcessLogMessageId(response_data['id'])

    # Load processLogId and level from the config file
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)
        processLog_id = configData.get('processLogApi', {}).get('processLogId')
        message_level = configData.get('messageLevelApi', {}).get('level')


    # Field validation
    field_validations = [
        ('id', uuid.UUID),
        ('updatedBy', str, (2, 250)),
        ('rowVersion', str),
        ('processLogId', str),
        ('level', str),
        ('message', str),
        ('messageTimeStamp', datetime)
    ]
    response_data['processLogId'] = processLog_id
    response_data['level'] = message_level
    validateFields(response_data, field_validations)


# Test to GET all processLogMessage
def testGetAllProcessLogMessage():
    response, response_data = makeRequest('get', f"/api/ProcessLogMessage?api-version={apiVersion}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert isinstance(response_data, list), "Expected response to be a list of processLogMessages"

# Test to GET a specific processLogMessage by Id
def testGetProcessLogMessageById():
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)
    processLogMessage_Id = configData.get("processLogMessageApi", {}).get('processLogMessageId')
    assert processLogMessage_Id, "processLogMessageId not found in config.json"
    response, _ = makeRequest('get', f"/api/ProcessLogMessage/{processLogMessage_Id}?api-version={apiVersion}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"


 # Test to GET a specific processLogMessage by processLogId
def testGetProcessLogMessageByProcessLogId():

    processLog_Id = configData.get("processLogMessageApi", {}).get('processLogId')
    assert processLog_Id, "processLogId not found in config.json"
    response, _ = makeRequest('get', f"/api/ProcessLogMessage/ProcessLog/{processLog_Id}?api-version={apiVersion}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

@ pytest.mark.parametrize("invalid_data, expected_error", [
    ({"id": "invalid-uuid"}, "Field 'id' is not a valid UUID"),
    ({"id": ""}, "Field 'id' cannot be empty"),
    ({"id": 123434}, "Field 'id' must be in a UUID"),
    ({"updatedBy": ""}, "Field 'updatedBy' cannot be empty"),
    ({"updatedBy": "a" * 251}, "Field 'updatedBy' must not exceed 250 characters"),
    ({"updatedBy": 1231}, "Field 'updatedBy' must be a string"),
    ({"rowVersion": 12343}, "Field 'rowVersion' is not in a format"),
    ({"rowVersion": ""}, "Field 'rowVersion' is not in a format"),
    ({"rowVersion": "!!@qeq"}, "Field 'rowVersion' is not in a format"),
    ({"processLogId": 12345}, "Field 'productId' must be a string"),
    ({"processLogId": ""}, "Field 'productId' cannot be empty"),
    ({"processLogId": "invalid-uuid"}, "Field 'productId' is not a valid UUID"),
    ({"level": ""}, "Field 'level' cannot be empty"),
    ({"level": "a" * 51}, "Field 'level' must not exceed 250 characters"),
    ({"level": 1231}, "Field 'level' must be a string"),
    ({"message": ""}, "Field 'message' cannot be empty"),
    ({"message": "a" * 51}, "Field 'message' must not exceed 250 characters"),
    ({"message": 1231}, "Field 'message' must be a string"),
    ({"messageTimeStamp": "07-10-2024", }, "Field 'messageTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"messageTimeStamp": "13-10-2024", }, "Field 'messageTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"messageTimeStamp": "13/10/2024", }, "Field 'messageTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"messageTimeStamp": "13/oct/2024", }, "Field 'messageTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),

])

def testPostInvalidData(invalid_data, expected_error):
    # Ensure invalid_data is merged with processLogMessage_post_data if needed
    data_to_send = processLogMessage_post_data.copy()
    data_to_send.update(invalid_data)
    response, response_data = makeRequest('post', f"/api/ProcessLogMessage?api-version={apiVersion}",data_to_send)

@pytest.mark.parametrize("processLogMessage_Id, expected_status_code, expected_error_message", [
    ("865a0e7f-4980-92bd-a7d89777b4a9", 404, "Field 'id' is not a valid UUID."),
    ("123e4567-e89b-12d3-a456-426614174000-not-found", 404, "ProcessLogId not found."),
    ("865a0e7f-4980-92bd-a7d89777b4@@", 404, "Field 'id' is not a valid UUID."),
])
def test_get_processLogMessage_by_id(processLogMessage_Id, expected_status_code, expected_error_message):

    response, response_data = makeRequest('get', f"/api/ProcessLogMessage/{processLogMessage_Id}?api-version={apiVersion}")

    # Assert that the response status code is as expected
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

@pytest.mark.parametrize("processLog_Id, expected_status_code, expected_error_message", [
    ("765a0e7f-4980-92bd-a7d89777b4a9", 404, "Field 'id' is not a valid UUID."),
    ("233e4567-e89b-12d3-a456-426614174000-not-found", 404, "ProcessLogId not found."),
    ("985a0e7f-4980-92bd-a7d89777b4@@", 404, "Field 'id' is not a valid UUID."),
])
def test_get_processLogMessage_by_ProcessLogId(processLog_Id, expected_status_code, expected_error_message):

    response, response_data = makeRequest('get', f"/api/ProcessLogMessage/ProcessLog/{processLog_Id}?api-version={apiVersion}")

    # Assert that the response status code is as expected
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"



# From here testing the api-Version 2.0
from datetime import datetime
# Test to POST userClient
def testPostRequestV2():


    response, response_data = makeRequest('post', f"/api/ProcessLogMessage?api-version={apiVersion2}",
                                          processLogMessage_post_data)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
    # Save userClientId if the POST is successful
    if 'id' in response_data:
        saveProcessLogMessageId(response_data['id'])

    # Load processLogId and level from the config file
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)
        processLog_id = configData.get('processLogApi', {}).get('processLogId')
        fileProcessLog_id = configData.get('fileProcessLogApiv2', {}).get('fileProcessLogId')
        message_level = configData.get('messageLevelApi', {}).get('level')


    # Field validation
    field_validations = [
        ('id', uuid.UUID),
        ('updatedBy', str, (2, 250)),
        ('rowVersion', str),
        ('processLogId', str),
        ('level', str),
        ('message', str),
        ('messageTimeStamp', datetime),
        ('fileProcessLogId', str)
    ]
    response_data['processLogId'] = processLog_id
    response_data['fileProcessLogId'] = fileProcessLog_id
    response_data['level'] = message_level
    validateFields(response_data, field_validations)


# Test to GET all processLogMessage
def testGetAllProcessLogMessageV2():
    response, response_data = makeRequest('get', f"/api/ProcessLogMessage?api-version={apiVersion2}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert isinstance(response_data, list), "Expected response to be a list of processLogMessages"

# Test to GET a specific processLogMessage by Id
def testGetProcessLogMessageByIdV2():
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)
    processLogMessage_Id = configData.get("processLogMessageApi", {}).get('processLogMessageId')
    assert processLogMessage_Id, "processLogMessageId not found in config.json"
    response, _ = makeRequest('get', f"/api/ProcessLogMessage/{processLogMessage_Id}?api-version={apiVersion2}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"


def testGetProcessLogMessageByProcessLogIdV2():
    processLog_Id = configData.get("processLogMessageApi", {}).get('processLogId')
    assert processLog_Id, "processLogId not found in config.json"

    response, _ = makeRequest(
        'get',
        f"/api/ProcessLogMessage/ProcessLog/{processLog_Id}?api-version={apiVersion2}"
    )

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    data = response.json()

    assert isinstance(data, list), "Expected response JSON to be a list"

    for item in data:
        assert 'fileProcessLogId' in item, "Missing 'fileProcessLogId' in response item"


@ pytest.mark.parametrize("invalid_data, expected_error", [
    ({"id": "invalid-uuid"}, "Field 'id' is not a valid UUID"),
    ({"id": ""}, "Field 'id' cannot be empty"),
    ({"id": 123434}, "Field 'id' must be in a UUID"),
    ({"updatedBy": ""}, "Field 'updatedBy' cannot be empty"),
    ({"updatedBy": "a" * 251}, "Field 'updatedBy' must not exceed 250 characters"),
    ({"updatedBy": 1231}, "Field 'updatedBy' must be a string"),
    ({"rowVersion": 12343}, "Field 'rowVersion' is not in a format"),
    ({"rowVersion": ""}, "Field 'rowVersion' is not in a format"),
    ({"rowVersion": "!!@qeq"}, "Field 'rowVersion' is not in a format"),
    ({"processLogId": 12345}, "Field 'productId' must be a string"),
    ({"processLogId": ""}, "Field 'productId' cannot be empty"),
    ({"processLogId": "invalid-uuid"}, "Field 'productId' is not a valid UUID"),
    ({"level": ""}, "Field 'level' cannot be empty"),
    ({"level": "a" * 51}, "Field 'level' must not exceed 250 characters"),
    ({"level": 1231}, "Field 'level' must be a string"),
    ({"message": ""}, "Field 'message' cannot be empty"),
    ({"message": "a" * 51}, "Field 'message' must not exceed 250 characters"),
    ({"message": 1231}, "Field 'message' must be a string"),
    ({"messageTimeStamp": "07-10-2024", }, "Field 'messageTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"messageTimeStamp": "13-10-2024", }, "Field 'messageTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"messageTimeStamp": "13/10/2024", }, "Field 'messageTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"messageTimeStamp": "13/oct/2024", }, "Field 'messageTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"fileProcessLogId": "invalid-uuid"}, "Field 'fileProcessLogId' is not a valid UUID"),
    ({"fileProcessLogId": ""}, "Field 'fileProcessLogId' cannot be empty"),
    ({"fileProcessLogId": 12345}, "Field 'fileProcessLogId' must be a string"),
])

def testPostInvalidDataV2(invalid_data, expected_error):
    # Ensure invalid_data is merged with processLogMessage_post_data if needed
    data_to_send = processLogMessage_post_data.copy()
    data_to_send.update(invalid_data)
    response, response_data = makeRequest('post', f"/api/ProcessLogMessage?api-version={apiVersion2}",data_to_send)

@pytest.mark.parametrize("processLogMessage_Id, expected_status_code, expected_error_message", [
    ("865a0e7f-4980-92bd-a7d89777b4a9", 404, "Field 'id' is not a valid UUID."),
    ("123e4567-e89b-12d3-a456-426614174000-not-found", 404, "ProcessLogId not found."),
    ("865a0e7f-4980-92bd-a7d89777b4@@", 404, "Field 'id' is not a valid UUID."),
])
def test_get_processLogMessage_by_id_V2(processLogMessage_Id, expected_status_code, expected_error_message):

    response, response_data = makeRequest('get', f"/api/ProcessLogMessage/{processLogMessage_Id}?api-version={apiVersion2}")

    # Assert that the response status code is as expected
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

@pytest.mark.parametrize("processLog_Id, expected_status_code, expected_error_message", [
    ("765a0e7f-4980-92bd-a7d89777b4a9", 404, "Field 'id' is not a valid UUID."),
    ("233e4567-e89b-12d3-a456-426614174000-not-found", 404, "ProcessLogId not found."),
    ("985a0e7f-4980-92bd-a7d89777b4@@", 404, "Field 'id' is not a valid UUID."),
])
def test_get_processLogMessage_by_ProcessLogId_V2(processLog_Id, expected_status_code, expected_error_message):

    response, response_data = makeRequest('get', f"/api/ProcessLogMessage/ProcessLog/{processLog_Id}?api-version={apiVersion2}")

    # Assert that the response status code is as expected
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"


if __name__ == "__main__":
    pytest.main()
