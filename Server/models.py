from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizza'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)

    __table_args__ = (
        CheckConstraint('price >= 1 AND price <= 30', name='check_price_range'),
    )

    restaurant = relationship('Restaurant', back_populates='pizzas')
    pizza = relationship('Pizza', back_populates='restaurants')

    def serialize(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'pizza_id': self.pizza_id,
            'price': self.price,
        }

class Restaurant(db.Model):
    __tablename__ ='restaurant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(55), unique=True, nullable=False)

    __table_args__ = (
        CheckConstraint('id >= 1 AND id <= 50', name='check_id_range'),
    )

    pizzas = relationship('RestaurantPizza', back_populates='restaurant')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
        }

class Pizza(db.Model):
    __tablename__ ='pizza'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    restaurants = relationship('RestaurantPizza', back_populates='pizza')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
        }

