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
        self._font.LoadFont('rpi-rgb-led-matrix/fonts/7x13.bdf')
        self._text_color = graphics.Color(255, 255, 0)
        self._h_font_size = 7
        self._h_buffer = 2
        self._w_buffer = 2

        self._duration = timedelta(seconds=30)

    def send_text(self, text: str):
        offscreen_canvas = self._matrix.CreateFrameCanvas()
        pos = offscreen_canvas.width
        start = datetime.utcnow()

        while (start + self._duration) > datetime.utcnow():
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, self._font, pos, self._h_buffer, self._text_color, text)
            pos -= 1
            if (pos + len) < 0:
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self._matrix.SwapOnVSync(offscreen_canvas)
        self._matrix.Clear()

    def send_flight(self, flight_dict):
        offscreen_canvas = self._matrix.CreateFrameCanvas()
        w_pos = offscreen_canvas.width
        h_pos = 0
        pages = 0
        disp_dict = {f'page {str(pages)}': []}
        for item in flight_dict.items():
            if item[1] != 'N/A':
                h_pos += self._h_buffer
                if h_pos > offscreen_canvas.height:
                    pages += 1
                    disp_dict[f'page {str(pages)}'] = []
                    h_pos = self._h_buffer
                disp_dict[f'page {str(pages)}'].append((item[1], h_pos))
                h_pos += self._h_font_size
        for page in disp_dict:
            start = datetime.utcnow()
            while (start + self._duration) > datetime.utcnow() and w_pos > 0:
                offscreen_canvas.Clear()
                len = []
                for item in page:
                    len.append(graphics.DrawText(offscreen_canvas, self._font, w_pos, item[1], self._text_color, item[0]))
                w_pos -= 1
                len = max(len)
                if (w_pos + len) < 0:
                    w_pos = offscreen_canvas.width

                time.sleep(0.05)
                offscreen_canvas = self._matrix.SwapOnVSync(offscreen_canvas)
            h_threshold = 0 - self._h_font_size
            while h_pos > h_threshold:
                offscreen_canvas.Clear()
                wid = []
                for item in page:
                    item[1] -= 1
                    graphics.DrawText(offscreen_canvas, self._font, w_pos, item[1], self._text_color, item[0])

                h_pos -= 1
                time.sleep(0.05)
                offscreen_canvas = self._matrix.SwapOnVSync(offscreen_canvas)

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
        




