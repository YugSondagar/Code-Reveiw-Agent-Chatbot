from services.ollama_client import OllamaClient
from config import Config
import json
from datetime import datetime
from collections import defaultdict

class ChatService:
    def __init__(self):
        self.ollama = OllamaClient()
        self.history = defaultdict(list)
        self.max_items = Config.MAX_HISTORY_ITEMS
    
    def add_message(self,session_id,message):
        """Add message to chat history"""
        message['timestamp'] = datetime.now().isoformat()
        self.history[session_id].append(message)

        if len(self.history[session_id])> self.max_items:
            self.history[session_id] = self.history[session_id][-self.max_items:]

    def get_history(self, session_id):
        """Return chat history for a session"""
        return self.history[session_id]

    def get_response(self, session_id, message, code_context='', language=''):
        """Get Chat response with context"""
        recent_history = self.get_history(session_id)[-10:] 

        messages = []

        messages.append({
            'role': 'system',
            'content': """You are an AI Code review assistant. Help users with:
            - Code reviews and improvements
            - Debugging issues
            - Best practices and design patterns
            - Language-specific questions
            Be concise but thorough in your responses.
            """
        })
        for msg in recent_history:
            if msg['role'] == 'user':
                content = msg['content']
                if 'language' in msg:
                    content = f"[Language: {msg['language']}]\n{content}"
                messages.append({'role':'user','content':msg['content']})
        
        messages.append({'role':'user','content':message})
        response = self.ollama.chat(messages)

        self.add_message(session_id,{'role':'user','content':message})
        self.add_message(session_id,{'role':'assistant','content':response})

        return response