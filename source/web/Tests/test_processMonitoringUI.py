import json 
import json as json_module
import os
import re
import time
from time import sleep
import requests
import pytest
import copy
import uuid
from datetime import datetime, timezone
import time
from selenium.common import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from config import (
    driver, load_secret, user_login, load_config,baseUrl,
    click, generate_random_word, send_keys, click_create_button, click_after_login,
    homeUrl, processLogUrl, verifyElementPresence, deleteNonProdHelper,
    capture_browser_config_json,browser_config_path, inject_config_into_browser, get_element_text, TableValidator
)

test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config_path = os.path.join(test_script_path, 'config.json').replace('\\', '/')


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

baseUrl = baseUrl
apiVersion = configData["common"]["apiVersion"]
cultureCode = configData["common"]["cultureCode"]
clientId = configData["common"]["testClientId"]
env = config.get("env")
pclapiBaseUrl = f'https://platform-core-api.{env}.eclipsevantage.com'
pcapiBaseUrl = pclapiBaseUrl
processdbclient = f"//span[normalize-space()='db{env}client']"
apiBaseUrl = f"https://process-logging-api.{env}.eclipsevantage.com"


# Token from runtests config
token = configData["tokenApi"]["token"]
header = {"Authorization": f"Bearer {token}"}

# Load configuration data from config.json
def read():
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)


def makeRequest(method, endpoint, json=None):
    url = f"{apiBaseUrl}{endpoint}"
    print(f"{method.upper()} URL: {url}")

    config = load_Config()
    clientId = config["common"]["testClientId"]
    token = config["tokenApi"]["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-EI-ClientId": clientId
    }
    print("Request headers:", headers)

    try:
        if method.lower() == 'post':
            response = requests.post(url, json=json, verify=False, headers=headers)
        elif method.lower() == 'get':
            response = requests.get(url, verify=False, headers=headers)
        elif method.lower() == 'put':
            response = requests.put(url, json=json, verify=False, headers=headers)
        else:
            raise ValueError(f"Invalid method '{method}' provided. Use 'get', 'post', or 'put'.")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        raise

    # Parse response
    try:
        response_data = response.json()
        print("Response body:", json_module.dumps(response_data, indent=4))
    except json_module.JSONDecodeError:
        print("Response body is not JSON:", response.text)
        response_data = {}

    return response, response_data

def force_click_with_retry(driver, xpath, verify_xpath=None, retries=5, delay=1):
    for attempt in range(1, retries + 1):
        try:
            # Wait until element is visible & clickable
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.3)
            try:
                element.click()
            except ElementClickInterceptedException:
                driver.execute_script("arguments[0].click();", element)
            print(f"[INFO] Clicked {xpath} (attempt {attempt})")

            # If we need to confirm dropdown visibility
            if verify_xpath:
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, verify_xpath))
                )
            return

        except (TimeoutException, StaleElementReferenceException) as e:
            print(f"[WARN] Attempt {attempt} failed for {xpath}: {type(e).__name__}")
            time.sleep(delay)

    raise AssertionError(f" Could not click {xpath} after {retries} retries")

def assert_no_signalr_close(driver):

    try:
        # Example: assume app pushes SignalR messages to window.signalREvents
        signalr_messages = driver.execute_script("return window.signalREvents || [];")
    except Exception:
        signalr_messages = []

    for msg in signalr_messages:
        if isinstance(msg, dict) and msg.get("type") == 7:
            raise AssertionError("SignalR connection closed. Type 7 message detected.")


def test_verify_that_the_user_can_log_in_successfully_to_the_eclipse_insights_website(driver, load_secret):
    user_login(driver, load_secret)
    
def test_verify_that_the_browser_config_json_is_copied_from_the_network(driver):
    browser_config_data = capture_browser_config_json(driver, baseUrl, browser_config_path, env)
    assert browser_config_data is not None, "config.json was not captured"

def test_verify_that_the_browser_config_json_is_injected_into_the_browser(driver):
    inject_config_into_browser(driver, browser_config_path)
    injected_config = driver.execute_script("return window.localStorage.getItem('mfConfigOverride');")
    assert injected_config is not None, "Config was not injected into browser"



def test_get_client_id(client_name='db' + env + 'client'):
    url = f"{pcapiBaseUrl}/api/Client/name/{client_name}"
    config = load_Config()
    token = config["tokenApi"]["token"]
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

class TestPostNewDataInProcessMonitorTable:


    def test_create_process_logs_table_datas_for_all_statuses(self, driver):
        
        activity_type_endpoint = "/api/ActivityType?api-version=1.0"
        type_response, type_data = makeRequest('get', activity_type_endpoint)

        assert type_response.status_code == 200, f"Activity type API call failed with status {type_response.status_code}"
        assert isinstance(type_data, list) and type_data, "Activity type API returned no data"

        type_value = type_data[0].get("type")  # e.g., 'ReceiveFile'
        print(f"Using activity type: {type_value}")

        
        # Step 1: Get all statuses from /api/ProcessStatus
        status_endpoint = "/api/ProcessStatus?api-version=1.0"
        response, statusData = makeRequest('get', status_endpoint)

        assert response.status_code == 200, f"Status API failed with {response.status_code}"
        assert statusData, "No statuses returned from API"

        print(f"Retrieved {len(statusData)} statuses from ProcessStatus API.")

        limited_statuses = statusData[:4]
        print(f"Testing only the first {len(limited_statuses)} statuses.")

        # Step 2: For each status, create a ProcessLog via POST
        process_log_endpoint = "/api/ProcessLog?api-version=1.0"

       

        for status_info in limited_statuses:
            
            current_status = status_info.get("status")
            assert current_status, f"Invalid status entry: {status_info}"

            # Generate dynamic timestamps
            start_ts = datetime.now(timezone.utc).isoformat()
            time.sleep(1)  # Ensure different timestamps for start & lastUpdated
            last_updated_ts = datetime.now(timezone.utc).isoformat()

            payload = {
                "id": None,
                "updatedBy": "",
                "rowVersion": "",
                "type": type_value,
                "status": current_status,
                "startTimestamp": start_ts,
                "lastUpdatedTimestamp": last_updated_ts
            }

            # Step 3: Make POST request
            post_response, post_data = makeRequest('post', process_log_endpoint, json=payload)

            # Step 4: Validate API response
            assert post_response.status_code in [200, 201], \
                f"POST failed for status '{current_status}' with code {post_response.status_code}"
            assert post_data, f"No data returned for status '{current_status}'"

            # Validate important response fields
            expected_fields = ["id", "status", "type", "startTimestamp", "lastUpdatedTimestamp"]
            for field in expected_fields:
                assert field in post_data, f"Field '{field}' missing in response for status '{current_status}'"

            # Check data consistency
            assert post_data["status"] == current_status, \
                f"Expected status '{current_status}', got '{post_data['status']}'"
            assert post_data["type"] == payload["type"], \
                f"Expected type '{payload['type']}', got '{post_data['type']}'"

            print(f" Successfully created ProcessLog for status: {current_status}")

        print(" All ProcessLog records created successfully for all statuses.")


