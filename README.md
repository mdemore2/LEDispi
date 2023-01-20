# LEDispi: **RaspberryPi powered LED matrix display**

Developed using a Pi Zero W

## Modules

- Pushbullet: display images or text from pushbullet pushes

- FlightRadar24: display flight details within an area of interest

## Config

config.py file required with:

- bounding box (for flight radar querying)
- pushbullet api key
- airport code (to determine arriving/departing, can be left blank to display all flight details)

**Example:**

```python
pb_key = 'key_here'  # TODO: replace with your pushbullet key
bounds = {'tl_y': -180, 'tl_x': -90, 'br_y': 180, 'br_x': 90}  # TODO: replace with desired bbox
bounds_str = "{},{},{},{}".format(bounds["tl_y"], bounds["br_y"], bounds["tl_x"], bounds["br_x"])
airport_icao = ''  # TODO: replace with desired airport ICAO
```

## Entrypoint

To run, execute:
`python3 app.py`
