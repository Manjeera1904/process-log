import json
import uuid
import concurrent.futures
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os
import time
from azure.identity import ClientSecretCredential
import requests
from datetime import datetime, UTC, date
import asb_utils
import threading


def test_get_client_id():
    """Test to fetch and save client ID"""
    client_name = f"db{asb_utils.env}client"
    url = f"{asb_utils.pcapiBaseUrl}/api/Client/name/{client_name}"
    headers = {
        "Authorization": f"Bearer {asb_utils.token}",
        "Accept": "application/json"
    }
    params = {
        "cultureCode": asb_utils.cultureCode,
        "api-version": asb_utils.apiVersion
    }

    response = requests.get(url, headers=headers, params=params)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    if response.status_code == 200:
        data = response.json()
        asb_utils.config["common"]["testClientId"] = data.get("id")
        asb_utils.save_config(asb_utils.config)
        print(f"Client ID saved: {data.get('id')}")
    else:
        print(f"Failed to fetch client. Status code: {response.status_code}, Response: {response.text}")
        return None

def test_send_and_validate_by_filename_versioned(message_version="3.0", should_pass=True):
    """Test using unique filenames to track messages with specified message version"""
    unique_filename = asb_utils.generate_unique_filename(f"v{message_version.replace('.', '_')}_contract")
    message_source = f"ConsoleTestApp_{str(uuid.uuid4())[:8]}"
    
    # Build message using helper functions
    message_body = asb_utils.build_base_message_body()
    message_body = asb_utils.add_message_to_body(message_body, "Information", f"Testing MessageVersion {message_version}")
    message_body = asb_utils.add_file_to_message(message_body, unique_filename, f"HASH_V{message_version.replace('.', '')}", "New")
    
    # Send message with specified version
    asb_utils.send_and_track_file(unique_filename, message_body, message_source, message_version)
    time.sleep(30)
    
    # Verify using FileProcessLog API
    file_records = asb_utils.get_file_process_logs()
    matching_file = asb_utils.find_file_by_filename(file_records, unique_filename)
    
    if should_pass:
        # We expect to find the file
        if matching_file:
            print(f" SUCCESS: Found FileProcessLog record with filename '{unique_filename}' using MessageVersion {message_version}")
            print(f" FileProcessLog ID: {matching_file.get('id')}")
            return matching_file
        else:
            print(f" FAILED: No FileProcessLog record found for filename '{unique_filename}' using MessageVersion {message_version}")
            assert False, f"FileProcessLog record with filename '{unique_filename}' not found for MessageVersion {message_version}!"
    else:
        # We expect NOT to find the file
        if matching_file:
            print(f" UNEXPECTED: Found FileProcessLog record with filename '{unique_filename}' using MessageVersion {message_version}")
            print(" This version should be rejected!")
            assert False, f"MessageVersion {message_version} should be rejected, but found FileProcessLog record!"
        else:
            print(f" EXPECTED: No FileProcessLog record found for filename '{unique_filename}' using MessageVersion {message_version}")
            assert True, f"MessageVersion {message_version} was correctly rejected!"


def test_version_2_should_pass():
    """MessageVersion 2.0 should pass"""
    test_send_and_validate_by_filename_versioned("2.0", should_pass=True)

def test_version_1_should_fail():
    """MessageVersion 1.0 should fail"""
    test_send_and_validate_by_filename_versioned("1.0", should_pass=False)

def test_version_3_should_pass():
    """MessageVersion 3.0 should pass"""
    test_send_and_validate_by_filename_versioned("3.0", should_pass=True)

