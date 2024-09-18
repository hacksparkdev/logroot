import hashlib
import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import schedule
import time
import importlib.util

es = Elasticsearch(['http://10.10.20.107:9200'])  # Change to your Elasticsearch server's IP and port

# Function to load and run the module
def load_and_run_module(module_name):
    try:
        # Dynamically load the module from the modules directory
        module_path = f'./modules/{module_name}.py'
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Check if the module has a run() function and execute it
        if hasattr(module, 'run'):
            output = module.run()  # Collect output from the module
            return True, f"Module executed successfully. Output: {output}"
        else:
            return False, f"Module {module_name} has no 'run' function"
    
    except FileNotFoundError:
        return False, f"Module {module_name} not found"
    except Exception as e:
        return False, f"Error while running module {module_name}: {str(e)}"

# Poll Elasticsearch for pending tasks
def poll_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)

