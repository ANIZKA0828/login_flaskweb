from .views import index_view
from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY')

    from .views import create_view, detail_view, modify_view, delete_view, register_view, find_view, profile_view
    app.register_blueprint(index_view.bp)
    app.register_blueprint(create_view.bp)
    app.register_blueprint(detail_view.bp)
    app.register_blueprint(modify_view.bp)
    app.register_blueprint(delete_view.bp)
    app.register_blueprint(register_view.bp)
    app.register_blueprint(find_view.bp)
    app.register_blueprint(profile_view.bp)

    return app