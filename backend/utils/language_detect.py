import os
from config import Config
import re

class LanguageDetector:
    def __init__(self):
        self.language_patterns = {
            'python': [
                r'^\s*def\s+\w+\s*\(',  # Function definition
                r'^\s*class\s+\w+:',     # Class definition
                r'^\s*import\s+\w+',      # Import statement
                r'^\s*from\s+\w+\s+import',
                r'if\s+__name__\s*==\s*[\'"]__main__[\'"]',
                r'print\s*\(',  # Python print
                r':\s*\n\s{4}',  # Indentation pattern
            ],
            'javascript': [
                r'function\s*\w*\s*\([^)]*\)\s*{',
                r'const\s+\w+\s*=\s*require\s*\(',
                r'import\s+.*\s+from\s+[\'"].*[\'"]',
                r'export\s+(default\s+)?(function|class|const)',
                r'console\.log\s*\(',
                r'var\s+\w+\s*=',
                r'let\s+\w+\s*=',
                r'=>\s*{',
            ],
            'typescript': [
                r'interface\s+\w+\s*{',
                r'type\s+\w+\s*=',
                r':\s*(string|number|boolean|any|void)\s*[=,;)]',
                r'<\s*\w+\s*>',  # Generics
                r'enum\s+\w+\s*{',
                r'namespace\s+\w+',
                r'public|private|protected\s+\w+',
            ],
            'java': [
                r'public\s+class\s+\w+',
                r'public\s+static\s+void\s+main',
                r'System\.out\.println',
                r'@Override',
                r'import\s+java\.',
                r'class\s+\w+\s+extends',
                r'implements\s+\w+',
            ],
            'cpp': [
                r'#include\s*<[^>]+>',
                r'std::',
                r'cout\s*<<',
                r'cin\s*>>',
                r'->\s*\w+',  # Arrow operator
                r'namespace\s+\w+',
                r'template\s*<',
            ],
            'c': [
                r'#include\s*<[^>]+>',
                r'int\s+main\s*\(',  # C-style main
                r'printf\s*\(',  # C-style printf
                r'malloc\s*\(',
                r'free\s*\(',
                r'->\s*\w+',  # Arrow operator
            ],
            'go': [
                r'package\s+\w+',
                r'func\s+\w+\s*\([^)]*\)\s*{',
                r'go\s+func\(',
                r'defer\s+\w+',
                r':=',  # Short variable declaration
                r'chan\s+\w+',
            ],
            'rust': [
                r'fn\s+\w+\s*\([^)]*\)\s*{',
                r'let\s+mut\s+\w+',
                r'println!',
                r'impl\s+\w+\s+for',
                r'->\s*\w+',  # Return type
                r'#\[derive\(',
            ],
            'php': [
                r'<\?php',
                r'\$\w+\s*=',
                r'echo\s+["\']',
                r'function\s+\w+\s*\([^)]*\)\s*{',
                r'namespace\s+\w+',
                r'use\s+\w+',
            ],
            'ruby': [
                r'def\s+\w+',
                r'class\s+\w+',
                r'require\s+[\'"].*[\'"]',
                r'attr_accessor',
                r'do\s*\|[^|]*\|',
                r'puts\s+',
            ],
            'swift': [
                r'import\s+(Foundation|UIKit|Swift)',
                r'func\s+\w+\s*\([^)]*\)\s*->',
                r'var\s+\w+:\s*\w+',
                r'let\s+\w+:\s*\w+',
                r'class\s+\w+:\s*\w+',
                r'print\s*\(',
            ],
            'kotlin': [
                r'fun\s+\w+\s*\([^)]*\)',
                r'class\s+\w+\([^)]*\)',
                r'var\s+\w+:\s*\w+',
                r'val\s+\w+:\s*\w+',
                r'println\s*\(',
                r'import\s+[a-z]+\.[A-Z]',
            ]
        }
    def detect(self,code,filename=''):
        """Detect programming language from code and filename"""
        if filename:
            ext = os.path.splitext(filename)[1].lower()
            for lang,info in Config.SUPPORTED_LANGUAGES.items():
                if ext in info['extensions']:
                    return lang
        
        scores = {lang:0 for lang in self.language_patterns}
        code_lower = code.lower()

        for lang,patterns in self.language_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern,code,re.MULTILINE)
                scores[lang]+=len(matches)*2
        
        lines = code.split('\n')
        if any(line.startswith('   ') or line.startswith('\t') for line in lines):
            scores['python']+=3
        if ';' in code and '{' in code and '}' in code:
            if 'function' in code_lower:
                scores['javascript']+=3
            if 'interface' in code_lower or 'type' in code_lower:
                scores['typescript']+=3
        
        if 'public static void main' in code:
            scores['java'] += 5
        
        if '#include' in code:
            if 'cout' in code or 'cin' in code or 'std::' in code:
                scores['cpp'] += 4
            elif 'printf' in code or 'scanf' in code:
                scores['c'] += 4
        
        if 'package main' in code_lower:
            scores['go'] += 4
        
        if '<?php' in code:
            scores['php'] += 5
        
        if re.search(r'def \w+$',code,re.MULTILINE):
            scores['ruby'] += 3
        
        detected_lang = max(scores,key=scores.get)
        return detected_lang if scores[detected_lang]>0 else 'python'
    