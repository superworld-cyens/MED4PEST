import os
import time

class log():

    def __init__(self, logpath):
        self.logpath = logpath
    


    def printDebug(self, msg: str, debug: bool):
        if debug:
            logtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f'{logtime} - {msg}')

            with open(os.path.join(self.logpath,'log.txt'), 'a') as f:
                f.write(f'{logtime} - {msg}')
                f.write('\n')

