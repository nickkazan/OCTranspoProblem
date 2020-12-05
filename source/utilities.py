# Description: File containing useful tools to facilitate the OCTranspoProblem
# Author: Nicholas Kazan
# Year: 2020

import json
import os


def parse_trip_times():
    accepted_busses = ["98", "97", "99", "44"]
    accepted_day = "SEPT20-SEPDA20-Weekday-11"
    stop_conversion_dict = {}
    flag = True

    with open("../google_transit/stops.txt", "r") as stop_file:
        for stop in stop_file:
            if flag:
                flag = False
                continue
            stop_data = stop.split(",")
            stop_id = stop_data[0]
            stop_number = stop_data[1]
            stop_conversion_dict[stop_id] = stop_number

    trip_conversion_dict = {}
    flag = True
    with open("../google_transit/trips.txt", "r") as trip_file:
        for trip in trip_file:
            if flag:
                flag = False
                continue
            trip_data = trip.split(",")
            if trip_data[1] == accepted_day:
                if trip_data[0].split("-")[0] in accepted_busses:
                    trip_conversion_dict[trip_data[2]] = trip_data[0].split("-")[0] + "-" + trip_data[4]
                else:
                    continue
            else:
                continue

    final_dict = {}
    flag = True
    with open("../google_transit/stop_times.txt", "r") as times_file:
        for time in times_file:
            if flag:
                flag = False
                continue
            time_data = time.split(",")
            if time_data[0] in trip_conversion_dict:
                if stop_conversion_dict[time_data[3]] in final_dict:
                    trip_time = time_data[1].split(":")
                    trip_seconds = ((int(trip_time[0]) * 60 * 60) + (int(trip_time[1]) * 60))
                    if trip_conversion_dict[time_data[0]] in final_dict[stop_conversion_dict[time_data[3]]]:
                        final_dict[stop_conversion_dict[time_data[3]]][trip_conversion_dict[time_data[0]]].append(trip_seconds)
                    else:
                        final_dict[stop_conversion_dict[time_data[3]]][trip_conversion_dict[time_data[0]]] = [trip_seconds]
                else:
                    final_dict[stop_conversion_dict[time_data[3]]] = {}
            else:
                # not in the list of trips
                continue
    for stop in final_dict.keys():
        for times in final_dict[stop].values():
            times.sort()
    return final_dict


def parse_trip_names():
    trip_dict = {}
    flag = True
    with open("../google_transit/trips.txt", "r") as trip_file:
        for trip in trip_file:
            if flag:
                flag = False
                continue
            trip_data = trip.split(",")
            bus = (trip_data[0].split("-"))[0]
            direction = trip_data[4]
            if (bus + "-" + direction) in trip_dict:
                continue
            else:
                trip_dict[bus + "-" + direction] = trip_data[3]
    return trip_dict


def parse_bus_data():
    bus_data = {}
    flag = True
    with open("./bus_data.txt", "r") as bus_file:
        for stop_info in bus_file:
            if flag:
                flag = False
                continue
            stop_time_data = stop_info.split(",")

            if stop_time_data[0] in bus_data:
                if stop_time_data[1] in bus_data[stop_time_data[0]]:
                    (bus_data[stop_time_data[0]])[stop_time_data[1]].append((stop_time_data[3], stop_time_data[2],stop_time_data[4]))
                else:
                    (bus_data[stop_time_data[0]])[stop_time_data[1]] = [(stop_time_data[3], stop_time_data[2],stop_time_data[4])]
            else:
                bus_data[stop_time_data[0]] = {}
                bus_data[stop_time_data[0]][stop_time_data[1]] = [(stop_time_data[3], stop_time_data[2],stop_time_data[4])]
    return bus_data


# def get_next_bus(stop_number, bus_number, direction_name, current_time_in_seconds):
#     if ('APP_ID' not in os.environ or 'API_KEY' not in os.environ):
#         print("Error with env variables")
#         return
#     print("Checking stop number: {} --- with bus number: {}".format(stop_number, bus_number))
#     url = "https://api.octranspo1.com/v2.0/GetNextTripsForStop?appID={}&apiKey={}&stopNo={}&routeNo={}&format={}".format(os.environ['APP_ID'], os.environ['API_KEY'], stop_number, bus_number, "json")
#     response = requests.post(url)
#     response_string = response.json()
#     next_bus_time = -1
#     if response_string["GetNextTripsForStopResult"] and response_string["GetNextTripsForStopResult"]["Route"] and response_string["GetNextTripsForStopResult"]["Route"]["RouteDirection"]:
#         routes = response_string["GetNextTripsForStopResult"]["Route"]["RouteDirection"]
#         for route in routes:
#             if route["RouteLabel"] == direction_name:
#                 for trip in route["Trips"]["Trip"]:
#                     trip_time = trip["TripStartTime"].split(":")
#                     trip_seconds = ((int(trip_time[0]) * 60 * 60) + (int(trip_time[1]) * 60))
#                     if trip_seconds >= current_time_in_seconds:
#                         next_bus_time = trip_seconds
#                         return next_bus_time
#                     else:
#                         # We must have just missed the bus so we can't connect to it
#                         continue

#     return next_bus_time
