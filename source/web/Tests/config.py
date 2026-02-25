import datetime
import json
import time
import os
import inspect
import random
import string
import traceback
import re
from time import sleep
import pyautogui
import requests
from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
import inspect
test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
browser_config_path = os.path.join(test_script_path, "browser_config.json").replace('\\', '/')
# Load Configuration
def load_config(path=os.path.join(test_script_path, 'config.json').replace('\\', '/')):
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise FileNotFoundError(f"Failed to load config file: {e}")

config = load_config()
baseUrl = config.get("baseUrl")
apiUrl = config.get("apiBaseUrl")
homeUrl = config.get("platformUrl")
env = config.get("env")
eclipseAnalyticsUrl = f"{baseUrl}/eclipse-analytics/reports"
tenantUrl = f"{baseUrl}/platform-core/tenant"
clientUrl = f"{baseUrl}/platform-core/client"
roleUrl = f"{baseUrl}/platform-core/role"
userUrl = f"{baseUrl}/platform-core/user"
productUrl = f"{baseUrl}/platform-core/product"
datasourceUrl = f"{baseUrl}/platform-core/data-source"
processLogUrl=f"{baseUrl}/process-log"

def capture_browser_config_json(driver, url, save_path, env, timeout=15):
    driver.get(url)
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    start_time = time.time()
    config_data = None

    while time.time() - start_time < timeout:
        # Get only config.json URLs from performance entries
        entries = driver.execute_script("""
            return window.performance.getEntries()
                .filter(e => e.name && e.name.includes("config.json"))
                .map(e => e.name);
        """)

        for entry_url in entries:
            resp = requests.get(entry_url)
            if resp.status_code == 200:
                config_data = resp.json()

                # Modify only host_app and web_process_log
                for item in config_data:
                    if not isinstance(item, dict):
                        continue
                    if item.get("name") == "host_app":
                        if "apiUrl" in item:
                            item["apiUrl"] = f"https://platform-core-api.{env}.eclipsevantage.com"

                    elif item.get("name") == "web_process_log":
                        if "url" in item:
                            item["url"] = f"https://process-logging-web.{env}.eclipsevantage.com"
                        if "apiUrl" in item:
                            item["apiUrl"] = f"https://process-logging-api.{env}.eclipsevantage.com"
                        
                    elif item.get("name") == "web_platform_core":
                        if "url" in item:
                            item["url"] = f"https://platform-core-web.{env}.eclipsevantage.com"
                        if "apiUrl" in item:
                            item["apiUrl"] = f"https://platform-core-api.{env}.eclipsevantage.com"

                # Save the modified config.json
                if os.path.exists(save_path):
                    os.remove(save_path)
                with open(save_path, "w") as f:
                    json.dump(config_data, f, indent=4)

                print(f"[INFO] config.json saved to {save_path}")
                return config_data

        time.sleep(1)

    print("[WARN] config.json not found")
    return None

    
def inject_config_into_browser(driver, config_path):
    """
    Reads the saved browser_config.json and injects it into localStorage.
    """
    with open(config_path, "r") as f:
        config_json = json.load(f)

    config_str = json.dumps(config_json)

    script = f"""
        console.clear();
        console.log('Allow pasting enabled');
        localStorage.setItem("mfConfigOverride", JSON.stringify({config_str}));
        console.log("Config injected into localStorage as mfConfigOverride");
    """
    driver.execute_script(script)

def generate_random_word(prefix='test_', length=4):
    return prefix + ''.join(random.choices(string.ascii_lowercase, k=length))


def log_failure(error_message, xpath=None):
    frame = inspect.stack()[2]
    file_name = os.path.basename(frame.filename)
    line_number = frame.lineno
    function_name = frame.function

    cls_name = type(frame.frame.f_locals.get('self')).__name__ if 'self' in frame.frame.f_locals else None
    caller = f"{cls_name}.{function_name}" if cls_name else function_name

    log_message = f"Failure in {file_name} file, method '{caller}', line {line_number}: {error_message}"

    if xpath:
        log_message += f" | XPath: {xpath}"

    print(log_message)


