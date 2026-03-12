import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from models.user_model import UserModel
    from models.project_model import ProjectModel, project_members
    from models.task_model import TaskModel
    from models.comment_model import CommentModel, AttachmentModel

    from routes.auth_routes import auth_bp
    from routes.project_routes import projects_bp
    from routes.task_routes import tasks_bp
    from routes.comment_routes import comments_bp
    from routes.analytics_routes import analytics_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(comments_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

    @app.route("/")
    def health():
        return {"status": "API running"}

    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables ready")
        except Exception as e:
            print(f"⚠️ DB init skipped: {e}")

    return app


# For Gunicorn
app = create_app()


# Local run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)