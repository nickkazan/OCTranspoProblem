# Description: File containing useful tools to facilitate the OCTranspoProblem
# Author: Nicholas Kazan
# Year: 2020

from utilities import parse_trip_names, parse_trip_times, parse_bus_data
import datetime
import random

# Set up global variables and parse txt files to create dictionaries
times_reaching_destinations = []
visited = []
direction_names = parse_trip_names()
trip_times = parse_trip_times()
bus_data_dictionary = parse_bus_data()

all_stops = []
for key in bus_data_dictionary.keys():
    all_stops.append(key)

def main():
    global times_reaching_destinations
    global visited

    max_time_wasted = 0
    average_wasted = []

    for index in range(100):
        times_reaching_destinations = []
        visited = []


        destinations = random.sample(all_stops, random.randint(1, 10))
        starting_point = (random.sample(all_stops, 1))[0]

        stop = next(iter(bus_data_dictionary[starting_point]))
        starting_bus = bus_data_dictionary[starting_point][stop][0]

        starting_time = random.randint(20000, 60000)
        delayed_starting_time = random.randint(starting_time, starting_time+360)

        # Run the program twice with different values to test the difference
        recursive_scan_new(starting_point, starting_bus[1], starting_bus[0], starting_time, destinations.copy())
        without_delay = max(times_reaching_destinations)

        times_reaching_destinations = []
        visited = []

        recursive_scan_new(starting_point, starting_bus[1], starting_bus[0], delayed_starting_time, destinations.copy())
        with_delay = max(times_reaching_destinations)

        wasted_this_run = abs(with_delay - without_delay)
        max_time_wasted += wasted_this_run
        average_wasted.append(wasted_this_run)
        print("Ending time WITHOUT delay: {} ----- Ending time WITH delay: {}".format(without_delay, with_delay))

    print(average_wasted)
    average_wasted_per_run = int(sum(average_wasted) / len(average_wasted))

    print("Total time wasted with delays: {}".format(str(datetime.timedelta(seconds=max_time_wasted))))
    print("Average time wasted each run: {}".format(str(datetime.timedelta(seconds=average_wasted_per_run))))
    print()


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
            # print("Next Stop: {} ----- Next Path: {} ----- New Time: {}".format(stop, new_option, new_current_time))
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