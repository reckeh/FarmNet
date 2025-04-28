from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.logger import setup_logger
from app.models import db
from app.routes import auth, products, users
from app.routes.weather import weather_bp
from app.routes.orders import orders_bp
from app.routes.farmer import farmer_bp
from app.routes.market_prices import market_prices_bp
from app.routes.cart import cart_bp
from app.routes.pattern import pattern_bp
from app.routes.reports import reports_bp
from app.routes.deliveries import deliveries_bp
import os

jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:10098@localhost:5432/farmnet_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    app.config['JWT_IDENTITY_CLAIM'] = 'identity'

    # Upload folder
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

    # Serve uploaded files
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    # Extensions
    db.init_app(app)
    Migrate(app, db)
    jwt.init_app(app)

    # Blueprints
    app.register_blueprint(auth.auth_bp, url_prefix="/auth")
    app.register_blueprint(products.products_bp, url_prefix="/products")
    app.register_blueprint(users.users_bp, url_prefix="/users")
    app.register_blueprint(weather_bp, url_prefix="/weather")
    app.register_blueprint(orders_bp, url_prefix='/api')
    app.register_blueprint(farmer_bp, url_prefix="/farmer")
    app.register_blueprint(market_prices_bp)
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(pattern_bp, url_prefix="/pattern")
    app.register_blueprint(reports_bp, url_prefix="/reports")
    app.register_blueprint(deliveries_bp)


    # Logging
    setup_logger(app)

    return app
