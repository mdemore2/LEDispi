import uuid
import requests
import logging
from pushbullet import Pushbullet
from src.config import pb_key
from src.show import Show


class Messages:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._pb = Pushbullet(pb_key)

    def get_messages(self) -> list[Show] | None:
        try:
            pushes = self._pb.get_pushes()  # IF RECEIVING A FILE, MUST DOWNLOAD BEFORE DELETING
        except Exception as e:
            self._logger.warning('Pushbullet error: %s', e)
            return

        msgs = []
        for push in pushes:
            if 'body' in push:  # 'url', 'file_url'
                msgs.append(Show('text', push['body']))
            elif 'file_type' in push:
                file_type = push['file_type'].split('/')
                if 'image' == file_type[0]:
                    filepath = f'images/image_{uuid.uuid4()}.{file_type[-1]}'
                    try:
                        r = requests.get(push['file_url'])
                    except Exception as e:
                        self._logger.warning('Unable to download file: %s', e)
                    else:
                        open(filepath, 'wb').write(r.content)
                        msgs.append(Show('image', filepath))
        try:
            self._pb.delete_pushes()
        except Exception as e:
            self._logger.warning('Pushbullet error: %s', e)
        return msgs
