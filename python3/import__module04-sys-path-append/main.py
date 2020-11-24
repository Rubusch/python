#!/usr/bin/python3

## Import module.py if it's in a different file location from where it is imported
import sys
import os
sys.path.append(os.path.abspath('./'))
from module import *

def main():
    ## call imported function
    func()
    print('READY.')


if __name__ == "__main__":
    main()
