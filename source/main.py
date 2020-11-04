STOP_TIMES = {
    "01" : [720, 725, 730],
    "02" : [720, 730, 740],
    "03" : [735, 740, 750],
    "04" : [735, 760, 770],
    "05" : [780, 785, 790],
    "06" : [800, 805, 810],
    "06" : [800, 850, 900],
}

GRAPH = {
    "01" : [("02", 5)],
    "02" : [("03", 1), ("05", 2)],
    "03" : [("04", 3)],
    "04" : [],
    "05" : [("06", 2), ("07", 5)],
    "06" : [],
    "07" : [],
}

def main():
    recursive_scan("01", 720)


def recursive_scan(stop_number, current_time):
    possible_routes = GRAPH[stop_number]

    for route in possible_routes:
        stop_times = STOP_TIMES[route[0]]
        earliest_stop_time = calculate_possible_stop_time(stop_times, current_time + route[1])
        recursive_scan(route[0], earliest_stop_time)


#Basic for now, but could become complex depending on how the OCTranspo API works
def calculate_possible_stop_time(stop_times, current_time):
    for time in stop_times:
        if current_time <= time:
            return time
    
    #We should never reach here, this means we can't catch any busses because the time doesn't match




if __name__ == "__main__":
    main()