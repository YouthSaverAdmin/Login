from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from flask_cors import CORS  # Add Flask-CORS
import os

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://loginfrontend-pi.vercel.app"])  # Restrict to frontend origin

# MongoDB Connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client['user_database']
users = db['users']

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    print("Received registration data")  # Debugging log

    if users.find_one({"email": email}):
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = generate_password_hash(password)
    print("Password hashed")  # Debugging log

    user_data = {
        "username": username,
        "email": email,
        "password": hashed_password
    }
    
    # Check MongoDB insertion
    try:
        users.insert_one(user_data)
        print("User data inserted")  # Debugging log
    except Exception as e:
        print(f"Error inserting data: {e}")
        return jsonify({"message": "Error inserting data"}), 500

    return jsonify({"message": "User registered successfully"}), 201

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = users.find_one({"email": email})
    if user and check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)
