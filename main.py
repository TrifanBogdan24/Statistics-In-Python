#!/usr/bin/env python3

import subprocess
import os

def main():
    all_files = os.listdir()

    # list comprehension:
    csv_files = [file for file in all_files if file.endswith(".csv")]

    for csv_file in csv_files:
        subprocess.Popen(["python3", "stats.py", csv_file])
        subprocess.Popen(["python3", "linear_reggr.py", csv_file])
    

if __name__ == "__main__":
    main()
