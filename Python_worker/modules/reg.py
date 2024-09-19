import re 
import subprocess as sub


def run():
    cmd = ['ipconfig']

    results = sub.run(cmd, stdout=sub.PIPE, stderr=sub.PIPE, text=True)
    
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ipconfig_result = results.stdout
    matches = re.findall(ip_pattern, ipconfig_result )
    for match in matches:
        return matches


