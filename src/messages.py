import uuid
import requests
from pushbullet import Pushbullet
from src.config import pb_key
from src.show import Show


class Messages:
    def __init__(self):
        self._pb = Pushbullet(pb_key)

    def get_messages(self) -> list[Show]:
        pushes = self._pb.get_pushes() #IF RECEIVING A FILE, MUST DOWNLOAD BEFORE DELETING
        print(pushes)
        msgs = []
        for push in pushes:
            if 'body' in push: #'url', 'file_url'
                msgs.append(Show('text', push['body']))
            elif 'file_type' in push:
                file_type = push['file_type'].split('/')
                if 'image' == file_type[0]:
                    filepath = f'image_{uuid.uuid4()}.{file_type[-1]}'
                    r = requests.get(push['file_url'])
                    open(filepath, 'wb').write(r.content)
                    msgs.append(Show('image', filepath))
        self._pb.delete_pushes()
        return msgs