class TestProcessMonitor:
    generatedClientName = None
    generatedClientDescription = None

    
    def test_Add_New_Client(self, driver):
        driver.set_page_load_timeout(90)
        driver.get(processLogUrl)
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        click_after_login(driver, config['common']['settingsGearIcon'])
        click(driver, config['client']['clientConfigurationButton'])
        click(driver, config['client']['addNewClientButton'])
        TestProcessMonitor.generatedClientName = generate_random_word()
        TestProcessMonitor.generatedClientDescription = generate_random_word()
        send_keys(driver, config['client']['nameInput'], TestProcessMonitor.generatedClientName)
        send_keys(driver, config['client']['descriptionTextarea'], TestProcessMonitor.generatedClientDescription)
        click_create_button(driver)
        click(driver, config['client']['selectTenantsButton'])
        click(driver, config['client']['selectTenantDropdown'])
        click(driver, config['client']['eclipseDevTenantOption'])
        click(driver, config['client']['selectProductsButton'])
        click(driver, config['client']['selectProductDropdown'])
        click(driver, config['client']['eclipseAnalyticsOption'])
        click(driver, config['client']['selectAnotherProductButton'])
        click(driver, config['client']['selectProductDropdownForAnotherProduct'])
        click(driver, config['client']['platformAdministrationOption'])
        click(driver, config['client']['selectAnotherProductButton'])
        click(driver, config['client']['selectProductDropdownForAnotherProduct2'])
        click(driver, config['client']['processMonitoringOption'])
        click(driver, config['common']['saveButton'])

    def test_For_Test_User_adding_Created_Client_as_active(self, driver):
       
        TestUserClientName = 'TestAutomation02@EclipseDevelopmentTest.onmicrosoft.com'
        click(driver, config['common']['settingsGearIcon'])
        click(driver, config['user']['userSectionButton'])
        click(driver, config['common']['searchButton'])
        send_keys(driver, config['user']['searchButton'], TestUserClientName)
        click(driver, config['user']['editIcon'])
        click(driver, config['user']['selectTenantDropdownButton'])
        click(driver, config['user']['eclipseDevTenantOption'])
        click(driver, config['user']['addAnotherClientButton'])
        click(driver, config['user']['selectLatestClientDropdown'])
        click(driver, config['user']['selectClientByName'].format(clientName=TestProcessMonitor.generatedClientName))
        add_role_button = f"(//div[normalize-space(text())='{TestProcessMonitor.generatedClientName}']/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div//button[normalize-space(.)='Add a role'])[1]"
        click(driver, add_role_button)
        role_dropdown_xpath = f"(//div[normalize-space(text())='{TestProcessMonitor.generatedClientName}']/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div//div[contains(@id,'clients.') and contains(@id, '.roles.') and contains(@id, '.roleId')])[last()]"
        click(driver, role_dropdown_xpath)
        click(driver, config['user']['processLogOption'])
        add_another_role_xpath = f"(//div[normalize-space(text())='{TestProcessMonitor.generatedClientName}']/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div//button[normalize-space()='Add another role'])[last()]"
        click(driver, add_another_role_xpath)
        another_role_dropdown = f"(//div[normalize-space(.)='{TestProcessMonitor.generatedClientName}']/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div//div[contains(@id,'clients.') and contains(@id,'.roleId') and @role='combobox'])[last()]"
        click(driver, another_role_dropdown)
        click(driver, config['user']['filemanageroption'])
        click(driver, add_another_role_xpath)
        third_role_dropdown_xpath = f"(//div[normalize-space(.)='{TestProcessMonitor.generatedClientName}']" \
                                    f"/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div" \
                                    f"//div[contains(@id,'clients.') and contains(@id,'.roleId') and @role='combobox'])[last()]"
        click(driver, third_role_dropdown_xpath)
        click(driver, config['user']['administratorOption'])
        click(driver, config['user']['saveButton'])


class TestProcessDbDefaultClient:
    processdbClientName = 'db' + env + 'client'

    def test_For_Test_User_adding_new_Client_as_active(self, driver):
        
        TestUserClientName = 'TestAutomation02@EclipseDevelopmentTest.onmicrosoft.com'
        click(driver, config['common']['settingsGearIcon'])
        click(driver, config['user']['userSectionButton'])
        click(driver, config['common']['searchButton'])
        send_keys(driver, config['user']['searchButton'], TestUserClientName)
        click(driver, config['user']['editIcon'])
        click(driver, config['user']['addAnotherClientButton'])
        click(driver, config['user']['selectLatestClientDropdown'])
        click(driver,
              config['user']['selectProcessdbClient'].format(clientName=TestProcessDbDefaultClient.processdbClientName))
        add_role_button = f"(//div[normalize-space(text())='{TestProcessDbDefaultClient.processdbClientName}']/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div//button[normalize-space(.)='Add a role'])[1]"
        click(driver, add_role_button)
        role_dropdown_xpath = f"(//div[normalize-space(text())='{TestProcessDbDefaultClient.processdbClientName}']/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div//div[contains(@id,'clients.') and contains(@id, '.roles.') and contains(@id, '.roleId')])[last()]"
        click(driver, role_dropdown_xpath)
        click(driver, config['user']['processLogOption'])
        add_another_role_xpath = f"(//div[normalize-space(text())='{TestProcessDbDefaultClient.processdbClientName}']/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div//button[normalize-space()='Add another role'])[last()]"
        click(driver, add_another_role_xpath)
        another_role_dropdown = f"(//div[normalize-space(.)='{TestProcessDbDefaultClient.processdbClientName}']/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div//div[contains(@id,'clients.') and contains(@id,'.roleId') and @role='combobox'])[last()]"
        click(driver, another_role_dropdown)
        click(driver, config['user']['filemanageroption'])
        click(driver, add_another_role_xpath)
        third_role_dropdown_xpath = f"(//div[normalize-space(.)='{TestProcessDbDefaultClient.processdbClientName}']" \
                                    f"/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div" \
                                    f"//div[contains(@id,'clients.') and contains(@id,'.roleId') and @role='combobox'])[last()]"
        click(driver, third_role_dropdown_xpath)
        click(driver, config['user']['administratorOption'])
        click(driver, config['user']['saveButton'])


