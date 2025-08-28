import subprocess
import sys
import os

def main():
    req_file = 'req.txt'
    if os.path.exists(req_file):
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req_file])
    else:
        print(f"{req_file} not found.")

if __name__ == '__main__':
    main()
