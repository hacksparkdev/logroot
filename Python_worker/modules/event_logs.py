import win32evtlog
from elasticsearch import Elasticsearch
import time

es = Elasticsearch(['http://10.10.20.107:9200'])  # Adjust to your Elasticsearch URL

def collect_windows_event_logs(log_type='Security'):
    server = 'localhost'
    log = win32evtlog.OpenEventLog(server, log_type)
    collected_logs = []  # To hold the logs temporarily

    while True:
        events = win32evtlog.ReadEventLog(log, win32evtlog.EVENTLOG_SEQUENTIAL_READ | win32evtlog.EVENTLOG_FORWARDS_READ, 0)
        
        if events:
            for event in events:
                event_data = {
                    'event_id': event.EventID,
                    'source': event.SourceName,
                    'message': win32evtlog.FormatMessage(event),
                    'timestamp': event.TimeGenerated.isoformat()
                }
                
                # Send event to Elasticsearch
                es.index(index='security-logs', document=event_data)

                # Collect logs to return them
                collected_logs.append(event_data)

        time.sleep(5)  # Adjust polling interval as needed

        # Return collected logs for display purposes
        if collected_logs:
            return collected_logs

    win32evtlog.CloseEventLog(log)

def run():
    """This is the required run function for the module."""
    return collect_windows_event_logs()

if __name__ == "__main__":
    run()

