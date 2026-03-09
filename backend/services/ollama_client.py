import requests
import time
from config import Config

class OllamaClient:
    def __init__(self):
        self.base_url = Config.OLLAMA_HOST
        self.model = Config.OLLAMA_MODEL
    
    def generate(self, prompt, system_prompt=None):
        """Generate response from Ollama"""
        try:
            # Check if Ollama is running
            try:
                health = requests.get(f"{self.base_url}/api/tags", timeout=2)
                if health.status_code != 200:
                    return self._create_fallback_response("Ollama not responding")
            except requests.exceptions.ConnectionError:
                return self._create_fallback_response("Cannot connect to Ollama. Make sure it's running with 'ollama serve'")
            except Exception as e:
                return self._create_fallback_response(f"Connection error: {str(e)}")
            
            payload = {
                'model': self.model,
                'prompt': prompt[:2000],
                'stream': False,
                'options': {
                    'temperature': 0.1,
                    'num_predict': 800
                }
            }
            
            if system_prompt:
                payload['system'] = system_prompt
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                return self._create_fallback_response(f"Ollama error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            return self._create_fallback_response("Request timed out. The model might be too slow.")
        except Exception as e:
            return self._create_fallback_response(f"Error: {str(e)}")
    
    def chat(self, messages):
        """Chat completion with history"""
        try:
            # Check connection
            try:
                requests.get(f"{self.base_url}/api/tags", timeout=2)
            except requests.exceptions.ConnectionError:
                return "❌ Cannot connect to Ollama. Please make sure it's running with 'ollama serve'"
            except Exception as e:
                return f"❌ Connection error: {str(e)}"
            
            payload = {
                'model': self.model,
                'messages': messages,
                'stream': False,
                'options': {
                    'temperature': 0.3,
                    'num_predict': 800
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('message', {}).get('content', '')
            else:
                return f"❌ Error: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "❌ Request timed out. The model might be too slow."
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _create_fallback_response(self, error_msg):
        """Create a helpful fallback response when Ollama fails"""
        print(f"⚠️ Using fallback response. Reason: {error_msg}")
        
        return f"""EXECUTIVE SUMMARY:
        Basic code analysis completed. AI-powered review limited due to: {error_msg}

        BUGS & ERRORS:
        - Check for syntax errors (unclosed strings, missing brackets)
        - Verify string literals are properly closed with quotes
        - Ensure all parentheses and brackets are matched

        SECURITY ISSUES:
        - Check for hardcoded credentials
        - Look for eval() or similar dangerous functions
        - Verify input validation

        CODE QUALITY ISSUES:
        - Check naming conventions (PEP 8 for Python, camelCase for JS)
        - Look for long functions (>20 lines)
        - Verify consistent indentation
        - Add comments for complex logic

        PERFORMANCE ISSUES:
        - Look for inefficient algorithms
        - Check for unnecessary computations in loops
        - Consider using vectorized operations for large datasets

        SUGGESTIONS FOR IMPROVEMENT:
        1. Add proper error handling with try-catch blocks
        2. Include input validation
        3. Follow language-specific best practices
        4. Add docstrings/comments for better documentation

        IMPROVED CODE:
        ```python
        # Example of improved code structure
        def main():
            try:
                # Your code here with proper error handling
                print("Hello, World!")
            except Exception as err:  # Fixed: using 'err' instead of 'e'
                print(f"Error: {{err}}")  # Fixed: escaped the curly braces

        if __name__ == "__main__":
            main()
        ```"""