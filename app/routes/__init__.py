from flask import Blueprint


from .pca import pca_bp
from .tsne import tsne_bp
from .lda import lda_bp
from .vars import vars_bp
from .univis import univis_bp
from .multivis import multivis_bp


def register_routes(app):
    app.register_blueprint(pca_bp)
    app.register_blueprint(tsne_bp)
    app.register_blueprint(lda_bp)
    app.register_blueprint(vars_bp)
    app.register_blueprint(univis_bp)
    app.register_blueprint(multivis_bp)
