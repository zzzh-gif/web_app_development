from flask import Blueprint

def register_blueprints(app):
    from .main_route import main_bp
    from .parking_route import parking_bp
    from .traffic_route import traffic_bp
    from .transit_route import transit_bp
    from .pedestrian_route import pedestrian_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(parking_bp)
    app.register_blueprint(traffic_bp)
    app.register_blueprint(transit_bp)
    app.register_blueprint(pedestrian_bp)
