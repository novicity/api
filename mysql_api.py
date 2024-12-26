from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure MySQL Database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:202313@localhost/db_1"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
#'NAME': 'db_1','USER': 'root','PASSWORD': '202313','HOST': 'localhost','PORT': '3306'

# Define the Item model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "available": self.available,
        }


# Initialize the Database During Startup
with app.app_context():
    db.create_all()
    print("Database initialized!")

# Create an item
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        abort(400, "Invalid input data.")
    
    new_item = Item(
        name=data["name"],
        description=data.get("description"),
        price=data["price"],
        available=data.get("available", True),
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

# Read all items
@app.route("/items", methods=["GET"])
def read_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

# Read a single item by ID
@app.route("/items/<int:item_id>", methods=["GET"])
def read_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        abort(404, "Item not found.")
    return jsonify(item.to_dict())

# Update an item
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    if not data:
        abort(400, "Invalid input data.")
    
    item = Item.query.get(item_id)
    if not item:
        abort(404, "Item not found.")
    
    item.name = data.get("name", item.name)
    item.description = data.get("description", item.description)
    item.price = data.get("price", item.price)
    item.available = data.get("available", item.available)
    
    db.session.commit()
    return jsonify(item.to_dict())

# Delete an item
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        abort(404, "Item not found.")
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
