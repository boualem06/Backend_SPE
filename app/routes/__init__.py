from flask import Blueprint

# Import the blueprints
from .pca import pca_bp
from .tsne import tsne_bp
from .lda import lda_bp

# Register the blueprints and their associated views
def register_routes(app):
    app.register_blueprint(pca_bp)
    app.register_blueprint(tsne_bp)
    app.register_blueprint(lda_bp)
