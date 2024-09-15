import win32evtlog as winevt

def read_event_log(log_type='Security'):
    server = 'localhost'
    handle = winevt.OpenEventLog(server, log_type)
    total = winevt.GetNumberOfEventLogRecords(handle)

    flags = winevt.EVENTLOG_BACKWARDS_READ | winevt.EVENTLOG_SEQUENTIAL_READ
    events = winevt.ReadEventLog(handle, flags, 0)

    event_data = []

    for event in events:
        event_info = {
            'EventID': event.EventID,
            'Source': event.SourceName
        }
        event_data.append(event_info)

    # Return the list of event logs instead of printing
    return event_data

def run():
    # Call the read_event_log function and return the result
    return read_event_log()
