#!/usr/bin/python3

## Most Robust: Import files in python with the bare import command
from foo.bar.module import func

def main():
    ## call imported function
    func()
    print('READY.')


if __name__ == "__main__":
    main()
