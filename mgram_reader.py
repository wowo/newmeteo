#!/usr/bin/python

from datetime import datetime,timedelta
import os

class TemperatureReader:

    x_range = range(79, 477)
    y_range = range(30, 133)
    pixel = (255, 0, 0)
    scale_x = 64
    time_y = 61
    step = 180
    image = None

    def __init__(self, image):
        self.image = image

    def __ocr_image(self, image):
        file = '/tmp/ocr_image.png'
        image.save(file)
        string = os.popen('gocr -C \'0123456789--\' -i %s' % file).read()

        return string

    def __get_times(self):
        times = []
        for x in range(self.scale_x, self.x_range[-1]):
            if (0, 0, 0) == self.image.getpixel((x, self.time_y)):
                if len(times) == 0:
                    number = self.image.crop((x - 8, self.time_y - 20, x + 8, self.time_y - 8))
                    string =  int(self.__ocr_image(number))
                    date = datetime.now()
                    times.append((x, date.replace(hour=int(), minute=0, second=0, microsecond=0)))
                else:
                    times.append((x, (times[-1][1] + timedelta(minutes=self.step))))

        return times

    def __get_scale(self):
        scale = []
        for y in self.y_range:
            if (0, 0, 0) == self.image.getpixel((self.scale_x, y)) and y - 1 not in scale:
                number = self.image.crop((self.scale_x - 27, y - 4, self.scale_x - 7, y + 10))
                scale.append((y, float(self.__ocr_image(number))))

        return scale

    def read(self, date_as_string=False):
        temperatures = []
        for x in self.x_range:
            for y in self.y_range:
                if self.pixel == self.image.getpixel((x,y)):
                    prev = None
                    for touple in self.__get_scale():
                        if touple[0] >= y:
                            temperature = round((touple[1] - prev[1]) * (float(y - prev[0]) / float(touple[0] - prev[0])), 1)
                            if touple[1] >= 0.0:
                                temperature = temperature * -1.0
                            break
                        prev = touple
                    prev = None
                    for touple in self.__get_times():
                        if touple[0] >= x:
                            minutes = round(self.step * (float(x - prev[0]) / float(touple[0] - prev[0])))
                            time = prev[1] + timedelta(minutes=minutes)
                        prev = touple
                    temperatures.append((time.strftime('%m-%d %H:%M') if date_as_string else time,temperature))
                    break

        return temperatures
