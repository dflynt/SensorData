import json
import pandas
import time
import numpy
import matplotlib
import matplotlib.pyplot as plt
from pprint import pprint

memoryList = []
compassList = []
GPSList = []
AccelList = []
GyroList = []
MagnetList = []

def calcTripleAvg(valList):
    sumx = 0.0
    sumy = 0.0
    sumz= 0.0
    for x in range(0, len(valList)):
        sumx = sumx + float(valList[x][0])
        sumy = sumy + float(valList[x][1])
        sumz = sumz + float(valList[x][2])
    avgx = sumx / len(valList)
    avgy = sumy / len(valList)
    avgz = sumz / len(valList)
    return [str(avgx)[:5], str(avgy)[:5], str(avgz)[:5]]

    
def parseMemory(slot, index):
    #This type of access is due to the layout of the json file
    #The iOS app created the json file  in an ugly, nested way like this
    value = str(data['entries'][index]['data'][3]['displayValue']).split(" ")
    value = float(value[0])
    memoryList.append(value)
    
def parseCompass(slot, index):
    #[:6] slices the string number and takes the first 6 characters
    direction = str(data['entries'][i]['data'][0]['displayValue'][:6])
    compassList.append(float(direction))

def parseGPS(slot, index):
    location = [str(data['entries'][index]['data'][2]['displayValue'][:5]), 
                str(data['entries'][index]['data'][3]['displayValue'])[:5],
                str(data['entries'][index]['data'][4]['displayValue'])[:5]]
    GPSList.append(location)

def parseAccel_Gyro_Magneto(slot, index):
    xyzVals = [str(data['entries'][index]['data'][0]['displayValue'][:5]),
               str(data['entries'][index]['data'][1]['displayValue'][:5]),
               str(data['entries'][index]['data'][2]['displayValue'][:5])]
    
    if data['entries'][i]['dataSource'] == "Acceleration (total)":
        AccelList.append(xyzVals)
    elif data['entries'][i]['dataSource'] == "Gyrometer (smooth)":
        GyroList.append(xyzVals)
    else:
        MagnetList.append(xyzVals)
        
with open("data.json") as json_data:
    data = json.load(json_data)
    for i in range(0, len(data['entries'])):
        if data['entries'][i]['dataSource'] == "Memory":
            parseMemory(data['entries'][i], i)

        elif data['entries'][i]['dataSource'] == "Compass":
            parseCompass(data['entries'][i], i)

        elif data['entries'][i]['dataSource'] == "GPS":
            parseGPS(data['entries'][i], i)

        elif data['entries'][i]['dataSource'] == "Acceleration (total)":
            parseAccel_Gyro_Magneto(data['entries'][i], i)

        elif data['entries'][i]['dataSource'] == "Gyrometer (smooth)":
            parseAccel_Gyro_Magneto(data['entries'][i], i)

        elif data['entries'][i]['dataSource'] == "Magnetometer (corrected for device)":
            parseAccel_Gyro_Magneto(data['entries'][i], i)

import pandas as pd
plot_df = pd.DataFrame({'Memory Usage': memoryList})
plot_df.plot(kind='line')

compass_df = pd.DataFrame({"Compass Direction": compassList})
compass_df.plot(kind='hist')

print("Average GPS position:", end = " ")
print(" ".join(calcTripleAvg(GPSList)))
print("Average Acceleration:", end = " ")
print(" ".join(calcTripleAvg(AccelList)))
print("Average Gyrometer placement:", end = " ")
print(" ".join(calcTripleAvg(GyroList)))
print("Average Magnetometer reading:", end = " ")
print(" ".join(calcTripleAvg(MagnetList)))

