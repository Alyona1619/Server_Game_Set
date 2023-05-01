# Server_Game_Set
Развертывание сервера:

1) sudo apt update
2) sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

3) cd *папка проекта*

4) pip install gunicorn flask

5) gunicorn --bind 0.0.0.0:8000 wsgi:app

Сервер доступен по адресу:
http://your_server_ip:8000
