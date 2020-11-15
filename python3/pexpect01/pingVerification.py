#!/usr/bin/python3
#
# RESOURCE: http://www.bx.psu.edu/~nate/pexpect/pexpect.html

import pexpect
import subprocess


# vagrant
def vagrant_prepare():
    subprocess.run(['vagrant', 'halt'])
    subprocess.run(['vagrant', 'up', 'client1'])
    subprocess.run(['vagrant', 'up', 'router1'])

    try:
        #subprocess.run(['vagrant', 'ssh', 'router1', '-c', '"sudo ip addr add 192.168.11.130/24 dev enp0s8"'])
        #subprocess.run(['vagrant', 'ssh', 'router1', '-c', '"sudo ip link set enp0s8 up"'])

        p = pexpect.spawn('vagrant ssh router1 -c "sudo ip addr add 192.168.11.130/24 dev enp0s8"', timeout=30)
        p.expect(pexpect.EOF)

        p = pexpect.spawn('vagrant ssh router1 -c "sudo ip link set enp0s8 up', timeout=30)
        p.expect(pexpect.EOF)

        #subprocess.run(['vagrant', 'ssh', 'client1', '-c', '"sudo ip addr add 192.168.11.131/24 dev enp0s8"'])
        #subprocess.run(['vagrant', 'ssh', 'client1', '-c', '"sudo ip link set enp0s8 up"'])

        p = pexpect.spawn('vagrant ssh client1 -c "sudo ip addr add 192.168.11.130/24 dev enp0s8"', timeout=30)
        p.expect(pexpect.EOF)

        p = pexpect.spawn('vagrant ssh client1 -c "sudo ip link set enp0s8 up', timeout=30)
        p.expect(pexpect.EOF)

        #subprocess.run(['vagrant', 'status'])
        #subprocess.run(['vagrant', 'ssh', 'router1', '-c', '"sudo ip addr"'])
        #subprocess.run(['vagrant', 'ssh', 'client1', '-c', '"sudo ip addr"'])

    except TIMEOUT:
        print('prepare failed! timeout caught')
    p.close()


def vagrant_teardown(child):
    child.close();
    subprocess.run(['vagrant', 'halt'])


# testing
def test_working():
    # test: command
    child = pexpect.spawn('vagrant ssh client1 -c "ping -c 3 192.168.11.130"')

    # expect: the first in the list is chosen
    index = child.expect([' 0% packet loss', pexpect.EOF, pexpect.TIMEOUT])
    if index==0:
        print("1: MATCHED! (expected)")
    else:
        print("1: NO MATCH (FAILED)")
    return child


def test_not_working():
    # test: command
    child = pexpect.spawn('vagrant ssh client1 -c "ping -c 3 192.168.11.200"')

    # expect: the first in the list is chosen
    index = child.expect([' 0% packet loss', pexpect.EOF, pexpect.TIMEOUT])
    if index==0:
        print("2: MATCHED! (FAILED)")
    else:
        print("2: NO MATCH (expected)")
    return child


# main #
def main():
    vagrant_prepare()

    try:
        child = test_working()
        child = test_not_working()

    except EOF:
        print("EOF caught")

    except TIMEOUT:
        print("TIMEOUT caught")

    vagrant_teardown(child)

    print( "READY." )

if __name__ == "__main__":
    main()
