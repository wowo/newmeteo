#!/usr/bin/python

from PIL import Image
from flask import Flask
from mgram_reader import TemperatureReader
import json
import sys
import urllib

app = Flask(__name__)

@app.route('/<int:row>/<int:col>')
def fetch(row, col):
    file = '/tmp/mgram_%d_%d.png' % (row, col)
    urllib.urlretrieve('http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=%d&col=%d&lang=pl' % (row, col), file)
    reader = TemperatureReader(Image.open(file, 'r').convert('RGB'))

    return json.dumps(reader.read(date_as_string=True))

if __name__ == "__main__" and len(sys.argv) == 1:
    app.run(host='0.0.0.0', debug=True)
