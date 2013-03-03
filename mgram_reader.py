#!/usr/bin/python

from PIL import Image
from datetime import datetime,timedelta
import os

i = Image.open('/home/wowo/Downloads/mgram_pict.png', 'r').convert('RGB')

x_range = range(40, 477)
y_range = range(30, 133)
pixel = (255, 0, 0)
temperature = []
scale_x = 64
time_y = 61
scale = []
time = []


def ocr_image(image):
    file = '/tmp/ocr_image.png'
    image.save(file)
    string = os.popen('gocr -C \'0123456789--\' -i %s' % file).read()
    os.remove(file)

    return string

for x in range(scale_x, x_range[-1]):
    step = 3
    if (0, 0, 0) == i.getpixel((x, time_y)):
        if len(time) == 0:
            number = i.crop((x - 8, time_y - 20, x + 8, time_y - 8))
            string =  int(ocr_image(number))
            date = datetime.now()
            time.append((x, date.replace(hour=int(), minute=0, second=0, microsecond=0)))
        else:
            time.append((x, (time[-1][1] + timedelta(hours=step))))

for y in y_range:
    if (0, 0, 0) == i.getpixel((scale_x, y)) and y - 1 not in scale:
        number = i.crop((scale_x - 27, y - 4, scale_x - 7, y + 5))
        scale.append((y, int(ocr_image(number))))

for x in x_range:
    for y in y_range:
        if pixel == i.getpixel((x,y)):
            temperature.append((x,y))
            break

print scale
print time
