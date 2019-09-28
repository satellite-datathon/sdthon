# Satellite Intelligence Datathon

Satellite Intelligence Datathon run by Melbourne Data Science and sponsored by Growing Data and ANZ.

http://www.datasciencemelbourne.com/datathon/

https://medium.com/satellite-intelligence

Project: Melbourne Datathon 2019, 14th Aug - 29 November. 

Delivery team: Jason Samaradiwakara, Rohit Kaul, Vijay, Eric Kimwatan, Brendan Houng

Date: 9 September 2019

Notes:

- extract phase-02 into data/ such that you have the following dir structure:

|-- data
|   `-- phase-02
|       |-- TileSugarPercent.txt
|       |-- geometries
|       |-- masks
|       |-- metadata
|       `-- sugarcanetiles

The full dir structure is as follows, ignoring json, geojson and png files.

$ tree -I '*.json|*.geojson|*.png'
.
|-- #README.md#
|-- README.md
|-- app
|   |-- public
|   |   |-- favicon.ico
|   |   `-- index.html
|   `-- src
|       |-- App.css
|       |-- App.js
|       |-- App.test.js
|       |-- Crush.js
|       |-- Dashboard.js
|       |-- History.js
|       |-- Main.js
|       |-- Price.js
|       |-- index.css
|       |-- index.js
|       |-- logo.svg
|       `-- registerServiceWorker.js
|-- code
|   |-- 0_external
|   |-- 1_raw
|   |   |-- demo.py
|   |   |-- image_hist.py
|   |   |-- ndvi.ipynb
|   |   |-- ndvi_calculation.py
|   |   `-- read_json.py
|   |-- 2_processed
|   |-- 3_models
|   |-- 4_analysis
|   |-- 5_tmp
|-- data
|   `-- phase-02
|       |-- TileSugarPercent.txt
|       |-- geometries
|       |-- masks
|       |-- metadata
|       `-- sugarcanetiles
|-- phase-01
|   |-- data
|   |   |-- harvested
|   |   `-- sentinel-2a-tile-7680x-10240y
|   |       |-- geometry
|   |       |-- masks
|   |       |-- metadata
|   |       `-- timeseries
|   |-- demo.py
|   |-- guide.pdf
|   |-- harvest_code.py
|   |-- readme.md
|   `-- requirements.txt
`-- tmp
    |-- readme.txt
    |-- weekly_crushing_2018.csv
    `-- weekly_crushing_2019.csv
