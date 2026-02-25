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

def save_config(config_data):
    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=4)

def read_config():
    with open(config_path, "r") as f:
        return json.load(f)

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
processdbclient = f"//span[normalize-space()='Virtus ProcessMonitor_LongFileName_Test_Data_Examplec']"
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
    driver.set_page_load_timeout(120)
    driver.get(processLogUrl)

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


class TestGridComponentsAndTableBehivour:

    def test_navigate_to_processlog(self, driver):
        click(driver, config["processMonitor"]["processMonitorProduct"])
        click(driver, config['processMonitor']['clientSelectionDropdown'])
        click(driver, config['processMonitor']['checkForOurClientOptionInProcessMonitorAsDefauls'].format(env=env))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, config['processMonitor']['processTable'])))
        click(driver, config['processMonitor']['DayButton'])
        click(driver, config['processMonitor']['Last30DaysOption'])
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, config['processMonitor']['processTable'])))

    @pytest.mark.skip(reason="Scheduled for re-activation following the completion of Task 4006 in Bug 3986. Keeping skipped to maintain clean test results for now")
    def test_TableSorting(self, driver):

        # Initialize the reusable validator
        validator = TableValidator(driver)
        
        # List of all columns you want to test
        columns_to_check = ["Type", "ID", "Description", "Client", "Processed On", "Duration", "Source", "State"]
        
        print("\nStarting Grid Sorting Validation...")
        
        # This list will store the names of columns that failed
        failed_columns = []

        print("\n--- Starting Global Sorting Validation ---")
        
        for col in columns_to_check:
            # Run the check and capture the result
            is_passed = validator.verify_sorting(col)
            
            # If it failed, add to our list
            if not is_passed:
                failed_columns.append(col)

        # --- THE MASTER ASSERTION ---
        # If the list is empty, it means everything passed.
        # If the list has items, the test fails and tells you exactly which columns were wrong.
        assert len(failed_columns) == 0, f"Sorting Test FAILED. Issues in columns: {', '.join(failed_columns)}"
        
        print("\n GLOBAL SORTING PASSED: All columns verified.")


    def test_TablePagination(self, driver):

        validator = TableValidator(driver)
        # Run Pagination Check
        pagination_passed = validator.verify_pagination()
        # Final Master Assert (Adding pagination to the success criteria)
        assert pagination_passed, "Table Pagination verification failed!"
        print("\n Pagination verified successfully.")


    def test_table_header_fontstyle_fontsize(self, driver):
            validator = TableValidator(driver)
            
            element_xpath = config['processMonitor']['TableHeaderFontSizeandStyle']
            expected_size = config['common']['expected_font_size']
            expected_font = config['common']['expected_font_family']

            assert validator.verify_typography(element_xpath, expected_size, expected_font), \
                f"Table header typography check failed! Expected {expected_font}, {expected_size}"
            
    def test_table_body_fontstyle_fontsize(self, driver):
        validator = TableValidator(driver)
        
        element_xpath = config['processMonitor']['TableBodyFontSizeandStyle']
        expected_size = config['common']['expected_font_size']
        expected_font = config['common']['expected_font_family']
        
        assert validator.verify_typography(element_xpath, expected_size, expected_font), \
            f"Table body typography check failed! Expected {expected_font}, {expected_size}"

    def create_process_log(self):

        config = read_config()

        post_data = {
            "id": None,
            "updatedBy": config["processLogApi"]["updatedBy"],
            "rowVersion": "",
            "type": config["processLogApi"]["type"],
            "status": "New",
            "startTimestamp": datetime.now(timezone.utc).isoformat(),
            "lastUpdatedTimestamp": datetime.now(timezone.utc).isoformat()
        }

        response, response_data = makeRequest(
            "post",
            "/api/ProcessLog?api-version=1.0",
            json=post_data
        )

        if response.status_code not in [200, 201]:
            print("POST URL:", response.url)
            print("Request body:", post_data)
            print("Response status:", response.status_code)
            print("Response body:", response.text)

        assert response.status_code in [200, 201], f"ProcessLog creation failed with {response.status_code}"
        assert "id" in response_data, "ProcessLog ID not returned"

        config["processLogApi"]["processLogId"] = response_data["id"]
        save_config(config)

        return response_data["id"]

    def test_post_process_log_success(self, driver):
        """
        Validate ProcessLog creation
        """
        process_log_id = self.create_process_log()
        assert process_log_id is not None

    def test_post_file_process_log_access(self, driver):
        """
        Validate FileProcessLog creation using ProcessLog ID
        """
        process_log_id = self.create_process_log()
        config = read_config()

        post_data = config["fileProcessLogApi"].copy()
        post_data["processLogId"] = process_log_id
        post_data["fileName"] = "ProcessMonitor_LongFileName_Test_Data_Example_Script"
        post_data["filePath"] = "/test/path/sample.txt"
        post_data["fileSize"] = 12345
        post_data["fileHash"] = "dummyhashvalue"

        response, response_data = makeRequest(
            "post",
            "/api/FileProcessLog?api-version=1.0",
            json=post_data
        )

        if response.status_code not in [200, 201]:
            print("POST URL:", response.url)
            print("Request body:", post_data)
            print("Response status:", response.status_code)
            print("Response body:", response.text)

        assert response.status_code in [200, 201], f"FileProcessLog creation failed with {response.status_code}"
        assert "id" in response_data, "FileProcessLog ID not returned"

        config["fileProcessLogApi"]["fileProcessLogId"] = response_data["id"]
        save_config(config)

    def test_table_column_overlap(self, driver):
        config = read_config()

        #Verify no columns overlap
        click(driver, config["processMonitor"]["processMonitorProduct"])
        validator = TableValidator(driver)
        overlaps = validator.check_overlap()
        if overlaps:
            for idx, colA, colB in overlaps:
                print(f"Overlap detected: '{colA}' overlaps into '{colB}'")
        assert len(overlaps) == 0, "Table column overlap detected!"

    def test_table_truncation(self, driver):
        config = read_config()

        #Verify that no column values are truncated
        click(driver, config["processMonitor"]["processMonitorProduct"])
        validator = TableValidator(driver)
        # List of columns to validate truncation
        columns_to_validate = ["Type", "ID", "Description", "Client", "Processed On", "Duration", "Source", "State"]

        truncated_issues = {}
        for col in columns_to_validate:
            truncated_cells = validator.check_truncation(col)
            if truncated_cells:
                truncated_issues[col] = truncated_cells
                for row_idx, val in truncated_cells:
                    print(f"Truncated value in '{col}' at row {row_idx}: '{val}'")

        assert len(truncated_issues) == 0, f"Truncation found in columns: {list(truncated_issues.keys())}"
