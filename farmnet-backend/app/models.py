from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

# --- ENUMS ---

class UserRole(Enum):
    FARMER = "farmer"
    BUYER = "buyer"
    AGRI_EXPERT = "agri_expert"
    ADMIN = "admin"
    COURIER = "courier"

    @classmethod
    def values(cls):
        return [role.value for role in cls]

class TransactionType(Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    OTHER = "other"

    @classmethod
    def values(cls):
        return [t.value for t in cls]

class OrderStatus(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


    @classmethod
    def values(cls):
        return [s.value for s in cls]


# --- MODELS ---

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    products = db.relationship('Product', back_populates='owner', cascade="all, delete-orphan")
    orders = db.relationship('Order', back_populates='buyer', cascade="all, delete-orphan")
    transactions = db.relationship('Transaction', back_populates='user', cascade="all, delete-orphan")
    cart_items = db.relationship('Cart', back_populates='user', cascade="all, delete-orphan")
    deliveries = db.relationship('Delivery', back_populates='courier', cascade="all, delete-orphan")
    feedbacks = db.relationship('Feedback', back_populates='user', cascade="all, delete-orphan")
    notifications = db.relationship('Notification', back_populates='user', cascade="all, delete-orphan")

    def is_courier(self):
        return self.role == UserRole.COURIER


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(50), default="kg")
    available = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(255), default="default_image_url.jpg")

    owner = db.relationship('User', back_populates='products')
    cart_items = db.relationship('Cart', back_populates='product', cascade="all, delete-orphan")
    order_items = db.relationship('OrderItem', back_populates='product', cascade="all, delete-orphan")


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='cart_items')
    product = db.relationship('Product', back_populates='cart_items')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Float, default=0.0)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    buyer = db.relationship('User', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order', cascade="all, delete-orphan")
    delivery = db.relationship('Delivery', back_populates='order', uselist=False)


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', back_populates='order_items')


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False)
    description = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='transactions')


class Delivery(db.Model):
    __tablename__ = 'deliveries'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    courier_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    address = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Pending')

    order = db.relationship('Order', back_populates='delivery')
    courier = db.relationship('User', back_populates='deliveries')


class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='feedbacks')


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='notifications')


class Logs(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)
    extra_info = db.Column(db.String(255))


class WeatherData(db.Model):
    __tablename__ = 'weather_data'

    id = db.Column(db.Integer, primary_key=True)
    county = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Numeric(5, 2), nullable=False)
    humidity = db.Column(db.Numeric(5, 2), nullable=False)
    wind_speed = db.Column(db.Numeric(5, 2), nullable=False)
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)


class MarketPrice(db.Model):
    __tablename__ = 'market_prices'

    id = db.Column(db.Integer, primary_key=True)
    commodity = db.Column(db.String(100))
    classification = db.Column(db.String(100))
    grade = db.Column(db.String(100))
    sex = db.Column(db.String(100))
    market = db.Column(db.String(100))
    wholesale_price = db.Column(db.Float)
    retail_price = db.Column(db.Float)
    supply_volume = db.Column(db.Float)
    county = db.Column(db.String(100))
    date = db.Column(db.Date)