class TestProcessMonitorTable:

    @pytest.fixture(scope="class")
    def wait(self, driver):
        return WebDriverWait(driver, 10)

    def get_column_index_by_label(self, driver, label_text):
        headers = driver.find_elements(By.XPATH, "//table//thead//th")
        for i, header in enumerate(headers, start=1):
            if header.text.strip() == label_text:
                return i
        return -1

    def test_Verify_that_the_process_monitor_product_displays_in_the_menu(self, driver):
        click(driver, config['common']['settingsGearIcon'])
        verifyElementPresence(driver, config['processMonitor']['processMonitorProduct'], elementName="processMonitorProduct")


    def test_validate_column_headers(self, driver, wait):
        
        click(driver, config["processMonitor"]["processMonitorProduct"])
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, config["filters"]["clientFilter"]))
        )

        click(driver, config["filters"]["clientFilter"])
        click(driver, processdbclient)
        
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]")))
        WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.XPATH, "//table//thead//th")))
        click(driver, config["filters"]["dateFilter"])
        click(driver, config["filters"]["Last30Days"])

        expected_headers = [
            "Type", "Id", "Description", "Client", "Source",
            "Processed On", "Duration", "State", "Disposition"
        ]

        
        # Re-fetch headers to avoid stale reference
        headers = driver.find_elements(By.XPATH, "//table//thead//th")
        actual_headers = [h.text.strip() for h in headers]

        for label in expected_headers:
            assert label.lower() in (h.lower() for h in actual_headers), f"Missing header: {label}"

    def test_validate_table_rows_data(self, driver, wait):
        
        # Step 1: Navigate to Process Monitor and apply filters
        click(driver, config["processMonitor"]["processMonitorProduct"])

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, config["filters"]["clientFilter"]))
        )
        click(driver, config["filters"]["clientFilter"])
        click(driver, processdbclient)

        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]")))


        click(driver, config["filters"]["dateFilter"])
        click(driver, config["filters"]["Last30Days"])

        # Step 2: Get table headers
        headers = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//table//thead//th"))
        )
        header_labels = [h.text.strip() for h in headers]

        # Step 3: Get table rows
        rows = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//table//tbody//tr"))
        )
        assert rows, "No rows present in the table"

        #  Normalize function to handle minor differences like dashes/spaces
        def normalize(text):
            return text.strip().lower().replace("-", "").replace(" ", "")

        # Step 4: Get list of valid 'name' values from API (and normalize)
        response, response_data = makeRequest("get", "/api/ProcessStatus?api-version=1.0")
        valid_state_names = [normalize(item["name"]) for item in response_data if "name" in item]

        # Step 5: Validate each row's "State" column against valid API names
        for row in rows:
            cells = row.find_elements(By.XPATH, "./td[contains(@class, 'MuiTableCell-body')]")
            cell_values = [cell.text.strip() for cell in cells]
            row_data = dict(zip(header_labels, cell_values))

            if "State" in row_data:
                status = row_data["State"]
                assert normalize(status) in valid_state_names, f"Invalid status value: {status}"


    def test_validate_table_rows_data2(self, driver, wait):
        
        click(driver, config["processMonitor"]["processMonitorProduct"])
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, config["filters"]["clientFilter"]))
        )
        

        click(driver, config["filters"]["clientFilter"])
        click(driver, processdbclient)
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]")))

        click(driver, config["filters"]["dateFilter"])
        click(driver, config["filters"]["Last30Days"])

        headers = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//table//thead//th"))
        )
        header_labels = [h.text.strip() for h in headers]

        rows = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//table//tbody//tr"))
        )
        assert len(rows) > 0, "No rows present in the table"

        table_data = []
        print("Headers:", header_labels)

        # Define valid types from API
        valid_types = ["Payor Contract Analysis", "Receive File"]

        # Normalize valid types (remove spaces, lowercase)
        normalized_valid_types = [v.replace(" ", "").lower() for v in valid_types]

        for row in rows:
            cells = row.find_elements(By.XPATH, "./td[contains(@class, 'MuiTableCell-body')]")
            cell_values = [cell.text.strip() for cell in cells]

            row_data = dict(zip(header_labels, cell_values))
            table_data.append(row_data)

            # validate "Type" column if present
            if "Type" in row_data:
                type_value = row_data["Type"]
                normalized_type_value = type_value.replace(" ", "").lower()

                assert normalized_type_value in normalized_valid_types, \
                    f"Invalid Type value: {type_value} (Valid types: {valid_types})"


    def test_Verify_that_the_process_monitor_product_search_field(self, driver):
        
        # Navigate to Process Monitor > Product
        click(driver, config["processMonitor"]["processMonitorProduct"])

        # Wait and apply Client filter
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config["filters"]["clientFilter"])))
        
        click(driver, config["filters"]["clientFilter"])
        click(driver, processdbclient)

        # Wait for table to render
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]")))


        # Apply date filter
        click(driver, config["filters"]["dateFilter"])
        click(driver, config["filters"]["Last30Days"])

        # Search for "Payor Contract Analysis"
        click(driver, config["processMonitor"]["searchField"])
        send_keys(driver, config["processMonitor"]["searchField"], "Payor Contract Analysis")

        # Wait for table rows OR empty state
        WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.XPATH, "//table//tbody/tr") or
                    d.find_elements(By.XPATH, "//*[contains(text(),'No data available')]")
        )

        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")

        if rows:
            for i in range(1, len(rows) + 1):
                for attempt in range(3):
                    try:
                        # Re-fetch source cell for each row to avoid stale element
                        source_cell_xpath = f"//table//tbody/tr[{i}]/td[2]"
                        source_cell = driver.find_element(By.XPATH, source_cell_xpath)
                        source_text = source_cell.text.strip()

                        assert source_text == "Payor Contract Analysis", \
                            f"Row {i}: Expected 'Payor Contract Analysis' in Source column, but got '{source_text}'"
                        print(f" Row {i}: Source = {source_text}")
                        break  # Exit retry loop if successful

                    except StaleElementReferenceException:
                        print(f" Retry {attempt + 1}: Row {i} stale — retrying...")
                        time.sleep(1)

        else:
            # Handle "No data available" case
            no_data_msg = driver.find_element(By.XPATH, "//*[contains(text(),'No data available')]")
            assert no_data_msg.is_displayed(), \
                "Expected 'No data available' message, but it was not displayed"
            print(" No data available for search term: 'Payor Contract Analysis'")