def click(driver, xpath, retries=3, timeout=20, error_message="Element click failed"):
    for attempt in range(10):  # Max 10 attempts for ElementClickInterceptedException
        try:
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            return
        except ElementClickInterceptedException as e:
            if attempt == 9:
                log_failure(f"{error_message} - {type(e).__name__}: {str(e)}", xpath)
                raise AssertionError(f"{error_message}: Could not click element with XPath: {xpath} - {type(e).__name__}: {str(e)}")
            sleep(5)
        except StaleElementReferenceException as e:
            if attempt == retries - 1:
                log_failure(f"{error_message} - {type(e).__name__}: {str(e)}", xpath)
                raise AssertionError(f"{error_message}: Could not click element with XPath: {xpath} - {type(e).__name__}: {str(e)}")
            sleep(2)
        except Exception as e:
            if attempt == retries - 1:
                log_failure(f"{error_message} - {type(e).__name__}: {str(e)}", xpath)
                raise AssertionError(f"{error_message}: Could not click element with XPath: {xpath} - {type(e).__name__}: {str(e)}")

def click_after_login(driver, xpath, retries=3, timeout=200, error_message="Element click failed"):
    for attempt in range(retries):
        try:
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            return
        except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            if attempt == retries - 1:
                log_failure(f"{error_message} - {type(e).__name__}: {str(e)}", xpath)
                raise AssertionError(f"{error_message}: Could not click element with XPath: {xpath} - {type(e).__name__}: {str(e)}")
            sleep(2)
        except Exception as e:
            if isinstance(e, TimeoutException):
                driver.refresh()
                sleep(3)
            elif attempt == retries - 1:
                log_failure(f"{error_message} - {type(e).__name__}: {str(e)}", xpath)
                raise AssertionError(f"{error_message}: Could not click element with XPath: {xpath} - {type(e).__name__}: {str(e)}")
            else:
                sleep(2)

def send_keys(driver, xpath, keys, timeout=20, element_name=""):
    for attempt in range(3):
        try:
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(keys)
            return
        except Exception as e:
            if attempt == 2:
                frame = inspect.stack()[1]
                log_failure(
                    f"Failed to send keys to element '{element_name}' - {type(e).__name__}: {str(e)}",
                    xpath
                )
                raise AssertionError(
                    f"Failed to send keys in function '{frame.function}' (line {frame.lineno}) "
                    f"to element '{element_name}' with XPath: {xpath} - Error: {str(e)}"
                )
            sleep(1)


def verifyElementPresence(driver, xpath, timeout=20, elementName="element"):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        frame = inspect.stack()[1]
        caller_function_name = frame.function
        line_number = frame.lineno

        log_failure(f"'{elementName}' not found", xpath)

        raise AssertionError(
            f"'{elementName}' not found in function '{caller_function_name}' (line {line_number}) with XPath: {xpath}"
        )

def verifyElementNotPresent(driver, xpath, timeout=20, elementName="element"):
    try:
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        frame = inspect.stack()[1]
        caller_function_name = frame.function
        line_number = frame.lineno

        log_failure(f"'{elementName}' was found unexpectedly", xpath)

        raise AssertionError(
            f"'{elementName}' was found unexpectedly in function '{caller_function_name}' (line {line_number}) with XPath: {xpath}"
        )

def hover(driver, xpath, timeout=10, elementName="element"):
    try:
        element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        ActionChains(driver).move_to_element(element).perform()
    except Exception as e:
        frame = inspect.stack()[1]
        caller_function_name = frame.function
        line_number = frame.lineno
        raise AssertionError(
            f"Hover failed in function '{caller_function_name}' (line {line_number}) for '{elementName}' with XPath: {xpath} - Error: {str(e)}"
        )

def verifyElementNotClickable(driver, xpath, elementName="Element"):
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        log_failure(f"{elementName} is clickable, but it shouldn't be.", xpath)
        print(f"{elementName} is clickable, but it shouldn't be.")
    except TimeoutException:
        frame = inspect.stack()[1]
        caller_function_name = frame.function
        line_number = frame.lineno
        print(f"{elementName} is not clickable as expected in function '{caller_function_name}' (line {line_number}) with XPath: {xpath}")

def hover_and_get_tooltip(driver, button_xpath, tooltip_xpath, elementName="tooltip"):
    try:
        button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, button_xpath)))
        ActionChains(driver).move_to_element(button).perform()
        tooltip = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, tooltip_xpath)))
        return tooltip.text.strip().splitlines()[0]
    except Exception as e:
        frame = inspect.stack()[1]
        caller_function_name = frame.function
        line_number = frame.lineno
        raise AssertionError(
            f"Tooltip retrieval failed in function '{caller_function_name}' (line {line_number}) for '{elementName}' - Error: {str(e)}"
        )
