import json
import os
import shutil
from time import sleep
from selenium.common import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import user_login, load_config, driver, load_secret, click
from functools import wraps
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from runtests import env

from config import (
    user_login, load_config, driver, load_secret, click, capture_browser_config_json, inject_config_into_browser,baseUrl
)

test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')

config_path = os.path.join(test_script_path, 'config_Template.json').replace('\\', '/')

config = load_config()

browser_config_path = os.path.join(test_script_path, "browser_config.json").replace('\\', '/')

config_path = os.path.join(test_script_path, 'config_Template.json').replace('\\', '/')

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


@handle_stale_element()
def test_get_msal_token(driver, load_secret):
    try:
        # First user login
        user_login(driver, load_secret, "user1")
        browser_config_data = capture_browser_config_json(driver, baseUrl, browser_config_path, env)
        assert browser_config_data is not None, "[ERROR] Failed to capture browser config.json"
        inject_config_into_browser(driver, browser_config_path)
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return !!window.localStorage.getItem('mfConfigOverride');"),
            message="[ERROR] mfConfigOverride not set in localStorage after injection"
        )
        print("Config injected successfully")
 
        WebDriverWait(driver, 60).until(
            lambda d: d.execute_script(
                "return window.localStorage.getItem('accessToken') !== null && window.localStorage.getItem('accessToken') !== '';"
            ),
            message="[ERROR] accessToken not set in localStorage"
        )      
        access_token = driver.execute_script("return window.localStorage.getItem('accessToken');")
        id_token = driver.execute_script("return window.localStorage.getItem('idToken');")
        assert access_token is not None and access_token != "", "Access Token is null or empty"
        assert id_token is not None and id_token != "", "ID Token is null or empty"
        config['tokenApi']['mtoken'] = access_token
        config['tokenApi']['idToken'] = id_token
        saveConfig(config)

    finally:
        # Ensure driver is closed even if test fails
        if 'driver' in locals() and driver:
            driver.quit()