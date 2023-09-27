#from models import db, Restaurant, Pizza, RestaurantPizza


from app import app, db
from models import Restaurant, Pizza, RestaurantPizza

# Function to seed data
def seed_database():
    # Create all database tables
    with app.app_context():
        db.create_all()

        # Sample restaurants
        restaurant1 = Restaurant(name="Pizza Palace", address="123 Main St")
        restaurant2 = Restaurant(name="Italian Delight", address="456 Oak St")

        # Sample pizzas
        pizza1 = Pizza(name="Margherita", ingredients="Tomato, Mozzarella, Basil")
        pizza2 = Pizza(name="Pepperoni", ingredients="Tomato, Mozzarella, Pepperoni")

        # Add and commit the restaurants and pizzas to the database
        db.session.add(restaurant1)
        db.session.add(restaurant2)
        db.session.add(pizza1)
        db.session.add(pizza2)
        db.session.commit()

        # Create relationships between restaurants and pizzas with prices
        rp1 = RestaurantPizza(restaurant=restaurant1, pizza=pizza1, price=10.99)
        rp2 = RestaurantPizza(restaurant=restaurant1, pizza=pizza2, price=12.99)
        rp3 = RestaurantPizza(restaurant=restaurant2, pizza=pizza1, price=11.99)

        # Add and commit the relationships to the database
        db.session.add(rp1)
        db.session.add(rp2)
        db.session.add(rp3)
        db.session.commit()

if __name__ == '__main__':
    seed_database()
    print("Sample data has been seeded into the database.")

