STOP_TIMES = {
    "01" : {
        "02" : [720, 725, 730, 735, 740, 745],
    },
    "02" : {
        "03" : [720, 725, 730, 740, 750, 800],
        "05" : [725, 735, 745, 755, 765],
    },
    "03" : {
        "04" : [740, 750, 760, 770],
    },
    "04" : {},
    "05" : {
        "06" : [745, 750, 755, 765, 775, 800, 830],
        "07" : [745, 750, 755, 770, 780, 800, 815, 830],
    },
    "06" : {},
    "07" : {},
}

GRAPH = {
    "01" : [("02", 15)],
    "02" : [("03", 10), ("05", 5)],
    "03" : [("04", 8)],
    "04" : [],
    "05" : [("06", 20), ("07", 15)],
    "06" : [],
    "07" : [],
}

total_trip_time = 0

def main():
    global total_trip_time

    # With Time Delay - 725
    recursive_scan("01", 725)
    print("Completed all trips by: {}".format(total_trip_time))

    total_trip_time = 0
    # Without Time Delay - 720
    recursive_scan("01", 720)
    print("Completed all trips by: {}".format(total_trip_time))


def recursive_scan(stop_number, current_time):
    global total_trip_time
    possible_routes = GRAPH[stop_number]
    destinations = STOP_TIMES[stop_number]
    
    for route in possible_routes:
        print("Checking route from: stop {} to stop {}".format(stop_number, route[0]))
        stop_times = destinations[route[0]]   
        earliest_stop_time = calculate_possible_stop_time(stop_times, current_time)
        print("    Arrive at: {}".format((earliest_stop_time + route[1])))
        recursive_scan(route[0], earliest_stop_time + route[1])
    
    if current_time > total_trip_time:
        total_trip_time = current_time


#Basic for now, but could become complex depending on how the OCTranspo API works
def calculate_possible_stop_time(stop_times, current_time):
    for time in stop_times:
        if current_time <= time:
            print("    Depart at: {}".format(time))
            return time
    #We should never reach here, this means we can't catch any busses because the time doesn't match


if __name__ == "__main__":
    main()