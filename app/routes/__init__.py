from flask import Blueprint

# Import the blueprints
from .pca import pca_bp
from .tsne import tsne_bp
from .lda import lda_bp
from .vars import vars_bp
from .anonymization import anonymization_bp
from .univis import univis_bp
from .multivis import multivis_bp
from .multivis_final_res import multivis_final_res_bp
from .univis_final_res import univis_final_res_bp
# Register the blueprints and their associated views
def register_routes(app):
    app.register_blueprint(pca_bp)
    app.register_blueprint(tsne_bp)
    app.register_blueprint(lda_bp)
    app.register_blueprint(vars_bp)
    app.register_blueprint(anonymization_bp)
    app.register_blueprint(univis_bp)
    app.register_blueprint(multivis_bp)
    app.register_blueprint(multivis_final_res_bp)
    app.register_blueprint(univis_final_res_bp)
