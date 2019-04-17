import json
import os
from do_get_flights import get_flight_info
import pprint
import filter_utils as uts

## Print function to check filter status throughout program
def printAll(q, title):
    print("")
    print("Stage: "+title)
    for city in q:
        if len(q[city]) < 5:
            for person in range(len(q[city])):
                print("Length of "+city+" "+str(person)+": "+str(len(q[city][person])))
        else: print("Length of "+city+": "+str(len(q[city])))

## Get all user input via individual JSON files
## either from direct terminal input or web interface
with open("data/cityTotals.json", "r") as read_file:
    if os.stat("data/cityTotals.json").st_size == 0:
        "Please update flight preferences online or type 'python3 flight_app.py' into the terminal"
    else: cityTotals = json.load(read_file)
    read_file.close()

with open("data/cityVariances.json", "r") as read_file:
    if os.stat("data/cityVariances.json").st_size == 0:
        "Please update flight preferences online or type 'python3 flight_app.py' into the terminal"
    else: cityVariances = json.load(read_file)
    read_file.close()


with open("data/groupPrefs.json", "r") as read_file:
    if os.stat("data/groupPrefs.json").st_size == 0:
        "Please update flight preferences online or type 'python3 flight_app.py' into the terminal"
    else: groupPrefs = json.load(read_file)
    read_file.close()

## Get flight info for relevant cities
Quotes = {}
Carriers = {}
Places = {}
for city in cityTotals:
    Quotes[city], Carriers[city], Places[city] = get_flight_info(city)

if __name__ == '__main__':
    printAll(Quotes, "Raw data obtained")

## Convert Carriers dict list to flat dict of Carrier :: id
for city in Carriers:
    tmp = Carriers[city]
    Carriers[city] = {}
    for carrier in range(len(tmp)-1):
        key = tmp[carrier]["Name"]
        Carriers[city][key] = tmp[carrier]["CarrierId"]

## Create dict of place id :: city id to add city to each quote
CityidDict = {}
for city in Places:
    curr = Places[city]
    CityidDict[city] = {}
    for place in curr:
        if "CityId" in place:
            key = place["PlaceId"]
            CityidDict[city][key] = place["CityId"]

## Add city id to all flight responses
for city in Quotes:
    for quote in Quotes[city]:
        dest = quote["OutboundLeg"]["DestinationId"]
        quote["CityId"] = CityidDict[city][dest]

if __name__ == '__main__':
    printAll(Quotes, "City Id's added")

## Create seperate flight list for each individual per city
for city in Quotes:
    tmp = Quotes[city]
    Quotes[city] = []
    for i in range(cityTotals[city]):
        Quotes[city].append(tmp)

if __name__ == '__main__':
    printAll(Quotes, "Individual lists created")

## Filter each flight list by the individual using city variances
if __name__ == '__main__':
    print("")
    print("Applying individual filters...")

for city in Quotes:
    for person in range(cityTotals[city]):
        flights = Quotes[city][person]
        prefs = cityVariances[city][person]

        # Remove flights that are too expensive
        flights = uts.price(prefs["fare"],flights)
        if __name__ == '__main__':
            print("Flights over $"+str(prefs["fare"])+" have been removed from "+city+" "+str(person))

        # Remove stopovers if direct only is indicated
        if prefs["direct"]:
            flights = uts.direct(flights)
            if __name__ == '__main__':
                print("Stopover flights have been removed from "+city+" "+str(person))

        Quotes[city][person] = flights

        # Remove banned airlines if any are included
        if prefs["carriersBanned"]:
            m = []
            for carrier in prefs["carriersBanned"]:
                if carrier in Carriers[city]:
                    m.append(Carriers[city][carrier])
            flights = uts.airlineBan(m,flights)
            if __name__ == '__main__':
                print(str(prefs["carriersBanned"])+ " airlines have been removed from "+city+" "+str(person))

if __name__ == '__main__':
    printAll(Quotes, "Individual filters applied")

## Get unique destinations (or any not shared by all flight lists)
if __name__ == '__main__':
    print("")
    print("Applying group filters...")

d = []
for city in Quotes:
    for l in Quotes[city]:
        m = list(set([d["CityId"] for d in l]))
        d.append(m)

## Get overlapped destinations from unique sets and filter individual lists accordingly
overlap = set(d[0])
for s in d[1:]:
    overlap.intersection_update(s)

if __name__ == '__main__':
    print("Overlapping destinations include: ")
    print(overlap)
for city in Quotes:
    curr = Quotes[city]
    for person in range(len(curr)):
        Quotes[city][person] = uts.destination_intersect(overlap,curr[person])

if __name__ == '__main__':
    printAll(Quotes, "Group filters applied")
    #pprint.pprint(Quotes)
