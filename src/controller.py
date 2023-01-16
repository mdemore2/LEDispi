import asyncio
import glob
from datetime import datetime, timedelta
from src.show import Show
from src.display import Display
from src.flights import Flights
from src.messages import Messages


class Controller:
    def __init__(self) -> None:
        self._display = Display()
        self._msgs = Messages()
        self._flights = Flights(self._display)
        self._flight_wait = timedelta(minutes=1)
        self._msg_wait = timedelta(minutes=15)
        self._last_poll_flight = datetime.utcnow() - self._flight_wait
        self._last_poll_msg = datetime.utcnow() - self._msg_wait

    async def run(self):
        while True:
            if self._last_poll_msg + self._msg_wait < datetime.utcnow():
                self._last_poll_msg = datetime.utcnow()
                msg_list = self._msgs.get_messages()
                if msg_list:
                    for msg in msg_list:
                        if msg.type == 'text':
                            self._display.send_text(msg.value)
                        elif msg.type == 'image':
                            self._display.send_image(msg.value)
                        elif msg.type == 'content':
                            self._display.send_content(msg.value)
            elif self._last_poll_flight + self._flight_wait < datetime.utcnow():
                self._last_poll_flight = datetime.utcnow()
                flight_list = self._flights.get_flights()
                if flight_list:
                    for flight in flight_list:
                        if flight.type == 'text':
                            self._display.send_text(flight.value)
                        elif flight.type == 'image':
                            self._display.send_image(flight.value)
                        elif flight.type == 'content':
                            self._display.send_content(flight.value)
            else:
                await asyncio.sleep(60)
