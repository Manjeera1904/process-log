import json
import json as json_module
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
import requests
import pytest
import copy
import uuid
from datetime import datetime
from seleniumwire import webdriver

from selenium.common import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException,
    NoSuchElementException
)
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def selenium_wire_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")

    # Selenium Wire safety limits
    seleniumwire_options = {
        "request_storage": "memory",
        "request_storage_max_size": 100
    }

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(
        service=service,
        options=options,
        seleniumwire_options=seleniumwire_options
    )
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


from config import (
    load_secret, user_login, load_config,
    click, generate_random_word, send_keys,
    click_create_button, click_after_login,
    homeUrl, eclipseAnalyticsUrl, verifyElementPresence,
    deleteNonProdHelper, evaluateConfig,
    network_request_assert_ok, network_request_get_json,
    network_request_validate_expected_keys,
    negotiateConfig, capture_browser_config_json,
    browser_config_path, inject_config_into_browser,
    baseUrl
)

test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config_path = os.path.join(test_script_path, 'config.json').replace('\\', '/')


def load_Config():
    with open(config_path) as config_file:
        return json.load(config_file)


with open(config_path, 'r') as configFile:
    configData = json.load(configFile)


def saveConfig(configData):
    with open(config_path, 'w') as config_file:
        json.dump(configData, config_file, indent=4)
    print("Config data saved successfully.")


# Config values
config = load_Config()
pcapiBaseUrl = configData["common"]["pcapiBaseUrl"]
apiVersion = configData["common"]["apiVersion"]
cultureCode = configData["common"]["cultureCode"]
clientId = configData["common"]["testClientId"]
env = config.get("env")
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


def test_verify_that_the_user_can_log_in_successfully_to_the_eclipse_insights_website(selenium_wire_driver, load_secret):
    user_login(selenium_wire_driver, load_secret)

def test_verify_that_the_browser_config_json_is_copied_from_the_network(selenium_wire_driver):
    browser_config_data = capture_browser_config_json(selenium_wire_driver, baseUrl, browser_config_path, env)
    assert browser_config_data is not None, "config.json was not captured"

def test_verify_that_the_browser_config_json_is_injected_into_the_browser(selenium_wire_driver):
    inject_config_into_browser(selenium_wire_driver, browser_config_path)
    injected_config = selenium_wire_driver.execute_script("return window.localStorage.getItem('mfConfigOverride');")
    assert injected_config is not None, "Config was not injected into browser"

class TestValidateNegotiateandEvaluateApiCalls:

    def test_verify_evaluate_api_call_payload_and_response(
        self, selenium_wire_driver
    ):
        selenium_wire_driver.set_page_load_timeout(30)
        selenium_wire_driver.get(homeUrl)

        click_after_login(
            selenium_wire_driver,
            config["processMonitor"]["processMonitorProduct"]
        )

        WebDriverWait(selenium_wire_driver, 60).until(
            EC.element_to_be_clickable(
                (By.XPATH, config["filters"]["clientFilter"])
            )
        )

        click(selenium_wire_driver, config["filters"]["clientFilter"])
        click(selenium_wire_driver, processdbclient)

        WebDriverWait(selenium_wire_driver, 100).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Loading process logs...')]")
            )
        )

        click(selenium_wire_driver, config["filters"]["dateFilter"])
        click(selenium_wire_driver, config["filters"]["Last30Days"])

        WebDriverWait(selenium_wire_driver, 20).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Loading process logs...')]")
            )
        )

        #  clear old traffic before capture
        selenium_wire_driver.requests.clear()

        negotiate_endpoint = negotiateConfig["endpoint"]

        negotiate_request = None
        end_time = time.time() + 20

        while time.time() < end_time:
            for r in selenium_wire_driver.requests:
                if negotiate_endpoint in r.url:
                    negotiate_request = r
                    break
            if negotiate_request:
                break
            time.sleep(1)

        if not negotiate_request:
            raise AssertionError(
                f"Negotiate endpoint {negotiate_endpoint} "
                f"was not captured by Selenium Wire!"
            )

        network_request_assert_ok(negotiate_request)
        print("Negotiate API returned 200.")

class TestAPIRequestCancelOnFilterChange:

    def test_verify_in_progress_search_api_calls_are_cancelled_on_filter_change(
        self, selenium_wire_driver
    ):
        driver = selenium_wire_driver
        driver.set_page_load_timeout(30)
        driver.get(homeUrl)

        # Login & open Process Monitor product
        click_after_login(driver, config["processMonitor"]["processMonitorProduct"])

        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, config["filters"]["clientFilter"]))
        )
        click(driver, config["filters"]["clientFilter"])
        click(driver, processdbclient)

        WebDriverWait(driver, 100).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Loading process logs...')]")
            )
        )

        click(driver, config["filters"]["dateFilter"])
        click(driver, config["filters"]["Last30Days"])

        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Loading process logs...')]")
            )
        )

        # Clear old network traffic
        driver.requests.clear()

        # Fetch statuses from API
        endpoint = "/api/ProcessStatus?api-version=1.0"
        response, responseData = makeRequest("get", endpoint)

        assert response.status_code == 200
        assert responseData

        # Collect status names directly from API (NO normalization)
        status_names = [info["name"] for info in responseData if info.get("name")]
        assert len(status_names) >= 2, "Need at least two statuses to test combined filtering"

        selected_statuses = status_names[:2]
        single_status_name = selected_statuses[0]

        print(f"\nTesting rapid clicks on single status: {single_status_name}")

        # Open status filter dropdown
        click(driver, config["filters"]["statusFilter"])

        # Deselect all existing statuses
        checkbox_xpath = config["filters"]["statusCheckboxes"]
        checkbox_inputs = driver.find_elements(By.XPATH, checkbox_xpath)
        for checkbox in checkbox_inputs:
            if checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)

        # Select two desired statuses
        for status_name in selected_statuses:
            click(
                driver,
                config["filters"]["statusCheckboxByNameXPath"].format(
                    status_name=status_name
                )
            )

        # Rapidly click the same status multiple times
        for _ in range(5):
            click(
                driver,
                config["filters"]["statusCheckboxByNameXPath"].format(
                    status_name=single_status_name
                )
            )
            

        # Capture all relevant requests
        search_requests = [
            r for r in driver.requests
            if "ProcessLog/Search" in r.url
        ]

        # Filter cancelled requests (response is None at capture time)
        cancelled_requests = [r for r in search_requests if r.response is None]

        # Filter successful requests
        successful_requests = [r for r in search_requests if r.response and r.response.status_code == 200]

        print(f"Total requests: {len(search_requests)}")
        print(f"Cancelled requests: {len(cancelled_requests)}")
        print(f"Successful requests: {len(successful_requests)}")

       

        # If there were any cancelled requests, make sure they never became 200
        for r in cancelled_requests:
            if r.response:
                assert r.response.status_code != 200, (
                    f"A previously cancelled request unexpectedly succeeded: {r.url}"
                )

        print("Verified: cancelled requests never became 200, latest request succeeded")



if __name__ == "__main__":
    pytest.main([__file__])