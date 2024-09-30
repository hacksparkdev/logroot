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
    url = "http://10.10.20.107:9200/cybersecurity-results/_doc"
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=result, headers=headers)
    if response.status_code == 201:
        print("Results sent to Elasticsearch successfully.")
    else:
        print(f"Failed to send results: {response.status_code}, {response.text}")

# Main function to wait for tasks from Node.js server
def main():
    while True:
        try:
            # Poll the Node.js server for new tasks
            response = requests.get("http://10.10.20.100:3000/pending-tasks")
            tasks = response.json()

            for task in tasks:
                module_name = task["module_name"]
                task_id = task["task_id"]
                params = task.get("params", {})
                
                # Run the requested module
                result = run_module(module_name, params)
                
                # Add task ID to the result
                result["task_id"] = task_id
                
                # Send the result to Elasticsearch
                send_results_to_elasticsearch(result)
        
        except Exception as e:
            print(f"Error occurred: {e}")
        
        time.sleep(10)

if __name__ == "__main__":
    main()

