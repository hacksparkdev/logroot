import socket
import time
import importlib.util
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://10.10.20.107:9200'])  # Change to your Elasticsearch server's IP and port

# Get the current machine's hostname
current_hostname = socket.gethostname()

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
        # Search for tasks in the "pending" state in the python-tasks index
        res = es.search(index='python-tasks', body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"status": "pending"}},
                        {"match": {"hostname": current_hostname}}  # Only match tasks for this hostname
                    ]
                }
            }
        })

        # Process each task found in Elasticsearch
        for hit in res['hits']['hits']:
            task_id = hit['_id']
            module_name = hit['_source']['moduleName']

            print(f"Running module {module_name} for task {task_id} on {current_hostname}")

            # Update task status to "running"
            es.update(index='python-tasks', id=task_id, body={
                "doc": {"status": "running"}
            })

            # Run the requested module and capture the result
            success, result = load_and_run_module(module_name)
            new_status = "completed" if success else "failed"

            # Update Elasticsearch with the new task status and result
            es.update(index='python-tasks', id=task_id, body={
                "doc": {
                    "status": new_status,
                    "result": result
                }
            })

        # Poll every 5 seconds to look for new tasks
        time.sleep(5)

if __name__ == "__main__":
    poll_tasks()

