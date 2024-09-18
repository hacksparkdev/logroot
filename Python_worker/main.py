import hashlib
import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import schedule
import time
import logging

# Hashing function
def compute_hash(file_path):
    hash_func = hashlib.sha256()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        return None

# Load and save known hashes
def load_known_hashes():
    with open('known_hashes.json', 'r') as file:
        return json.load(file)

def save_known_hashes(hashes):
    with open('known_hashes.json', 'w') as file:
        json.dump(hashes, file, indent=4)

# Real-time file integrity handler
class FileIntegrityHandler(PatternMatchingEventHandler):
    def __init__(self, known_hashes):
        super().__init__(patterns=["*.exe", "*.dll", "*.log", "*.ini", "*.msc"])
        self.known_hashes = known_hashes

    def on_modified(self, event):
        current_hash = compute_hash(event.src_path)
        if current_hash != self.known_hashes.get(event.src_path):
            logging.warning(f"File integrity compromised: {event.src_path}")

# Monitor a directory
def monitor_directory(directory, known_hashes):
    event_handler = FileIntegrityHandler(known_hashes)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Periodic check function
def periodic_check(known_hashes):
    for file_path, known_hash in known_hashes.items():
        current_hash = compute_hash(file_path)
        if current_hash != known_hash:
            logging.warning(f"File integrity compromised: {file_path}")

# Main run function
def run():
    logging.basicConfig(filename='integrity_monitor.log', level=logging.INFO)
    known_hashes = load_known_hashes()

    # Monitor directory in real-time
    monitor_directory('C:\\Windows\\System32', known_hashes)

    # Schedule periodic checks
    schedule.every(10).minutes.do(periodic_check, known_hashes)
    while True:
        schedule.run_pending()
        time.sleep(1)

