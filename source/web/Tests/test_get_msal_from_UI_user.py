import inspect
import json
import os
import sys
from time import sleep
import time
from selenium.common import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functools import wraps
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

env = os.environ.get('ENVIRONMENT')

# Example usage:
# env = "dev"

baseurl = f"https://{env}.eclipsevantage.com"

test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')

config_path = os.path.join(test_script_path, 'config_Template.json').replace('\\', '/')

def initialize_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

def load_config(path=os.path.join(test_script_path, 'config_Template.json').replace('\\', '/')):
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise FileNotFoundError(f"Failed to load config file: {e}")

config = load_config()

def saveConfig(config_data):
    with open(config_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print("Config data saved successfully.")
    
def handle_stale_element(retries=3, delay=0.5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except StaleElementReferenceException as e:
                    last_exception = e
                    if attempt == retries - 1:
                        raise last_exception
                    sleep(delay)
        return wrapper
    return decorator

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
        
def login(driver, email, password, baseUrl):
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

def user_login(driver, load_secret, baseUrl):
    email1, password1 = load_secret
    login(driver, email1, password1, baseUrl)

@handle_stale_element()
def test_get_msal_token(driver, load_secret):
    try:
        user_login(driver, load_secret, baseurl)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script(
                "return window.localStorage.getItem('accessToken') !== null && window.localStorage.getItem('accessToken') !== '';"
            )
        )
        
        access_token = driver.execute_script("return window.localStorage.getItem('accessToken');")
        id_token = driver.execute_script("return window.localStorage.getItem('idToken');")
        assert access_token is not None and access_token != "", "Access Token is null or empty"
        assert id_token is not None and id_token != "", "ID Token is null or empty"
        config['tokenApi']['mtoken'] = access_token
        config['tokenApi']['idToken'] = id_token
        saveConfig(config)

    finally:
        if 'driver' in locals() and driver:
            driver.quit()
            
def load_secret():
    json_file = os.path.join(test_script_path, 'secrets.json')
    try:
        with open(json_file, 'r') as file:
            secrets = json.load(file)

        for secret in secrets:
            if secret['SecretName'] == 'eclipse-testautomation-user-01':
                UserId1 = secret['SecretValue']['UserId']
                Password1 = secret['SecretValue']['Password']
        return UserId1, Password1
    except Exception as e:
        raise AssertionError(f"Failed to load secret: {str(e)}")
    
def main():
    try:
        driver = initialize_driver()
        secrets = load_secret()
        test_get_msal_token(driver, secrets)        
        print("Test completed successfully!")
    except Exception as e:
        print(f"Test failed: {str(e)}")
        sys.exit(1)
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()