class TestProcessMonitorPagination:

    def scroll_to_load_all_rows(self, driver, table_xpath):
        previous_count = -1
        while True:
            rows = driver.find_elements(By.XPATH, table_xpath)
            current_count = len(rows)
            if current_count == previous_count:
                break
            previous_count = current_count
            driver.execute_script("arguments[0].scrollIntoView();", rows[-1])
        return current_count

    def wait_for_rows_to_load(self, driver, table_xpath, expected_min_rows=1, timeout=20):
        WebDriverWait(driver, timeout).until(
            lambda d: len(d.find_elements(By.XPATH, table_xpath)) >= expected_min_rows
        )

    @pytest.mark.parametrize("row_count", [20, 50, 100])
    def test_pagination_row_count(self, driver, row_count):
        # Step 1: Open Process Monitor
        
        click(driver, config['processMonitor']['processMonitorProduct'])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config["filters"]["clientFilter"])))

        # Step 2: Apply filters
        click(driver, config["filters"]["clientFilter"])

        click(driver, processdbclient)
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]")))

        click(driver, config["filters"]["dateFilter"])
        click(driver, config["filters"]["Last30Days"])
        
        click(driver, config['pagination']['rowsdropdown'])
        options_container_xpath = config["pagination"]["valueslist"]
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, options_container_xpath))
        )
        option_xpath = f"//li[contains(@class, 'MuiMenuItem-root') and text()='{row_count}']"
        click(driver, option_xpath)

        # Step 4: Wait for table rows to load
        table_rows_xpath = config["pagination"]["table"]
        self.wait_for_rows_to_load(driver, table_rows_xpath)

        # Step 5: Read pagination text like "1–17 of 17"
        pagination_text_xpath = config["pagination"]["pagination_text"]
        pagination_text = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, pagination_text_xpath))
        ).text

        # Extract visible row count from text (e.g., "1–17 of 17" → 17)
        match = re.search(r'–\s*(\d+)\s+of\s+(\d+)', pagination_text)
        assert match, f"Could not parse pagination text: {pagination_text}"
        visible_rows = int(match.group(1))
        total_records = int(match.group(2))
        print(f"Pagination text: {pagination_text} (visible rows: {visible_rows}, total: {total_records})")

        # Step 6: Count actual table rows displayed
        actual_row_count = self.scroll_to_load_all_rows(driver, table_rows_xpath)
        print(f"Actual rows displayed in table: {actual_row_count}")

        # Step 7: Validate the count
        expected_rows = min(row_count, total_records)
        assert actual_row_count == expected_rows, f"Expected {expected_rows} rows, found {actual_row_count}"


class TestProcessMonitorHeader:
    def test_verify_that_the_process_monitor_headers(self, driver):
        
        
        click(driver, config['processMonitor']['processMonitorProduct'])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config["filters"]["clientFilter"])))

        click(driver, config["filters"]["clientFilter"])
        click(driver, processdbclient)
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]")))
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//table//thead//th")))
        click(driver, config["filters"]["dateFilter"])
        click(driver, config["filters"]["Last30Days"])
        verifyElementPresence(driver, config['processMonitor']['type'], elementName="Type")
        verifyElementPresence(driver, config['processMonitor']['id'], elementName="Id")
        verifyElementPresence(driver, config['processMonitor']['description'], elementName="Description")
        verifyElementPresence(driver, config['processMonitor']['client'], elementName="Client")
        verifyElementPresence(driver, config['processMonitor']['source'], elementName="Source")
        verifyElementPresence(driver, config['processMonitor']['processedOn'], elementName="Processed On")
        verifyElementPresence(driver, config['processMonitor']['duration'], elementName="Duration")
        verifyElementPresence(driver, config['processMonitor']['state'], elementName="State")
        verifyElementPresence(driver, config['processMonitor']['disposition'], elementName="Disposition")

    @pytest.mark.skip(
        reason="Process Monitor expand behavior currently disabled; AutoAwesome icon not expected"
    )
    def test_Verify_that_the_process_monitor_AutoAwesome_icon_expand_field(self, driver):
        
        click(driver, config["processMonitor"]["processMonitorProduct"])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config["filters"]["clientFilter"])))
 
        click(driver, config["filters"]["clientFilter"])
        click(driver, processdbclient)
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]")))

        click(driver, config["filters"]["dateFilter"])
        click(driver, config["filters"]["Last30Days"])
        click(driver, config["pagination"]["table"])
        verifyElementPresence(driver, config['pagination']['autoAwesomeIcon'])

    @pytest.mark.skip(
        reason="Process Monitor expand behavior currently disabled; AutoAwesome icon not expected"
    )
    def test_verify_autoawesome_icon_and_expanded_properties(self, driver):
        
        click(driver, config["processMonitor"]["processMonitorProduct"])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config["filters"]["clientFilter"])))

        click(driver, config["filters"]["clientFilter"])
        click(driver, processdbclient)
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]")))

        click(driver, config["filters"]["dateFilter"])
        
        click(driver, config["filters"]["Last30Days"])
        
        table_xpath = config["pagination"]["table"]
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, table_xpath)))
        click(driver, table_xpath)

        # Locate the AutoAwesome icon <svg>
        icon_svg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, config['pagination']['autoAwesomeIcon'])))

        # Verify color and font-size
        icon_color = icon_svg.value_of_css_property("color")
        icon_size = icon_svg.value_of_css_property("font-size")
        assert icon_color == "rgba(128, 38, 41, 1)", f"Icon color is incorrect: {icon_color}"
        assert icon_size == "36px", f"Icon size is incorrect: {icon_size}"

#skipping padding test since tests needs to be updated
        # # Get the parent wrapper where padding is applied
        # icon_wrapper = icon_svg.find_element(By.XPATH, "..")
        #
        # # Verify padding on the wrapper
        # expected_paddings = {
        #     "padding-left": "8px",
        #     "padding-right": "8px",
        #     "padding-top": "3px",
        #     "padding-bottom": "3px",
        # }
        #
        # for side, expected in expected_paddings.items():
        #     actual = icon_wrapper.value_of_css_property(side)
        #     assert actual == expected, f"{side} is {actual}, expected {expected}"
        #
        # # Get element positions for alignment checks
        # icon_rect = icon_svg.rect
        # wrapper_rect = icon_wrapper.rect
        #
        # # Tolerance in pixels
        # tolerance = 2
        #
        # # Check left alignment (wrapper left + padding-left)
        # icon_left = icon_rect['x']
        # wrapper_left = wrapper_rect['x'] + 8  # padding-left
        # assert abs(icon_left - wrapper_left) <= tolerance, (
        #     f"Icon is not left-aligned. icon_left={icon_left}, wrapper_left={wrapper_left}"
        # )
        #
        # # Check bottom alignment (accounting for CSS 'top' offset)
        # icon_bottom = icon_rect['y'] + icon_rect['height']
        # wrapper_bottom = wrapper_rect['y'] + wrapper_rect['height'] - 3  # padding-bottom
        # css_top_offset = -5  # as defined in JSX: top: -5
        #
        # expected_bottom = wrapper_bottom + css_top_offset  # icon is shifted up
        # assert abs(icon_bottom - expected_bottom) <= tolerance, (
        #     f"Icon is not bottom-aligned. icon_bottom={icon_bottom}, expected_bottom={expected_bottom}")
        # print("All properties verified successfully!")


