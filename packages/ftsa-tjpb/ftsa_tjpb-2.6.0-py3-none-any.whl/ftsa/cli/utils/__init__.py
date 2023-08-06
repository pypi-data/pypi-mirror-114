import os
from time import sleep


def execute(cmd, seconds=10):
    print(f'{cmd}')
    os.system(cmd)
    sleep(seconds)
