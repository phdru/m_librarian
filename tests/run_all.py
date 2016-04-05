#! /usr/bin/env python


import os
import sys
import subprocess


def isexecutable(filename):
    infile = open(filename, 'r')
    magic = infile.read(2)
    infile.close()
    return magic == "#!"


def collect_tests():
    tests = []
    for dirpath, dirs, files in os.walk("tests"):
        tests.extend(
            [os.path.join(dirpath, filename) for filename in files
             if filename.startswith("test") and filename.endswith(".py")
             ])
    return [test[:-3].replace(os.sep, '.') for test in tests
            if isexecutable(test)]


def main():
    os.chdir(os.path.join(os.path.dirname(sys.argv[0]), os.pardir))
    tests = collect_tests()

    os.environ["PYTHONPATH"] = os.curdir

    for test in sorted(tests):
        sys.stdout.write("Test: %s... " % test)
        sys.stdout.flush()
        rc = subprocess.call((sys.executable, '-m', test))
        if rc:
            sys.stdout.write("ERROR\n")
        else:
            sys.stdout.write("Ok\n")
        sys.stdout.flush()

if __name__ == '__main__':
    main()