class TestProcessMonitorFilter:
    #  Filter by Client
    def test_filter_by_client(self, driver):
        
        click(driver, config["processMonitor"]["processMonitorProduct"])

        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config["filters"]["clientFilter"])))

        click(driver, config["filters"]["clientFilter"])
        

        click(driver, processdbclient)

        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]")))

        click(driver, config["filters"]["dateFilter"])
        click(driver, config["filters"]["Last30Days"])

        rows = driver.find_elements(By.XPATH, "//table//tbody/tr/td[5]")
        assert len(rows) > 0, " No rows found in the table for client "
        for i, row in enumerate(rows, 1):
            cell_text = row.text.strip()
            assert cell_text == 'db' + env + 'client', f" Row {i}: Expected 'db' + env + 'client', but found '{cell_text}'"
            # print(f" Row {i}: Client = {cell_text}")

    
    #  Filter by Days
    def test_filter_by_days(self, driver):
        
        click(driver, config["processMonitor"]["processMonitorProduct"])

        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]"))
        )

        # Select client
        click(driver, config["filters"]["clientFilter"])
        click(driver, processdbclient)
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]")))

        # Iterate over each date range filter
        for option in ["Last 7 Days", "Last 14 Days", "Last 30 Days"]:
            print(f"\n Checking filter: {option}")

            click(driver, config["filters"]["dateFilter"])
            option_xpath = f"//li[contains(@class, 'MuiMenuItem-root') and .//span[normalize-space(.)='{option}']]"
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            # Click the desired option
            click(driver, option_xpath)

            # Wait for table to reload
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]"))
            )

            # Verify rows in "Processed On" column (assumed 7th column, adjust if needed)
            rows = driver.find_elements(By.XPATH, "//table//tbody/tr/td[7]")
            assert len(rows) > 0, f" No rows found for filter: {option}"

            for i, row in enumerate(rows, 1):
                cell_text = row.text.strip()
                assert cell_text != "", f" Row {i}: Empty date under filter '{option}'"
                print(f" Row {i}: Date = {cell_text}")

            



    def test_filter_by_status(self, driver):
        
        endpoint = "/api/ProcessStatus?api-version=1.0"
        response, responseData = makeRequest('get', endpoint)

        assert response.status_code == 200, f"API call failed with status code {response.status_code}"
        assert responseData, "API returned no status items"

        for status_info in responseData:
            expected_status_value = status_info.get("name")
            # expected_status = status_info.get("status")

            click(driver, config["processMonitor"]["processMonitorProduct"])
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config["filters"]["clientFilter"])))

            # Apply Client and Date filters
            click(driver, config["filters"]["clientFilter"])
            click(driver, processdbclient)
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]"))
            )
            click(driver, config["filters"]["dateFilter"])
            click(driver, config["filters"]["Last30Days"])

            # Open Status Filter
            click(driver, config["filters"]["statusFilter"])

            # Deselect all statuses
            checkbox_xpath = config["filters"]["statusCheckboxes"]
            checkbox_inputs = driver.find_elements(By.XPATH, checkbox_xpath)

            for index, checkbox in enumerate(checkbox_inputs, start=1):
                if checkbox.is_selected():
                    parent_span_xpath = f"({checkbox_xpath})[{index}]/ancestor::span[1]"
                    click(driver, parent_span_xpath)

            # Select only the current status
            status_li_xpath = f"//li[.//span[normalize-space(text())='{expected_status_value}']]"
            status_li = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, status_li_xpath))
            )

            checkbox_to_select = status_li.find_element(By.XPATH, ".//input[@type='checkbox']")
            if not checkbox_to_select.is_selected():
                span_xpath = f".//span[normalize-space(text())='{expected_status_value}']"
                all_status_lis = driver.find_elements(By.XPATH, "//ul//li")
                for index, li in enumerate(all_status_lis, start=1):
                    if li == status_li:
                        span_full_xpath = f"(//ul//li)[{index}]{span_xpath[1:]}"
                        break

                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, span_full_xpath)))
                click(driver, span_full_xpath)
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()

            # Wait for table or empty message
            WebDriverWait(driver, 10).until(
                lambda d: d.find_elements(By.XPATH, "//table//tbody/tr") or
                        d.find_elements(By.XPATH, "//*[contains(text(),'No data available')]")
            )

            # Enhanced normalization function
            def normalize_status(status):
                spaced = re.sub(r'(?<!^)(?=[A-Z])', ' ', status)
                cleaned = re.sub(r'\s+', ' ', spaced.replace("-", " "))
                return cleaned.strip().lower()

            rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
            if rows:
                status_cells = driver.find_elements(By.XPATH, "//table//tbody/tr/td[9]")
                for i, cell in enumerate(status_cells, 1):
                    status_text = cell.text.strip()
                    assert normalize_status(status_text) == normalize_status(expected_status_value), \
                        f"Row {i}: Expected '{expected_status_value}', but got '{status_text}'"
                    print(f"Row {i}: Status = {status_text}")
            else:
                no_data_msg = driver.find_element(By.XPATH, "//*[contains(text(),'No data available')]")
                assert no_data_msg.is_displayed(), \
                    f"No data for status '{expected_status_value}', but no message shown"
                print(f"No data found for status: {expected_status_value}")

    

    def test_filter_by_two_statuses(self, driver):
        endpoint = "/api/ProcessStatus?api-version=1.0"
        response, responseData = makeRequest('get', endpoint)

        assert response.status_code == 200, f"API call failed with status code {response.status_code}"
        assert responseData, "API returned no status items"

        # Normalize the names for matching dropdown items (case-insensitive + spacing)
        def normalize_name(name):
            spaced = re.sub(r'(?<!^)(?=[A-Z])', ' ', name)
            cleaned = re.sub(r'\s+', ' ', spaced.replace("-", " "))
            return cleaned.strip().lower()

        # Build mapping of normalized name → original name
        name_map = {}
        for info in responseData:
            name = info.get("name")
            if name:
                normalized = normalize_name(name)
                name_map[normalized] = name

        valid_names = list(name_map.keys())[:2]
        assert len(valid_names) == 2, "Need at least two statuses to test combined filtering"
        print(f"\nTesting combined filter for normalized names: {valid_names}")

        # Open Process Monitor product
        click(driver, config["processMonitor"]["processMonitorProduct"])

        # Wait for table to load
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]"))
        )

        # Apply base filters
        click(driver, config["filters"]["clientFilter"])
        click(driver, processdbclient)
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]"))
        )
        click(driver, config["filters"]["dateFilter"])
        click(driver, config["filters"]["Last30Days"])

        # Open status filter
        click(driver, config["filters"]["statusFilter"])

        # Deselect all existing statuses
        checkbox_xpath = config["filters"]["statusCheckboxes"]
        checkbox_inputs = driver.find_elements(By.XPATH, checkbox_xpath)
        for index, checkbox in enumerate(checkbox_inputs, start=1):
            if checkbox.is_selected():
                parent_span_xpath = f"({checkbox_xpath})[{index}]/ancestor::span[1]"
                click(driver, parent_span_xpath)

        # Select the two desired statuses using the *original name*
        for normalized_name in valid_names:
            original_name = name_map[normalized_name]
            status_li_xpath = f"//li[.//span[normalize-space(text())='{original_name}']]"
            status_li = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, status_li_xpath))
            )

            checkbox_to_select = status_li.find_element(By.XPATH, ".//input[@type='checkbox']")
            if not checkbox_to_select.is_selected():
                span_xpath = f".//span[normalize-space(text())='{original_name}']"
                all_status_lis = driver.find_elements(By.XPATH, "//ul//li")
                for index, li in enumerate(all_status_lis, start=1):
                    if li == status_li:
                        span_full_xpath = f"(//ul//li)[{index}]{span_xpath[1:]}"
                        break

                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, span_full_xpath)))
                click(driver, span_full_xpath)

        # Close dropdown with Escape
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        # Wait for table or empty message
        WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.XPATH, "//table//tbody/tr") or
                    d.find_elements(By.XPATH, "//*[contains(text(),'No data available')]")
        )

        # Now both dropdown and table show NAME, not STATUS
        expected_names = [name_map[n] for n in valid_names]

        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        if rows:
            # 9th column assumed to be the status/name column
            name_cells = driver.find_elements(By.XPATH, "//table//tbody/tr/td[9]")
            assert len(name_cells) == len(rows), "Mismatch in row and name cell counts"

            for i, cell in enumerate(name_cells, 1):
                cell_text = cell.text.strip()
                assert cell_text in expected_names, (
                    f"Row {i}: Expected one of {expected_names}, but found '{cell_text}'"
                )
                print(f"Row {i}: Name = {cell_text}")
        else:
            no_data_msg = driver.find_element(By.XPATH, "//*[contains(text(),'No data available')]")
            assert no_data_msg.is_displayed(), "Expected 'No data available' message but not found"
            print(f"No data found for names: {expected_names}")

    def test_filter_status_and_compare_UIcount_with_APIcount(self, driver):
    

         # Step 1: Get all available statuses from API
        status_endpoint = "/api/ProcessStatus?api-version=1.0"
        response, responseData = makeRequest('get', status_endpoint)
        assert response.status_code == 200, f"API call failed with status code {response.status_code}"
        assert responseData, "API returned no status items"

        expected_status_value = responseData[2].get("name")    
        status_name = responseData[2].get("status")            
        print(f"Using status filter: {expected_status_value} ({status_name})")

        # Step 2: Get Activity Type from API
        activity_type_endpoint = "/api/ActivityType?api-version=1.0"
        type_response, type_data = makeRequest('get', activity_type_endpoint)
        assert type_response.status_code == 200, f"Activity type API call failed with status {type_response.status_code}"
        assert isinstance(type_data, list) and type_data, "Activity type API returned no data"

        type_value = type_data[0].get("type")
        print(f"Using activity type: {type_value}")

        # Step 3: Apply filters in UI
        click(driver, config["processMonitor"]["processMonitorProduct"])

        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]"))
        )

        # Apply Client Filter
        click(driver, config["filters"]["clientFilter"])
        click(driver, processdbclient)
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]"))
        )

        # Apply Date Filter
        click(driver, config["filters"]["dateFilter"])
        click(driver, config["filters"]["Last30Days"])

        # Apply Status Filter
        click(driver, config["filters"]["statusFilter"])

        # Deselect all statuses
        checkboxes_xpath = config["filters"]["statusCheckboxes"]
        checkboxes = driver.find_elements(By.XPATH, checkboxes_xpath)
        for index, checkbox in enumerate(checkboxes, start=1):
            if checkbox.is_selected():
                checkbox_xpath = f"({checkboxes_xpath})[{index}]"
                parent_span_xpath = f"{checkbox_xpath}/.."
                click(driver, parent_span_xpath)

        # Select desired status
        status_option_xpath = f"//span[normalize-space(text())='{expected_status_value}']"
        click(driver, status_option_xpath)
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]"))
        )

        # Step 4: Iterate through all pages and count total rows
        def get_total_ui_rows(driver):
            total_rows = 0
            page_num = 1

            while True:
                # Wait for table rows to load
                WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//table//tbody/tr"))
                )

                # Count rows on current page
                rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
                total_rows += len(rows)
                print(f"Page {page_num}: Found {len(rows)} rows (Total so far: {total_rows})")

                # Check if “Next Page” button exists and is enabled
                try:
                    next_button = driver.find_element(By.XPATH, "//button[@aria-label='Go to next page']")
                    if not next_button.is_enabled():
                        print("Reached last page.")
                        break
                    next_button.click()
                    page_num += 1

                    # Wait for page transition/loading
                    WebDriverWait(driver, 15).until(
                        EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]"))
                    )
                    time.sleep(1)  # small delay for stability
                except NoSuchElementException:
                    print("Next page button not found — assuming last page.")
                    break

            return total_rows

        ui_total_rows = get_total_ui_rows(driver)
        print(f"Total UI rows across all pages: {ui_total_rows}")

        # Step 5: API Call with filters
        process_endpoint = (
            f"/api/ProcessLog/Search?"
            f"ActivityType={type_value}"
            f"&Statuses={status_name}"
            f"&DateRange=Last30Days"
            f"&PageNumber=1"
            f"&PageSize=100"
            f"&api-version=1.0"
        )

        process_response, process_data = makeRequest('get', process_endpoint)

        if process_response.status_code == 204:
            api_total_count = 0
            print("API returned 204 No Content — no data found")
        elif process_response.status_code == 200:
            assert process_data, "API /ProcessLog/Search returned empty data"
            api_total_count = process_data.get("totalCount", 0)
            print(f"API total count: {api_total_count}")
        else:
            assert False, f"API call to /ProcessLog/Search failed with status {process_response.status_code}"

        # Step 6: Compare UI and API counts
        if ui_total_rows == api_total_count:
            print(f" Success: UI total ({ui_total_rows}) matches API total ({api_total_count})")
        elif ui_total_rows == 0 and api_total_count == 0:
            print(f" No data found for status '{expected_status_value}' — both UI and API returned 0 results")
        else:
            assert False, (
                f" Mismatch: UI shows {ui_total_rows} rows, API shows {api_total_count} rows "
                f"for status '{expected_status_value}' and type '{type_value}'"
            )
    
    def test_error_message_for_unconfigured_database(self, driver):
    
        
        click(driver, config["processMonitor"]["processMonitorProduct"])
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]"))
        )

        # Apply Client Filter
        click(driver, config["filters"]["clientFilter"])
        click(driver, config["user"]["eclipseInsightsAutomationClient"])

        # Wait for the page to load and for the error message to appear
        error_xpath = "//*[contains(text(), 'There is no configured database for this client.')]"
        
        try:
            error_element = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, error_xpath))
            )
            assert error_element.is_displayed(), "Error message is not visible"
            print(" Verified: Correct error message is displayed for unconfigured database")
        except TimeoutException:
            assert False, " Error message not displayed within timeout"

    

    def test_process_monitor_page_remains_visible_after_tab_switch_for_configuredclient(self, driver):

        
        click(driver, config["processMonitor"]["processMonitorProduct"])
        click(driver, config["filters"]["clientFilter"])
        click(driver, processdbclient)
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Loading process logs...')]")))


        click(driver, config["filters"]["dateFilter"])
        click(driver, config["filters"]["Last30Days"])

        # Step 2: Open a new tab and switch to it
        driver.execute_script("window.open('about:blank', '_blank');")
        windows = driver.window_handles
        original_tab = windows[0]
        new_tab = windows[1]

        driver.switch_to.window(new_tab)
        driver.get("https://www.google.com")  # New tab simulating user activity

        print(" Switched to new tab. Waiting for 2 minutes...")
        time.sleep(120)  # Wait for 2 minutes on the new tab

        # Step 3: Switch back to the original Process Monitor tab
        driver.switch_to.window(original_tab)

        try:
            # Try to click the Process Monitor product again to verify the page is responsive
            click(driver, config["processMonitor"]["processMonitorProduct"])
            print(" Page is still responsive after tab switch — click action succeeded.")
        except Exception as e:
            assert False, f" Process Monitor page went blank or is unresponsive after tab switch: {e}"

    def test_process_monitor_page_remains_visible_after_tab_switch_for_unconfiguredclient(self, driver):

        
        click(driver, config["processMonitor"]["processMonitorProduct"])

        # Step 2: Open a new tab and switch to it
        driver.execute_script("window.open('about:blank', '_blank');")
        windows = driver.window_handles
        original_tab = windows[0]
        new_tab = windows[1]

        driver.switch_to.window(new_tab)
        driver.get("https://www.google.com")  # New tab simulating user activity

        print(" Switched to new tab. Waiting for 2 minutes...")
        time.sleep(120)  # Wait for 2 minutes on the new tab

        # Step 3: Switch back to the original Process Monitor tab
        driver.switch_to.window(original_tab)

        try:
            # Try to click the Process Monitor product again to verify the page is responsive
            click(driver, config["processMonitor"]["processMonitorProduct"])
            print(" Page is still responsive after tab switch — click action succeeded.")
        except Exception as e:
            assert False, f" Process Monitor page went blank or is unresponsive after tab switch: {e}"


