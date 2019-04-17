import os
import re
import pickle

f = open("key_values.txt","r")
data = f.read()
f.close()

pattern = re.compile("([\-/& \w,\(\)\.–'•—]+)", re.UNICODE)
match = pattern.findall(data)
iataDict = dict(zip(match[3::5],match[0::5]))

print(iataDict["San Francisco"])

l = open("data/cityDict.pkl","wb")
pickle.dump(iataDict,l)
l.close()
