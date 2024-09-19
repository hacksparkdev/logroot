import subprocess as sub
import json  # Import the json library to handle JSON conversion

# Running a Powershell command and parsing the output
def run():
    # Run the PowerShell command to get process information
    result = sub.run(['powershell', '-command', 
                      'Get-Process | Select-Object Name, Id, CPU, WS, StartTime | ConvertTo-Json'], 
                      stdout=sub.PIPE, text=True)

    # Convert the result into a Python dictionary (since PowerShell is converting to JSON)
    try:
        process_list = json.loads(result.stdout)  # Parse the JSON output from PowerShell into a Python object
    except json.JSONDecodeError:
        # Handle JSON decoding issues (if PowerShell output isn't valid JSON)
        return {"error": "Failed to decode JSON from PowerShell output"}

    return process_list  # Return the parsed JSON object (list of processes)

