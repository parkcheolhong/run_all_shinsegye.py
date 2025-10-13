#!/usr/bin/env python3
"""Example script 2 - File operations"""

import os

def main():
    print("Example Script 2: File Operations")
    
    # Get current directory
    cwd = os.getcwd()
    print(f"Current directory: {cwd}")
    
    # List files in current directory
    files = os.listdir('.')
    print(f"Files in current directory: {len(files)} files")
    
    for file in sorted(files):
        if file.endswith('.py'):
            print(f"  - {file}")

if __name__ == '__main__':
    main()
