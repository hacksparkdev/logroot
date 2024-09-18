import subprocess as sub

def run():
    result = sub.run(['cmd', '/c', 'dir'], stdout=sub.PIPE, text=True)
    print(result.stdout)
