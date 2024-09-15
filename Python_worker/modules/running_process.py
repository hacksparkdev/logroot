import psutil

def run():
    # Capture a list of running processes
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        processes.append({
            'pid': proc.info['pid'],
            'name': proc.info['name']
        })

    # Return the list of processes
    return processes
