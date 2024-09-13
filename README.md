# Distributed Cybersecurity Task Execution and Monitoring System

## Overview

This project is a custom-built, distributed cybersecurity system designed to deploy, monitor, and automate the execution of Python modules across multiple Windows endpoints. Leveraging **Elasticsearch** for task management, log aggregation, and data storage, the system provides an efficient and scalable solution for **Automated Threat Detection**, **Incident Response**, and **Proactive Security Monitoring**.

### Key Features:

- **Task Execution**: Python modules can be dynamically deployed to Windows computers to perform various security-related tasks.
- **Real-Time Monitoring**: Tracks the status of each module, ensuring visibility of task execution across the network.
- **Endpoint Detection and Response (EDR)**: Automates the detection of malware, suspicious activities, or security anomalies.
- **Centralized Log Aggregation**: Gathers logs from multiple machines for analysis, anomaly detection, and response.
- **Modular Structure**: The system supports custom Python modules for various cybersecurity use cases, including IoC detection, vulnerability scanning, and forensic data collection.

## Architecture

1. **Python Worker**: Each Windows machine has a Python worker that pulls tasks from an Elasticsearch cluster and runs security-related modules.
2. **Elasticsearch**: Used for both storing tasks (modules) to be executed and aggregating logs or data sent back from endpoints.
3. **Task Manager**: Centralized polling mechanism that checks Elasticsearch for pending tasks and sends them to endpoints.
4. **Modular Design**: Python modules are located in a `modules/` directory and can be easily added, modified, or removed.

## Project Goals

1. **Automated Threat Detection and Response**: Modules designed to detect and respond to malicious activities on endpoints.
2. **Incident Investigation Automation**: Automate the collection of forensic data from endpoints during incidents.
3. **Vulnerability Management**: Automate the scanning of endpoints for vulnerabilities.
4. **Custom Log Aggregation and Analysis**: Centralized log collection for security event analysis and anomaly detection.
5. **Proactive Security Monitoring**: Continuous monitoring of systems for security health checks and configuration audits.

## Prerequisites

- **Python 3.8+**
- **Elasticsearch 7.x+**
- **Logstash** (Optional, if using for log shipping)
- **Windows endpoints** with Python installed

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/distributed-cybersecurity-task-system.git
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up Elasticsearch:
   - Configure your Elasticsearch server and note down the IP address and port.

4. Configure Python workers on each Windows machine to communicate with the Elasticsearch server.

## Usage

### 1. Running the Python Task Manager:

This component continuously polls the Elasticsearch cluster for pending tasks (modules) and distributes them across the Windows endpoints.

```bash
python main.py
```

### 2. Writing a Python Module:

Modules are placed in the `modules/` directory and should follow this structure:

```python
# Example module: modules/my_module.py

def run():
    # Your module logic here
    return "Module completed successfully"
```

Make sure each module contains a `run()` function, as this is the entry point for task execution.

### 3. Submitting a Task:

Tasks are submitted via Elasticsearch. A typical task looks like this:

```json
{
  "moduleName": "my_module",
  "status": "pending",
  "target": "192.168.1.101"
}
```

Use the Elasticsearch API to submit the task:

```bash
curl -X POST "http://localhost:9200/python-tasks/_doc/" -H 'Content-Type: application/json' -d '
{
  "moduleName": "my_module",
  "status": "pending",
  "target": "192.168.1.101"
}'
```

### 4. Monitoring Task Status:

You can monitor the status of tasks via the `python-tasks` index in Elasticsearch. The task status will update to "running" when in progress and "completed" or "failed" once the module finishes.

## Project Structure

```
distributed-cybersecurity-task-system/
│
├── modules/                   # Contains all Python modules
│   └── my_module.py            # Example module
├── main.py                     # Main task manager script
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Future Plans

- **Scalability Enhancements**: Improve the system to handle a large number of endpoints.
- **UI Dashboard**: Develop a frontend dashboard for visualizing task statuses, logs, and alerts.
- **Advanced Modules**: Write more sophisticated Python modules for IoC detection, malware analysis, and incident response.

## Contributing

Contributions to this project are welcome. Please submit a pull request with your proposed changes.
