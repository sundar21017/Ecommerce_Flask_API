import jwt

def encode_token(SECRET_KEY, data):
    # Generate a JWT token with an expiration time of 1 hour
    payload = {'data': data}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(SECRET_KEY, token):
    try:
        # Decode the JWT token using the secret key
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_data
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}, 401
    except Exception as e:
        return {'error': str(e)}, 500
