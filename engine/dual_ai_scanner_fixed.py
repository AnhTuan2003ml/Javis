import ast
import os
import sys
import re

def analyze_code(code):
    """Analyze Python code for issues"""
    issues = []
    
    try:
        # Check syntax
        ast.parse(code)
    except SyntaxError as e:
        issues.append(f"Syntax Error at line {e.lineno}: {e.msg}")
        return issues
    
    lines = code.split('\n')
    for i, line in enumerate(lines, 1):
        line_stripped = line.strip()
        
        # CRITICAL: Check for missing input() function
        if 'float(' in line and '"' in line and 'input(' not in line:
            if re.search(r'float\s*\(\s*["\''][^"\']*["\']\s*\)', line):
                fixed_line = re.sub(r'float\s*\(\s*(["\''][^"\']*["\'"])\s*\)', r'float(input(\1))', line)
                issues.append(f"CRITICAL - Line {i}: Missing input() function\n    Current: {line.strip()}\n    Fix: {fixed_line.strip()}")
        
        if 'int(' in line and '"' in line and 'input(' not in line:
            if re.search(r'int\s*\(\s*["\''][^"\']*["\']\s*\)', line):
                fixed_line = re.sub(r'int\s*\(\s*(["\''][^"\']*["\'"])\s*\)', r'int(input(\1))', line)
                issues.append(f"CRITICAL - Line {i}: Missing input() function\n    Current: {line.strip()}\n    Fix: {fixed_line.strip()}")
        
        # Check for common issues
        if len(line) > 100:
            issues.append(f"Line {i}: Line too long ({len(line)} chars)")
        
        if line_stripped.startswith('def ') and '"""' not in line:
            issues.append(f"Line {i}: Missing docstring for function")
        
        if '=' in line and '==' not in line and '!=' not in line:
            if not ' = ' in line:
                issues.append(f"Line {i}: Missing spaces around '=' operator")
        
        if line_stripped.endswith(', )'):
            issues.append(f"Line {i}: Trailing comma in function call")
        
        # Check for runtime errors
        if '=' in line and 'float(' in line and '"' in line and 'input(' not in line:
            issues.append(f"RUNTIME ERROR - Line {i}: Will cause ValueError - trying to convert string to float")
    
    return issues

def code_review():
    """Review code from stdin"""
    code = sys.stdin.read()
    issues = analyze_code(code)
    
    if not issues:
        print("No issues found in the code")
    else:
        print(f"Found {len(issues)} issues:")
        for issue in issues:
            print(f"  - {issue}")

def folder_review(folder_path="."):
    """Review all Python files in folder"""
    total_issues = 0
    files_scanned = 0
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    issues = analyze_code(code)
                    files_scanned += 1
                    
                    if issues:
                        print(f"\n{file_path}:")
                        for issue in issues:
                            print(f"  - {issue}")
                        total_issues += len(issues)
                
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    print(f"\nSummary: Scanned {files_scanned} files, found {total_issues} total issues")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dual_ai_scanner_fixed.py [code_review|folder_review] [folder_path]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "code_review":
        code_review()
    elif command == "folder_review":
        folder_path = sys.argv[2] if len(sys.argv) > 2 else "."
        folder_review(folder_path)
    else:
        print("Unknown command. Use 'code_review' or 'folder_review'")