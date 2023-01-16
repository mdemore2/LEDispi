from collections import namedtuple
from rgbmatrix import graphics, RGBMatrix

Show = namedtuple("Show", ["type", "value"])
Page = namedtuple("Page", ["text", "max_w_len", "max_h_pos"])


class Text:
    def __init__(self, txt: str, h_pos: int, w_len: int):
        self.msg = txt
        self.h_pos = h_pos
        self.w_len = w_len


# new datatype -- page.text.h_pos page.text.w_len page.max_w_len page.max_h_pos
class Content:
    def __init__(self, content: dict, canvas: RGBMatrix):
        self._canvas = canvas
        self._font = graphics.Font()
        self._font.LoadFont('rpi-rgb-led-matrix/fonts/7x13.bdf')
        self._text_color = graphics.Color(255, 255, 0)
        self._h_font_size = 7
        self._h_buffer = 4
        self._w_buffer = 2
        self._disp_height = 32
        self._disp_width = 64
        self.pages = self._build_content(content)

    def _build_content(self, content: dict) -> list[Page]:
        cont_list = []
        pg_list = []
        max_h_pos = 0
        max_w_len = 0
        h_pos = self._h_font_size
        for key, value in content.items():
            if value != 'N/A':
                h_pos += self._h_buffer
                if h_pos > self._disp_height:
                    cont_list.append(Page(pg_list, max_w_len, max_h_pos))
                    pg_list = []
                    max_w_len = 0
                    max_h_pos = 0
                    h_pos = self._h_buffer + self._h_font_size
                w_len = graphics.DrawText(self._canvas, self._font, 0, 0, self._text_color, f'{key.upper()}: {value}')
                if w_len > max_w_len:
                    max_w_len = w_len
                if h_pos > max_h_pos:
                    max_h_pos = h_pos
                pg_list.append(Text(f'{key.upper()}: {value}', h_pos, w_len))
                h_pos += self._h_font_size + (2 * self._h_buffer)

        return cont_list



