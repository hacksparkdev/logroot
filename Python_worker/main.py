import socket
from elasticsearch import Elasticsearch
import time
import importlib.util

# Get the current machine's identifier (hostname)
machine_id = socket.gethostname()

es = Elasticsearch(['http://10.10.20.107:9200'])

# Function to load and run the module
def load_and_run_module(module_name):
    try:
        module_path = f'./modules/{module_name}.py'
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, 'run'):
            output = module.run()
            return True, f"Module executed successfully. Output: {output}"
        else:
            return False, f"Module {module_name} has no 'run' function"
    except FileNotFoundError:
        return False, f"Module {module_name} not found"
    except Exception as e:
        return False, f"Error while running module {module_name}: {str(e)}"

# Poll Elasticsearch for pending tasks assigned to this machine
def poll_tasks():
    while True:
        # Search for tasks assigned to this machine and in "pending" status
        res = es.search(index='python-tasks', body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"status": "pending"}},
                        {"match": {"target_machine": machine_id}}  # Only fetch tasks for this machine
                    ]
                }
            }
        })

        # Process each task found in Elasticsearch
        for hit in res['hits']['hits']:
            task_id = hit['_id']
            module_name = hit['_source']['moduleName']

            print(f"Running module {module_name} on machine {machine_id} for task {task_id}")

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

        time.sleep(5)

if __name__ == "__main__":
    print(f"Python worker running on machine: {machine_id}")
    poll_tasks()

