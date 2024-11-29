import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import matplotlib.ticker as mpl_tick
import datetime

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

gesamtErzeugung = []
prozentualeErzeugung = []
jahre = []

data = open('RAW/43311-0002_Steinkohle.csv', 'r')

for zeile in data:
    if zeile.startswith('2'):
        temp = zeile.split(";")                                                     #die Zeile am Zeichen ';' aufsplitten
        if temp[2] == "Insgesamt":
            prozentualeErzeugung.append(int(temp2) / int(temp[3]))
            gesamtErzeugung.append(int(temp[3]))
            jahre.append(datetime.date(int(temp[0]), monthToInt(temp[1]), 1))
        elif temp[2] == "Steinkohlen":
            temp2 = temp[3]

data.close()




fig, ax1 = plt.subplots()

ax1.set_xlabel("Jahr")                                  #x-Achsen name hinzufügen
ax1.set_ylabel("Gesamtenergieproduktion in GW")
ax1.plot(jahre, gesamtErzeugung, '-o')                  #Plot erstellen aus der x-Achse 'jahre' und der y-Achse 'gesamtErzeugung' mit Punkten an Wertestellen

ax1.xaxis.set_major_locator(mpl_dates.YearLocator())
ax1.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y'))    #Datumsformat definiert, siehe https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
ax1.xaxis.set_minor_locator(mpl_dates.MonthLocator())

ax2 = ax1.twinx()

ax2.set_ylabel("Kohlestrom prozentual an Gesamtproduktion", color='tab:red')
ax2.plot(jahre, prozentualeErzeugung, '-or')
ax2.tick_params(axis='y', labelcolor='tab:red')
ax2.yaxis.set_major_formatter(mpl_tick.PercentFormatter(1.0, 0))  #y-Achse von Graph 2 auf Prozent einstellen für Werte von 0 bis 1 mit 0 Stellen nach dem Komma

fig.tight_layout()

plt.gcf().autofmt_xdate()                              #y-Achsen Beschriftung anwinkeln
plt.show()