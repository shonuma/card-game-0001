

class Game(object):
    def __init__(self, client, room_id):
        self.client = client
        self.players = []
        self.room_id = room_id
 
    def _get_redis_key(self, events=[]):
        base = 'GAME::{}'.format(
            self.room_id,
        )
        for event in events:
            base += '::{}'.format(event)
        return base

    def create_room(self, player_id):
        self.client.set(
            self._get_redis_key(
                'created',
            ),
            player_id
        )

    def get_owner_player_id(self):
        return self.client.get(
            self._get_redis_key(
                'created',
            )
        )

    def join(self, player_id):
        # プレイに参加する
        self.client.set(
            self._get_redis_key(
                'member'
            )
        )
