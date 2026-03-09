import sys
sys.path.append(r"c:\Users\Yug Sondagar\Intel Unnati\Code Review Agent\backend")

# Test Formatter
from utils.formatter import ReviewFormatter
import json

f = ReviewFormatter()
llm_review = """EXECUTIVE SUMMARY:
This is a multi-line
summary test.
It should all be captured.

BUGS:
- A bug here
- Another bug there

SECURITY ISSUES:
- A security issue

IMPROVED CODE:
```python
def test():
    pass
```
"""

print("--- FORMATTER TEST ---")
parsed = f._parse_llm_review(llm_review)
print("Summary:", repr(parsed.get('summary')))
print("Bugs:", parsed.get('bugs'))
print("Security:", parsed.get('security'))
print("Improved Code:", repr(parsed.get('improved_code')))

# Test Chat Service instantiation and method
from services.chat_service import ChatService
print("\n--- CHAT SERVICE TEST ---")
try:
    c = ChatService()
    print("ChatService initialized successfully with history:", c.get_history("test_session"))
    print("Methods available:", [m for m in dir(c) if not m.startswith('_')])
except Exception as e:
    print("Error:", e)