def verify_tooltip(driver, element, expected_tooltip):
    ActionChains(driver).move_to_element(element).perform()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, f'//div[contains(@class, "MuiTooltip-tooltip") and contains(text(), "{expected_tooltip}")]'))
    )
    tooltip_element = driver.find_element(By.XPATH, f'//div[contains(@class, "MuiTooltip-tooltip") and contains(text(), "{expected_tooltip}")]')
    tooltip_text = tooltip_element.text.split('\n')[0]
    assert tooltip_text == expected_tooltip, f"Expected tooltip text to be '{expected_tooltip}' but got '{tooltip_text}'"

def makeRequest(method, endpoint, data=None, isJsonResponse="true", header=None):
    url = f"{apiUrl}{endpoint}"
    print(f"\n{method.upper()} Request to URL: {url}")

    # Use headers or default with token
    if header is None:
        header = {}
    if "Authorization" not in header:
        token = config.get("tokenApi", {}).get("token")
        if not token:
            raise ValueError("Authorization token not found in config['tokenApi']['token']")
        header["Authorization"] = f"Bearer {token}"

    print("Request Headers:", json.dumps(header, indent=4))
    if data:
        print("Request Body:", json.dumps(data, indent=4))

    try:
        if method == 'post':
            response = requests.post(url, json=data, verify=False, headers=header)
        elif method == 'get':
            response = requests.get(url, verify=False, headers=header)
        elif method == 'delete':
            response = requests.delete(url, json=data, verify=False, headers=header)
        elif method == 'put':
            response = requests.put(url, json=data, verify=False, headers=header)
        else:
            raise ValueError("Invalid method type provided.")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        raise

    print(f"Response Status Code: {response.status_code}")
    print("Response Headers:", json.dumps(dict(response.headers), indent=4))

    try:
        if isJsonResponse.lower() == "true":
            response_data = response.json()
            print("Response Body (JSON):", json.dumps(response_data, indent=4))
        else:
            response_data = {"content": response.content}
            print("Response Body (Raw):", response.content)
    except json.JSONDecodeError:
        print("Response Body is not JSON:", response.text)
        response_data = {}

    return response, response_data

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def incognitoDriver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--incognito")
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

platformUrl = config.get("platformUrl")

@pytest.fixture(scope="module")
def load_secret():
    json_file = os.path.join(test_script_path, 'secrets.json')
    try:
        with open(json_file, 'r') as file:
            secrets = json.load(file)

        for secret in secrets:
            if secret['SecretName'] == 'eclipse-testautomation-user-02':
                UserId = secret['SecretValue']['UserId']
                Password = secret['SecretValue']['Password']
                TotpKey = secret['SecretValue'].get('TotpKey', None)
        return UserId, Password, TotpKey
    except Exception as e:
        raise AssertionError(f"Failed to load secret: {str(e)}")


@pytest.fixture(scope="module")
def loadincognito():
    json_file = os.path.join(test_script_path, 'secrets.json')
    try:
        with open(json_file, 'r') as file:
            secrets = json.load(file)

        for secret in secrets:
            if secret['SecretName'] == 'eclipse-testautomation-user-01':
                UserId = secret['SecretValue']['UserId']
                Password = secret['SecretValue']['Password']
                TotpKey = secret['SecretValue'].get('TotpKey', None)
        return UserId, Password, TotpKey
    except Exception as e:
        raise AssertionError(f"Failed to load secret: {str(e)}")

@pytest.fixture(scope="module")
def loadTestUserFour():
    json_file = os.path.join(test_script_path, 'secrets.json')
    try:
        with open(json_file, 'r') as file:
            secrets = json.load(file)

        for secret in secrets:
            if secret['SecretName'] == 'eclipse-testautomation-user-04':
                UserId = secret['SecretValue']['UserId']
                Password = secret['SecretValue']['Password']
                TotpKey = secret['SecretValue'].get('TotpKey', None)
        return UserId, Password, TotpKey
    except Exception as e:
        raise AssertionError(f"Failed to load secret: {str(e)}")

