import secrets
from flask import Flask, request, jsonify

app = Flask(__name__)

users = []


@app.route('/user/register', methods=['POST'])
def register_user():
    username = request.json.get('nickname')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Please provide a nickname and password'}), 400

    for user in users:
        if user['nickname'] == username:
            return jsonify({'error': 'This nickname is already taken'}), 400

    access_token = secrets.token_urlsafe(16)

    users.append({'nickname': username, 'password': password, 'accessToken': access_token})

    return jsonify({'nickname': username, 'accessToken': access_token}), 201


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
