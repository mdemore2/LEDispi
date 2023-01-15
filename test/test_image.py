from PIL import Image, ImageDraw, ImageFont

if __name__ == "__main__":
    bounds_width = 128
    bounds_height = 64
    h_buffer = 1
    w_buffer = 2
    font_size = 8
    font_color = (255, 243, 1)
    font = ImageFont.truetype('../lib/Gidole-Regular.ttf', font_size)
    test_flight = {'origin': "Hartsfield Atlanta", 'airline': 'United', 'number': 'UA2073', 'aircraft': 'Airbus A320',
                   'registration': 'N823452', 'altitude': '1500'}

    im = Image.new(mode='RGB', size=(bounds_width, bounds_height))
    # im.show()
    arr = Image.open('../lib/arrivals.png')
    # dep = Image.open('../lib/departures.png')
    width, height = arr.size
    h_to_w = height / width
    arr = arr.resize((int(bounds_width * 0.5), int(bounds_width * 0.5 * h_to_w)))

    im.paste(arr, (int(bounds_width * 0.25), h_buffer))

    draw = ImageDraw.Draw(im)
    h_pos = arr.size[1] + h_buffer
    for item in test_flight.items():
        h_pos += h_buffer
        draw.text((w_buffer, h_pos), f"{item[0].upper()}:    {item[1]}", font=font, fill=font_color)
        h_pos += font_size

    im.show()

    # TODO: add text:
    # ORIGIN:
    # AIRLINE:
    # FLIGHT #:
    # AIRCRAFT:
    # REGISTRATION:
    # ALTITUDE:
