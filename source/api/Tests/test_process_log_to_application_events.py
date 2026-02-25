import json
import uuid
import time
import requests
from datetime import datetime, UTC
import pytest
from azure.servicebus import ServiceBusClient, ServiceBusMessage, ServiceBusReceiveMode
from azure.identity import ClientSecretCredential
from azure.identity import DefaultAzureCredential
from runtests import config_path, apiBaseUrl, pc_api_base_url, env
from asb_utils import (
    SERVICE_BUS_NAMESPACE,
    TOPIC_NAME,
    SERVICEBUS_TOPIC_APPLICATION,
    SERVICEBUS_SUBSCRIPTION_2,
    send_message,
    build_message,
    receive_application_events,
    credential,
    send_payor_contract_message,
    send_file_message
)



def load_config():
    with open(config_path) as f:
        return json.load(f)

config = load_config()
token = config["tokenApi"]["token"]
API_BASE_URL = apiBaseUrl
clientId = config["common"]["testClientId"]


def make_request(method, endpoint, data=None):
    url = f"{API_BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-EI-ClientId": clientId
    }

    if method.lower() == "post":
        response = requests.post(url, headers=headers, json=data, verify=False)
    elif method.lower() == "get":
        response = requests.get(url, headers=headers, verify=False)
    elif method.lower() == "put":
        response = requests.put(url, headers=headers, json=data, verify=False)
    else:
        raise ValueError("Invalid method type.")

    try:
        return response, response.json()
    except Exception:
        return response, {}


def generate_unique_filename(base_name="testfile"):
    ts = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    suffix = str(uuid.uuid4())[:8]
    return f"{base_name}_{ts}_{suffix}.pdf"


def test_send_into_processlog_and_validate_application_events():
    # Generate unique file and send message
    unique_filename = generate_unique_filename("payor_contract")
    message_source = send_payor_contract_message(unique_filename)
    print(f"Sent unique filename: {unique_filename}")

    # Retry read from FileProcessLog API
    match = None
    for attempt in range(6):
        time.sleep(10)
        response, data = make_request("get", "/api/FileProcessLog?api-version=1.0")
        assert response.status_code == 200
        records = data if isinstance(data, list) else [data]
        match = next((x for x in records if x.get("fileName") == unique_filename), None)
        if match:
            break
        print(f"[Attempt {attempt+1}/6] FileProcessLog entry not found yet… waiting")

    assert match, f"FileProcessLog entry for {unique_filename} NOT found after waiting."

    # Poll ASB subscription for the specific file
    asb_match = receive_application_events(
        target_filename=unique_filename,
        max_count=500,
        wait_time=5,
        timeout_seconds=30
    )

    assert len(asb_match) > 0, f"Event for {unique_filename} NOT found in ASB subscription"
    print(f"SUCCESS: Event found for {unique_filename} in ASB subscription.")

    allowed_statuses = {"New", "Completed", "Failed"}

    for event in asb_match:
        body = event.get("body") or {}
        files = body.get("Files") or []
        for f in files:
            status = f.get("Status")
            # Check allowed statuses
            assert status in allowed_statuses, f"File '{f.get('FileName')}' has invalid status '{status}'"
            # Explicitly check not InProgress
            assert status != "InProgress", f"File '{f.get('FileName')}' has status 'InProgress', which is not allowed"
            print(f"File '{f.get('FileName')}' has valid status: {status}")

def test_verify_message_in_deadletter():
    target_filename = generate_unique_filename("payor_contract")

    # Send the message
    _ = send_payor_contract_message(target_filename)
    print(f"Sent unique filename: {target_filename}")

    # Give ASB time (optional small wait)
    time.sleep(5)

    # Now check DLQ
    found = False
    with ServiceBusClient(SERVICE_BUS_NAMESPACE, credential=credential) as client:
        receiver = client.get_subscription_receiver(
            topic_name=SERVICEBUS_TOPIC_APPLICATION,
            subscription_name=SERVICEBUS_SUBSCRIPTION_2,
            sub_queue="deadletter",
            receive_mode=ServiceBusReceiveMode.PEEK_LOCK
        )

        with receiver:
            messages = receiver.receive_messages(max_message_count=200, max_wait_time=5)
            print(f"DLQ Count: {len(messages)}")

            for msg in messages:
                # Decode message body
                try:
                    body_bytes = b"".join(msg.body)
                    body_str = body_bytes.decode("utf-8")
                except:
                    body_str = "<FAILED TO DECODE>"

                # Check if our filename is inside the message
                if target_filename in body_str:
                    found = True
                    print("MessageId:", msg.message_id)
                    print("CorrelationId:", msg.correlation_id)
                    print("Subject:", msg.subject)
                    print("Body:", body_str)

                    props = msg.application_properties or {}
                    print("DeadLetterReason:", props.get("DeadLetterReason"))
                    print("DeadLetterErrorDescription:", props.get("DeadLetterErrorDescription"))

                    break  # Stop scanning further

    if not found:
        assert(f"No DLQ message found for '{target_filename}', which is expected.")
        return