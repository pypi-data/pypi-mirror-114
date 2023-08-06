import sys
from pypi_Deploy_Demo.component import process

def main():
    if len(sys.argv) == 1: return process()
        
    for arg in sys.argv:
        if arg == '-v' or arg == '--version':
            print('Version 0.0.1')
    