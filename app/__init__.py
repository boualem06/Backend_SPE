# from flask import Flask

# def create_app():
#     app = Flask(__name__)

#     from .routes import pca_bp, tsne_bp, lda_bp
#     app.register_blueprint(pca_bp)
#     app.register_blueprint(tsne_bp)
#     app.register_blueprint(lda_bp)

#     return app


from flask import Flask
from flask_cors import CORS
# Import the register_routes function from app/routes/__init__.py
from .routes import register_routes

def create_app():
    app = Flask(__name__)

    CORS(app)
    # Call the register_routes function to register the routes
    register_routes(app)

    return app





