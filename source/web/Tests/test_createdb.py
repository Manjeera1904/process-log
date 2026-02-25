import time
import os
import base64
import json
import requests
import pytest

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from config import (
    driver, load_secret, user_login, load_config,baseUrl,
    click, generate_random_word, send_keys, click_create_button, click_after_login,
    homeUrl, eclipseAnalyticsUrl, verifyElementPresence, deleteNonProdHelper,
    capture_browser_config_json,browser_config_path, inject_config_into_browser
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

# Token from runtests config
token = configData["tokenApi"]["token"]
header = {"Authorization": f"Bearer {token}"}

# Load configuration data from config.json
def read():
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)


def get_azure_devops_token():
    token = os.environ.get("SYSTEM_ACCESSTOKEN")
    if not token:
        raise ValueError("SYSTEM_ACCESSTOKEN is not available")
    return base64.b64encode(f":{token}".encode()).decode()

# Configuration
organization = os.environ.get('OrganizationName').lower()
project = os.environ.get('ProjectName').lower()
pipeline_id = os.environ.get('PipelineId').lower()
access_token = get_azure_devops_token()
env = config.get("env")
dataSourceKey = "EIProcessLog"
pcapiBaseUrl = f'https://platform-core-api.{env}.eclipsevantage.com'
# organization = 'EclipseInsightsHC'
# project = 'Commercialization'
# pipeline_id = '111'
# access_token = ''

# Generic method for making requests
def makeRequest(method, endpoint, data=None):
    
    url = f"{pcapiBaseUrl}{endpoint}"
    print(f"\n=== {method.upper()} Request ===")
    print(f"URL: {url}")
    config = load_Config()
    token = config["tokenApi"]["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",

        
    }
    print("Request headers:", headers)

    try:
        if method == 'post':
            response = requests.post(url, json=data, verify=False, headers=headers)
        elif method == 'get':
            response = requests.get(url, verify=False, headers=headers)
        elif method == 'put':
            response = requests.put(url, json=data, verify=False, headers=headers)
        else:
            raise ValueError("Invalid method type provided.")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        raise

    # --- Always show raw response ---
    print("\n--- Raw Response Body ---")
    print(response.text)

    # --- Try to parse JSON if possible ---
    try:
        response_data = response.json()
        print("\n--- Parsed JSON Response ---")
        print(json.dumps(response_data, indent=4))
    except json.JSONDecodeError:
        print("\n Response body is not valid JSON")
        response_data = {}

    return response, response_data

def test_verify_that_the_user_can_log_in_successfully_to_the_eclipse_insights_website(driver, load_secret):
    user_login(driver, load_secret)
    
def test_verify_that_the_browser_config_json_is_copied_from_the_network(driver):
    browser_config_data = capture_browser_config_json(driver, baseUrl, browser_config_path, env)
    assert browser_config_data is not None, "config.json was not captured"

def test_verify_that_the_browser_config_json_is_injected_into_the_browser(driver):
    inject_config_into_browser(driver, browser_config_path)
    injected_config = driver.execute_script("return window.localStorage.getItem('mfConfigOverride');")
    assert injected_config is not None, "Config was not injected into browser"

