"""
Project 1: REST API Fundamentals
Goal: Build a stateless web server that serves data.
Key Skills: HTTP methods, routing logic, JSON formatting.
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample in-memory data
items = [
    {"id": 1, "name": "Item One", "description": "First item"},
    {"id": 2, "name": "Item Two", "description": "Second item"},
]


# GET route - return all items
@app.route("/items", methods=["GET"])
def get_items():
    return jsonify({
        "status": "ok",
        "count": len(items),
        "data": items
    }), 200


# GET route - return single item by id
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        return jsonify({"status": "error", "message": "Item not found"}), 404
    return jsonify({"status": "ok", "data": item}), 200


# POST route - add a new item
@app.route("/items", methods=["POST"])
def create_item():
    body = request.get_json()

    if not body or "name" not in body:
        return jsonify({"status": "error", "message": "Missing 'name' field"}), 400

    new_item = {
        "id": items[-1]["id"] + 1 if items else 1,
        "name": body["name"],
        "description": body.get("description", ""),
    }
    items.append(new_item)

    return jsonify({"status": "ok", "message": "Item created", "data": new_item}), 201


# Health check route
@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok", "message": "REST API is running"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
