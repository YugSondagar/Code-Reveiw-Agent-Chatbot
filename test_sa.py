import sys
import traceback
sys.path.append(r"c:\Users\Yug Sondagar\Intel Unnati\Code Review Agent\backend")
from services.static_analysis import StaticAnalyzer
import json

analyzer = StaticAnalyzer()
code = """def test():
    eval("1+1")
    x = 1
    x = 1
    print("Hello")
"""

try:
    results = analyzer.analyze(code, 'python')
    with open('sa_output.json', 'w') as f:
        json.dump(results, f, indent=2)
except Exception as e:
    with open('sa_output.json', 'w') as f:
        f.write(traceback.format_exc())