def verifyDefaultClientName(driver, xpath, expectedText, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        actualText = driver.find_element(By.XPATH, xpath).text
        assert actualText == expectedText, f"Expected: '{expectedText}' but got: '{actualText}'"

    except TimeoutException:
        try:
            actualText = driver.find_element(By.XPATH, xpath).text
            error_message = f"Expected: '{expectedText}' but got: '{actualText}'"
            log_failure(error_message, xpath)
            raise AssertionError(error_message)
        except NoSuchElementException:
            # Now search for any <h6> starting with 'Viewing content for:' to report what's actually there
            h6_elements = driver.find_elements(By.XPATH, "//h6[starts-with(text(), 'Viewing content for: ')]")
            if h6_elements:
                found_texts = [el.text for el in h6_elements]
                error_message = f"Expected: '{expectedText}' but found: {found_texts}"
                log_failure(error_message, xpath)
                raise AssertionError(error_message)
            else:
                error_message = f"No element found with XPath: '{xpath}' and no <h6> with 'Viewing content for:' found"
                log_failure(error_message, xpath)
                raise AssertionError(error_message)
    except AssertionError as e:
        log_failure(str(e), xpath)
        raise
def verifyDefaultClientNameAlphabetically(driver, xpath, expectedText, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        actualText = driver.find_element(By.XPATH, xpath).text
        assert actualText == expectedText, f"Expected alphabetically sorted client: '{expectedText}', but got: '{actualText}'"

    except TimeoutException:
        try:
            actualText = driver.find_element(By.XPATH, xpath).text
            error_message = f"Expected alphabetically sorted client: '{expectedText}', but got: '{actualText}'"
            log_failure(error_message, xpath)
            raise AssertionError(error_message)
        except NoSuchElementException:
            # Check for any <h6> starting with 'Viewing content for:' and report all found
            h6_elements = driver.find_elements(By.XPATH, "//h6[starts-with(text(), 'Viewing content for: ')]")
            if h6_elements:
                found_texts = [el.text for el in h6_elements]
                error_message = f"Expected alphabetically sorted client: '{expectedText}', but found: {found_texts}"
                log_failure(error_message, xpath)
                raise AssertionError(error_message)
            else:
                error_message = f"No element found with XPath: '{xpath}' and no <h6> with 'Viewing content for:' found"
                log_failure(error_message, xpath)
                raise AssertionError(error_message)
    except AssertionError as e:
        log_failure(str(e), xpath)
        raise

def deleteNonProdHelper():
    # Load fresh config data
    with open(os.path.join(test_script_path, 'config.json'), 'r') as config_file:
        config_data = json.load(config_file)

    # Get data from config
    nonProdHelper_post_data = config_data.get('nonProdHelperApi')
    version_id = config_data.get("common", {}).get("versionId")
    token = config_data.get("tokenApi", {}).get("token")

    # Build request
    base_url = config['apiBaseUrl']
    endpoint = f"/api/NonProdHelper?api-version={version_id}"
    url = f"{base_url}{endpoint}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.delete(url, json=nonProdHelper_post_data, headers=headers, verify=False)

    if response.status_code != 200:
        print("\n======= DEBUG INFO =======")
        print(f"URL: {url}")
        print("Headers:", headers)
        print("Payload:", nonProdHelper_post_data)
        print(f"Status: {response.status_code}")
        print("Response:", response.text)
        print("==========================\n")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

def clickCorrespondingElement(driver, text):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[text()='{text}']/following::button[1]"))
        ).click()
    except Exception as e:
        raise AssertionError(f"Click failed: {e}")

def clickCorrespondingToggle(driver, dropdownText):
    # Locate the dropdown by its role and visible text
    dropdownXPath = f"//div[@role='combobox' and normalize-space(text())='{dropdownText}']"
    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, dropdownXPath))
    )
    assert dropdown.is_displayed(), "Dropdown is not visible"

    # Go to parent <p>, then next sibling <div> with the checkbox
    toggleXPath = f"{dropdownXPath}/ancestor::p/following-sibling::div//input[@type='checkbox']"
    toggleCheckbox = driver.find_element(By.XPATH, toggleXPath)

    # Optional: highlight before clicking
    driver.execute_script("arguments[0].style.border='2px solid red'", toggleCheckbox)
    toggleCheckbox.click()

