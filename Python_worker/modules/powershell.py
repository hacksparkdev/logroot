import subprocess as sub

# Running a Powershell command 

def run():
    result = sub.run(['powershell', '-command', 'Get-Process'], stdout=sub.PIPE, text=True)
    return result.stdout