class TestProcessMonitorTableValidations:
   

    def test_validate_specific_column_logic_after_filtering_client(self, driver):
        
        
        click(driver, config["processMonitor"]["processMonitorProduct"])

        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Loading process logs...')]")))
        

        # Apply filters
        click(driver, config["filters"]["clientFilter"])
        click(driver, processdbclient)
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Loading process logs...')]")))
        click(driver, config["filters"]["dateFilter"])
        click(driver, config["filters"]["Last30Days"])

        # Wait for table rows to load
        rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(
            (By.XPATH, "//table//tbody//tr")))
        assert len(rows) > 0, "No rows found after filtering by client"

        headers = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(
            (By.XPATH, "//table//thead//th")))
        header_labels = [h.text.strip() for h in headers]

        for i, row in enumerate(rows, 1):
            cells = row.find_elements(By.XPATH, "./td[contains(@class, 'MuiTableCell-body')]")
            cell_values = [cell.text.strip() for cell in cells]
            row_data = dict(zip(header_labels, cell_values))

            # 1. Client Validation
            if "Client" in row_data:
                expected_client_name = 'db' + env + 'client'
                actual_client_name = row_data["Client"]
                assert actual_client_name == expected_client_name, \
                    f"Row {i}: Expected client '{expected_client_name}', but found '{actual_client_name}'"
                

            # 2. Type Validation
            if "Type" in row_data:
                assert row_data["Type"] == "Payor Contract Analysis", \
                    f"Row {i}: Expected 'Payor Contract Analysis', got '{row_data['Type']}'"
                

     
            # 3. Disposition (Progress Bar) Validation
            if "Disposition" in header_labels:
                disposition_cell = cells[header_labels.index("Disposition")]
                progress_bars = disposition_cell.find_elements(By.XPATH, ".//div[contains(@style, 'width')]")

                if progress_bars:
                    style_attr = progress_bars[0].get_attribute("style")
                    match = re.search(r'width:\s*(\d+)%', style_attr)
                    assert match, f"Row {i}: Disposition style does not contain width percentage: '{style_attr}'"
                    progress_percent = int(match.group(1))
                    assert 0 <= progress_percent <= 100, \
                        f"Row {i}: Disposition progress percent out of range: {progress_percent}%"
                else:
                    print(f"Row {i}: No progress bar found in Disposition cell.")
                

