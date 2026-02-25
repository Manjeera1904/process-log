import json
import requests
import pytest
import os

test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config_path = os.path.join(test_script_path, 'config.json').replace('\\', '/')

with open(config_path, 'r') as file:
    config_data = json.load(file)

def read_config():
    with open(config_path, 'r') as f:
        return json.load(f)

def write_config(data):
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=4)


base_url = config_data.get("apiBaseUrl")
version_id = config_data.get("common", {}).get("versionId")
userclient_config = config_data.get("userClientApi", {})

def makeRequest(method, endpoint, data=None):
    token = read_config().get("tokenApi", {}).get("token")
    headers = {"Authorization": f"Bearer {token}"}

    url = f"{base_url}{endpoint}"
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
        data = response.json()
        print("Response JSON:", json.dumps(data, indent=4))
    except json.JSONDecodeError:
        print("Response Text:", response.text)
        data = {}

    return response, data

def test_user_client_initial():
    config = read_config()

    payload_email = "TestAutomation02@EclipseDevelopmentTest.onmicrosoft.com"
    endpoint = f"/api/User?api-version={version_id}"
    response, users = makeRequest('get', endpoint)

    assert response.status_code == 200 and isinstance(users, list), "Failed to fetch users"

    for user in users:
        if user.get('userName') == payload_email:
            config.setdefault("userClientApi", {})["userIdTestUserTwo"] = user.get('id')
            write_config(config)
            print(f" Saved userIdTestUserTwo: {user.get('id')}")
            return

    assert False, f" User with email {payload_email} not found"


# === Test for valid userId ===
def test_get_user_clients_by_user_id():
    user_key = "userIdTestUserTwo"
    user_id = read_config().get("userClientApi", {}).get(user_key)
    assert user_id, f"'{user_key}' not found in config.json under 'userClientApi'"
    print(f"[DEBUG] user_id: {user_id}")
    endpoint = f"/api/UserClient/User/{user_id}?api-version={version_id}"
    response, data = makeRequest("get", endpoint)
    print(f"[DEBUG] GET endpoint: {endpoint}")
    assert response.status_code in [200, 204], f"Expected 200 or 204, got {response.status_code}"

    userclient_count = len(data)
    print(f"\n  Count of user clients: {userclient_count}\n")

    # Load full config fresh
    with open(config_path, 'r') as file:
        full_config = json.load(file)

    # Clean up existing keys like userClientIdForTestUserTwo*
    prefix = f"userClientIdFor{user_key.replace('userId', '')}"
    keys_to_remove = [k for k in full_config["userClientApi"] if k.startswith(prefix)]
    for k in keys_to_remove:
        del full_config["userClientApi"][k]

    # Save new user client IDs
    for idx, client in enumerate(data, start=1):
        full_config["userClientApi"][f"{prefix}{idx}"] = client.get("id")

    # Save updated config
    with open(config_path, 'w') as file:
        json.dump(full_config, file, indent=4)

def test_create_clients_for_userclient_count():
    user_key = "userIdTestUserTwo"
    user_id = read_config().get("userClientApi", {}).get(user_key)
    assert user_id, f"'{user_key}' not found"

    # Get user client count
    endpoint = f"/api/UserClient/User/{user_id}?api-version={version_id}"
    response, userclients = makeRequest("get", endpoint)
    assert response.status_code in [200, 204], f"Expected 200 or 204, got {response.status_code}"
    count = len(userclients)
    print(f"User client count: {count}")

    # Load config and template
    config = read_config()

    payload_template = config.get("createClientPostData")
    assert payload_template, "'createClientPostData' missing"

    # Clean old client IDs
    prefix = f"ClientIdFor{user_key.replace('userId', '')}"
    api_config = config["userClientApi"]
    for key in list(api_config):
        if key.startswith(prefix):
            del api_config[key]

    # Create clients and save IDs
    for i in range(1, count + 1):
        payload = payload_template.copy()
        payload["name"] = f"test_client_{i}_TestUserTwo"
        payload["description"] = f"Client {i} for TestUserTwo"

        post_url = f"/api/Client?api-version={version_id}"
        resp, body = makeRequest("post", post_url, data=payload)
        assert resp.status_code == 201, f"Client {i} creation failed"
        api_config[f"{prefix}{i}"] = body["id"]
        config["createClientTenantPostData"]["clientId"] = body["id"]
        print(f"Created client {i}: {body['id']}")

    # Save updated config
    write_config(config)

def test_get_userclient_by_id_and_store_response():
    user_key = "userIdTestUserTwo"
    prefix = f"userClientIdFor{user_key.replace('userId', '')}"

    # Load config
    config = read_config()

    api_config = config.get("userClientApi", {})
    response_section = {}

    # Filter keys like userClientIdForTestUserTwo1, 2...
    userclient_ids = sorted(
        [(k, v) for k, v in api_config.items() if k.startswith(prefix)],
        key=lambda x: int(x[0].replace(prefix, ""))  # Sort by index
    )

    for key, userclient_id in userclient_ids:
        endpoint = f"/api/UserClient/{userclient_id}?api-version={version_id}"
        response, data = makeRequest("get", endpoint)
        assert response.status_code == 200, f"Failed to get {key}"
        response_key = f"{key}Response"
        response_section[response_key] = data
        print(f"Fetched and stored: {response_key}")

    # Save to config
    config["userClientForTestUserTwoResponses"] = response_section
    write_config(config)

