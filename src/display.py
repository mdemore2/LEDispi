from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image
from datetime import datetime, timedelta
import time
import os


class Display:
    def __init__(self):
        self._options = RGBMatrixOptions()
        self._options.rows = 32
        self._options.cols = 64
        self._options.chain_length = 1
        self._options.parallel = 1
        self._options.hardware_mapping = 'adafruit-hat'

        self._matrix = RGBMatrix(options=self._options)

        self._font = graphics.Font()
        self._font.LoadFont('rpi-rgb-led-matrix/fonts/4x6.bdf')
        self._text_color = graphics.Color(255, 255, 0)

        self._duration = timedelta(seconds=15)

    def send_text(self, text: str):
        offscreen_canvas = self._matrix.CreateFrameCanvas()
        pos = offscreen_canvas.width
        start = datetime.utcnow()

        while (start + self._duration) > datetime.utcnow():
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, self._font, pos, 7, self._text_color, text)
            pos -= 1
            if (pos + len) < 0:
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self._matrix.SwapOnVSync(offscreen_canvas)
        self._matrix.Clear()

    def send_flight(self, flight):
        canvas = self._matrix
        h_font_size = 6
        h_buffer = 1
        w_buffer = 2
        post_dict = {'airline': flight.airline_short_name,
                     'flt#': flight.number,
                     'acft': flight.aircraft_model,
                     'alt': flight.altitude,
                     'reg': flight.registration}
        if flight.origin_airport_icao == '':
            flight_dict = {'dest': flight.destination_airport_name}
        elif flight.destination_airport_icao == '':
            flight_dict = {'origin': flight.origin_airport_name}
        else:
            flight_dict = {'origin': flight.origin_airport_name,
                           'dest': flight.destination_airport_name}
        flight_dict.update(post_dict)
        h_pos = h_font_size
        for item in flight_dict.items():
            if item[1] != 'N/A':
                h_pos += h_buffer
                graphics.DrawText(canvas, self._font, w_buffer, h_pos, self._text_color, f"{item[1]}")
                h_pos += h_font_size
        start = datetime.utcnow()
        while (start + self._duration) > datetime.utcnow():
            time.sleep(5)
        #TODO: wipe screen
        self._matrix.Clear()

    def send_image(self, path: str):
        image = Image.open(path)
        image.thumbnail((self._matrix.width, self._matrix.height), Image.ANTIALIAS)
        self._matrix.SetImage(image.convert('RGB'))
        start = datetime.utcnow()
        while (start + self._duration) > datetime.utcnow():
            time.sleep(5)
        #TODO: wipe screen
        self._matrix.Clear()
        #TODO: delete img
        os.remove(path)
        




