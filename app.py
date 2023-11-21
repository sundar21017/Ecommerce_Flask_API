# Using flask to make an api 
# import necessary libraries and functions 
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from config.db import *
import jwt

from components.userComponent import initialize_user_component
from utils import encode_token

# creating a Flask app 
app = Flask(__name__)

# creating an API object 
api = Api(app)

# Call the function to initialize resources
initialize_user_component(api)

class Hello(Resource): 
    def get(self): 
        return jsonify({'message': 'hello world'})

class Square(Resource):
    def get(self, num):
  
        return jsonify({'square': num**2})

class EncodeToken(Resource):
    def post(self):
        SECRET_KEY = 'sundarscretekey'
        payload = request.get_json()

        # Encode the token
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'EncodeToken': token})
    
class DecodeToken(Resource):
    def post(self):
        SECRET_KEY = 'sundarscretekey'
        try:
            # Get the token from the URL parameter
            token = request.get_json()

            # Decode the token
            decoded_data = jwt.decode(token['DecodeToken'], SECRET_KEY, algorithms=['HS256'])

            return jsonify({'decoded_data': decoded_data})
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

class userList(Resource):
    def get(self):
        try:
            SECRET_KEY = 'sundarscretekey'
            mycursor = db.cursor()

            mycursor.execute("SELECT * FROM tblUser")

            users = mycursor.fetchall()

            # Convert the data to a list of dictionaries
            user_list = []
            for user in users:
                # Create a new user dictionary
                user_ls = {
                    'username': user[2],
                    'email': user[3]
                }

                # Add the new user to the list
                user_list.append(user_ls)

            # Close the cursor
            mycursor.close()

            # Generate JWT token with user data using the common function
            token = encode_token(SECRET_KEY, user_list)

            print(token)

            # Return the new user details
            return jsonify({'statusCode' : 200, 'response' : token})
        except Exception as e:
            return jsonify({'error': f'Error fetching user list: {str(e)}'}), 500


# adding the defined resources along with their corresponding urls 
api.add_resource(Hello, '/') 
api.add_resource(Square, '/square/<int:num>')

api.add_resource(EncodeToken, '/EncodeToken') 
api.add_resource(DecodeToken, '/DecodeToken') 

api.add_resource(userList, '/userList') 

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
