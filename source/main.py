from utilities import parseBusStops
from utilities import parseBusRoutes

STOP_TIMES = {
    "01" : {
        "02" : [720, 722, 725, 727, 730, 735, 740, 745],
    },
    "02" : {
        "03" : [720, 723, 725, 726, 731, 736, 740, 745, 748, 753],
        "05" : [725, 727, 728, 731, 738, 740, 745, 749, 753, 760],
    },
    "03" : {
        "04" : [733, 736, 740, 743, 750, 755, 759, 761, 764],
    },
    "04" : {},
    "05" : {
        "06" : [740, 743, 747, 750, 754, 759, 763, 765, 770, 775, 800],
        "07" : [740, 743, 749, 750, 753, 757, 760, 764, 768, 769, 775, 780, 800, 803, 805, 808],
    },
    "06" : {},
    "07" : {},
}

GRAPH = {
    "01" : [("02", 12)],
    "02" : [("03", 6), ("05", 5)],
    "03" : [("04", 7)],
    "04" : [],
    "05" : [("06", 18), ("07", 6)],
    "06" : [],
    "07" : [],
}

total_trip_time = 0

def main():
    global total_trip_time
    passenger_destinations = ["02", "05", "07"]

    # With Time Delay - 725
    recursive_scan("01", 725, passenger_destinations)
    print("Completed all trips by: {}\n".format(total_trip_time))

    # Clean up anything before running again
    print("-----------------------------------------\n")
    total_trip_time = 0
    passenger_destinations = ["02", "05", "07"]

    # Without Time Delay - 720
    recursive_scan("01", 720, passenger_destinations)
    print("Completed all trips by: {}".format(total_trip_time))

    # Parse the stop text file with every bus stop
    print(parseBusStops())

    # Parse the routes text file with every bus route
    print(parseBusRoutes())
    


def recursive_scan(stop_number, current_time, passenger_destinations):
    global total_trip_time
    possible_routes = GRAPH[stop_number]
    destinations = STOP_TIMES[stop_number]
    stop_flag = False

    if stop_number in passenger_destinations:
        stop_flag = True
        passenger_destinations.remove(stop_number)
    
    if len(passenger_destinations) > 0:
        for route in possible_routes:
            print("Checking route from: stop {} to stop {}".format(stop_number, route[0]))
            stop_times = destinations[route[0]]   
            earliest_stop_time = calculate_possible_stop_time(stop_times, current_time)
            print("    Arrive at: {}".format((earliest_stop_time + route[1])))
            recursive_scan(route[0], earliest_stop_time + route[1], passenger_destinations)
        
    if current_time > total_trip_time and stop_flag:
        total_trip_time = current_time


# Basic for now, but could become complex depending on how the OCTranspo API works
def calculate_possible_stop_time(stop_times, current_time):
    for time in stop_times:
        if current_time <= time:
            print("    Depart at: {}".format(time))
            return time
    # We should never reach here, this means we can't catch any busses because the time doesn't match


if __name__ == "__main__":
    main()