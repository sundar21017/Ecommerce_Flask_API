from flask import Flask, request, jsonify
from flask_restful import Resource
from utils import encode_token, decode_token
from config.db import *

users = []

class UserResource(Resource):
    def post(self, endpoint=None):
        if endpoint == 'userDetails':
            return self.userDetails()
        elif endpoint == 'userLogin':
            return self.userLogin()
        else:
            return jsonify({'error': 'Invalid endpoint'}), 404
        
    def userDetails(self):
        try:
            SECRET_KEY = 'sundarscretekey'

            # Get JSON data from the request
            json_data = request.get_json()

            # Check if 'token' is present in the JSON data
            if 'payload' not in json_data:
                return jsonify({'error': 'Token not found in JSON data'}), 400
            
            decoded_data = decode_token(SECRET_KEY, json_data['payload'])

            # Check if required fields are present
            if not decoded_data or 'username' not in decoded_data or 'email' not in decoded_data:
                return jsonify({'error': 'Missing username or email in the request'}), 400

            # Extract user details from JSON data
            username = decoded_data['username']
            email = decoded_data['email']

            # Create a new user dictionary
            new_user = {
                'username': username,
                'email': email
            }

            # Add the new user to the list
            users.append(new_user)

            # Generate JWT token with user data using the common function
            token = encode_token(SECRET_KEY, users)

            # Return the new user details
            return jsonify({'response' : token}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Return the exception details with a 500 Internal Server Error status
        
    def userLogin(self):
        try:
            # Get user input from the request
            username = request.json.get('username')
            password = request.json.get('password')

            mycursor = db.cursor()

            # Fetch user details from the database based on the username
            mycursor.execute("SELECT userID, userName, userPassword FROM tblUser WHERE userName = %s AND userPassword = %s", (username, password))
            user = mycursor.fetchone()

            # Close the cursor
            mycursor.close()

            if user:
                # Passwords match, return a success response
                response = {'statusCode' : 200, 'message': 'Login successful', 'user_id': user[0]}
                return jsonify(response)
            else:
                # Either user not found or incorrect password, return an error response
                response = {'statusCode' : 401, 'message': 'Login failed. Invalid username or password.'}
                return jsonify(response)
        except Exception as e:
            return jsonify({'statusCode' : 401, 'error': f'Error fetching user list: {str(e)}'})

def initialize_user_component(api):
    # Add resources to the API
    api.add_resource(UserResource, '/user/<string:endpoint>')