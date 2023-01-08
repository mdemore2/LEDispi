from src.flights import Flights
from src.messages import Messages

if __name__ == "__main__":
    fr = Flights()
    flights = fr.get_flights()
    print(flights)
    for flight in flights:
        print(flight.origin_airport_name)
        print(flight.airline_short_name)
        print(flight.number)
        print(flight.aircraft_model)
        print(flight.altitude)
        print(flight.registration)

    # TODO: make image
    # base size 1530x720px
    # arrivals or departures img centered across top
    # text below with following headers in order
    # ORIGIN:
    # AIRLINE:
    # FLIGHT #:
    # AIRCRAFT:
    # REGISTRATION:
    # ALTITUDE:

    msgs = Messages()
    info = msgs.get_messages()
    print(info)
