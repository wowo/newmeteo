#!/usr/bin/python

from datetime import datetime,timedelta
import os

class TemperatureReader:

    x_range = range(79, 477)
    y_range = range(30, 133)
    pixel = (255, 0, 0)
    scale_x = 64
    scale_y = 59
    time_y = 61
    step = 180
    image = None

    def __init__(self, image):
        self.image = image

    def __ocr_image(self, image, suffix=''):
        file = '/tmp/ocr_image%s.png' % suffix
        image.save(file)
        string = os.popen('PATH=$PATH:/home/wowo/www/bin && gocr -C \'0123456789--\' -i %s' % file).read()

        return string.replace(' ', '')

    def __get_times(self):
        times = []
        for x in range(self.scale_x, self.x_range[-1]):
            if (0, 0, 0) == self.image.getpixel((x, self.time_y)):
                if len(times) == 0:
                    number = self.image.crop((x - 8, self.time_y - 20, x + 8, self.time_y - 8))
                    times.append((x, datetime.now().replace(hour=int(self.__ocr_image(number)), minute=0)))
                else:
                    times.append((x, (times[-1][1] + timedelta(minutes=self.step))))

        return times

    def __get_scale(self):
        scale = []
        number = self.image.crop((self.scale_x - 27, self.y_range[0] + 20, self.scale_x - 7, self.y_range[-1] + 5))
        numbers = self.__ocr_image(number, 'x').split("\n")

        counter = 0
        for y in range(self.scale_y, self.y_range[-1]):
            if (0, 0, 0) == self.image.getpixel((self.scale_x, y)) and y - 1 not in scale:
                if '' != numbers[counter]:
                    scale.append((y, float(numbers[counter])))
                counter = counter + 1

        return scale

    def read(self):
        temperatures = []
        scale = self.__get_scale()
        times = self.__get_times()
        for x in self.x_range:
            for y in self.y_range:
                if self.pixel == self.image.getpixel((x,y)):
                    prev = None
                    for touple in times:
                        if touple[0] >= x:
                            minutes = round(self.step * (float(x - prev[0]) / float(touple[0] - prev[0])))
                            time = prev[1] + timedelta(minutes=minutes)
                        prev = touple
                    prev = None
                    for touple in scale:
                        if touple[0] >= y and prev:
                            temp = round(prev[1] - abs(touple[1] - prev[1]) * ((float(y - prev[0]) / float(touple[0] - prev[0]))), 1)
                            break
                        prev = touple
                    temperatures.append((time,temp))
                    break

        return temperatures
