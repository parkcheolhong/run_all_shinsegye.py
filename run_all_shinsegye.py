#!/usr/bin/env python3
"""
run_all_shinsegye.py - 편리한 나의 도구 (My Convenient Tool)
신비로운 가방처럼 다양한 작업을 실행할 수 있는 유틸리티

A utility tool like a mysterious bag that can execute various tasks.
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from typing import List, Optional


class RunAllTool:
    """Main tool class for running multiple scripts and commands."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results = []
    
    def log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")
    
    def run_command(self, command: str, shell: bool = True) -> dict:
        """
        Run a single command and return the result.
        
        Args:
            command: Command to execute
            shell: Whether to use shell execution
            
        Returns:
            Dictionary with command results
        """
        self.log(f"Running command: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            output = {
                'command': command,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
            
            if result.returncode == 0:
                self.log(f"✓ Command succeeded: {command}")
            else:
                self.log(f"✗ Command failed: {command}")
            
            return output
            
        except subprocess.TimeoutExpired:
            self.log(f"✗ Command timed out: {command}")
            return {
                'command': command,
                'returncode': -1,
                'stdout': '',
                'stderr': 'Command timed out',
                'success': False
            }
        except Exception as e:
            self.log(f"✗ Error running command: {command} - {str(e)}")
            return {
                'command': command,
                'returncode': -1,
                'stdout': '',
                'stderr': str(e),
                'success': False
            }
    
    def run_script(self, script_path: str) -> dict:
        """
        Run a Python script.
        
        Args:
            script_path: Path to the Python script
            
        Returns:
            Dictionary with script results
        """
        if not os.path.exists(script_path):
            self.log(f"✗ Script not found: {script_path}")
            return {
                'command': f"python {script_path}",
                'returncode': -1,
                'stdout': '',
                'stderr': f'Script not found: {script_path}',
                'success': False
            }
        
        return self.run_command(f"python {script_path}")
    
    def run_all_from_file(self, file_path: str) -> List[dict]:
        """
        Run all commands listed in a file.
        
        Args:
            file_path: Path to file containing commands (one per line)
            
        Returns:
            List of result dictionaries
        """
        results = []
        
        if not os.path.exists(file_path):
            self.log(f"✗ File not found: {file_path}")
            return results
        
        with open(file_path, 'r', encoding='utf-8') as f:
            commands = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        self.log(f"Found {len(commands)} commands to execute")
        
        for i, command in enumerate(commands, 1):
            self.log(f"Executing command {i}/{len(commands)}")
            result = self.run_command(command)
            results.append(result)
            self.results.append(result)
        
        return results
    
    def run_all_scripts_in_directory(self, directory: str, pattern: str = "*.py") -> List[dict]:
        """
        Run all Python scripts in a directory.
        
        Args:
            directory: Directory path
            pattern: File pattern to match (default: *.py)
            
        Returns:
            List of result dictionaries
        """
        results = []
        
        if not os.path.isdir(directory):
            self.log(f"✗ Directory not found: {directory}")
            return results
        
        scripts = list(Path(directory).glob(pattern))
        self.log(f"Found {len(scripts)} scripts to execute")
        
        for i, script in enumerate(scripts, 1):
            self.log(f"Executing script {i}/{len(scripts)}: {script.name}")
            result = self.run_script(str(script))
            results.append(result)
            self.results.append(result)
        
        return results
    
    def print_summary(self):
        """Print summary of all executed commands."""
        if not self.results:
            print("\nNo commands were executed.")
            return
        
        total = len(self.results)
        successful = sum(1 for r in self.results if r['success'])
        failed = total - successful
        
        print("\n" + "="*60)
        print("EXECUTION SUMMARY")
        print("="*60)
        print(f"Total commands: {total}")
        print(f"Successful: {successful} ✓")
        print(f"Failed: {failed} ✗")
        print("="*60)
        
        if failed > 0:
            print("\nFailed commands:")
            for result in self.results:
                if not result['success']:
                    print(f"  ✗ {result['command']}")
                    if result['stderr']:
                        print(f"    Error: {result['stderr'][:100]}")
        
        print()


def main():
    """Main entry point for the tool."""
    parser = argparse.ArgumentParser(
        description='run_all_shinsegye.py - 편리한 나의 도구 (My Convenient Tool)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run a single command
  %(prog)s --command "echo Hello World"
  
  # Run a Python script
  %(prog)s --script my_script.py
  
  # Run all commands from a file
  %(prog)s --file commands.txt
  
  # Run all Python scripts in a directory
  %(prog)s --directory ./scripts
  
  # Verbose mode
  %(prog)s --file commands.txt --verbose
        """
    )
    
    parser.add_argument('-c', '--command', help='Run a single command')
    parser.add_argument('-s', '--script', help='Run a Python script')
    parser.add_argument('-f', '--file', help='Run all commands from a file')
    parser.add_argument('-d', '--directory', help='Run all Python scripts in a directory')
    parser.add_argument('-p', '--pattern', default='*.py', help='File pattern for directory mode (default: *.py)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--no-summary', action='store_true', help='Disable summary output')
    
    args = parser.parse_args()
    
    # Check if at least one action is specified
    if not any([args.command, args.script, args.file, args.directory]):
        parser.print_help()
        sys.exit(1)
    
    tool = RunAllTool(verbose=args.verbose)
    
    # Execute based on arguments
    if args.command:
        result = tool.run_command(args.command)
        tool.results.append(result)
        if not args.verbose:
            print(result['stdout'], end='')
        if result['stderr']:
            print(result['stderr'], file=sys.stderr, end='')
    
    if args.script:
        result = tool.run_script(args.script)
        tool.results.append(result)
        if not args.verbose:
            print(result['stdout'], end='')
        if result['stderr']:
            print(result['stderr'], file=sys.stderr, end='')
    
    if args.file:
        tool.run_all_from_file(args.file)
    
    if args.directory:
        tool.run_all_scripts_in_directory(args.directory, args.pattern)
    
    # Print summary unless disabled
    if not args.no_summary and (args.file or args.directory):
        tool.print_summary()
    
    # Exit with error code if any command failed
    if any(not r['success'] for r in tool.results):
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
