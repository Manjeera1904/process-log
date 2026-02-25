import json
import time
import os
import inspect
import requests
from time import sleep
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from runtests import ui_base_url, platform_url
from runtests import env

test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
browser_config_path = os.path.join(test_script_path, "browser_config.json").replace('\\', '/')
# Load Configuration
def load_config(path=os.path.join(test_script_path, 'config_Template.json').replace('\\', '/')):
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise FileNotFoundError(f"Failed to load config file: {e}")

config = load_config()
baseUrl = ui_base_url

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

                # Modify only host_app and web_file_manager
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

versionId = config.get("common", {}).get("apiVersion")

def click(driver, xpath, retries=3, timeout=10, error_message="Element click failed"):
    for _ in range(retries):
        try:
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            return
        except StaleElementReferenceException as e:
            if _ == retries - 1:
                caller_function_name = inspect.stack()[1].function
                raise AssertionError(
                    f"{error_message} in function '{caller_function_name}': Could not click element with XPath: {xpath} - Stale element error."
                )
            sleep(1)  # small delay before retrying
        except Exception as e:
            if _ == retries - 1:
                caller_function_name = inspect.stack()[1].function
                raise AssertionError(
                    f"{error_message} in function '{caller_function_name}': Could not click element with XPath: {xpath} - Error: {str(e)}"
                )

def send_keys(driver, xpath, keys, timeout=10):
    for _ in range(3):  # Retry mechanism for send_keys
        try:
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(keys)
            return
        except StaleElementReferenceException as e:
            sleep(1)  # small delay before retrying
        except Exception as e:
            raise AssertionError(f"Failed to send keys to {xpath}: {str(e)}")

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

platformUrl = platform_url

@pytest.fixture(scope="module")
def load_secret():
    json_file = os.path.join(test_script_path, 'secrets.json')
    try:
        with open(json_file, 'r') as file:
            secrets = json.load(file)

        for secret in secrets:
            if secret['SecretName'] == 'eclipse-testautomation-user-01':
                UserId1 = secret['SecretValue']['UserId']
                Password1 = secret['SecretValue']['Password']
                TotpKey1 = secret['SecretValue'].get('TotpKey', None)
            if secret['SecretName'] == 'eclipse-testautomation-user-02':
                UserId2 = secret['SecretValue']['UserId']
                Password2 = secret['SecretValue']['Password']
                TotpKey2 = secret['SecretValue'].get('TotpKey', None)
        return UserId1, Password1, TotpKey1, UserId2, Password2, TotpKey2
    except Exception as e:
        raise AssertionError(f"Failed to load secret: {str(e)}")

def login(driver, email, password, totp_key):
    for attempt in range(2):
        try:
            driver.get(baseUrl)
            WebDriverWait(driver, 40).until(EC.number_of_windows_to_be(2))
            driver.switch_to.window(driver.window_handles[1])
            send_keys(driver, config['login']['emailInput'], email, timeout=40)
            click(driver, config['login']['nextButton'], timeout=40)
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

def user_login(driver, load_secret, user):
    email1, password1, totp_secret1,email2, password2, totp_secret2, = load_secret
    if(user == "user1"):
        login(driver, email1, password1, totp_secret1)
    elif(user == "user2"):
        login(driver, email2, password2, totp_secret2)