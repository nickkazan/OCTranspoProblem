# File containing useful tools to facilitate the OCTranspoProblem

def parseBusStops():
    list_of_stops = set()
    counter = 0
    with open("../google_transit/stops.txt", "r") as stop_file:
        for stop in stop_file:
            counter += 1
            if counter == 1:
                continue
            elif counter > 10:
                break
            stop_data = stop.split(",")
            stop_number = stop_data[1]
            list_of_stops.add(stop_number)
    return list_of_stops


def parseBusRoutes():
    routes_dict = {}
    route_counter = 0
    with open("../google_transit/routes.txt", "r") as route_file:
        for route in route_file:
            route_counter += 1
            if route_counter == 1:
                continue
            elif route_counter > 20:
                break
            route_data = route.split(",")
            routes_dict[route_data[1]] = []
    return routes_dict