def test_out_of_order_statuses_must_be_new():
    """FAIL if backend sets any status other than 'New' for out-of-order sequences"""
    unique_filename = asb_utils.generate_unique_filename("out_of_order")
    message_source = f"ConsoleTestApp_{str(uuid.uuid4())[:8]}"
    
    # Build out-of-order message
    message_body = asb_utils.build_base_message_body()
    
    # Add messages in out-of-order sequence
    message_body = asb_utils.add_message_to_body(message_body, "Status", "Processing completed")
    message_body = asb_utils.add_message_to_body(message_body, "Information", "Process started successfully")
    message_body = asb_utils.add_message_to_body(message_body, "Error", "Validation failed")
    message_body = asb_utils.add_message_to_body(message_body, "Information", "File validated")
    
    # Add file with Completed status (illogical)
    message_body = asb_utils.add_file_to_message(message_body, unique_filename, "HASH_OUT_OF_ORDER", "Completed")
    
    # Send message
    asb_utils.send_and_track_file(unique_filename, message_body, message_source)
    time.sleep(30)
    
    # Find the FileProcessLog record
    file_records = asb_utils.get_file_process_logs()
    matching_file = asb_utils.find_file_by_filename(file_records, unique_filename)
    assert matching_file is not None, f"No FileProcessLog found for filename: {unique_filename}"
    
    # Get the related ProcessLog
    process_log_id = matching_file.get('processLogId')
    assert process_log_id is not None, "FileProcessLog has no associated ProcessLog"
    
    process_response, process_data = asb_utils.get_process_log(process_log_id)
    assert process_response.status_code == 200
    
    final_status = process_data.get('status', 'N/A')
    
    assert final_status == "New", (
        f"Out-of-order message should remain in 'New' status\n"
        f"   Expected: 'New'\n"
        f"   Actual: '{final_status}'\n"
        f"   Filename: {unique_filename}\n"
        f"   ProcessLog ID: {process_log_id}\n"
        f"   Full Record: {json.dumps(process_data, indent=2)}\n"
    )
    
    print(f" SUCCESS: Out-of-order message correctly kept status as 'New'")

def test_same_file_multiple_times_acceptance():
    """Test: Backend accepts same file repeated multiple times in one message"""
    unique_filename = asb_utils.generate_unique_filename("multi_file_test")
    message_source = f"ConsoleTestApp_{str(uuid.uuid4())[:8]}"
    
    # Create message with same file repeated 6 times
    message_body = asb_utils.build_base_message_body()
    message_body = asb_utils.add_message_to_body(message_body, "Information", "Testing same file acceptance")
    
    # Add the same file 6 times
    for i in range(6):
        file_data = {
            "FileName": unique_filename,
            "FilePath": "/files/2025/11/",
            "FileSize": 1024,
            "FileType": "application/pdf",
            "FileHash": f"SAMEHASH_{str(uuid.uuid4())[:8]}",
            "FilePurpose": "Originating Contract",
            "Status": "InProgress",
            "Messages": [{"MessageLevel": "Information", "Message": f"File {i + 1}"}]
        }
        message_body["Files"].append(file_data)
    
    asb_utils.send_payor_contract_message_custom(message_body, message_source)
    print(f" Sent message with same file '{unique_filename}' repeated 6 times")
    time.sleep(30)
    
    # Check if any FileProcessLog was created
    file_records = asb_utils.get_file_process_logs()
    matching_files = [f for f in file_records if f.get("fileName") == unique_filename]
    
    print(f" RESULT: Backend {'ACCEPTED' if matching_files else 'REJECTED'} 6 identical files")
    print(f"   Files created: {len(matching_files)}")
    
    assert len(matching_files) > 0, "No FileProcessLog records created for the test files"


def test_detect_duplicate_file_processing_should_fail():
    """FAIL if backend creates multiple FileProcessLog records for duplicate files"""
    unique_filename = asb_utils.generate_unique_filename("duplicate_detection")
    message_source = f"ConsoleTestApp_{str(uuid.uuid4())[:8]}"
    
    # Build message with same file 6 times
    message_body = asb_utils.build_base_message_body()
    message_body = asb_utils.add_message_to_body(message_body, "Information", "Duplicate file detection test")
    
    # Add the same file 6 times
    for i in range(6):
        file_data = {
            "FileName": unique_filename,
            "FilePath": "/detection/test/",
            "FileSize": 1000,
            "FileType": "application/pdf",
            "FileHash": f"DETECTIONHASH_{str(uuid.uuid4())[:8]}",
            "Status": "InProgress",
            "FilePurpose": "Originating Contract",
            "Messages": [{"MessageLevel": "Information", "Message": f"File {i + 1}"}]
        }
        message_body["Files"].append(file_data)
    
    asb_utils.send_payor_contract_message_custom(message_body, message_source)
    print(f" Sent duplicate detection test message with filename: {unique_filename}")
    time.sleep(30)
    
    # Get FileProcessLog records
    file_records = asb_utils.get_file_process_logs()
    
    # Find all files with our unique filename
    our_files = [f for f in file_records if f.get("fileName") == unique_filename]
    
    print(f"\n DUPLICATE FILE DETECTION RESULTS:")
    print(f"   Filename: {unique_filename}")
    print(f"   Files Sent: 6 (all identical)")
    print(f"   Files Processed: {len(our_files)}")
    
    # THIS WILL MAKE THE TEST FAIL IF DUPLICATES ARE PROCESSED
    assert len(our_files) == 1, (
            f" BACKEND PROCESSED DUPLICATE FILES\n"
            f"   Expected: 1 FileProcessLog record (duplicates should be detected)\n"
            f"   Actual: {len(our_files)} FileProcessLog records created\n"
            f"   FileProcessLog IDs created:\n" +
            "\n".join([f"     - {f.get('id')}" for f in our_files])
    )
    
    print(f" SUCCESS: Backend correctly detected duplicates - processed only 1 file")


