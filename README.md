newmeteo
========

new.meteo.pl meteograms parser (temperatures) written in Python

It parses new.meteo.pl temperature charts and presents them as a JSON resultset.
mgram_parser.py uses GOCR to adjust scales and PIL library to read pixels from chart.

API uses Flask microframework to expose data through REST API.
