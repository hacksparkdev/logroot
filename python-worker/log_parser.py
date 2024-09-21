import socket
import json
from elasticsearch import Elasticsearch
from datetime import datetime

# Elasticsearch connection
es = Elasticsearch([{'host': '10.10.20.107', 'port': 9200, 'scgene': 'http'}])  # Replace with your Elasticsearch host

# Function to clean and parse logs
def clean_log(data):
    try:
        # Decode the log data to string
        log_str = data.decode('utf-8')

        # Attempt to parse the log string into JSON (Winlogbeat sends logs in JSON format)
        parsed_log = json.loads(log_str)

        # Clean the log (remove non-UTF-8 characters if necessary)
        cleaned_log = {
            k: ''.join([c for c in str(v) if ord(c) < 128]) for k, v in parsed_log.items()
        }

        return cleaned_log
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None
    except Exception as e:
        print(f"Error cleaning log: {e}")
        return None

# Function to send log to Elasticsearch
def send_to_elasticsearch(log):
    try:
        index_name = "winlogbeat-" + datetime.now().strftime("%Y.%m.%d")  # Create a daily index
        response = es.index(index=index_name, body=log)
        print(f"Log successfully indexed to Elasticsearch: {response['_id']}")
    except Exception as e:
        print(f"Error sending log to Elasticsearch: {e}")

# TCP listener to receive logs from Winlogbeat
def tcp_listener(host='0.0.0.0', port=5045):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Listening for logs on {host}:{port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        data = client_socket.recv(1024)
        if data:
            cleaned_log = clean_log(data)
            if cleaned_log:
                send_to_elasticsearch(cleaned_log)
        client_socket.close()

if __name__ == "__main__":
    # Start the TCP listener
    tcp_listener()

