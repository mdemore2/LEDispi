# LEDispi
raspi powered LED matrix display

## Modules
Pushbullet: display images or text from pushbullet pushes

FlightRadar24: display flight details within an area of interest

## Config
config.py file required with bounding box details and pushbullet api key
airport code used to determine arriving/departing, can be left blank to display both origin and destination
Example:
pb_key = 'key_here'
bounds = {'tl_y': -180, 'tl_x': -90, 'br_y': 180, 'br_x': 90}
bounds_str = "{},{},{},{}".format(bounds["tl_y"], bounds["br_y"], bounds["tl_x"], bounds["br_x"])
airport_icao = ''

### Entrypoint
python3 app.py

