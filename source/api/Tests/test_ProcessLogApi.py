import datetime
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
cultureCode = configData["common"]["cultureCode"]
clientId = configData["common"]["testClientId"]

# Token from runtests config
token = config["tokenApi"]["token"]
header = {"Authorization": f"Bearer {token}"}

# Load configuration data from config.json
def read():
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

# Get ActivityType and ProcessStatus from config.json
activityType = configData.get('activityTypeApi', {}).get('activityType')
processStatus = configData.get('processStatusApi', {}).get('status')

# Prepare processLog data, including the activityType and processStatus
processLog_post_data = configData.get('processLogApi')
processLog_post_data['type'] = activityType
processLog_post_data['status'] = processStatus

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
        response_data = response.json()
        print("Response body:", json.dumps(response_data, indent=4))
    except json.JSONDecodeError:
        print("Response body is not JSON:", response.text)
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


# Save updated timestamps to config.json
def saveTimestamps(startTime, lastUpdatedTime):
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    configData['processLogApi']['startTimeStamp'] = startTime
    configData['processLogApi']['lastUpdatedTimeStamp'] = lastUpdatedTime

    with open(config_path, 'w') as config_file:
        json.dump(configData, config_file, indent=4)

    print(f"Timestamps saved in config.json: startTimeStamp={startTime}, lastUpdatedTimeStamp={lastUpdatedTime}")

# Save processLogId to config.json
def saveProcessLogId(processLog_Id):
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    configData['processLogApi']['processLogId'] = processLog_Id

    with open(config_path, 'w') as configFile:
        json.dump(configData, configFile, indent=4)

    print(f"'processLogId' saved in config.json under processLogApi: {processLog_Id}")

# Save activityType to config.json
def saveActivityType(activity_Type):
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    configData['processLogApi']['activityType'] = activity_Type

    with open(config_path, 'w') as configFile:
        json.dump(configData, configFile, indent=4)

    print(f"'activityType' saved in config.json under processLogApi: {activity_Type}")

# Validate the fields
def validateFields(response_data, field_validations):
    for field, field_type, *length in field_validations:
        field_value = response_data.get(field)

        if field == 'id':
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
    assert processLog_Id, "No 'id' found in the response for the new process log."
    saveProcessLogId(processLog_Id)

    # --- 🔍 Verify data was actually stored ---
    get_response, get_data = makeRequest(
        'get',
        f"/api/ProcessLog/{processLog_Id}?api-version={apiVersion}"
    )

    print("Fetched Data (GET after POST):")
    print(json.dumps(get_data, indent=4))

    assert get_response.status_code == 200, f"Expected 200, got {get_response.status_code}"
    # --- Deep Compare (ignoring auto-generated fields) ---
    # ignore_fields = ['id', 'rowVersion', 'startTimeStamp', 'lastUpdatedTimeStamp', 'activityType', 'sortBy']
    #
    # for key, value in processLog_post_data.items():
    #     if key not in ignore_fields:
    #         assert get_data.get(key) == value, \
    #             f"Mismatch for field '{key}': expected {value}, got {get_data.get(key)}"
    # Optional: validate fields exist and types are correct
    field_validations = [
        ('id', uuid.UUID),
        ('updatedBy', str, (2, 250)),
        ('rowVersion', str),
        ('type', str),
        ('status', str),
        ('startTimeStamp', datetime.datetime),
        ('lastUpdatedTimeStamp', datetime.datetime),
    ]
    validateFields(get_data, field_validations)




