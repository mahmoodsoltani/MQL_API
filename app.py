from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (you can replace this with database integration later)
data = [
    {"id": 1, "name": "Apple", "price": 1.2},
    {"id": 2, "name": "Banana", "price": 0.5},
    {"id": 3, "name": "Orange", "price": 0.8},
]

# Home route
@app.route('/')
def home():
    return "Welcome to the Simple RESTful API!"

# Get all items
@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(data)

# Get a specific item by ID
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
