import socket
import json
import requests

# Logstash server details
LOGSTASH_URL = 'http://10.10.20.106:5044'  # Replace with your Logstash IP and port

# Function to clean and convert log to JSON
def clean_log(data):
    try:
        # Decode the log data to string
        log_str = data.decode('utf-8')

        # Attempt to parse the log string into JSON (Winlogbeat usually sends logs in JSON format)
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

# Function to send log to Logstash
def send_to_logstash(log):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(LOGSTASH_URL, data=json.dumps(log), headers=headers)
        if response.status_code == 200:
            print("Log successfully sent to Logstash")
        else:
            print(f"Failed to send log to Logstash: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending log to Logstash: {e}")

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
                send_to_logstash(cleaned_log)
        client_socket.close()

if __name__ == "__main__":
    # Start the TCP listener
    tcp_listener()