def nonclickable(driver, xpath, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        log_failure(f"Element with XPath '{xpath}' was clickable and clicked, but it shouldn't be.", xpath)
    except Exception:
        pass



def verifyToggleIsOn(driver, dropdownText):
    dropdownXPath = f"//div[@role='combobox' and normalize-space(text())='{dropdownText}']"
    dropdown = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, dropdownXPath))
    )
    assert dropdown.is_displayed(), "Dropdown is not visible"
    print(dropdown.get_attribute('outerHTML'))

    rootContainer = dropdown.find_element(By.XPATH, "./ancestor::div[contains(@class, 'MuiBox-root')]")

    toggleCheckbox = rootContainer.find_element(By.XPATH, ".//input[@type='checkbox']")
    assert toggleCheckbox.is_selected(), "Toggle checkbox is not ON"
    driver.execute_script("arguments[0].style.border='2px solid red'", toggleCheckbox)

def enableAllTogglesByDropdownText(driver):
    dropdownTexts = [
        "Edit Client Data Sources", "Edit Clients", "Edit Client Products", "Edit Client Status",
        "Edit Client Tenants", "Edit Data Sources", "Edit Roles", "Edit Tenants", "Edit User Clients",
        "Edit User Roles", "Edit Users", "View Applications", "View Client Data Sources", "View Client Products",
        "View Client Tenants", "View Clients", "View Data Sources", "View Products", "View Roles", "View Tenants",
        "View User Clients", "View User Roles", "View Users"
    ]

    for label in dropdownTexts:
        try:
            print(f"Attempting to toggle: {label}")

            # Locate the dropdown and checkbox directly
            dropdown = driver.find_element(By.XPATH, f"//div[@role='combobox' and normalize-space()='{label}']")
            checkbox = driver.find_element(By.XPATH,
                                           f"//div[@role='combobox' and normalize-space()='{label}']/ancestor::p/following-sibling::div//input[@type='checkbox']")

            # If the checkbox is not selected, click it
            if not checkbox.is_selected():
                driver.execute_script("arguments[0].style.border='2px solid red'", checkbox)
                checkbox.click()
                print(f"Successfully toggled ON: {label}")
            else:
                print(f"Already ON: {label}")

        except Exception as e:
            print(f"Error toggling '{label}': {str(e)}")
            driver.save_screenshot(f"error_{label.replace(' ', '_')}.png")

def clickable(driver, xpath, retries=3, timeout=20, element_name=""):
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            return
        except StaleElementReferenceException as e:
            if attempt == retries - 1:
                frame = inspect.stack()[1]
                function_name = frame.function
                line_number = frame.lineno
                log_failure(
                    f"Stale element error in function '{function_name}' (line {line_number}): "
                    f"Element '{element_name}' not clickable (XPath: {xpath})"
                )
                raise AssertionError(
                    f"Stale element error in function '{function_name}' (line {line_number}): "
                    f"Element '{element_name}' not clickable (XPath: {xpath})"
                ) from e
            sleep(1)
        except TimeoutException as e:
            if attempt == retries - 1:
                frame = inspect.stack()[1]
                function_name = frame.function
                line_number = frame.lineno
                log_failure(
                    f"Timeout in function '{function_name}' (line {line_number}): "
                    f"Element '{element_name}' not clickable (XPath: {xpath})"
                )
                raise AssertionError(
                    f"Timeout in function '{function_name}' (line {line_number}): "
                    f"Element '{element_name}' not clickable (XPath: {xpath})"
                ) from e
        except ElementNotInteractableException as e:
            if attempt == retries - 1:
                frame = inspect.stack()[1]
                function_name = frame.function
                line_number = frame.lineno
                log_failure(
                    f"Element not interactable in function '{function_name}' (line {line_number}): "
                    f"Element '{element_name}' exists but is not interactable (XPath: {xpath})"
                )
                raise AssertionError(
                    f"Element not interactable in function '{function_name}' (line {line_number}): "
                    f"Element '{element_name}' exists but is not interactable (XPath: {xpath})"
                ) from e
        except Exception as e:
            if attempt == retries - 1:
                frame = inspect.stack()[1]
                function_name = frame.function
                line_number = frame.lineno
                log_failure(
                    f"Error in function '{function_name}' (line {line_number}): "
                    f"Failed to click '{element_name}': {str(e)} (XPath: {xpath})"
                )
                raise AssertionError(
                    f"Error in function '{function_name}' (line {line_number}): "
                    f"Failed to click '{element_name}': {str(e)} (XPath: {xpath})"
                ) from e

