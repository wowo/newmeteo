#!/usr/bin/python

from PIL import Image
from datetime import datetime, timedelta
from flask import Flask, render_template, request
from mgram_reader import TemperatureReader
from pymongo import MongoClient
import json
import os
import sys
import urllib
import yaml

app = Flask(__name__)

@app.route('/<int:rows>/<int:cols>')
def fetch(rows, cols):
    start = datetime.now() - timedelta(days=int(request.args.get('days', 2)))
    result = getCollection().find({'date': {'$gte': start}, 'location.rows': rows, 'location.cols': cols}).sort('date', 1)
    print result.count()
    data = [('Data', 'Prognoza')]
    for temperature in result:
        data.append((temperature['date'], float(temperature['temperature'])))

    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
    return json.dumps(data, default=dthandler)


@app.route('/')
def chart():
    return render_template('chart.html')


def store(rows, cols):
    collection = getCollection()
    dates = []
    stats = {'inserted': 0, 'updated': 0, 'removed': 0}
    forecast = getReader(rows, cols).read()
    date = forecast[1][0].replace(minute = ((forecast[1][0].minute / 10) * 10), second=0, microsecond=0)
    stats['removed'] = collection.remove({'date': {'$gte': date}})['n']
    for row in forecast[1:]:
        date = row[0].replace(minute = ((row[0].minute / 10) * 10), second=0, microsecond=0)
        if date not in dates:
            dates.append(date)
            document = {
                'date': date,
                'location': {'rows': rows, 'cols': cols},
                'temperature': round(row[1], 1)
            }
            stats['inserted'] += 1
            collection.save(document)

    return stats


def getReader(rows, cols):
    file = '/tmp/mgram_%d_%d.png' % (rows, cols)
    urllib.urlretrieve('http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=%d&col=%d&lang=pl' % (rows, cols), file)

    return TemperatureReader(Image.open(file, 'r').convert('RGB'))


def getCollection():
    config = getConfig()['database']
    conn = MongoClient(config['host'], config['port'])
    db = conn[config['collection']]
    db.authenticate(config['user'], config['pass'])

    return db.temperatures


def getConfig():
  return yaml.load(file(os.path.dirname(os.path.realpath(__file__)) + '/config.yml'))


if __name__ == "__main__" and len(sys.argv) == 1:
    #app.run(host='0.0.0.0', debug=True)
    app.run(host='91.227.39.112', port=8000, debug=True)
elif sys.argv[1] == '--store':
    stats = store(int(sys.argv[2]), int(sys.argv[3]))
    print '[%s] newmeteo store method, update: %d, insert: %d, removed: %d' % (datetime.now().strftime('%Y-%m-%d %H:%m'), stats['updated'], stats['inserted'], stats['removed'])
