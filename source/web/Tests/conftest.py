import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from config import capture_browser_config_json, inject_config_into_browser, baseUrl, browser_config_path, config
from selenium.webdriver.support.ui import WebDriverWait
import json
# ---------------- Global driver for fallback ----------------
GLOBAL_DRIVER = None

env = config.get("env")

# ---------------- Screenshot Utility ----------------
def take_screenshot(driver, name):
    """Save screenshot in Tests/screenshots-local folder with timestamp"""
    # Check if driver is still valid
    if not driver or not hasattr(driver, 'session_id'):
        print(" Driver not valid for screenshot")
        return
        
    try:
        driver.current_url  # This will fail if driver is closed
    except:
        print(" Driver session ended; screenshot not taken")
        return
        
    screenshots_dir = os.path.join(
        os.path.dirname(__file__),
        f"screenshots-{os.getenv('ENVIRONMENT', 'local')}"
    )
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    path = os.path.join(screenshots_dir, filename)
    try:
        driver.save_screenshot(path)
        print(f"\n Screenshot saved at: {path}")
    except Exception as e:
        print(f" Could not save screenshot: {e}")

# ---------------- Selenium Helpers ----------------
class SeleniumHelpers:
    def __init__(self, driver):
        self.driver = driver

    def verifyElementPresence(self, by, locator):
        """Passes if element exists, fails if not"""
        self.driver.find_element(by, locator)
        return True

    def verifyElementNotPresent(self, by, locator):
        """Passes if element does NOT exist, fails if found"""
        try:
            self.driver.find_element(by, locator)
            raise AssertionError(f"Element {locator} is present but should not be")
        except NoSuchElementException:
            return True

# ---------------- WebDriver Fixture ----------------
@pytest.fixture
def driver(request):
    global GLOBAL_DRIVER
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--headless')  # remove for debugging locally
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    # Attach driver to pytest node so hook can access it
    request.node.driver = driver
    GLOBAL_DRIVER = driver
    
    yield driver
    
    try:
        if driver and hasattr(driver, 'session_id'):
            driver.quit()
    except:
        pass
    
    GLOBAL_DRIVER = None

# ---------------- Pytest Hook for final screenshot ----------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot for any test failure"""
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        driver = getattr(item, "driver", None)

        if not driver and GLOBAL_DRIVER and hasattr(GLOBAL_DRIVER, 'session_id'):
            driver = GLOBAL_DRIVER

        if not driver and hasattr(item, 'funcargs'):
            for arg in item.funcargs.values():
                if hasattr(arg, "driver") and hasattr(arg.driver, 'session_id'):
                    driver = arg.driver
                    break
                elif isinstance(arg, WebDriver) and hasattr(arg, 'session_id'):
                    driver = arg
                    break

        if driver:
            take_screenshot(driver, f"{item.name}")
        else:
            print("\n Driver not available; screenshot not taken")