def verifyOverlayLoadingIconAppearsAndDisappears(driver, elementName="loading overlay"):
    xpath = "//div[@class='MuiBox-root css-1lb6n3v']//div[@class='MuiBox-root css-ff4fss']//div[@class='MuiBox-root css-dh9067']"

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        return

    for attempt in range(4):
        try:
            WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.XPATH, xpath)))
            return
        except TimeoutException:
            if attempt == 3:
                frame = inspect.stack()[1]
                raise AssertionError(
                    f"'{elementName}' did not disappear in function '{frame.function}' "
                    f"(line {frame.lineno}) with XPath: {xpath}"
                )


def click_save_button(driver):
    click(driver, config['common']['saveButton'])
    sleep(3)


def click_create_button(driver):
    click(driver, config['common']['createButton'])
    sleep(3)

evaluateConfig = {
    "endpoint": config["evaluateEndpoint"],
    "rootKeys": config["evaluateRootKeys"],
    "connectionKeys": config["evaluateConnectionKeys"],
    "payloadKeys": config["evaluatePayloadKeys"]
}

negotiateConfig = {
    "endpoint": config["negotiateEndpoint"]
}

def network_request_assert_ok(req):
    """Assert response is HTTP 200."""
    assert req.response and req.response.status_code == 200, \
        f"Expected 200, got {req.response.status_code if req.response else 'No response'}"


def network_request_get_json(req):
    """Extract JSON body safely."""
    try:
        return json.loads(req.body.decode("utf-8"))
    except Exception:
        pytest.fail("Request body is not valid JSON")


def network_request_validate_expected_keys(
    data,
    root_keys,
    connection_keys=None,
    payload_keys=None
):
    missing = []

    #  1. Validate root-level keys
    for key in root_keys:
        if key not in data:
            missing.append(key)

    #  2. Validate connection.* keys
    if connection_keys:
        if "connection" not in data:
            missing.append("connection")
        else:
            for key in connection_keys:
                if key not in data["connection"]:
                    missing.append(f"connection.{key}")

    # 3. Validate payload.* keys
    if payload_keys:
        if "payload" not in data:
            missing.append("payload")
        else:
            for key in payload_keys:
                if key not in data["payload"]:
                    missing.append(f"payload.{key}")

    if missing:
        missing = list(set(missing))

        missing_root = [m for m in missing if "." not in m]
        missing_nested = [m for m in missing if "." in m]

        msg = []
        if missing_root:
            msg.append(f"Missing root keys: {missing_root}")
        if missing_nested:
            msg.append(f"Missing nested keys: {missing_nested}")

        raise AssertionError(" | ".join(msg))

def get_element_text(driver, xpath, timeout=15, retries=3):
    wait = WebDriverWait(driver, timeout)

    for attempt in range(retries):
        try:
            element = wait.until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            text = element.text.strip()
            if text:
                return text
        except StaleElementReferenceException:
            time.sleep(0.5)

    raise Exception(f"Failed to get stable text for element: {xpath}")


def login(driver, email, password, totp_key):
    for attempt in range(2):
        try:
            driver.get(baseUrl)
            WebDriverWait(driver, 40).until(EC.number_of_windows_to_be(2))
            driver.switch_to.window(driver.window_handles[1])
            send_keys(driver, config['login']['emailInput'], email, timeout=40)
            click(driver, config['login']['nextButton'], timeout=40)
            sleep(2)#small delay
            send_keys(driver, config['login']['passwordInput'], password, timeout=40)
            click(driver, config['login']['signInButton'], timeout=40)
            sleep(2)#small delay
            click(driver, config['login']['staySignedInYesButton'], timeout=40)
            WebDriverWait(driver, 40).until(EC.number_of_windows_to_be(1))
            driver.switch_to.window(driver.window_handles[0])
            return
        except Exception as e:
            if attempt == 0:
                time.sleep(5)
            else:
                raise AssertionError(f"Login failed after retry: {str(e)}")

def user_login(driver, load_secret):
    email, password, totp_secret = load_secret
    login(driver, email, password, totp_secret)

def click_with_retry(driver, element_or_locator, retries=3, delay=1):
    """
    Click an element with retry logic to handle stale element references
    
    Args:
        driver: WebDriver instance
        element_or_locator: Either a WebElement or a tuple (By, locator)
        retries: Number of retry attempts
        delay: Delay between retries in seconds
    """
    
    attempt = 0
    while attempt < retries:
        try:
            if isinstance(element_or_locator, tuple):
                # If it's a locator tuple (By.XPATH, "xpath_string")
                by, locator = element_or_locator
                element = driver.find_element(by, locator)
                element.click()
            else:
                # If it's already a WebElement
                element_or_locator.click()
            return True
        except StaleElementReferenceException:
            attempt += 1
            if attempt >= retries:
                raise
            time.sleep(delay)
    return False

