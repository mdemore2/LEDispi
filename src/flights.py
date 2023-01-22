import logging
from PIL import Image, ImageDraw, ImageFont
import FlightRadar24.flight
from FlightRadar24.api import FlightRadar24API
from src.show import Show, Content
from src.display import Display
from src.config import bounds_str, airport_icao


class Flights:
    def __init__(self, disp: Display):
        self._logger = logging.getLogger(__name__)
        self._display = disp
        self._fr = FlightRadar24API()
        self._bounds = bounds_str
        self._airport_icao = airport_icao
        self._img_width = 64
        self._img_height = 32
        self._h_buffer = 1
        self._w_buffer = 2
        self._font_size = 8
        self._font_color = (255, 243, 1)
        self._font = ImageFont.truetype('lib/Gidole-Regular.ttf', self._font_size)

    def get_flights(self) -> list[Show] | None:
        try:
            flights = self._fr.get_flights(bounds=self._bounds)
        except Exception as e:
            self._logger.warning('FlightRadar error: %s', e)
            return
        show_list = []
        for flight in flights:
            try:
                details = self._fr.get_flight_details(flight.id)
            except Exception as e:
                self._logger.warning('FlightRadar error: %s', e)
                continue
            flight.set_flight_details(details)
            post_dict = {'arln': flight.airline_short_name,
                         'flt#': flight.number,
                         'acft': flight.aircraft_model,
                         'alt': f'{str(flight.altitude)} ft',
                         'reg': flight.registration}
            if flight.origin_airport_icao == self._airport_icao:
                flight_dict = {'dest': flight.destination_airport_name}
            elif flight.destination_airport_icao == self._airport_icao:
                flight_dict = {'orig': flight.origin_airport_name}
            else:
                flight_dict = {'orig': flight.origin_airport_name,
                               'dest': flight.destination_airport_name}
            flight_dict.update(post_dict)
            show_list.append(Show('content', Content(flight_dict, self._display._matrix)))
        return show_list

    def build_img(self, flights: list[FlightRadar24.flight]) -> list[Show]:
        flight_imgs = []
        for flight in flights:
            im = Image.new(mode='RGB', size=(self._img_width, self._img_height))
            post_dict = {'airline': flight.airline_short_name,
                         'flight number': flight.number,
                         'aircraft': flight.aircraft_model,
                         'altitude': flight.altitude,
                         'registration': flight.registration}
            if flight.origin_airport_icao == self._airport_icao:
                header = Image.open('lib/departures.png')
                flight_dict = {'destination': flight.destination_airport_name}
            elif flight.destination_airport_icao == self._airport_icao:
                header = Image.open('lib/arrivals.png')
                flight_dict = {'origin': flight.origin_airport_name}
            else:
                header = Image.open('lib/flyover.png')
                flight_dict = {'origin': flight.origin_airport_name,
                               'destination': flight.destination_airport_name}

            flight_dict.update(post_dict)
            width, height = header.size
            h_to_w = height / width
            header = header.resize((int(self._img_width * 0.5), int(self._img_width * 0.5 * h_to_w)))
            im.paste(header, (int(self._img_width * 0.25), self._h_buffer))

            draw = ImageDraw.Draw(im)
            # h_pos = header.size[1] + self._h_buffer
            h_pos = self._h_buffer
            for item in flight_dict.items():
                h_pos += self._h_buffer
                draw.text((self._w_buffer, h_pos), f"{item[0].upper()}:    {item[1]}", font=self._font,
                          fill=self._font_color)
                h_pos += self._font_size
            flight_num = flight.number.replace('/', '')
            path = f'images/{flight_num}.png'
            im.save(path)
            flight_imgs.append(Show('image', path))

        return flight_imgs