#            # 4. Validate Number of Files (unlabeled column)
                num_files = None
                if len(cells) > len(header_labels):
                    num_files_col = cells[-1].text.strip()
                    assert num_files_col.isdigit(), f"Row {i}: Number of files should be numeric, got: {num_files_col}"
                    num_files = int(num_files_col)
                    assert num_files >= 0, f"Row {i}: Invalid file count ({num_files})"

                # 5. Description Validation (only if files exist)
                if "Description" in row_data:
                    if num_files and num_files > 0:
                        raw_filenames = row_data["Description"].split(", ")
                        for fn in raw_filenames:
                            match = re.search(r'(.+\.pdf)', fn, re.IGNORECASE)
                            assert match, f"Row {i}: Invalid filename in Description: '{fn}'"

                            # Extract file count if available, else assume 1
                            count_match = re.search(r'\((\d+)\s*files?\)', fn)
                            file_count = int(count_match.group(1)) if count_match else 1
                            assert file_count >= 1, f"Row {i}: Invalid file count ({file_count}) in: '{fn}'"
                    else:
                        print(f"Row {i}: File count = 0, skipping Description validation.")

class TestClientPersistAfterRefresh:

    def test_switch_client_and_verify_persistence_after_refresh(self, driver):
        click(driver, config['common']['settingsGearIcon'])
        click(driver, config["processMonitor"]["processMonitorProduct"])
        click(driver, config["processMonitor"]["clientSelectionDropdown"])
        click(driver, config["processMonitor"]["eclipseInsightsAutomationClient"])
        
        # Navigate to Process Monitor via settings gear

        click(driver, config['common']['settingsGearIcon'])
        click(driver, config["processMonitor"]["processMonitorProduct"])

        # Default client (before switching)
        client_dropdown_xpath = config["processMonitor"]["clientSelectionDropdown"]
        default_client = get_element_text(
            driver,
            client_dropdown_xpath
        )
        print(f"\nDefault client before change: {default_client}\n")

        # Updated client (select new client from dropdown)
        click(driver, config["processMonitor"]["clientSelectionDropdown"])
        click(driver, processdbclient)

        # Capture the updated client text immediately after selection
        client_dropdown_xpath = config["processMonitor"]["clientSelectionDropdown"]

        updated_client = get_element_text(
            driver,
            client_dropdown_xpath
        )

        expected_client = "DB" + env + "CLIENT"
        print(f"\nClient switched to: {updated_client}\n")

        # Verify updated client matches the expected name from config
        assert updated_client.upper() == expected_client.upper(), (
            f"Selected client '{updated_client}' does not match expected '{expected_client}' from config."
        )

        # Navigate again to Process Monitor to simulate refresh token behavior
        click(driver, config['common']['settingsGearIcon'])
        click(driver, config["processMonitor"]["processMonitorProduct"])

        # Verify persistence before browser refresh
        client_dropdown_xpath = config["processMonitor"]["clientSelectionDropdown"]

        client_before_refresh = get_element_text(
            driver,
            client_dropdown_xpath
        )

        print(f"\nClient selection before browser refresh: {client_before_refresh}\n")

        # Refresh the page
        driver.set_page_load_timeout(90)
        driver.get(processLogUrl)
        ActionChains(driver).send_keys(Keys.ENTER).perform()

        
        click_after_login(driver, config['common']['settingsGearIcon'])
        click(driver, config['client']['clientConfigurationButton'])
        click(driver, config["processMonitor"]["processMonitorProduct"])
        # Verify persistence after browser refresh
        client_dropdown_button = config["processMonitor"]["clientSelectionDropdown"]

        client_after_refresh = get_element_text(
            driver,
            client_dropdown_button
        )

        print(f"\nClient selection after browser refresh: {client_after_refresh}\n")

        # Compare and report
        if client_after_refresh == default_client:
            pytest.fail(
                f"After refresh, the default client '{default_client}' was displayed again instead of the updated client '{updated_client}'."
            )
        elif client_after_refresh == updated_client:
            print(f"\nUpdated client '{updated_client}' retained after refresh.\n")
        else:
            pytest.fail(
                f"After refresh, an unexpected client '{client_after_refresh}' was displayed "
                f"(neither default '{default_client}' nor updated '{updated_client}')."
            )



