# connection.py

import wmi

def connect_to_workstation(workstation_name, user, password):
    try:
        connection = wmi.WMI(remote_server=workstation_name, user=user, password=password)
        return connection
    except Exception as e:
        print(f"Error connecting to {workstation_name}: {e}")
        return None

