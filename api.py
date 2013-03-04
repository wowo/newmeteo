#!/usr/bin/python

from PIL import Image
from datetime import datetime, timedelta
from flask import Flask, render_template
from mgram_reader import TemperatureReader
import json
import sys
import urllib
import os

app = Flask(__name__)

@app.route('/<int:row>/<int:col>')
def fetch(row, col):
    delta = datetime.now() - timedelta(hours=3)

    file = '/tmp/mgram_%d_%d.png' % (row, col)
    if not os.path.exists(file) or datetime.fromtimestamp(os.path.getmtime(file)) < delta:
        urllib.urlretrieve('http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=%d&col=%d&lang=pl' % (row, col), file)

    reader = TemperatureReader(Image.open(file, 'r').convert('RGB'))

    return json.dumps([['Data', 'Prognoza']] + reader.read(date_as_string=True))

@app.route('/chart')
def chart():
    return render_template('chart.html')

if __name__ == "__main__" and len(sys.argv) == 1:
    #app.run(host='0.0.0.0', debug=True)
    app.run(host='91.227.39.112', port=8000, debug=True)