def test_create_client_tenants_for_created_clients():
    user_key = "userIdTestUserTwo"
    client_prefix = f"ClientIdFor{user_key.replace('userId', '')}"

    # Load config
    config = read_config()
    client_tenant_template = config.get("createClientTenantPostData")
    assert client_tenant_template, "'createClientTenantPostData' not found in config"

    api_config = config.get("userClientApi", {})
    tenant_id = api_config.get("eclipseDevTestTenantId")
    assert tenant_id, "'eclipseDevTestTenantId' not found in 'userClientApi'"

    for i in range(1, 100):
        client_id = api_config.get(f"{client_prefix}{i}")
        if not client_id:
            continue

        payload = client_tenant_template.copy()
        payload["clientId"] = client_id
        payload["tenantId"] = tenant_id

        print(f"\n[DEBUG] Creating ClientTenant for client {i}")
        print(f"[DEBUG] clientId: {client_id}")
        print(f"[DEBUG] tenantId: {tenant_id}")

        endpoint = f"/api/ClientTenant?api-version={version_id}"
        response, res_data = makeRequest("post", endpoint, data=payload)

        print(f"[DEBUG] Status: {response.status_code}")
        if response.status_code != 201:
            print(f"[DEBUG] Response text: {response.text}")

        if response.status_code == 201:
            print(f"  ClientTenant created for client {i}: {res_data.get('id')}")
        elif response.status_code == 400:
            print(f"  Skipped client {i}: Dependent record not found or bad request.")
        else:
            assert False, f"Unexpected status {response.status_code} for client {client_id}"



def test_update_userclients_with_new_client_ids():
    user_key = "userIdTestUserTwo"
    prefix = f"userClientIdFor{user_key.replace('userId', '')}"
    client_prefix = f"ClientIdFor{user_key.replace('userId', '')}"
    response_section_key = f"userClientFor{user_key.replace('userId', '')}Responses"

    # Load config
    config = read_config()

    api_config = config.get("userClientApi", {})
    response_data = config.get(response_section_key, {})

    # Loop over matching user client entries
    for i in range(1, 100):
        userclient_id = api_config.get(f"{prefix}{i}")
        new_client_id = api_config.get(f"{client_prefix}{i}")
        response_payload = response_data.get(f"{prefix}{i}Response")

        if not (userclient_id and new_client_id and response_payload):
            continue

        # Update only clientId in the response payload
        updated_payload = response_payload.copy()
        updated_payload["clientId"] = new_client_id

        put_url = f"/api/UserClient/{userclient_id}?api-version={version_id}"
        response, body = makeRequest("put", put_url, data=updated_payload)

        assert response.status_code in [200, 204], f"PUT failed for {userclient_id}, got {response.status_code}"
        print(f"  Updated userClient {userclient_id} with new clientId {new_client_id}")

def test_delete_nonprod_helper():
    endpoint = "/api/NonProdHelper?api-version=1.0"
    response, data = makeRequest("delete", endpoint, data={})
    assert response.status_code in [200, 204], f"Expected 200 or 204, got {response.status_code}"
    print("  NonProdHelper cleanup executed successfully")

def test_store_eclipse_test_automation_client_id():
    config = read_config()

    response, clients = makeRequest("get", f"/api/Client?api-version={version_id}")
    assert response.status_code == 200 and isinstance(clients, list), "Failed to fetch clients"

    client = next((c for c in clients if c.get("name") == "Eclipse_Insights_Automation"), None)
    assert client, "'Eclipse_Test_Automation' client not found"

    config.setdefault("userClientApi", {})["eclipseInsightsAutomationClientId"] = client["id"]

    write_config(config)

    print(f"Client ID stored: {client['id']}")

def test_create_user_client_link():
    config = read_config()

    api_config = config.get("userClientApi", {})
    user_id = api_config.get("userIdTestUserTwo")
    client_id = api_config.get("eclipseInsightsAutomationClientId")
    base_payload = config.get("userClientPostData")

    assert user_id and client_id and base_payload, "Missing user ID, client ID, or post data in config"

    payload = base_payload.copy()
    payload["userId"] = user_id
    payload["clientId"] = client_id

    endpoint = f"/api/UserClient?api-version={version_id}"
    response, res_data = makeRequest("post", endpoint, data=payload)

    if response.status_code == 201:
        user_client_id = res_data.get("id")
    elif response.status_code == 409:
        # Record already exists – extract ID from response
        user_client_id = res_data[0].get("id") if isinstance(res_data, list) and res_data else None
        print("UserClient already exists. Using existing ID.")
    else:
        assert False, f"UserClient creation failed with status {response.status_code}"

    assert user_client_id, "UserClient ID could not be determined"

    config["userClientApi"]["userClientIdTestUserTwo"] = user_client_id
    write_config(config)

    print(f"UserClient ID saved: {user_client_id}")

def test_create_user_client_roles():
    config = read_config()

    api_config = config.get("userClientApi", {})
    user_client_id = api_config.get("userClientIdTestUserTwo")
    role_ids = config.get("roleId", {})
    base_payload = config.get("userClientRolePostData")

    assert user_client_id and role_ids and base_payload, "Missing userClientId, role IDs, or post data in config"

    for role_name, role_id in role_ids.items():
        payload = base_payload.copy()
        payload["userClientId"] = user_client_id
        payload["roleId"] = role_id

        endpoint = f"/api/UserClientRole?api-version={version_id}"
        response, res_data = makeRequest("post", endpoint, data=payload)

        if response.status_code == 201:
            print(f"UserClientRole created for role '{role_name}': {res_data.get('id')}")
        elif response.status_code == 409:
            existing_id = res_data[0].get("id") if isinstance(res_data, list) and res_data else None
            print(f"UserClientRole already exists for role '{role_name}': {existing_id}")
        else:
            assert False, f"Failed to create UserClientRole for {role_name} — status: {response.status_code}"