# Test to GET all processLog
def testGetAllProcessLogs():
    response, response_data = makeRequest('get', f"/api/ProcessLog?api-version={apiVersion}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert isinstance(response_data, list), "Expected response to be a list of processLogs"



# Test to GET a specific processLog by ID
def testGetProcessLogById():
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    processLog_Id = configData.get("processLogApi", {}).get('processLogId')
    assert processLog_Id, "processLogId not found in config.json"
    response, _ = makeRequest('get', f"/api/ProcessLog/{processLog_Id}?api-version={apiVersion}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    print(f"Retrieved processLog with ID: {processLog_Id}")

# Test to update a processLog
def testPutProcessLog():
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    # assertion of ProcessLog Id
    processLog_Id = configData.get("processLogApi", {}).get('processLogId')
    assert processLog_Id, "processLogId not found in config.json"
     # Fetch current product data
    _, current_processLog_data = makeRequest('get', f"/api/ProcessLog/{processLog_Id}?api-version={apiVersion}")

    current_processLog_data["updatedBy"]="Lavanya Processlog updated"

    response, _ = makeRequest('put', f"/api/ProcessLog/{processLog_Id}?api-version={apiVersion}", current_processLog_data)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

def print_response(response):
    if response.status_code == 204:
        print("No content returned (204).")
        return
    try:
        print(json.dumps(response.json(), indent=4))
    except Exception:
        print("Response body is not JSON:")
        print(response.text)

def assert_valid_response(response, test_name=""):
    """
    Assert that the response is either 200 (with JSON) or 204 (no content).
    Prints the response safely.
    """
    assert response.status_code in [200, 204], \
        f"{test_name} - Expected 200 or 204, got {response.status_code}"

    if response.status_code == 204:
        print(f"{test_name} - No content returned (204).")
    else:
        try:
            data = response.json()
            print(f"{test_name} - Response JSON:")
            print(json.dumps(data, indent=4))
        except Exception as e:
            print(f"{test_name} - Response body not JSON: {e}")
            print(response.text)


# Test to GET a specific processLog by searching a type and timestamps
def testGetProcessLogSearchByActivityType():
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    activity_Type = configData.get("processLogApi", {}).get('activityType')
    assert activity_Type, "activityType not found or is empty in config.json"

    start_TimeStamp = configData.get("processLogApi", {}).get('startTimeStamp')
    lastUpdated_TimeStamp = configData.get("processLogApi", {}).get('lastUpdatedTimeStamp')
    assert start_TimeStamp, "startTimeStamp not found in config.json"
    assert lastUpdated_TimeStamp, "lastUpdatedTimeStamp not found in config.json"

    response, _ = makeRequest(
        'get',
        f"/api/ProcessLog/Search?activityType={activity_Type}&startTime={start_TimeStamp}&endTime={lastUpdated_TimeStamp}&api-version={apiVersion}"
    )

    assert_valid_response(response, "SearchByActivityType")



def get_date_range(option):
    now = datetime.datetime.now(datetime.UTC).replace(microsecond=0)

    if option == "Today":
        start = now.replace(hour=0, minute=0, second=0)
    elif option == "Last7Days":
        start = now - datetime.timedelta(days=7)
    elif option == "Last14Days":
        start = now - datetime.timedelta(days=14)
    elif option == "Last30Days":
        start = now - datetime.timedelta(days=30)
    else:
        raise ValueError("Invalid date range option")
    return start.isoformat() + "Z", now.isoformat() + "Z"


def update_config_with_ranges():
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    # always refresh ranges
    for option in ["Today", "Last7Days", "Last14Days", "Last30Days"]:
        start, end = get_date_range(option)
        configData['processLogApi'][f'{option}Start'] = start
        configData['processLogApi'][f'{option}End'] = end

    with open(config_path, 'w') as configFile:
        json.dump(configData, configFile, indent=4)

    return configData



@pytest.fixture(scope="session", autouse=True)
def setup_config():
    return update_config_with_ranges()

@pytest.mark.parametrize("range_option", ["Today", "Last7Days", "Last14Days", "Last30Days"])
def testGetProcessLogSearchByDateRange(range_option, setup_config):
    configData = setup_config
    start_TimeStamp = configData['processLogApi'][f"{range_option}Start"]
    end_TimeStamp = configData['processLogApi'][f"{range_option}End"]

    dateRange = f"{start_TimeStamp}/{end_TimeStamp}"

    response, _ = makeRequest(
        'get',
        f"/api/ProcessLog/Search?DateRange={dateRange}&api-version={apiVersion}"
    )

    assert_valid_response(response, f"SearchByDateRange[{range_option}]")

def testGetProcessLogSearchBySortBy():
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    sortBy = configData.get("processLogApi", {}).get('sortBy', ["Status"])
    sortBy_param = ",".join(sortBy) if isinstance(sortBy, list) else sortBy

    response, _ = makeRequest(
        'get',
        f"/api/ProcessLog/Search?SortBy={sortBy_param}&api-version={apiVersion}"
    )

    assert_valid_response(response, f"SearchBySortBy[{sortBy_param}]")


def testGetProcessLogSearchBySortDirection():
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    sortDirection = configData.get("processLogApi", {}).get('sortDirection', "asc")

    response, _ = makeRequest(
        'get',
        f"/api/ProcessLog/Search?SortDirection={sortDirection}&api-version={apiVersion}"
    )

    assert_valid_response(response, f"SearchBySortDirection[{sortDirection}]")

def testGetProcessLogSearchByPageNumber():
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    pageNumber = configData.get("processLogApi", {}).get('pageNumber', 1)

    response, _ = makeRequest(
        'get',
        f"/api/ProcessLog/Search?PageNumber={pageNumber}&api-version={apiVersion}"
    )

    assert_valid_response(response, f"SearchByPageNumber[{pageNumber}]")

def testGetProcessLogSearchByPageSize():
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    pageSize = configData.get("processLogApi", {}).get('pageSize', 10)

    response, _ = makeRequest(
        'get',
        f"/api/ProcessLog/Search?PageSize={pageSize}&api-version={apiVersion}"
    )

    assert_valid_response(response, f"SearchByPageSize[{pageSize}]")

def testGetProcessLogSearchByTimeZone():
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    timeZone = configData.get("processLogApi", {}).get('timeZone', "UTC")
    assert timeZone, "timeZone not found in config.json"

    response, _ = makeRequest(
        'get',
        f"/api/ProcessLog/Search?TimeZone={timeZone}&api-version={apiVersion}"
    )

    assert_valid_response(response, f"SearchByTimeZone[{timeZone}]")


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
    ({"type": ""}, "Field 'type' cannot be empty"),
    ({"type": "a" * 51}, "Field 'type' must not exceed 250 characters"),
    ({"type": 1231}, "Field 'type' must be a string"),
    ({"activityType": ""}, "Field 'activityType' cannot be empty"),
    ({"activityType": "a" * 51}, "Field 'activityType' must not exceed 250 characters"),
    ({"activityType": 1231}, "Field 'activityType' must be a string"),
    ({"startTimeStamp": "07-10-2024", }, "Field 'startTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"startTimeStamp": "13-10-2024", }, "Field 'startTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"startTimeStamp": "13/10/2024", }, "Field 'startTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"startTimeStamp": "13/oct/2024", }, "Field 'startTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"lastUpdatedTimeStamp": "07-10-2024", }, "Field 'lastUpdatedTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"lastUpdatedTimeStamp": "13-10-2024", }, "Field 'lastUpdatedTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"lastUpdatedTimeStamp": "13/10/2024", }, "Field 'lastUpdatedTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"lastUpdatedTimeStamp": "13/oct/2024", }, "Field 'lastUpdatedTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
])

