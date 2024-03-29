from flask import Flask, render_template
from flask_sockets import Sockets
from libs.redis_client import RedisClient
import logging
from models.game import Game
import json
import sys


app = Flask(__name__)
sockets = Sockets(app)

# gunicorn_logger = logging.getLogger('gunicorn.info')
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

@sockets.route('/message')
def chat_global(ws):
    while not ws.closed:
        message = ws.receive()
        if message is None:  # message is "None" if the client has closed.
            continue
        if message == 'PING':
            continue
        # Send the message to all clients connected to this webserver
        # process. (To support multiple processes or instances, an
        # extra-instance storage or messaging system would be required.)
        clients = ws.handler.server.clients.values()
        for client in clients:
            client.ws.send(message)
# [END gae_flex_websockets_app]


def log(message):
    app.logger.info(message)

@sockets.route('/message/<room_id>')
def chat_in_room(ws, room_id):
    db = RedisClient('global')
    while not ws.closed:
        message = ws.receive()
        log(
            ('Got message: {}'.format(str(message)))
        )
        if message is None:  # message is "None" if the client has closed.
            continue
        if not message or message == 'PING':
            continue
        model = Game(db, room_id)
        parameter = {}
        try:
            parameter = json.loads(message)
        except Exception as e:
            print(e)
            return
        # {"method": String, "meta": {}}
        meta = parameter.get('meta') or {}
        if parameter['method'] == 'CREATEROOM':
            model.create_room(
                meta['playerId']
            )
        elif parameter['method'] == 'JOIN':
            model.join(
                meta['playerId']
            )
        elif parameter['method'] == 'START':
            model.start()
        elif parameter['method'] == 'GETCURRENT':
            model.get_current()
        
        # Send the message to all clients connected to this webserver
        # process. (To support multiple processes or instances, an
        # extra-instance storage or messaging system would be required.)
        clients = ws.handler.server.clients.values()
        for client in clients:
            client.ws.send(message)
# [END gae_flex_websockets_app]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/room/<room_id>')
def room(room_id):
    return render_template(
        'room.html',
        data={
            'roomId': room_id,
        }
    )


if __name__ == '__main__':
    print("""
This can not be run directly because the Flask development server does not
support web sockets. Instead, use gunicorn:
gunicorn -b 127.0.0.1:8080 -k flask_sockets.worker main:app
""")
