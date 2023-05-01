import secrets
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

users = []


@app.after_request
def add_base_response_format(response):
    if response.status_code >= 400:
        success = False
    else:
        success = True
    exception = None
    if response.status_code == 401:
        exception = {'message': 'Unauthorized'}
    elif response.status_code == 404:
        exception = {'message': 'Not found'}
    elif response.status_code == 500:
        exception = {'message': 'Internal server error'}
    response_data = {
        'success': success,
        'exception': exception
    }
    response_data.update(response.json)
    response.data = json.dumps(response_data)
    response.content_type = 'application/json'
    return response


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


def check_token(token):
    for user in users:
        if user["nickname"] == nickname and user["accessToken"] == accessToken:
            return True
    return False


def create_room():
    
    if not check_token(token):
        return {"success": False, "exception": {"message": "Invalid token"}}

    global rooms
    game_id = len(rooms)
    rooms[game_id] = {
        "creator": get_nickname(token),
        "players": [get_nickname(token)],
        "cards": list(range(1, 10)),
        "current_set": None
    }
    return {"success": True, "exception": None, "gameId": game_id}


@app.route('/set/room/create', methods=['POST'])
def create_room_route():
    access_token = request.json.get('accessToken')
    nickname = request.json.get('nickname')
    if not check_token(access_token):
        response_data = {
            "success": False,
            "exception": {
                "message": "Invalid access token"
            }
        }
        return jsonify(response_data), 401

    game_id = create_room()

    response_data = {
        "success": True,
        "exception": None,
        "gameId": game_id
    }
    return jsonify(response_data), 200


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