def testPostInvalidData(invalid_data, expected_error):
    # Ensure invalid_data is merged with processLog_post_data if needed
    data_to_send = processLog_post_data.copy()
    data_to_send.update(invalid_data)
    response, response_data = makeRequest('post', f"/api/ProcessLog?api-version={apiVersion}",data_to_send)

@pytest.mark.parametrize("processLog_Id, expected_status_code, expected_error_message", [
    ("865a0e7f-4980-92bd-a7d89777b4a9", 404, "Field 'id' is not a valid UUID."),
    ("123e4567-e89b-12d3-a456-426614174000-not-found", 404, "ProcessLogId not found."),
    ("865a0e7f-4980-92bd-a7d89777b4@@", 404, "Field 'id' is not a valid UUID."),
])
def test_get_processLog_by_id(processLog_Id, expected_status_code, expected_error_message):

    response, response_data = makeRequest('get', f"/api/ProcessLog/{processLog_Id}?api-version={apiVersion}")

    # Assert that the response status code is as expected
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"


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
    ({"type": ""}, "Field 'type' cannot be empty"),
    ({"type": "a" * 51}, "Field 'type' must not exceed 250 characters"),
    ({"type": 1231}, "Field 'type' must be a string"),
    ({"activityType": ""}, "Field 'activityType' cannot be empty"),
    ({"activityType": "a" * 51}, "Field 'activityType' must not exceed 250 characters"),
    ({"activityType": 1231}, "Field 'activityType' must be a string"),
    ({"startTimeStamp": "07-10-2024", }, "Field 'startTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"startTimeStamp": "13-10-2024", }, "Field 'startTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"startTimeStamp": "13/10/2024", }, "Field 'startTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"startTimeStamp": "13/oct/2024", }, "Field 'startTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"lastUpdatedTimeStamp": "07-10-2024", }, "Field 'lastUpdatedTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"lastUpdatedTimeStamp": "13-10-2024", }, "Field 'lastUpdatedTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"lastUpdatedTimeStamp": "13/10/2024", }, "Field 'lastUpdatedTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
    ({"lastUpdatedTimeStamp": "13/oct/2024", }, "Field 'lastUpdatedTimeStamp' is not in the correct format. Expected 'yyyy-mm-ddTHH:MM:SSZ'."),
])

def testPutInvalidData(invalid_data, expected_error):
    with open(config_path, 'r') as configFile:
        configData = json.load(configFile)

    processLog_Id = configData.get("processLogApi", {}).get('processLogId')
    assert processLog_Id, "processLogId not found in config.json"
    # Fetch current processLog data
    _, current_processLog_data = makeRequest('get', f"/api/ProcessLog/{processLog_Id}?api-version={apiVersion}")
    # Update the current_processLog_data with invalid data
    data_to_send = current_processLog_data.copy()
    data_to_send.update(invalid_data)
    # Make the PUT request with invalid data
    response, response_data = makeRequest('put', f"/api/ProcessLog/{processLog_Id}?api-version={apiVersion}", data_to_send)


if __name__ == "__main__":
    pytest.main()
