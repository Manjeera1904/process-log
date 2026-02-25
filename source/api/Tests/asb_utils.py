import json
import uuid
import time
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.identity import DefaultAzureCredential
from azure.identity import ClientSecretCredential
import os
import requests
from datetime import datetime, UTC
from runtests import config_path, apiBaseUrl, pc_api_base_url, env
from azure.servicebus import ServiceBusReceiveMode


with open(config_path, 'r') as configFile:
    configData = json.load(configFile)

def load_config():
    with open(config_path) as f:
        return json.load(f)

config = load_config()
token = config["tokenApi"]["token"]
API_BASE_URL = apiBaseUrl
clientId = config["common"]["testClientId"]
pcapiBaseUrl = pc_api_base_url
apiVersion = configData["common"]["apiVersion"]
cultureCode = configData["common"]["cultureCode"]



SERVICE_BUS_NAMESPACE = os.getenv("SERVICEBUS_NAMESPACE")
TOPIC_NAME = os.getenv("SERVICEBUS_TOPIC")
SUBSCRIPTION_NAME = os.getenv("SERVICEBUS_SUBSCRIPTION_1")
SERVICEBUS_TOPIC_APPLICATION =  os.getenv("SERVICEBUS_TOPIC_APPLICATION")
SERVICEBUS_SUBSCRIPTION_2 =  os.getenv("SERVICEBUS_SUBSCRIPTION_2")

tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")

if not all([tenant_id, client_id, client_secret]):
    raise EnvironmentError("Missing Azure credentials in environment variables.")

credential = ClientSecretCredential(tenant_id, client_id, client_secret)