class TestCombinedFilterPersistence:

    def test_combined_filters_persist_after_idle_and_signalr_reconnect(self, driver):


        # Step 0: Get statuses from API
        endpoint = "/api/ProcessStatus?api-version=1.0"
        response, responseData = makeRequest('get', endpoint)

        assert response.status_code == 200, f"API call failed with {response.status_code}"
        assert responseData, "API returned no status items"

        selected_status_api = responseData[0].get("name")

        # Step 1: Navigate to Process Monitor
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        click(driver, config['common']['settingsGearIcon'])
        click(driver, config["processMonitor"]["processMonitorProduct"])

        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Loading process logs...')]")
            )
        )

        # Step 2: Apply Client Filter
        click(driver, config["filters"]["clientFilter"])
        click(driver, processdbclient)

        selected_client = get_element_text(
            driver,
            config["filters"]["clientFilter"]
        )

        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Loading process logs...')]")
            )
        )

        # Step 3: Apply Date Filter
        click(driver, config["filters"]["dateFilter"])
        click(driver, config["filters"]["Last30Days"])

        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Loading process logs...')]")
            )
        )

        selected_date = get_element_text(
            driver,
            config["filters"]["dateFilter"]
        )

        # Step 4: Apply Status Filter (Deselect all, then select one)
        click(driver, config["filters"]["statusFilter"])

        checkbox_xpath = config["filters"]["statusCheckboxes"]
        checkbox_inputs = driver.find_elements(By.XPATH, checkbox_xpath)

        # Unselect all selected checkboxes
        for index, checkbox in enumerate(checkbox_inputs, start=1):
            if checkbox.is_selected():
                parent_span_xpath = f"({checkbox_xpath})[{index}]/ancestor::span[1]"
                click(driver, parent_span_xpath)

        status_li_xpath = config["filters"]["statusclickoption"].format(statusName=selected_status_api)
        status_li = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, status_li_xpath))
        )

        checkbox_to_select = status_li.find_element(By.XPATH, config["filters"]["checkboxToSelectStatus"])

        if not checkbox_to_select.is_selected():
            click(driver, status_li_xpath)
    

        ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        # Step 5: Idle to trigger SignalR reconnect
        idle_seconds = 120
        time.sleep(idle_seconds)
        assert_no_signalr_close(driver)



        # Step 6: Validate filters after idle
        after_client = get_element_text(
            driver,
            config["filters"]["clientFilter"]
        )

        after_date = get_element_text(
            driver,
            config["filters"]["dateFilter"]
        )

        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        assert rows, "Table rows missing after idle period. Filters may have reset."

        status_after_idle = []
        for r in rows: 
            col_text = r.find_element(By.XPATH, "//table//tbody/tr/td[9]").text.strip()
            status_after_idle.append(col_text)

        # Step 7: Assertions for persistence
        assert after_client == selected_client, (
            f"Client filter did not persist. Before: {selected_client}, After: {after_client}"
        )

        assert after_date == selected_date, (
            f"Date filter did not persist. Before: {selected_date}, After: {after_date}"
        )

        assert all(s == selected_status_api for s in status_after_idle), (
            f"Status filter did not persist. Expected: {selected_status_api}, Found: {status_after_idle}"
        )

        print("All filters persisted after idle and SignalR reconnect without Selenium Wire.")


    def test_delete_all_test_data(self):
        deleteNonProdHelper()
