from FlightRadar24.api import FlightRadar24API
from config import bounds_str


class frAPI:
    def __init__(self):
        self.fr = FlightRadar24API()
        self.bounds = bounds_str

    def ret_flights(self):
        flights = self.fr.get_flights(bounds=self.bounds)
        return flights

    def get_flight_details(self, flights):
        for flight in flights:
            details = self.fr.get_flight_details(flight.id)
            flight.set_flight_details(details)
        return flights