def save_config(config_data):
    with open(config_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print("Config data saved successfully.")


def make_request(method, endpoint, data=None):
    """Generic method for making HTTP requests"""
    url = f"{API_BASE_URL}{endpoint}"
    print(f"{method.upper()} URL: {url}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-EI-ClientId": clientId
    }
    try:
        if method == 'post':
            response = requests.post(url, headers=headers, json=data, verify=False)
        elif method == 'get':
            response = requests.get(url, headers=headers, verify=False)
        elif method == 'put':
            response = requests.put(url, headers=headers, json=data, verify=False)
        else:
            raise ValueError("Invalid method type provided.")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        raise

    try:
        response_data = response.json()
        print("Response body:", json.dumps(response_data, indent=4))
    except json.JSONDecodeError:
        print("Response body is not JSON:", response.text)
        response_data = {}

    return response, response_data

def build_message():
    message_id = str(uuid.uuid4())
    correlation_id = str(uuid.uuid4())

    body = {
        "Files": [
            {
                "FileId": str(uuid.uuid4()),
                "FileName": f"TestFile-{int(time.time())}.txt",
                "FileSize": 1234
            }
        ]
    }

    header = {
        "MessageId": message_id,
        "CorrelationId": correlation_id,
        "ContentType": "application/json"
    }

    msg = ServiceBusMessage(
        json.dumps(body),
        message_id=message_id,
        correlation_id=correlation_id,
        content_type="application/json"
    )

    return msg, header, body



def send_message(header=None, body=None):
    if header is None or body is None:
        msg, header, body = build_message()
    else:
        msg = ServiceBusMessage(
            json.dumps(body),
            message_id=header["MessageId"],
            correlation_id=header["CorrelationId"],
            content_type="application/json"
        )

    with ServiceBusClient(SERVICE_BUS_NAMESPACE, credential=credential) as client:
        sender = client.get_topic_sender(topic_name=TOPIC_NAME)
        with sender:
            sender.send_messages(msg)

    return header, body




def send_payor_contract_message(file_name):
    message_source = f"ConsoleTestApp_{uuid.uuid4().hex[:8]}"
    body = {
        "Requester": "464b6f6c-ebf9-4c73-991f-3391243c2460",
        "ReceiveTimestamp": datetime.now(UTC).isoformat(),
        "Messages": [{"MessageLevel": "Information", "Message": "Testing unique filename"}],
        "Files": [{
            "FileName": file_name,
            "FilePath": "/files/2025/11/",
            "FileSize": 256,
            "FileType": "application/pdf",
            "FileHash": f"HASH_{uuid.uuid4().hex[:8]}",
            "Status": "New",
        }]
    }

    msg = ServiceBusMessage(
        json.dumps(body),
        message_id=str(uuid.uuid4()),
        correlation_id=str(uuid.uuid4()),
        subject="PayorContractAnalysis",
        content_type="application/json"
    )
    msg.application_properties = {
        "MessageSource": message_source,
        "MessageStatus": "New",
        "ClientIdentifier": clientId,
        "SendingApplication": message_source,
        "SendingApplicationId": "unknown",
    }

    with ServiceBusClient(SERVICE_BUS_NAMESPACE, credential=credential) as client:
        sender = client.get_topic_sender(topic_name=TOPIC_NAME)
        with sender:
            sender.send_messages(msg)

    return message_source


def receive_application_events(target_filename, max_count=500, wait_time=5, timeout_seconds=60):

    start = time.time()
    matching_events = []

    print(f"\n--- Polling for messages with FileName='{target_filename}' ---")

    with ServiceBusClient(SERVICE_BUS_NAMESPACE, credential=credential) as client:
        receiver = client.get_subscription_receiver(
            topic_name=SERVICEBUS_TOPIC_APPLICATION,
            subscription_name=SERVICEBUS_SUBSCRIPTION_2,
            receive_mode=ServiceBusReceiveMode.PEEK_LOCK
        )

        with receiver:
            while time.time() - start < timeout_seconds:
                messages = receiver.receive_messages(
                    max_message_count=max_count,
                    max_wait_time=wait_time
                )

                if not messages:
                    time.sleep(1)
                    continue

                for msg in messages:
                    try:
                        body_bytes = (
                            b"".join(msg.body)
                            if hasattr(msg.body, "__iter__")
                            else msg.body
                        )
                        body_str = (
                            body_bytes.decode()
                            if isinstance(body_bytes, bytes)
                            else str(body_bytes)
                        )
                        body_json = json.loads(body_str)
                    except Exception as e:
                        print("Failed to decode message body:", e)
                        body_json = {}

                    inner_body = body_json.get("message", body_json)
                    print("\nDEBUG - Received event body:\n", json.dumps(inner_body, indent=2))

                    # if msg.application_properties:
                    #     msg.application_properties = {
                    #         (k.decode() if isinstance(k, bytes) else k):
                    #             (v.decode() if isinstance(v, bytes) else v)
                    #         for k, v in msg.application_properties.items()
                    #     }


                    event = {
                        "messageId": msg.message_id,
                        "correlationId": msg.correlation_id,
                        "subject": msg.subject,
                        "messageStatus": msg.application_properties.get("MessageStatus") if msg.application_properties else None,
                        "messageSource": msg.application_properties.get("MessageSource") if msg.application_properties else None,
                        "clientIdentifier": msg.application_properties.get("ClientIdentifier") if msg.application_properties else None,
                        "body": inner_body,
                        "application_properties": msg.application_properties
                    }

                    # --- Check for matching filename ---
                    files = inner_body.get("Files") or []

                    if any(f.get("FileName", "").endswith(target_filename) for f in files):
                        matching_events.append(event)
                        receiver.complete_message(msg)
                    else:
                        receiver.abandon_message(msg)

                # Found a match → exit polling loop
                if matching_events:
                    break

    # After timeout
    if not matching_events:
        raise AssertionError(
            f"No event found in subscription with FileName='{target_filename}'"
        )

    print(f"Received {len(matching_events)} matching event(s) for '{target_filename}'")
    return matching_events


def send_file_message(file_name, status="New"):
    message_source = f"ConsoleTestApp_{uuid.uuid4().hex[:8]}"
    body = {
        "Requester": "464b6f6c-ebf9-4c73-991f-3391243c2460",
        "ReceiveTimestamp": datetime.now(UTC).isoformat(),
        "Messages": [{"MessageLevel": "Information", "Message": f"Testing {status} status"}],
        "Files": [{
            "FileName": file_name,
            "FilePath": "/files/2025/11/",
            "FileSize": 256,
            "FileType": "application/pdf",
            "FileHash": f"HASH_{uuid.uuid4().hex[:8]}",
            "Status": status,
        }]
    }

    msg = ServiceBusMessage(
        json.dumps(body),
        message_id=str(uuid.uuid4()),
        correlation_id=str(uuid.uuid4()),
        subject="PayorContractAnalysis",
        content_type="application/json"
    )
    msg.application_properties = {
        "MessageSource": message_source,
        "MessageStatus": status,
        "ClientIdentifier": clientId,
        "SendingApplication": message_source,
        "SendingApplicationId": "unknown",
    }

    with ServiceBusClient(SERVICE_BUS_NAMESPACE, credential=credential) as client:
        sender = client.get_topic_sender(topic_name=TOPIC_NAME)
        with sender:
            sender.send_messages(msg)

    return file_name, status

def generate_unique_filename(base_name="testfile"):
    """Generate unique filename with timestamp and random suffix"""
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    random_suffix = str(uuid.uuid4())[:8]
    return f"{base_name}_{timestamp}_{random_suffix}.pdf"

def send_payor_contract_message_custom(message_body, message_source, message_version="3.0"):
    """Send custom message to Service Bus with configurable message version"""
    body = json.dumps(message_body)

    sb_message = ServiceBusMessage(
        body,
        message_id=str(uuid.uuid4()),
        correlation_id=str(uuid.uuid4()),
        subject="PayorContractAnalysis",
        content_type="application/json"
    )

    sb_message.application_properties = {
        "MessageSource": message_source,
        "MessageStatus": "New",
        "ClientIdentifier": clientId,
        "SendingApplication": message_source,
        "SendingApplicationId": "unknown",
        "MessageVersion": message_version 
    }

    with ServiceBusClient(SERVICE_BUS_NAMESPACE, credential) as client:
        sender = client.get_topic_sender(topic_name=TOPIC_NAME)
        with sender:
            sender.send_messages(sb_message)
            print(f" Sent custom message with MessageId={sb_message.message_id}, Version={message_version}")
            return message_source
        
def build_base_message_body():
    """Create base message structure that can be customized for tests"""
    return {
        "Requester": "464b6f6c-ebf9-4c73-991f-3391243c2460",
        "ReceiveTimestamp": datetime.now(UTC).isoformat(),
        "Messages": [],
        "Files": []
    }


def add_file_to_message(message_body, filename, file_hash_prefix="HASH", status="New"):
    """Add a file to the message body"""
    file_data = {
        "FileName": filename,
        "FilePath": "/files/2025/11/",
        "FileSize": 256,
        "FileType": "application/pdf",
        "FileHash": f"{file_hash_prefix}_{str(uuid.uuid4())[:8]}",
        "FilePurpose": "Originating Contract",
        "Status": status,
        "Messages": [
            {"MessageLevel": "Warning", "Message": "File uploaded to blob"},
            {"MessageLevel": "Status", "Message": "Checksum verified"},
        ]
    }
    
    message_body["Files"].append(file_data)
    return message_body


def add_message_to_body(message_body, level, text):
    """Add a message to the message body"""
    message_body["Messages"].append({"MessageLevel": level, "Message": text})
    return message_body


def send_and_track_file(unique_filename, message_body, message_source, message_version="3.0"):
    send_payor_contract_message_custom(message_body, message_source, message_version)
    print(f" Sent message with filename: {unique_filename}, version: {message_version}")
    return unique_filename


def get_file_process_logs():
    """Get all FileProcessLog records"""
    response, response_data = make_request('get', "/api/FileProcessLog?api-version=1.0")
    assert response.status_code == 200
    return response_data if isinstance(response_data, list) else [response_data]


def find_file_by_filename(file_records, unique_filename):
    """Find a file record by filename"""
    return next((f for f in file_records if f.get("fileName") == unique_filename), None)


def get_process_log(process_log_id):
    """Get ProcessLog by ID"""
    return make_request('get', f"/api/ProcessLog/{process_log_id}?api-version=1.0")

