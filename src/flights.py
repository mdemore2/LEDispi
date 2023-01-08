from FlightRadar24.api import FlightRadar24API
from src.config import bounds_str


class Flights:
    def __init__(self):
        self._fr = FlightRadar24API()
        self._bounds = bounds_str

    def get_flights(self):
        flights = self._fr.get_flights(bounds=self._bounds)
        for flight in flights:
            details = self._fr.get_flight_details(flight.id)
            flight.set_flight_details(details)
        return flights

