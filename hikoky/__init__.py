from flask import Flask
from config import SECRET_KEY

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    
    app.secret_key = SECRET_KEY
    # تسجيل الوحدات الفرعية
    from .blueprints.main.routes import main
    from .blueprints.manga.routes import manga
    from .blueprints.chapter.routes import chapter

    app.register_blueprint(main)
    app.register_blueprint(manga)
    app.register_blueprint(chapter)

    return app
