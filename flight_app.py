import pprint
import pickle
import os
import json

#########################
## Get input from user ##
#########################


##Get all origin cities from user
origins = [input("Please type the first origin city: ")]
nextCity = ""
while True:
    nextCity = input("Type next city or type done if finished adding: ")
    if(nextCity == "done"):
        break
    origins.append(nextCity)

if __name__ == '__main__':
    print(origins)

##Get # of individuals coming from each city
cityTotals = {}
for city in origins:
    val = int(input("How many people are flying from "+city+"?: "))
    cityTotals[city] = val

if __name__ == '__main__':
    print(cityTotals)

##Get personal preferences for each individual
cityVariances = {}
for city in cityTotals:
    tmp = []
    for i in range(cityTotals[city]):
        personPrefs = {}
        print("Person",i+1,"flying from",city,", please answer the following.")

        fare = int(input("What is your max price? Enter a number: "))

        if input("Do you need a nonstop flight? Type T or F: ") == "T":
            direct = True
        else: direct = False

        carriersBanned = input("Do you want to exclude any airlines? Please type a comma seperated list of airlines, or type 'none' to skip: ")
        if carriersBanned == "none":
             carriersBanned = ""
        else: carriersBanned = carriersBanned.split(",")

        tmp.append({"fare":fare, "direct":direct, "carriersBanned":carriersBanned})

    cityVariances[city] = tmp

if __name__ == '__main__':
    pprint.pprint(cityVariances)

##Get group preferences
if input("Is your group looking for only domestic flights? Type T or F: ") == "T":
    groupDomestic = True
else: groupDomestic = False

blockDates = input("Are there any months you do not want this trip to take place? Please type a comma seperated list, or type 'none' to skip: ")
if blockDates == "none":
     blockDates = ""
else: blockDates = blockDates.split(",")

blockDestinations = input("Are there any destinations you do not want? Please type a comma seperated list of cities, or type 'none' to skip: ")
if blockDestinations == "none":
     blockDestinations = ""
else: blockDestinations = blockDestinations.split(",")

groupPrefs = {"groupDomestic":groupDomestic, "blockDates":blockDates, "blockDestinations":blockDestinations}

if __name__ == '__main__':
    pprint.pprint(groupPrefs)

## Save all inputs to a file
if __name__ == '__main__':
    with open("data/cityTotals.json", "w") as write_file:
        json.dump(cityTotals, write_file)
    json.dumps(cityTotals, indent=4)

    with open("data/cityVariances.json", "w") as write_file:
        json.dump(cityVariances, write_file)
    json.dumps(cityVariances, indent=4)

    with open("data/groupPrefs.json", "w") as write_file:
        json.dump(groupPrefs, write_file)
    json.dumps(groupPrefs, indent=4)
