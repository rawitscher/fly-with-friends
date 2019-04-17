##################################################
### Get all flight matches from valid airports ###
##################################################

def price(max, l):
    keyVal = max
    return [d for d in l if d["MinPrice"] < keyVal]

def direct(l):
    return [d for d in l if d["Direct"] == True]

def airlineBan(m, l):
    return [d for d in l if d["OutboundLeg"]['CarrierIds'] not in m]

def destination_intersect(m, l):
    return [d for d in l if d["CityId"] in m]
