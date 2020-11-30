# Description: File containing useful tools to facilitate the OCTranspoProblem
# Author: Nicholas Kazan
# Year: 2020

from utilities import parse_trip_names, parse_trip_times, parse_bus_data
from datetime import datetime

# Set up global variables and parse txt files to create dictionaries
times_reaching_destinations = []
visited = []
direction_names = parse_trip_names()
trip_times = parse_trip_times()
bus_data_dictionary = parse_bus_data()


def main():
    global times_reaching_destinations
    global visited

    # Run the program twice with different values to test the difference
    recursive_scan_new("3030", 98, 0, 26400, ["3035", "3227", "3038", "3039"])
    print("\n")
    without_delay = max(times_reaching_destinations)
    times_reaching_destinations = []
    visited = []
    recursive_scan_new("3030", 98, 0, 26520, ["3035", "3227", "3038", "3039"])
    print("\n")
    with_delay = max(times_reaching_destinations)
    print("Ending time WITHOUT delay: {} ----- Ending time WITH delay: {}".format(without_delay, with_delay))


def recursive_scan_new(stop_number, bus_number, direction, current_time, passenger_destinations):
    global visited
    global times_reaching_destinations

    if stop_number in passenger_destinations:
        passenger_destinations.remove(stop_number)
        times_reaching_destinations.append(current_time)
    if len(passenger_destinations) == 0:
        return
    if stop_number in bus_data_dictionary and stop_number not in visited:
        visited.append(stop_number)
        next_stops = bus_data_dictionary[stop_number]

        for stop, options in next_stops.items():
            (new_option, new_current_time) = determine_best_bus(stop_number, bus_number, direction, options, current_time)
            print("Next Stop: {} ----- Next Path: {} ----- New Time: {}".format(stop, new_option, new_current_time))
            recursive_scan_new(stop, new_option[1], new_option[0], (int(new_option[2]) + new_current_time), passenger_destinations)
    return


def determine_best_bus(stop_number, bus_number, direction, options, current_time):
    best = options[0]
    best_time = 0
    flag = True

    # Loop through all potential options to determine the best one
    for option in options:
        bus_choice = option[1]
        if int(option[0]) == int(direction) and int(bus_choice) == int(bus_number):
            return (option, current_time)
        elif bus_choice == bus_number and int(option[0]) != direction and len(options) > 1: 
            continue
        else:
            # This format is how we parsed the txt files
            bus_with_direction = str(bus_choice) + "-" + str(direction)
            if trip_times[stop_number] and trip_times[stop_number][bus_with_direction]:
                for time_index in range(len(trip_times[stop_number][bus_with_direction])):
                    time_for_next_bus = trip_times[stop_number][bus_with_direction][time_index]
                    if trip_times[stop_number][bus_with_direction][time_index] < current_time:
                        # the bus is from the past so we can't take it
                        continue
                    elif time_for_next_bus >= current_time:
                        # we will take this bus as it's the next available one
                        # flag makes sure that we set this the first time with no comparison
                        if flag:
                            flag = False
                            best = option
                            best_time = time_for_next_bus
                        else:
                            if time_for_next_bus < best_time:
                                best_time = time_for_next_bus
                                best = option
            else:
                print("-----ERROR: somehow we're missing a stop and bus in trip_times")    
    # return best option
    return (best, best_time)

if __name__ == "__main__":
    main()