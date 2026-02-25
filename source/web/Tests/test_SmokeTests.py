import datetime
import inspect
import os
from time import sleep
import pytest
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from runtestsui import env

from config import (
    driver, load_secret, user_login, load_config,loadincognito,
    click, generate_random_word, send_keys,
    verifyElementNotPresent,
    hover, verifyElementNotClickable, hover_and_get_tooltip,
    verify_tooltip, homeUrl, baseUrl, processLogUrl, click_after_login,
    capture_browser_config_json,browser_config_path, inject_config_into_browser
)
test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config_path = os.path.join(test_script_path, 'config.json').replace('\\', '/')

class ConfigWrapper:
    def __getitem__(self, key):
        return load_config()[key]

# create a global instance
config = ConfigWrapper()

def get_token():
    return config.get("tokenApi", {}).get("token")

def get_header():
    token = get_token()
    return {"Authorization": f"Bearer {token}"}


def verifyElementPresence(driver, xpath, timeout=10, elementName="element"):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        caller_function_name = inspect.stack()[1].function
        raise AssertionError(f"'{elementName}' not found in function '{caller_function_name}' with XPath: {xpath}")

def test_verify_that_the_user_can_log_in_successfully_to_the_eclipse_insights_website(driver, load_secret):
    user_login(driver, load_secret)

def test_verify_that_the_browser_config_json_is_copied_from_the_network(driver):
    browser_config_data = capture_browser_config_json(driver, baseUrl, browser_config_path, env)
    assert browser_config_data is not None, "config.json was not captured"

def test_verify_that_the_browser_config_json_is_injected_into_the_browser(driver):
    inject_config_into_browser(driver, browser_config_path)
    injected_config = driver.execute_script("return window.localStorage.getItem('mfConfigOverride');")
    assert injected_config is not None, "Config was not injected into browser"

class TestMandatoryElementPresence:

    def test_verify_processMonitorProductButton_element_presence(self, driver):
        driver.set_page_load_timeout(90)
        driver.get(processLogUrl)
        click_after_login(driver, config['common']['settingsGearIcon'])
        verifyElementPresence(driver, config['processMonitor']['processMonitorProduct'], elementName="processMonitorProduct")

    def test_verify_processMonitorProduct_elementsPresence(self, driver):
        click(driver, config['processMonitor']['processMonitorProduct'])
        verifyElementPresence(driver, config['processMonitor']['processMonitorLabel'],elementName="processMonitorLabel")

    def test_verify_processMonitor_clientField_elementsPresence(self, driver):
        click(driver, config['processMonitor']['processMonitorProduct'])
        verifyElementPresence(driver, config["processMonitor"]["clientSelectionButton"],
                              elementName="clientSelectionButton")

    def test_verify_processMonitor_dateRangeField_elementsPresence(self, driver):
        verifyElementPresence(driver, config["processMonitor"]["todayButton"], elementName="todayButton")

    def test_verify_processMonitor_statusField_elementsPresence(self, driver):
        verifyElementPresence(driver, config["processMonitor"]["statusButton"], elementName="statusButton")

    def test_verify_processMonitor_restart_buttonPresence(self, driver):
        verifyElementPresence(driver, config["processMonitor"]["restartButton"], elementName="restartButton")







