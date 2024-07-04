import os 
from market import db 
from market import app 
from market.models import Item , User

# Ensure the database path is correct
db_path = os.path.join(app.instance_path, "market.db")

# Check if the database already exists, create it if it doesn't
if not os.path.exists(db_path):
    with app.app_context():
        db.create_all()
        print('Database created')

# Add items to the database
with app.app_context():
    u1 = User(username='jsc' , password_hash = '12345' , email_address = 'js@js.com')
    item1 = Item(name="IPhone 10", price=500, barcode="1234567890", description="This is an IPhone", owner=u1.id)
    item2 = Item(name="Laptop 10", price=900, barcode="123456340", description="This is a laptop")
    item3 = Item(name="Keyboard", price=100, barcode="123123890", description="This is a keyboard")

    db.session.add_all([item1, item2, item3 , u1])
    db.session.commit()
    print('Items added to the database')
