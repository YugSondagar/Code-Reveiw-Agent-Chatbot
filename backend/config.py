import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OLLAMA_HOST = os.getenv('OLLAMA_HOST','http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL','deepseek-coder:6.7b')

    SECRET_KEY = os.getenv('SECRET_KEY','dev-secret-key')
    MAX_CODE_SIZE = int(os.getenv('MAX_CODE_SIZE',1000000))
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE',3000))
    MAX_HISTORY_ITEMS = int(os.getenv('MAX_HISTORY_ITEMS',50))

    SUPPORTED_LANGUAGES = {
        'python': {'extensions':['.py'],'tree_sitter':'python'},
        'javascript': {'extensions':['.js','.mjs'],'tree_sitter':'javascript'},
        'typescript': { 'extensions': ['.ts', '.tsx'], 'tree_sitter': 'typescript' },
        'java': { 'extensions': ['.java'], 'tree_sitter': 'java' },
        'cpp': { 'extensions': ['.cpp', '.cc', '.cxx', '.hpp'], 'tree_sitter': 'cpp' },
        'c': { 'extensions': ['.c', '.h'], 'tree_sitter': 'c' },
        'go': { 'extensions': ['.go'], 'tree_sitter': 'go' },
        'rust': { 'extensions': ['.rs'], 'tree_sitter': 'rust' },
        'php': { 'extensions': ['.php'], 'tree_sitter': 'php' },
        'ruby': { 'extensions': ['.rb'], 'tree_sitter': 'ruby' },
        'swift': { 'extensions': ['.swift'], 'tree_sitter': 'swift' },
        'kotlin': { 'extensions': ['.kt', '.kts'], 'tree_sitter': 'kotlin' }
    }