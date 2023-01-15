import asyncio
from src.controller import Controller

if __name__ == "__main__":
    controller = Controller()
    loop = asyncio.get_event_loop()
    loop.create_task(controller.run())
    loop.run_forever()
    
