# **Custom Log Monitoring System**

This project is a custom-built log monitoring solution that collects logs from Windows workstations, processes them with Logstash, stores them in Elasticsearch, and provides a real-time web-based dashboard using Node.js. The system is designed to handle large volumes of logs, allow real-time visualization, and provide search capabilities—all without relying on third-party tools like Kibana.

## **Table of Contents**

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Components](#components)
- [Installation](#installation)
- [File Structure](#file-structure)
- [Usage](#usage)
- [Technologies](#technologies)
- [Contributing](#contributing)
- [License](#license)

---

## **Project Overview**

This system collects logs from remote Windows workstations using Python scripts and sends them to a Logstash server, which forwards the logs to Elasticsearch for indexing and storage. A custom Node.js server provides a web interface that displays logs in real time, with the ability to search logs and visualize event types using charts.

### Key Features:
- Collect Windows Event Logs (Application, System, etc.).
- Send logs from remote workstations to Logstash.
- Store and index logs in Elasticsearch.
- View logs in real-time via a Node.js-powered web interface.
- Perform log searches and visualize event types in charts.

---

## **Architecture**

Here’s an overview of the system architecture:

1. **Python Workstation Scripts**: 
   - Run on remote Windows workstations to collect logs and send them to Logstash.
2. **Logstash Server**: 
   - Receives logs from workstations via TCP and forwards them to Elasticsearch.
3. **Elasticsearch Server**: 
   - Stores and indexes logs for querying and visualization.
4. **Node.js Server**: 
   - Hosts a web-based frontend that allows real-time log viewing, searching, and charting of log events.

---

## **Components**

### **1. Python Workstation Scripts**
Python scripts that run on each Windows workstation to collect and send logs to Logstash.
- **`config.py`**: Configuration for workstations and Elasticsearch.
- **`connection.py`**: Handles connections to remote workstations.
- **`log_retrieval.py`**: Retrieves logs from the workstations.
- **`client.py`**: Sends logs to Logstash and manages continuous log retrieval.

### **2. Logstash**
Processes incoming log data and forwards it to Elasticsearch.
- **`logstash.conf`**: Configuration for the Logstash pipeline, set to receive logs via TCP from Python scripts.

### **3. Elasticsearch**
Stores and indexes the logs for real-time queries and visualization.
- **`docker-compose.yml`**: Docker configuration to set up Elasticsearch.

### **4. Node.js Server**
Hosts a web-based frontend that displays the logs and provides search functionality.
- **`server.js`**: Main server script that sets up WebSocket communication, handles log data, and serves the frontend.
- **Frontend (HTML + JS)**: Real-time log display, search functionality, and visual representation of event types.

---

## **Installation**

Follow these steps to set up the system across different servers:

### **1. Python Workstation Scripts**

- **Clone the repository on your Windows workstations:**
  ```bash
  git clone https://github.com/yourusername/custom-log-monitoring.git
  cd custom-log-monitoring/python_scripts
  ```

- **Install the required Python packages:**
  ```bash
  pip install requests wmi
  ```

- **Configure the workstations**:
  Modify the `config.py` file to include the correct workstation details (name, username, password).

### **2. Logstash Server**

- **Install Logstash**:
  Follow the [official instructions](https://www.elastic.co/guide/en/logstash/current/installing-logstash.html).

- **Configure Logstash**:
  Place the `logstash.conf` file in your Logstash config directory and run Logstash:
  ```bash
  logstash -f /path/to/logstash.conf
  ```

### **3. Elasticsearch Server**

- **Install Docker**:
  Follow the [official Docker installation instructions](https://docs.docker.com/get-docker/).

- **Run Elasticsearch using Docker Compose**:
  Navigate to the `elasticsearch` directory and run:
  ```bash
  docker-compose up -d
  ```

### **4. Node.js Server**

- **Clone the repository on your Node.js server:**
  ```bash
  git clone https://github.com/yourusername/custom-log-monitoring.git
  cd custom-log-monitoring/node_server
  ```

- **Install the necessary Node.js packages:**
  ```bash
  npm install
  ```

- **Run the Node.js server:**
  ```bash
  node server.js
  ```

---

## **File Structure**

```
/project-root
│
├── /python_scripts
│   ├── config.py
│   ├── connection.py
│   ├── log_retrieval.py
│   └── client.py
│
├── /node_server
│   ├── package.json
│   ├── server.js
│   ├── /public
│   │   ├── index.html
│   │   └── script.js
│
├── /logstash
│   └── logstash.conf
│
└── /elasticsearch
    └── docker-compose.yml
```

---

## **Usage**

### **1. Running the Python Script**
On each Windows workstation, execute the Python script:
```bash
python client.py
```
This will collect logs from the workstation and send them to the Logstash server.

### **2. Running Logstash**
Ensure Logstash is running on its own server with the correct configuration:
```bash
logstash -f /path/to/logstash.conf
```

### **3. Running Elasticsearch**
Make sure Elasticsearch is running on its own server, and logs from Logstash are being indexed.

### **4. Accessing the Web Interface**
On the Node.js server, visit the following URL in your browser to access the log viewer and dashboard:
```
http://your-node-server-ip:5000
```

- **Live Logs**: Displays logs in real-time.
- **Search Logs**: Enter a query to search the logs in Elasticsearch.
- **Event Types**: Visual representation of the types of events (e.g., Error, Warning, Information).

---

## **Technologies**

- **Python**: For log collection from workstations.
- **Node.js + Express**: Backend for serving the web interface and WebSocket management.
- **Socket.IO**: Real-time communication between the server and the frontend.
- **Logstash**: Processes and forwards logs to Elasticsearch.
- **Elasticsearch**: Stores and indexes logs.
- **Chart.js**: Provides charts for visualizing log events in the frontend.
- **Docker**: To deploy Elasticsearch (and optionally Logstash).

---

## **Contributing**

Contributions are welcome! If you have suggestions or find issues, please open an issue or submit a pull request.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for more details.