def test_concurrent_ordering():
    """Test message ordering when sent concurrently using filenames"""
    base_filename = f"conc_order_{datetime.now(UTC).strftime('%H%M%S')}"
    send_order = []
    order_lock = threading.Lock()
    
    def send_single_message(i):
        """Send one message with precise timestamp and unique filename"""
        unique_filename = f"{base_filename}_{i}.pdf"
        message_source = f"ConsoleTestApp_concorder{i}"
        send_time = datetime.now(UTC)
        
        # Build message using helper functions
        message_body = asb_utils.build_base_message_body()
        message_body = asb_utils.add_message_to_body(message_body, "Information", f"Concurrent order test {i}")
        message_body = asb_utils.add_file_to_message(message_body, unique_filename, f"CONC_ORDER_HASH_{i}", "InProgress")
        
        asb_utils.send_payor_contract_message_custom(message_body, message_source)
        
        # Thread-safe recording of send order
        with order_lock:
            send_order.append({
                "message_number": i,
                "filename": unique_filename,
                "send_time": send_time
            })
            print(f" Sent message {i} with filename '{unique_filename}' at {send_time.strftime('%H:%M:%S.%f')[:-3]}")
        
        return unique_filename
    
    # Send 5 messages concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(send_single_message, i) for i in range(5)]
        filenames = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    time.sleep(60)
    
    # Check results and analyze ordering
    file_records = asb_utils.get_file_process_logs()
    
    # Match processed records with send order
    processed_records = []
    for file_record in file_records:
        filename = file_record.get("fileName")
        for sent_msg in send_order:
            if filename == sent_msg["filename"]:
                # Get the ProcessLog to check start timestamp
                process_log_id = file_record.get("processLogId")
                if process_log_id:
                    process_response, process_data = asb_utils.get_process_log(process_log_id)
                    if process_response.status_code == 200:
                        process_start_time = datetime.fromisoformat(
                            process_data.get("startTimestamp").replace('Z', '+00:00'))
                        processed_records.append({
                            "message_number": sent_msg["message_number"],
                            "filename": sent_msg["filename"],
                            "send_time": sent_msg["send_time"],
                            "process_start_time": process_start_time
                        })
                break
    
    # Sort by send time and process time
    send_sorted = sorted(processed_records, key=lambda x: x["send_time"])
    process_sorted = sorted(processed_records, key=lambda x: x["process_start_time"])
    
    print(f"\n CONCURRENT ORDERING RESULTS:")
    print(f"   Send Order (by time):    {[msg['message_number'] for msg in send_sorted]}")
    print(f"   Process Order (by time): {[msg['message_number'] for msg in process_sorted]}")
    
    # Check if ordering is preserved despite concurrent sending
    send_nums = [msg["message_number"] for msg in send_sorted]
    process_nums = [msg["message_number"] for msg in process_sorted]
    
    if send_nums == process_nums:
        print(f" PERFECT ORDERING: Despite concurrent sending!")
    else:
        print(f"  ORDERING LOST: Concurrent sending affected processing order")
    
    assert len(processed_records) == 5, f"Expected 5 records, got {len(processed_records)}"