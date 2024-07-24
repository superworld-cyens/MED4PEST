import os
import time
import json

class log():

    def __init__(self, logpath):
        self.logpath = logpath
    


    def printDebug(self, msg: str, debug: bool):
        if debug:
            logtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f'{msg}')

            with open(os.path.join(self.logpath,f'{logtime[:10]}_log.txt'), 'a') as f:
                f.write(f'{msg}')
                f.write('\n')

class Configuration():
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.load_json()

    def load_json(self):
        with open(self.filepath, 'r') as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                setattr(self, key, value)


import subprocess

def force_stop_camera():
    """
    Runs the command 'sudo fuser -k /dev/video0' to force stop any process using the camera.

    Returns:
        tuple: (returncode, stdout, stderr) from the command execution.
    """
    command = "sudo fuser -k /dev/video0"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # return process.returncode, stdout.decode(), stderr.decode()

# retcode, stdout, stderr = force_stop_camera()


