from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from config import Config

def create_app():
    # Get the absolute path to the frontend folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_folder = os.path.join(base_dir, 'frontend')
    
    print(f"Frontend folder path: {frontend_folder}")  # Debug print
    print(f"Index.html exists: {os.path.exists(os.path.join(frontend_folder, 'index.html'))}")  # Debug print
    
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    
    # Register blueprints
    from routes.review import review_bp
    app.register_blueprint(review_bp, url_prefix='/api')
    
    # Serve frontend
    @app.route('/')
    def serve_index():
        return send_from_directory(frontend_folder, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(frontend_folder, path)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)