from services.ollama_client import OllamaClient
from services.static_analysis import StaticAnalyzer
from utils.formatter import ReviewFormatter
import os
import traceback

class CodeAnalyzer:
    def __init__(self):
        """Initialize the CodeAnalyzer with required services"""
        self.ollama = OllamaClient()
        self.static_analyzer = StaticAnalyzer()
        self.formatter = ReviewFormatter()
        
        # Load review prompt
        prompt_path = os.path.join(os.path.dirname(__file__), '../prompts/review_prompt.txt')
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                self.review_prompt = f.read()
            print(f"✅ Loaded review prompt from {prompt_path}")
        except FileNotFoundError:
            print(f"⚠️ Prompt file not found at {prompt_path}, using fallback prompt")
            # Fallback prompt
            self.review_prompt = """
You are an expert code reviewer. Analyze this {language} code:

CODE TO REVIEW:
```{language}
{code}

STATIC ANALYSIS RESULTS:
{static_analysis}

Provide a comprehensive code review in the following format:

EXECUTIVE SUMMARY:
[summary]

BUGS:

[bugs with line numbers]

SECURITY ISSUES:

[security issues]

CODE QUALITY ISSUES:

[quality issues]

PERFORMANCE ISSUES:

[performance issues]

SUGGESTIONS:

[suggestions]

IMPROVED CODE:

{language}
[improved code]
"""
        except Exception as e:
            print(f"⚠️ Error loading prompt: {e}")
            self.review_prompt = "Review this code: {code}"

    def analyze(self, code, language):
        """
        Main method to analyze code using static analysis and LLM
        
        Args:
            code (str): The code to analyze
            language (str): The programming language
            
        Returns:
            dict: Structured review results
        """
        try:
            print(f"🔍 Starting analysis for {language} code...")
            
            # Step 1: Run static analysis
            print("📊 Running static analysis...")
            static_results = self.static_analyzer.analyze(code, language)
            print(f"✅ Static analysis complete. Found {len(static_results.get('bugs', []))} bugs, {len(static_results.get('security', []))} security issues")
            
            # Step 2: Format static results for the prompt
            static_summary = self.formatter.format_static_results(static_results)
            
            # Step 3: Prepare the prompt for LLM
            code_length = len(code.split('\n'))
            issue_count = (len(static_results.get('bugs', [])) + 
                        len(static_results.get('security', [])) + 
                        len(static_results.get('style', [])))
            
            prompt = self.review_prompt.format(
                language=language,
                code=code[:3000],  # Limit code length to avoid token limits
                static_analysis=static_summary,
                code_length=code_length,
                issue_count=issue_count
            )
            
            # Step 4: Get LLM review
            print("🤖 Getting AI review from Ollama...")
            system_prompt = "You are an expert code reviewer. Provide detailed, structured feedback with improved code."
            llm_review = self.ollama.generate(prompt, system_prompt)
            print("✅ Received AI review")
            
            # Step 5: Format the final review
            print("📝 Formatting final review...")
            final_review = self.formatter.format_final_review(static_results, llm_review, language)
            print("✅ Analysis complete!")
            
            return final_review
            
        except Exception as e:
            print(f"❌ Error in analyze method: {str(e)}")
            print(traceback.format_exc())
            
            # Return a basic review if something fails
            return {
                'language': language,
                'summary': f'Analysis encountered an error: {str(e)}',
                'bugs': self._create_fallback_issues(code),
                'security': [],
                'code_quality': [],
                'performance': [],
                'suggestions': ['Check if Ollama is running and the model is downloaded'],
                'improved_code': code,
                'metrics': {
                    'function_count': code.count('def ') + code.count('function '),
                    'class_count': code.count('class '),
                    'line_count': len(code.split('\n')),
                    'health_score': 50,
                    'bug_count': 0,
                    'security_count': 0,
                    'quality_count': 0
                }
            }

    def _create_fallback_issues(self, code):
        """Create basic issues when analysis fails"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            if len(line) > 100:
                issues.append({
                    'description': f'Line {i} is too long ({len(line)} characters). Consider breaking it up.',
                    'severity': 'low',
                    'line': i
                })
        
        return issues[:3]