def get_text_lowercase(dropdown, retries=5):
   
    for attempt in range(retries):
        try:
            text = dropdown.text.strip()
            return text.lower() if text else ""
        except StaleElementReferenceException:
            if attempt < retries - 1:
                import time
                time.sleep(0.3)
                continue
            return ""  # Return empty if permanently stale
    
    return ""

def get_element_text_safely(element, retries=5):

    for attempt in range(retries):
        try:
            # Try to get the text
            text = element.text.strip()
            return text
        except StaleElementReferenceException:
            if attempt < retries - 1:
                # Wait briefly before retry
                import time
                time.sleep(0.5)
                continue
            else:
                # Last attempt failed, re-raise the exception
                raise StaleElementReferenceException("Failed to get xpath text after retries")
            
        

class TableValidator:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def get_column_data(self, column_name):
        """
        Dynamically finds the column index based on the header name 
        and extracts data from all rows.
        """
        # 1. Find the column index (e.g., 'Type' is index 2)
        # 1. Find the index
        headers = self.driver.find_elements(By.XPATH, config['processMonitor']['processTableHeader'])
        col_index = -1
        for i, h in enumerate(headers):
            if column_name in h.text:
                col_index = i + 1
                break
                
        if col_index == -1:
            return []

        # 2. Use the corrected config access
        # Ensure you use square brackets [] for config
        cell_xpath = config['processMonitor']['processTableColumnIndex'].format(col_index=col_index)
        
        cells = self.driver.find_elements(By.XPATH, cell_xpath)
        return [get_text_lowercase(c).split('\n')[0] for c in cells if get_element_text_safely(c)]

    def verify_sorting(self, column_name):
        """Clicks the header and verifies both Asc and Desc order."""
        try: 
            print(f"\n--- Testing {column_name} column ---")
            
            # Test Ascending
            print(f"Clicking {column_name} for ascending sort...")
            
            # Find and click the header (FIRST TIME)
            header_xpath = f"//th//span[normalize-space()='{column_name}']"
            header_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, header_xpath))
            )
            click_with_retry(driver, header_element)
            time.sleep(2)  # Wait for sorting to complete
            
            data_asc = self.get_column_data(column_name)
            if not data_asc:
                print(f"No data extracted for {column_name}")
                return False
                
            asc_sorted = data_asc == sorted(data_asc)
            print(f"Ascending sorted: {asc_sorted}")

            # Test Descending
            print(f"Clicking {column_name} again for descending sort...")
            
            # RE-FIND the header element (it's stale after first click)
            header_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, header_xpath))
            )
            click_with_retry(driver, header_element)
            time.sleep(2)
            
            data_desc = self.get_column_data(column_name)
            desc_sorted = data_desc == sorted(data_desc, reverse=True)
            print(f"Descending sorted: {desc_sorted}")

            if asc_sorted and desc_sorted:
                print(f" {column_name}: PASSED")
                return True
            else:
                print(f" {column_name}: FAILED (Asc:{asc_sorted}, Desc:{desc_sorted})")
                return False
                
        except Exception as e:
            print(f" {column_name}: Error - {str(e)}")
            traceback.print_exc()
            return False
        

    def verify_pagination(self):
        """Verifies that Next and Previous page buttons update the table."""
        try:
            # 1. Get initial range (e.g., "1-20 of 742")
            initial_range = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, config['processMonitor']['paginationInfo'])
            )).text
            
            # 2. Click Next Page
            next_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, config['processMonitor']['goToNextPageButton'])
            ))
            next_btn.click()
            
            # 3. Wait for the range text to change (indicates data loaded)
            time.sleep(2) # Allow UI to refresh
            new_range = self.driver.find_element(By.XPATH, config['processMonitor']['paginationInfo']).text
            
            if initial_range == new_range:
                print("Pagination FAILED: Range text did not update after clicking Next.")
                return False
                
            print(f"Clicked Next: Range updated from {initial_range} to {new_range}")

            # 4. Click Previous Page
            prev_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, config['processMonitor']['goToPreviousPageButton'])
            ))
            click_with_retry(driver, prev_btn)
            
            time.sleep(2)
            final_range = self.driver.find_element(By.XPATH, config['processMonitor']['paginationInfo']).text
            
            if final_range == initial_range:
                print(f"Clicked Previous: Range returned to {final_range}")
                return True
            else:
                print(f"Pagination FAILED: Range did not return to initial state.")
                return False

        except Exception as e:
            print(f"Pagination Error: {str(e)}")
            return False
                
    
    def verify_typography(self, element_xpath, expected_size="14px", expected_font="Roboto"):
        """
        Checks the font size and font style (family) for any elements 
        passed via header_xpath.
        """
        # 1. Use the passed-in header_xpath variable instead of a hardcoded string
        elements = self.driver.find_elements(By.XPATH, element_xpath)
        
        
        if not elements:
            print(f" No elements found for XPath: {element_xpath}")
            return False

        mismatches = []

        for element in elements:
            actual_text = get_element_text_safely(element)
            
            # Get CSS Properties
            actual_size = element.value_of_css_property('font-size')
            actual_font = element.value_of_css_property('font-family')
            
            # Validation Logic
            size_match = (actual_size == expected_size)
            font_match = (expected_font.lower() in actual_font.lower())

            if not size_match or not font_match:
                mismatches.append(
                    f"Element '{actual_text}': Found {actual_size} and {actual_font}"
                )

        # 2. Final Report
        if mismatches:
            print(f" Typography Mismatch found in {len(mismatches)} elements:")
            for m in mismatches:
                print(f"   -> {m}")
            return False
        
        print(f" All elements at XPath verified: {expected_size}, {expected_font}")
        return True

    def find_row_by_process_log_id(self):
        config = load_config()
        #Locate the row corresponding to the processLogId from config.
        loc = config["processMonitor"]["gridLocators"]
        process_log_id = config["processLogApi"]["processLogId"]
        assert process_log_id, "processLogId not found in config"
        short_id = process_log_id[:8]
        row_xpath = loc["rowByIdentifier"].format(value=short_id)
        return self.wait.until(EC.presence_of_element_located((By.XPATH, row_xpath)))

    def wait_for_process_log_loading(self):
        #Wait for loader to disappear and table rows to render
        loc = config["processMonitor"]["gridLocators"]
        try:
            self.wait.until_not(EC.visibility_of_element_located((By.XPATH, loc["loader"])))
        except:
            pass
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, loc["tableRows"])))

    def check_truncation(self, column_name):
        #Check if any cell text in the specified column is truncated.
        loc = config["processMonitor"]["gridLocators"]
        data_cells = self.get_column_data(column_name)
        truncated_cells = []

        for i, _ in enumerate(data_cells):
            headers = self.driver.find_elements(By.XPATH, config['processMonitor']['processTableHeader'])
            col_index = -1
            for j, h in enumerate(headers):
                if column_name in h.text:
                    col_index = j + 1
                    break
            if col_index == -1:
                continue

            cell_xpath = config['processMonitor']['processTableColumnIndex'].format(col_index=col_index)
            cell_element = self.driver.find_elements(By.XPATH, cell_xpath)[i]

            truncated = self.driver.execute_script(
                """
                const el = arguments[0].querySelector('*') || arguments[0];
                const style = getComputedStyle(el);
                return style.textOverflow === 'ellipsis' || el.scrollWidth > el.clientWidth + 2;
                """,
                cell_element
            )

            if truncated:
                truncated_cells.append((i, data_cells[i]))

        return truncated_cells

    def check_overlap(self):
        #Check if any columns overlap

        loc = config["processMonitor"]["gridLocators"]
        row = self.find_row_by_process_log_id()
        cells = row.find_elements(By.XPATH, loc["rowCells"])
        headers = self.driver.find_elements(By.XPATH, loc["tableHeaders"])
        column_names = [h.text.strip() or f"Column_{i}" for i, h in enumerate(headers)]

        overlaps = []
        for i in range(len(cells) - 1):
            overlap = self.driver.execute_script(
                """
                const a = arguments[0].getBoundingClientRect();
                const b = arguments[1].getBoundingClientRect();
                return a.right - b.left > 4;  // tolerance
                """,
                cells[i], cells[i + 1]
            )
            if overlap:
                overlaps.append((i, column_names[i], column_names[i + 1]))

        return overlaps


