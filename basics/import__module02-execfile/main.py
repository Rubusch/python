#!/usr/bin/python3

## using execfile or exec, respectively

## python2:
#execfile("./module.py")
##
## python3:
exec(open("./module.py").read())

def main():
    ## call imported function
    func()
    print('READY.')


if __name__ == "__main__":
    main()