class TestToCreateDb:
    generatedClientName = None
    generatedClientDescription = None

    @pytest.mark.xfail(reason="Running the test to refresh session after login")
    def test_verify_presence_after_login(self, driver):
        driver.set_page_load_timeout(30)
        driver.get(homeUrl)

    def test_getclientid(self,driver):
        client_name= 'db' + env + 'client'
        endpoint = f"/api/Client/name/{client_name}?api-version=1.0"
        response, response_data = makeRequest('get', endpoint)
        assert response.status_code in [200, 404], f"Expected status code 200 or 404, but got {response.status_code}"
        
        if response.status_code == 200:
            config["common"]["testClientId"] = response_data.get("id")
            clientIdDs = response_data.get("id")
            getBaseUrl = f"{pcapiBaseUrl}/api/DataSource/Client/{clientIdDs}/DataSourceKey/{dataSourceKey}?api-version={apiVersion}"
            config["common"]["getBaseUrl"] = getBaseUrl
            saveConfig(config)

        if response.status_code == 404:
            print(f"Failed to fetch client. Status code: {response.status_code}, Response: {response.text}")
            self.add_New_Client(driver)
            self.assignUser_and_adding_new_Client_as_active_and_getClientId(driver)

    def add_New_Client(self, driver):
        try:
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            click_after_login(driver, config['common']['settingsGearIcon'])
            click(driver, config['client']['clientConfigurationButton'])
            click(driver, config['client']['addNewClientButton'])
            TestToCreateDb.generatedClientName = f"db{env}client"
            TestToCreateDb.generatedClientDescription = generate_random_word()
            send_keys(driver, config['client']['nameInput'], TestToCreateDb.generatedClientName)
            send_keys(driver, config['client']['descriptionTextarea'], TestToCreateDb.generatedClientDescription)
            click_create_button(driver)

            click(driver, config['client']['selectTenantsButton'])
            click(driver, config['client']['selectTenantDropdown'])
            click(driver, config['client']['eclipseDevTenantOption'])
            click(driver, config['client']['SelectAnotherTenant'])
            click(driver, config['client']['selectAnotherTenantDropdown'])
            click(driver, config['client']['eclipseInsightsOption'])
            click(driver, config['client']['selectProductsButton'])
            click(driver, config['client']['selectProductDropdown'])
            click(driver, config['client']['analyzePayorContractsOption'])
            click(driver, config['client']['selectAnotherProductButton'])
            click(driver, config['client']['selectProductDropdownForAnotherProduct'])
            click(driver, config['client']['platformAdministrationOption'])
            click(driver, config['client']['selectAnotherProductButton'])
            click(driver, config['client']['selectProductDropdownForAnotherProduct2'])
            click(driver, config['client']['processMonitoringOption'])
            click(driver, config['common']['saveButton'])
            
        except Exception as e:
            print(f"Error in add_New_Client: {str(e)}")
            # Take screenshot for debugging
            driver.save_screenshot(f"/home/vsts/work/1/s/source/web/Tests/error_screenshot_{int(time.time())}.png")
            raise

    def assignUser_and_adding_new_Client_as_active_and_getClientId(self, driver):
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        TestUserClientName = 'TestAutomation02@EclipseDevelopmentTest.onmicrosoft.com'
        click(driver, config['common']['settingsGearIcon'])
        click(driver, config['user']['userSectionButton'])
        click(driver, config['common']['searchButton'])
        send_keys(driver, config['user']['searchButton'], TestUserClientName)
        click(driver, config['user']['editIcon'])
        click(driver, config['user']['addAnotherClientButton'])
        click(driver, config['user']['selectLatestClientDropdown'])
        click(driver,config['user']['selectProcessdbClient'].format(clientName=TestToCreateDb.generatedClientName))
        add_role_button = f"(//div[normalize-space(text())='{TestToCreateDb.generatedClientName}']/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div//button[normalize-space(.)='Add a role'])[1]"
        click(driver, add_role_button)
        role_dropdown_xpath = f"(//div[normalize-space(text())='{TestToCreateDb.generatedClientName}']/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div//div[contains(@id,'clients.') and contains(@id, '.roles.') and contains(@id, '.roleId')])[last()]"
        click(driver, role_dropdown_xpath)
        click(driver, config['user']['processLogOption'])
        add_another_role_xpath = f"(//div[normalize-space(text())='{TestToCreateDb.generatedClientName}']/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div//button[normalize-space()='Add another role'])[last()]"
        click(driver, add_another_role_xpath)
        another_role_dropdown = f"(//div[normalize-space(.)='{TestToCreateDb.generatedClientName}']/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div//div[contains(@id,'clients.') and contains(@id,'.roleId') and @role='combobox'])[last()]"
        click(driver, another_role_dropdown)
        click(driver, config['user']['filemanageroption'])
        click(driver, add_another_role_xpath)
        third_role_dropdown_xpath = f"(//div[normalize-space(.)='{TestToCreateDb.generatedClientName}']" \
                                    f"/ancestor::div[contains(@class,'MuiFormControl-root')]/parent::div/following-sibling::div" \
                                    f"//div[contains(@id,'clients.') and contains(@id,'.roleId') and @role='combobox'])[last()]"
        click(driver, third_role_dropdown_xpath)
        click(driver, config['user']['administratorOption'])
        click(driver, config['user']['saveButton'])

        client_name= TestToCreateDb.generatedClientName
        endpoint = f"/api/Client/name/{client_name}?api-version=1.0"
        response, response_data = makeRequest('get', endpoint)
        
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        
        config["common"]["testClientId"] = response_data.get("id")
        clientIdDs = response_data.get("id")
        getBaseUrl = f"{pcapiBaseUrl}/api/DataSource/Client/{clientIdDs}/DataSourceKey/{dataSourceKey}?api-version={apiVersion}"
        config["common"]["getBaseUrl"] = getBaseUrl
        saveConfig(config)
    
    def test_Check_DataSource_ClientDataSource(self):
        config = load_Config()
        token = config["tokenApi"]["token"]
        header = {"Authorization": f"Bearer {token}"}
        getBaseUrl = config["common"]["getBaseUrl"]
        response = requests.get(getBaseUrl, verify=False, headers=header)
        config["common"]["responsestatus"] = response.status_code
        saveConfig(config)
        assert response.status_code in [200, 404], f"Expected status code 200 or 404, but got {response.status_code}"

    def test_trigger_pipeline(self):
        # Trigger the pipeline
        config = load_Config()
        clientId = config["common"]["testClientId"]        
        parameters = {
            "environmentName": env,
            "clientId": clientId,
            "createSqlDb": 'Yes',
            "createBlobStorage": 'No',
            "clientShortName": 'db' + env + 'client'
        }

        url = f"https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipeline_id}/runs?api-version=7.1-preview.1"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {access_token}"
        }
        payload = {
            "resources": {},
            "templateParameters": parameters
        }

        response = requests.post(url, json=payload, headers=headers)
        print("Pipeline trigger response:", response.status_code, response.text)
        assert response.status_code == 200, f"Failed to trigger pipeline. Status code: {response.status_code}, Response: {response.text}"
        run = response.json()
        run_id = run["id"]
        print(f"Pipeline triggered. Run ID: {run_id}")

        # Poll for completion
        status = "inProgress"
        while status in ["inProgress", "queued"]:
            time.sleep(10)
            run_status_url = f"https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipeline_id}/runs/{run_id}?api-version=7.1-preview.1"
            run_response = requests.get(run_status_url, headers=headers)
            run_data = run_response.json()
            status = run_data["state"]
            print(f"Current status: {status}")

        # Display result
        result = run_data.get("result", "unknown")
        print(f"Pipeline completed with result: {result}")

def run_tests():
    pytest.main([__file__, '-v'])

if __name__ == "__main__":
    run_tests()
