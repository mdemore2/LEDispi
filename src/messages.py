from pushbullet import Pushbullet
from src.config import pb_key


class Messages:
    def __init__(self):
        self._pb = Pushbullet(pb_key)

    def get_messages(self):
        pushes = self._pb.get_pushes()
        self._pb.delete_pushes()
        msgs = [x['body'] for x in pushes]
        return msgs
