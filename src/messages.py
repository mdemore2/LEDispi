from pushbullet import Pushbullet
from src.config import pb_key


class Messages:
    def __init__(self):
        self._pb = Pushbullet(pb_key)

    def get_messages(self):
        pushes = self._pb.get_pushes() #IF RECEIVING A FILE, MUST DOWNLOAD BEFORE DELETING
        print(pushes)
        self._pb.delete_pushes()
        msgs = []
        for push in pushes:
            if 'body' in push: #'url', 'file_url'
                msgs.append(push['body'])
        return msgs
