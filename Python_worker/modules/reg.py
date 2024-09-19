import re 
import subprocess as sub


def get_ip():
    cmd = ['ipconfig']

    results = sub.run(cmd, stdout=sub.PIPE, stderr=sub.PIPE, text=True)
    
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ipconfig_result = result.stdout
    matches = re.findall(ip_pattern, ipconfig_result )

    for match in matches:
        print(match)


def run():
    return get_ip()

