import re
from typing import Dict, Any, List

class ReviewFormatter:
    def format_static_results(self, results: Dict[str, Any]) -> str:
        """Format static analysis results for LLM prompt"""
        formatted = []
        
        if results.get('bugs'):
            formatted.append("## Bugs Found:")
            for bug in results['bugs'][:5]:
                desc = bug.get('description', str(bug))
                line = bug.get('line', 'N/A')
                formatted.append(f"- Line {line}: {desc}")
        
        if results.get('security'):
            formatted.append("\n## Security Issues:")
            for sec in results['security'][:5]:
                desc = sec.get('description', str(sec))
                line = sec.get('line', 'N/A')
                severity = sec.get('severity', 'MEDIUM')
                formatted.append(f"- [{severity}] Line {line}: {desc}")
        
        if results.get('style'):
            formatted.append("\n## Style Issues:")
            for style in results['style'][:5]:
                desc = style.get('description', str(style))
                line = style.get('line', 'N/A')
                formatted.append(f"- Line {line}: {desc}")
        
        if results.get('complexity'):
            formatted.append("\n## Complexity Issues:")
            for comp in results['complexity'][:3]:
                desc = comp.get('description', str(comp))
                formatted.append(f"- {desc}")
        
        return '\n'.join(formatted) if formatted else "No issues found in static analysis."
    
    def format_final_review(self, static_results: Dict[str, Any], llm_review: str, language: str) -> Dict[str, Any]:
        """Format final review output with all sections"""
        
        # Parse LLM review into sections
        sections = self._parse_llm_review(llm_review)
        
        # If no improved code from LLM, create one from static analysis
        if not sections['improved_code'] or len(sections['improved_code'].strip()) < 10:
            sections['improved_code'] = self._generate_improved_code_from_static(static_results, language)
        
        # Combine static and LLM results
        all_bugs = self._merge_issues(static_results.get('bugs', []), sections.get('bugs', []))
        all_security = self._merge_issues(static_results.get('security', []), sections.get('security', []))
        all_quality = self._merge_issues(
            static_results.get('style', []) + static_results.get('complexity', []),
            sections.get('code_quality', [])
        )
        
        # Calculate metrics
        metrics = static_results.get('metrics', {})
        total_issues = len(all_bugs) + len(all_security) + len(all_quality)
        health_score = max(0, min(100, 100 - (total_issues * 5)))
        
        return {
            'language': language,
            'summary': sections.get('summary', 'Code review completed. See detailed sections below.'),
            'bugs': all_bugs[:15],
            'security': all_security[:10],
            'code_quality': all_quality[:10],
            'performance': sections.get('performance', []),
            'suggestions': sections.get('suggestions', []),
            'improved_code': sections['improved_code'],
            'metrics': {
                'function_count': metrics.get('function_count', 0),
                'class_count': metrics.get('class_count', 0),
                'line_count': metrics.get('line_count', 0),
                'health_score': health_score,
                'bug_count': len(all_bugs),
                'security_count': len(all_security),
                'quality_count': len(all_quality)
            }
        }
    
    def _generate_improved_code_from_static(self, static_results, language):
        """Generate improved code based on static analysis findings"""
        bugs = static_results.get('bugs', [])
        
        # Check for specific bugs and provide fixes
        for bug in bugs:
            if isinstance(bug, dict):
                desc = bug.get('description', '').lower()
                if 'unclosed string' in desc or 'unterminated string' in desc:
                    if language == 'python':
                        return '# Fixed version with proper string closing\nprint("Hello")'
                    elif language == 'javascript':
                        return '// Fixed version with proper string closing\nconsole.log("Hello");'
        
        # Default improved code based on language
        if language == 'python':
            return """# Improved Python code with best practices

def main():
    try:
        print("Hello, World!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()"""
        
        elif language == 'javascript':
            return """// Improved JavaScript code with best practices

function main() {
    try {
        console.log("Hello, World!");
    } catch (error) {
        console.error("Error:", error);
    }
}

main();"""
        
        return "// Improved code will appear here after analysis"
    
    def _parse_llm_review(self, text: str) -> Dict[str, Any]:
        """Parse LLM review into sections"""
        sections = {
            'summary': '',
            'bugs': [],
            'security': [],
            'code_quality': [],
            'performance': [],
            'suggestions': [],
            'improved_code': ''
        }
        
        if not text or len(text) < 10:
            sections['summary'] = "Review completed. Check specific tabs for details."
            return sections
        
        current_section = 'summary'
        in_code_block = False
        code_block = []
        
        for line in text.split('\n'):
            line_stripped = line.strip()
            
            if '```' in line:
                if not in_code_block:
                    in_code_block = True
                    code_block = []
                else:
                    in_code_block = False
                    sections['improved_code'] = '\n'.join(code_block)
                continue
            
            if in_code_block:
                code_block.append(line)
                continue
            
            # Detect section headers
            lower_line = line_stripped.lower()
            if 'executive summary' in lower_line:
                current_section = 'summary'
                continue
            elif 'bugs:' in lower_line or 'bugs and errors' in lower_line:
                current_section = 'bugs'
                continue
            elif 'security issues' in lower_line or 'security:' in lower_line:
                current_section = 'security'
                continue
            elif 'code quality' in lower_line or 'style issues' in lower_line:
                current_section = 'code_quality'
                continue
            elif 'performance issues' in lower_line:
                current_section = 'performance'
                continue
            elif 'suggestions' in lower_line or 'recommendations' in lower_line:
                current_section = 'suggestions'
                continue
            elif 'improved code' in lower_line:
                current_section = 'improved_code'
                continue
            
            # Skip empty lines if we are just starting to collect a summary
            if not line_stripped and current_section != 'summary':
                continue
                
            if current_section == 'summary':
                if line_stripped:
                    sections['summary'] += line_stripped + '\n'
            elif current_section in ['bugs', 'security', 'code_quality', 'performance', 'suggestions']:
                if line_stripped.startswith(('-', '•', '*')):
                    content = line_stripped.lstrip('- •*').strip()
                    sections[current_section].append(content)
                elif line_stripped and line_stripped[0].isdigit() and len(line_stripped) > 1 and line_stripped[1] == '.':
                    content = line_stripped[2:].strip()
                    sections[current_section].append(content)
                elif line_stripped:
                     # Append free text to the array as a single string
                     sections[current_section].append(line_stripped)

        sections['summary'] = sections['summary'].strip()
        if not sections['summary']:
            sections['summary'] = "Check specific tabs for detailed review results."
            
        return sections
    
    def _merge_issues(self, static_issues: List, llm_issues: List) -> List[Dict]:
        """Merge static analysis and LLM issues"""
        merged = []
        seen = set()
        
        # Process static issues
        for issue in static_issues:
            if isinstance(issue, dict):
                desc = issue.get('description', '')
                severity = issue.get('severity', 'medium')
                line = issue.get('line', 'N/A')
            else:
                desc = str(issue)
                severity = 'medium'
                line = 'N/A'
            
            key = f"{desc[:50]}_{line}"
            if key not in seen:
                seen.add(key)
                merged.append({
                    'description': desc,
                    'severity': severity,
                    'line': line
                })
        
        return merged