import sys
import logging
import asyncio
from time import sleep
from src.controller import Controller

if __name__ == "__main__":
    logging.basicConfig(format='%%(asctime)s (levelname)s:%(message)s', level=logging.DEBUG, stream=sys.stdout)
    sleep(10)  # wait for raspi to boot and get connection
    controller = Controller()
    loop = asyncio.get_event_loop()
    loop.create_task(controller.run())
    loop.run_forever()
    
