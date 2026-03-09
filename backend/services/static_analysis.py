import re
import ast
from typing import Dict, Any, List

class StaticAnalyzer:
    def __init__(self):
        self.supported_languages = ['python', 'javascript', 'typescript']
    
    def analyze(self, code: str, language: str) -> Dict[str, Any]:
        """Run static analysis tools based on language"""
        
        results = {
            'bugs': [],
            'security': [],
            'complexity': [],
            'style': [],
            'metrics': self._get_basic_metrics(code),
            'warnings': []
        }
        
        if language == 'python':
            return self._analyze_python(code, results)
        elif language == 'javascript':
            return self._analyze_javascript(code, results)
        elif language == 'typescript':
            return self._analyze_typescript(code, results)
        else:
            return self._analyze_generic(code, results)
    
    def _get_basic_metrics(self, code: str) -> Dict[str, Any]:
        lines = code.split('\n')
        non_empty = [l for l in lines if l.strip()]
        
        return {
            'line_count': len(lines),
            'code_line_count': len(non_empty),
            'character_count': len(code),
            'empty_line_count': len(lines) - len(non_empty),
            'function_count': code.count('def ') + code.count('function ') + code.count('=>'),
            'class_count': code.count('class ')
        }
    
    def _analyze_python(self, code: str, results: Dict) -> Dict:
        """Python-specific analysis with better error detection"""
        lines = code.split('\n')
        
        # Check for syntax errors using AST
        try:
            ast.parse(code)
        except SyntaxError as e:
            error_msg = str(e)
            line_num = getattr(e, 'lineno', 1)
            
            # Specific error messages based on common issues
            if 'unterminated string' in error_msg.lower():
                results['bugs'].append({
                    'description': f'Line {line_num}: Unterminated string - missing closing quote (")',
                    'severity': 'high',
                    'line': line_num,
                    'fix': 'print("Hello")'  # Add closing quote
                })
            elif 'invalid syntax' in error_msg.lower():
                results['bugs'].append({
                    'description': f'Line {line_num}: Invalid syntax - {error_msg}',
                    'severity': 'high',
                    'line': line_num
                })
            else:
                results['bugs'].append({
                    'description': f'Line {line_num}: Syntax error - {error_msg}',
                    'severity': 'high',
                    'line': line_num
                })
        
        # Check each line for common issues
        in_string = False
        string_char = None
        string_start = 1
        
        for i, line in enumerate(lines, 1):
            # Check for unclosed strings
            for j, char in enumerate(line):
                if char in ['"', "'"] and (j == 0 or line[j-1] != '\\'):
                    if not in_string:
                        in_string = True
                        string_char = char
                        string_start = i
                    elif char == string_char:
                        in_string = False
            
            # Print statement detection
            if 'print(' in line:
                results['style'].append({
                    'description': f'Line {i}: Using print() - consider using logging for production code',
                    'severity': 'low',
                    'line': i
                })
            
            # Long lines
            if len(line) > 79:
                results['style'].append({
                    'description': f'Line {i}: Line too long ({len(line)} chars). PEP 8 recommends max 79',
                    'severity': 'low',
                    'line': i
                })
            
            # Missing whitespace around operators
            if re.search(r'\w[=]\w', line) and '==' not in line:
                results['style'].append({
                    'description': f'Line {i}: Add spaces around assignment operator (=)',
                    'severity': 'low',
                    'line': i
                })
            
            # Multiple statements on one line
            if ';' in line and not line.strip().startswith('#'):
                results['style'].append({
                    'description': f'Line {i}: Multiple statements on one line (using ;)',
                    'severity': 'low',
                    'line': i
                })
        
        # Check for unclosed string at end of file
        if in_string:
            results['bugs'].append({
                'description': f'Line {string_start}: Unclosed string - missing closing {string_char}',
                'severity': 'high',
                'line': string_start,
                'fix': 'print("Hello")'  # Example fix
            })
            
        # Run external tools
        try:
            import tempfile
            import subprocess
            import json
            import os
            
            # Create a temporary file to run tools on
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp:
                temp.write(code)
                temp_path = temp.name
                
            try:
                # Run pylint
                import sys
                pylint_cmd = [sys.executable, '-m', 'pylint', '--output-format=json', temp_path]
                process = subprocess.run(pylint_cmd, capture_output=True, text=True)
                if process.stdout:
                    try:
                        pylint_output = json.loads(process.stdout)
                        for issue in pylint_output:
                            severity = 'low'
                            if issue['type'] in ['error', 'fatal']:
                                severity = 'high'
                            elif issue['type'] == 'warning':
                                severity = 'medium'
                                
                            item = {
                                'description': f"Line {issue['line']}: {issue['message']} ({issue['message-id']})",
                                'severity': severity,
                                'line': issue['line']
                            }
                            if issue['type'] in ['error', 'fatal']:
                                results['bugs'].append(item)
                            else:
                                results['style'].append(item)
                    except json.JSONDecodeError:
                        pass

                # Run bandit
                bandit_cmd = [sys.executable, '-m', 'bandit', '-f', 'json', '-q', temp_path]
                process = subprocess.run(bandit_cmd, capture_output=True, text=True)
                if process.stdout:
                    try:
                        bandit_output = json.loads(process.stdout)
                        for issue in bandit_output.get('results', []):
                            severity = issue['issue_severity'].lower()
                            results['security'].append({
                                'description': f"Line {issue['line_number']}: {issue['issue_text']} ({issue['test_id']})",
                                'severity': severity,
                                'line': issue['line_number']
                            })
                    except (json.JSONDecodeError, KeyError):
                        pass
                
                # Run radon (complexity)
                radon_cmd = [sys.executable, '-m', 'radon', 'cc', '-j', temp_path]
                process = subprocess.run(radon_cmd, capture_output=True, text=True)
                if process.stdout:
                    try:
                        radon_output = json.loads(process.stdout)
                        file_results = radon_output.get(temp_path, [])
                        for item in file_results:
                            if isinstance(item, dict) and item.get('complexity', 0) > 10:
                                results['complexity'].append({
                                    'description': f"Line {item.get('lineno', 0)}: {item.get('type', 'Item').capitalize()} '{item.get('name', 'unknown')}' has high cyclomatic complexity ({item.get('complexity')}, rank {item.get('rank', 'N/A')})",
                                    'severity': 'medium',
                                    'line': item.get('lineno', 0)
                                })
                    except (json.JSONDecodeError, AttributeError, TypeError):
                        pass
                        
            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
        except Exception as e:
            print(f"Error running static analysis tools: {e}")
        
        return results
    
    def _analyze_javascript(self, code: str, results: Dict) -> Dict:
        """JavaScript analysis"""
        lines = code.split('\n')
        
        # Check for unclosed strings
        in_string = False
        string_char = None
        string_start = 1
        
        for i, line in enumerate(lines, 1):
            for j, char in enumerate(line):
                if char in ['"', "'", '`'] and (j == 0 or line[j-1] != '\\'):
                    if not in_string:
                        in_string = True
                        string_char = char
                        string_start = i
                    elif char == string_char:
                        in_string = False
            
            # Eval usage
            if 'eval(' in line:
                results['security'].append({
                    'description': f'Line {i}: eval() usage - security risk',
                    'severity': 'high',
                    'line': i
                })
            
            # InnerHTML
            if '.innerHTML' in line:
                results['security'].append({
                    'description': f'Line {i}: innerHTML usage - potential XSS risk',
                    'severity': 'high',
                    'line': i
                })
            
            # Console.log
            if 'console.log' in line:
                results['style'].append({
                    'description': f'Line {i}: console.log - remove in production',
                    'severity': 'low',
                    'line': i
                })
            
            # == vs ===
            if '==' in line and '===' not in line:
                results['bugs'].append({
                    'description': f'Line {i}: Use === instead of == for strict equality',
                    'severity': 'medium',
                    'line': i
                })
        
        if in_string:
            results['bugs'].append({
                'description': f'Line {string_start}: Unclosed string - missing closing {string_char}',
                'severity': 'high',
                'line': string_start
            })
        
        return results
    
    def _analyze_typescript(self, code: str, results: Dict) -> Dict:
        """TypeScript analysis"""
        results = self._analyze_javascript(code, results)
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if ': any' in line:
                results['style'].append({
                    'description': f'Line {i}: Avoid using "any" type',
                    'severity': 'medium',
                    'line': i
                })
        
        return results
    
    def _analyze_generic(self, code: str, results: Dict) -> Dict:
        """Generic analysis"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            if len(line) > 100:
                results['style'].append({
                    'description': f'Line {i}: Line too long ({len(line)} chars)',
                    'severity': 'low',
                    'line': i
                })
        
        return results