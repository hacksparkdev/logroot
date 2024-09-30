import json
import requests
import importlib.util
import os
import time

# Load the modules.json from the config folder
def load_modules():
    config_path = os.path.join(os.getcwd(), 'config', 'modules.json')
    with open(config_path, 'r') as f:
        return json.load(f)["modules"]

# Function to run the requested module
def run_module(module_name, params):
    modules = load_modules()
    
    for module in modules:
        if module["name"] == module_name:
            script = module["script"]
            script_path = os.path.join(os.getcwd(), 'modules', script)  # Load script from 'modules' folder
            
            if os.path.exists(script_path):
                # Dynamically load and run the module from the 'modules' folder
                spec = importlib.util.spec_from_file_location(module_name, script_path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                
                if hasattr(mod, "run"):
                    return mod.run(params)
                else:
                    raise Exception(f"Module {module_name} does not have a 'run' function.")
            else:
                raise FileNotFoundError(f"Module script {script} not found in 'modules' directory.")
    
    raise Exception(f"Module {module_name} not found in the JSON config.")

# Function to send results to Elasticsearch
def send_results_to_elasticsearch(result):
    es_url = "http://<elasticsearch-server-ip>:9200/cybersecurity-results/_doc"
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(es_url, json=result, headers=headers)
    if response.status_code == 201:
        print("Results sent to Elasticsearch successfully.")
    else:
        print(f"Failed to send results: {response.status_code}, {response.text}")

# Function to poll the Node.js server for tasks
def poll_for_tasks():
    try:
        # Poll the Node.js server for new tasks
        response = requests.get("http://<node-server-ip>:3000/pending-tasks")
        if response.status_code == 200:
            tasks = response.json()
            return tasks
        else:
            print(f"Error polling tasks: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error occurred while polling for tasks: {e}")
        return []

# Main function to process tasks
def main():
    while True:
        tasks = poll_for_tasks()

        for task in tasks:
            module_name = task["module_name"]
            task_id = task["task_id"]
            params = task.get("params", {})
            
            print(f"Running module {module_name} for task {task_id}")
            try:
                # Run the requested module
                result = run_module(module_name, params)
                
                # Add task ID to the result for tracking
                result["task_id"] = task_id
                
                # Send the result to Elasticsearch
                send_results_to_elasticsearch(result)
                print(f"Task {task_id} completed successfully.")
                
            except Exception as e:
                print(f"Error processing task {task_id}: {e}")
        
        # Wait before polling for new tasks again (adjust polling interval as needed)
        time.sleep(10)

if __name__ == "__main__":
    main()

