from PIL import Image, ImageDraw, ImageFont
import FlightRadar24.flight
from FlightRadar24.api import FlightRadar24API
from src.show import Show
from src.config import bounds_str, airport_icao


class Flights:
    def __init__(self):
        self._fr = FlightRadar24API()
        self._bounds = bounds_str
        self._airport_icao = airport_icao
        self._img_width = 1280
        self._img_height = 720
        self._h_buffer = 25
        self._w_buffer = 50
        self._font_size = 48
        self._font_color = (255, 243, 1)
        self._font = ImageFont.truetype('../lib/Gidole-Regular.ttf', self._font_size)

    def get_flights(self) -> list[Show]:
        flights = self._fr.get_flights(bounds=self._bounds)
        for flight in flights:
            details = self._fr.get_flight_details(flight.id)
            flight.set_flight_details(details)
        flight_imgs = self.build_img(flights)
        return flight_imgs

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
                header = Image.open('../lib/departures.png')
                flight_dict = {'destination': flight.destination_airport_name}
            elif flight.destination_airport_icao == self._airport_icao:
                header = Image.open('../lib/arrivals.png')
                flight_dict = {'origin': flight.origin_airport_name}
            else:
                header = Image.open('../lib/flyover.png')
                flight_dict = {'origin': flight.origin_airport_name,
                               'destination': flight.destination_airport_name}

            flight_dict.update(post_dict)
            width, height = header.size
            h_to_w = height / width
            header = header.resize((int(self._img_width * 0.5), int(self._img_width * 0.5 * h_to_w)))
            im.paste(header, (int(self._img_width * 0.25), self._h_buffer))

            draw = ImageDraw.Draw(im)
            h_pos = header.size[1] + self._h_buffer
            for item in flight_dict.items():
                h_pos += self._h_buffer
                draw.text((self._w_buffer, h_pos), f"{item[0].upper()}:    {item[1]}", font=self._font, fill=self._font_color)
                h_pos += self._font_size
            path = f'../images/{flight.number}.png'
            im.save('path')
            flight_imgs.append(Show('image', path))

        return flight_imgs

