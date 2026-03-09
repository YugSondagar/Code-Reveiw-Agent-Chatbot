from flask import Blueprint, request, jsonify
from services.code_analyzer import CodeAnalyzer
from services.chat_service import ChatService
from utils.language_detect import LanguageDetector
from utils.chunker import CodeChunker
import uuid
import traceback

review_bp = Blueprint('review', __name__)

# Initialize services
analyzer = CodeAnalyzer()
chat_service = ChatService()
language_detector = LanguageDetector()
chunker = CodeChunker()


@review_bp.route('/review', methods=['POST'])
def review_code():

    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        code = data.get('code', '')
        language = data.get('language', 'auto')  # Default to auto
        filename = data.get('filename', '')
        session_id = data.get('session_id', str(uuid.uuid4()))

        if not code or not code.strip():
            return jsonify({'error': 'No code provided'}), 400
            
        # Auto-detect language if specified
        if language == 'auto':
            language = language_detector.detect(code, filename)
        
        # Analyze the code
        review_result = analyzer.analyze(code, language)

        # Add to chat history
        chat_service.add_message(session_id, {
            'role': 'user',
            'content': code[:500],  # Truncate for history
            'language': language,
            'filename': filename
        })

        chat_service.add_message(session_id, {
            'role': 'assistant',
            'content': review_result,
            'type': 'review'
        })

        return jsonify({
            'success': True,
            'session_id': session_id,
            'language': language,
            'review': review_result
        })
        
    except Exception as e:
        print(f"Error in review_code: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@review_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        message = data.get('message', '')
        session_id = data.get('session_id', str(uuid.uuid4()))
        code_context = data.get('code', '')  # Get current code
        language = data.get('language', '')  # Get language
        
        if not message or not message.strip():
            return jsonify({'error': 'No message provided'}), 400
        
        # Get chat response with code context
        response = chat_service.get_response(
            session_id, 
            message, 
            code_context=code_context,
            language=language
        )
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'response': response
        })
        
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
        
@review_bp.route('/history/<session_id>', methods=['GET'])
def get_history(session_id):
    try:
        history = chat_service.get_history(session_id)
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@review_bp.route('/languages', methods=['GET'])
def get_languages():
    """Return list of supported languages"""
    try:
        from config import Config
        languages = list(Config.SUPPORTED_LANGUAGES.keys())
        return jsonify({
            'success': True,
            'languages': languages
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'languages': ['python', 'javascript', 'typescript']  # Fallback
        }), 200

@review_bp.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'running',
        'message': 'Code Review Agent API is running'
    })