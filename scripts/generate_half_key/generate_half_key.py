from random import randint
import math
import csv

isFull = False

DevID = set()
DevKey = list()
DevKey.append("Data448ID")

while isFull == False:
    randomID = randint(1000000, 9999999)

    DevID.add(randomID)

    if len(DevID) == 161:
        isFull = True

for id in DevID:
    DevKey.append(str(id))

with open("HalfKey.csv", "w") as f:
    writer = csv.writer(f, lineterminator='\n')
    for id in DevKey:
        writer.writerow([id])
f.close()
