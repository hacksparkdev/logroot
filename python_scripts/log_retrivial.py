# log_retrieval.py

def retrieve_logs(connection, log_type='Application'):
    logs = []
    try:
        for log in connection.Win32_NTLogEvent(LogFile=log_type):
            logs.append({
                'EventID': log.EventID,
                'SourceName': log.SourceName,
                'TimeGenerated': log.TimeGenerated.Format(),
                'EventType': log.EventType,
                'Category': log.EventCategory,
                'Message': log.Strings
            })
    except Exception as e:
        print(f"Error retrieving logs: {e}")
    return logs

