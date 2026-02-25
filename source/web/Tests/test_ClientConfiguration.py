import json
import requests
import os
import pytest

test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config_path = os.path.join(test_script_path, 'config.json').replace('\\', '/')

def read_config():
    with open(config_path, 'r') as f:
        return json.load(f)

def write_config(data):
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=4)

def makeRequest(method, endpoint, data=None):
    token = read_config().get("tokenApi", {}).get("token")
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{read_config().get('apiBaseUrl')}{endpoint}"
    print(f"{method.upper()} URL: {url}")

    try:
        if method == 'get':
            response = requests.get(url, headers=headers, verify=False)
        elif method == 'post':
            response = requests.post(url, json=data, headers=headers, verify=False)
        elif method == 'put':
            response = requests.put(url, json=data, headers=headers, verify=False)
        elif method == 'delete':
            headers["Content-Type"] = "application/json"
            response = requests.delete(url, headers=headers, json=data or {}, verify=False)
        else:
            raise ValueError("Unsupported method")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        raise

    try:
        res_data = response.json()
        print("Response JSON:", json.dumps(res_data, indent=4))
    except json.JSONDecodeError:
        print("Response Text:", response.text)
        res_data = {}

    return response, res_data

def test_get_automation_clients():
    config = read_config()
    version_id = config.get("common", {}).get("versionId")

    endpoint = f"/api/Client?api-version={version_id}"
    response, clients = makeRequest("get", endpoint)
    print(f"GET /api/Client status code: {response.status_code}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    matching_clients = [c for c in clients if c.get("name") == "Eclipse_Insights_Automation"]

    if not matching_clients:
        print("No client found with name 'Eclipse_Insights_Automation'. Skipping storing step.")
    else:
        automation_responses = {
            f"automationClient{idx + 1}": client
            for idx, client in enumerate(matching_clients)
        }
        config["automationClientResponses"] = automation_responses
        write_config(config)
        print(f"Stored {len(matching_clients)} automation client responses in config.")

def test_update_automation_clients():
    config = read_config()
    version_id = config.get("common", {}).get("versionId")
    automation_responses = config.get("automationClientResponses", {})

    if not automation_responses:
        pytest.skip("No automation client responses found in config")

    for key, client in automation_responses.items():
        client_id = client.get("id")
        assert client_id, f"Missing ID for client in key: {key}"

        updated_payload = client.copy()
        updated_payload["name"] = "test_testclient"

        endpoint = f"/api/Client/{client_id}?api-version={version_id}"
        response, _ = makeRequest("put", endpoint, data=updated_payload)
        print(f"PUT /api/Client/{client_id} status code: {response.status_code}")
        assert response.status_code in [200, 204], f"Expected status code 200 or 204, but got {response.status_code}"

        print(f"Updated {key}: name changed to 'test_testclient'")

def test_delete_nonprod_helper():
    endpoint = "/api/NonProdHelper?api-version=1.0"
    response, _ = makeRequest("delete", endpoint, data={})
    assert response.status_code in [200, 204], f"Expected status code 200 or 204, but got {response.status_code}"
    print("NonProdHelper cleanup executed successfully.")

def test_create_automation_client():
    config = read_config()
    version_id = config.get("common", {}).get("versionId")
    client_payload = config.get("testClientApi", {}).copy()

    client_payload.pop("id", None)
    client_payload.pop("clientId", None)

    endpoint = f"/api/Client?api-version={version_id}"
    response, response_data = makeRequest("post", endpoint, data=client_payload)

    print(f"POST /api/Client status code: {response.status_code}")
    print("Response body:", response_data)

    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

    created_id = response_data.get("id")
    config["testClientApi"]["clientId"] = created_id
    write_config(config)
    print(f"Client created and saved with clientId: {created_id}")

def test_create_client_tenant():
    config = read_config()
    version_id = config.get("common", {}).get("versionId")

    client_id = config.get("testClientApi", {}).get("clientId")
    assert client_id, "Missing clientId in config['testClientApi']"

    # First tenant
    tenant_payload = config.get("clientTenantApi", {}).copy()
    tenant_payload["clientId"] = client_id
    tenant_payload.pop("id", None)

    endpoint = f"/api/ClientTenant?api-version={version_id}"
    response, response_data = makeRequest("post", endpoint, data=tenant_payload)

    print(f"POST /api/ClientTenant status code: {response.status_code}")
    print("Response body:", response_data)

    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
    config["clientTenantApi"]["id"] = response_data.get("id")

    # Second tenant
    tenant_payload["tenantId"] = config["clientTenantApi"]["tenantId2"]
    response2, response_data2 = makeRequest("post", endpoint, data=tenant_payload)

    print(f"POST /api/ClientTenant (tenantId2) status code: {response2.status_code}")
    print("Response body:", response_data2)

    assert response2.status_code == 201, f"Expected status code 201, but got {response2.status_code}"
    config["clientTenantApi"]["id2"] = response_data2.get("id")

    write_config(config)
    print(f"ClientTenant created and saved with IDs: {config['clientTenantApi']['id']} and {config['clientTenantApi']['id2']}")


def test_create_client_product():
    config = read_config()
    version_id = config.get("common", {}).get("versionId")

    client_id = config.get("testClientApi", {}).get("clientId")
    assert client_id, "Missing clientId in config['testClientApi']"

    product_ids = config.get("clientProduct", {}).get("productIds", [])
    assert product_ids, "No productIds found in config['clientProduct']"

    for product_id in product_ids:
        product_payload = config.get("clientProduct", {}).copy()
        product_payload["clientId"] = client_id
        product_payload["productId"] = product_id
        product_payload.pop("id", None)
        product_payload.pop("productIds", None)

        endpoint = f"/api/ClientProduct?api-version={version_id}"
        response, response_data = makeRequest("post", endpoint, data=product_payload)

        print(f"POST {endpoint} (productId: {product_id}) status: {response.status_code}")
        print("Response:", response_data)

        assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

    print("All client products created successfully.")

def test_create_datasource():
    config = read_config()
    version_id = config.get("common", {}).get("versionId")

    datasource_payload = config.get("datasourceForClientApi", {}).copy()

    endpoint = f"/api/Datasource?api-version={version_id}"
    response, response_data = makeRequest("post", endpoint, data=datasource_payload)

    print(f"POST /api/Datasource status code: {response.status_code}")
    print("Response body:", response_data)

    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

    created_id = response_data.get("id")
    config["datasourceForClientApi"]["datasourceId"] = created_id
    write_config(config)
    print(f"Datasource created and saved with datasourceId: {created_id}")

def test_create_client_datasource():
    config = read_config()
    version_id = config.get("common", {}).get("versionId")

    client_id = config.get("testClientApi", {}).get("clientId")
    assert client_id, "Missing clientId in config['testClientApi']"

    datasource_id = config.get("datasourceForClientApi", {}).get("datasourceId")
    assert datasource_id, "Missing datasourceId in config['datasourceForClientApi']"

    client_datasource_payload = config.get("clientDatasourceApi", {}).copy()
    client_datasource_payload.pop("id", None)
    client_datasource_payload["clientId"] = client_id
    client_datasource_payload["dataSourceId"] = datasource_id

    endpoint = f"/api/ClientDatasource?api-version={version_id}"
    response, response_data = makeRequest("post", endpoint, data=client_datasource_payload)

    print(f"POST /api/ClientDatasource status code: {response.status_code}")
    print("Response body:", response_data)

    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

    created_id = response_data.get("id")
    config["clientDatasourceApi"]["id"] = created_id
    write_config(config)
    print(f"ClientDatasource created and saved with ID: {created_id}")

