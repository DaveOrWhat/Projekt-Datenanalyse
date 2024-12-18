import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import matplotlib.ticker as mpl_tick
import datetime
from statistics import mean, median, mode, multimode
import numpy as np
import pandas as pd

#Funktion um einen Monat als String in einen Integer Wert umzuwandeln
def monthToInt(month):
    match month:
        case "Januar":
            return 1
        case "Februar":
            return 2
        case "März":
            return 3
        case "April":
            return 4
        case "Mai":
            return 5
        case "Juni":
            return 6
        case "Juli":
            return 7
        case "August":
            return 8
        case "September":
            return 9
        case "Oktober":
            return 10
        case "November":
            return 11
        case "Dezember":
            return 12
        

def abweichungMedian(data):     # gibt die mittlere Abweichung vom Median zurück
    median = median(data)
    for i in data:
        returnValue += abs(i - median)
    return returnValue / len(data)

def quartile(data):             # gibt die 25% 50% und 75% quartile zurück
    data.sort()
    lenght = len(data)
    quart1 = int(lenght / 4)
    quart2 = int(lenght / 2)
    quart3 = int(lenght * 0.75)
    return [data[quart1], data[quart2], data[quart3]]

def dezile(data):               # gibt alle 9 Dezile zurück
    length = len(data)
    returnValue = []
    i = 0.1
    while i < 1:
        returnValue.append(data[int(length * i)])
        i += 0.1
    return returnValue

def variationsKoeffizient(data):
    return np.std(data) / mean(data)

def korrelationsKoeffizient(data, data2):
    return np.cov(data, data2) / (np.std(data) * np.std(data2))

# statistic Funktionen https://www.python4data.science/de/latest/workspace/pandas/descriptive-statistics.html

# bestimmen des Modus durch mode() wenn nur der erste Modus bestimmt werden soll, multimode() wenn eine Liste aller Modus bestimmt werden soll    
# berechenn des Median durch median()
# berechnen des Mittelwerts durch mean()
    

steinkohleErzeugung = []        #monatliche Erzeugung von Steinkohlestrom
gesamtErzeugung = []            #monatliche Gesamtproduktion an Strom
prozentualeErzeugung = []       #prozentuale Erzeugung von Steinkohlestrom an der Gesamtproduktion pro Monat
jahre = []

data = open('RAW/43311-0002_Steinkohle.csv', 'r')

for zeile in data:
    if zeile.startswith('2'):
        temp = zeile.split(";")                                                     #die Zeile am Zeichen ';' aufsplitten
        if temp[2] == "Insgesamt":
            gesamtErzeugung.append(int(temp[3]))
            jahre.append(datetime.date(int(temp[0]), monthToInt(temp[1]), 1))
        elif temp[2] == "Steinkohlen":
            steinkohleErzeugung.append(int(temp[3]))
            
i = 0
while i < len(steinkohleErzeugung):
    prozentualeErzeugung.append(int(steinkohleErzeugung[i]) / int(gesamtErzeugung[i]))
    i += 1

data.close()




fig, ax1 = plt.subplots()

ax1.set_xlabel("Jahr")                                  #x-Achsen Name hinzufügen
ax1.set_ylabel("Gesamtenergieproduktion in GW")
ax1.plot(jahre, steinkohleErzeugung, '-ob', label='Steinkohlestrom')
ax1.plot(jahre, gesamtErzeugung, '-og', label='Gesamtstrom')

plt.legend(loc="upper right")

ax1.xaxis.set_major_locator(mpl_dates.YearLocator())
ax1.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y'))    #Datumsformat definiert, siehe https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
ax1.xaxis.set_minor_locator(mpl_dates.MonthLocator())

ax2 = ax1.twinx()

ax2.set_ylabel("Kohlestrom prozentual an Gesamtproduktion", color='tab:red')
ax2.plot(jahre, prozentualeErzeugung, '-or', label='Kohlestrom prozentual an Gesamtproduktion')
ax2.tick_params(axis='y', labelcolor='tab:red')
ax2.yaxis.set_major_formatter(mpl_tick.PercentFormatter(1.0, 0))  #y-Achse von Graph 2 auf Prozent einstellen für Werte von 0 bis 1 mit 0 Stellen nach dem Komma


plt.legend()

fig.tight_layout()

plt.gcf().autofmt_xdate()                              #x-Achsen Beschriftung anwinkeln
plt.show()