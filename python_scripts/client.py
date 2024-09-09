# client.py

import time
import json
import requests
from config import WORKSTATIONS, LOGSTASH_HOST, LOGSTASH_PORT
from connection import connect_to_workstation
from log_retrieval import retrieve_logs

LOGSTASH_URL = f'http://{10.10.20.106}:{5044}'

def send_to_logstash(log_entry):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(LOGSTASH_URL, headers=headers, data=json.dumps(log_entry))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending log to Logstash: {e}")

def monitor_logs():
    for workstation in WORKSTATIONS:
        name = workstation['name']
        user = workstation['user']
        password = workstation['password']
        connection = connect_to_workstation(name, user, password)
        if connection:
            while True:
                logs = retrieve_logs(connection)
                for log in logs:
                    send_to_logstash(log)
                time.sleep(10)  # Poll every 10 seconds

if __name__ == "__main__":
    monitor_logs()

