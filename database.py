from dotenv import load_dotenv
import random


load_dotenv()

# Regardless of the lint error you receive,
# load_dotenv must run before running this
# so that the environment variables are
# properly loaded.
from app import app, db
from app.models import Employee, Menu, MenuItem, MenuItemType, Table


with app.app_context():
    db.drop_all()
    db.create_all()

    
    # Create an employee
    employee = Employee(name="Margot", employee_number=1234, password="password")
    

    # Create instances of MenuItemType
    beverages = MenuItemType(name="Beverages")
    entrees = MenuItemType(name="Entrees")
    sides = MenuItemType(name="Sides")

    # Create instance of Menu
    dinner = Menu(name="Dinner")

    # Create instances of MenuItem
    fries = MenuItem(name="French fries", price=3.50, type=sides, menu=dinner)
    drp = MenuItem(name="Dr. Pepper", price=1.0, type=beverages, menu=dinner)
    jambalaya = MenuItem(name="Jambalaya", price=21.98, type=entrees, menu=dinner)

    # Add instances to the session
    db.session.add(employee)
    db.session.add(beverages)
    db.session.add(entrees)
    db.session.add(sides)
    db.session.add(dinner)
    
    # Create 10 tables with different numbers and capacities
    for i in range(1, 11):
        table = Table(number=i, capacity=random.randint(0, 6))  # Example: capacities from 2 to 5
        db.session.add(table)
    
    db.session.commit()