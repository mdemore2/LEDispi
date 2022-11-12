from flights import frAPI

if __name__ == "__main__":
    fr = frAPI()
    flights = fr.ret_flights()
    print(flights)
    flights = fr.get_flight_details(flights)
    for flight in flights:
        print(flight.origin_airport_name)
