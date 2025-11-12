import os
from app import app

# Ensure upload folder exists if app expects to save files
UPLOAD_FOLDER = getattr(app.config, 'UPLOAD_FOLDER', 'static/uploads') if hasattr(app, 'config') else 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Expose the WSGI application as 'app' for Gunicorn/Render

if __name__ == '__main__':
    # Local debug runner (bind to PORT if provided by environment)
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
