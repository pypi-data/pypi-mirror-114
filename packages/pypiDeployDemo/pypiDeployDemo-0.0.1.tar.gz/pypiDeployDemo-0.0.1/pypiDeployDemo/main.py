import sys

def main():
    if len(sys.argv) == 1:
        return 'DEMO IS WORKING!!'
    for arg in sys.argv:
        if arg == '-v' or arg == '--version':
            print('Version 0.0.1')
    