import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import matplotlib.ticker as mpl_tick
from statistics import mean, median, mode, multimode
import numpy as np
import csv
from scipy.optimize import curve_fit



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
        case _:
            return -1
        
def intToMonth(month):
    match month:
        case 1:
            return "Januar"
        case 2:
            return "Februar"
        case 3:
            return "März"
        case 4:
            return "April"
        case 5:
            return "Mai"
        case 6:
            return "Juni"
        case 7:
            return "Juli"
        case 8:
            return "August"
        case 9:
            return "September"
        case 10:
            return "Oktober"
        case 11:
            return "November"
        case 12:
            return "Dezember"
        case _:
            return -1

def abweichungMedian(data):     # gibt die mittlere Abweichung vom Median zurück
    medianValue = median(data)
    returnValue = 0
    for i in data:
        returnValue += abs(i - medianValue)
    return returnValue / len(data)

def quartile(data):             # gibt die 25% 50% und 75% quartile zurück
    array = data
    array.sort()
    lenght = len(data)
    return [array[int(lenght / 4)], array[int(lenght / 2)], array[int(lenght * 0.75)], array[lenght - 1]]

def dezile(data):               # gibt alle 9 Dezile zurück
    length = len(data)
    array = data
    array.sort()
    returnValue = []
    i = 0.1
    while i < 1:
        returnValue.append(array[int(length * i)])
        i += 0.1
    return returnValue

def variationsKoeffizient(data):
    return np.std(data) / mean(data)

def korrelationsKoeffizient(data, data2):
    return np.cov(data, data2) / (np.std(data) * np.std(data2))

def readFromDataToArray(data, array, dataSet):     #diese Funktion ist speziell auf die jeweiligen Datensätze angepasst
    i = 0
    if dataSet == 1:
        for zeile in data:
            if i > 1:
                temp = zeile.split(",")
                array.append([int(temp[0]), monthToInt(temp[1]), int(temp[3])])
            i += 1
    elif dataSet == 2:
        for zeile in data:
            if i > 1:
                temp = zeile.split(",")
                try:    #falls das Jahr nicht in ein int Wert gewandelt wird, wird das Jahr auf 0 gesetzt
                    jahr = int(temp[0])
                except ValueError:
                    jahr = 0
                try:    #falls der Wert nicht in ein float konvertiert werden kann, wird dieser auf 0 gesetzt
                    wert = float(temp[2])
                except ValueError:
                    wert = 0.0
                if wert != wert:    #überprüft ob bei der konvertierung 'nan' herausgekommen ist, wenn ja wird Wert auf 0 gesetzt
                    wert = 0.0
                array.append([jahr, monthToInt(temp[1]), wert])
            i += 1
    elif dataSet == 3:
        for zeile in data:
            temp = zeile.split(",")
            array.append([temp[0], int(temp[1]), monthToInt(temp[2].replace("\n", ""))])
    elif dataSet == 31:
        for zeile in data:
            if i > 1:
                temp = zeile.split(",")
                array.append([temp[0], int(temp[1]), int(temp[2])])
            i += 1
    elif dataSet == 4:
        for zeile in data:
            if i > 0:
                temp = zeile.split(",")
                array.append([float(temp[0]), float(temp[1])])
            i += 1
    return array

def clean(array):   #diese Funktion ist speziell auf den Datensatz 2 abgestimmt
    i = 0
    length = len(array)
    while i < length:
        if ((array[i][0] > 2100) or (array[i][0] < 1900)):  #falls die Jahreszahl nicht zwischen 1900 und 2100 liegt, wird diese aus den benachbarten Werten ermittelt
            if array[i - 1][0] == array[i - 2][0]:
                array[i][0] = array[i + 1][0]
            else:
                array[i][0] = array[i - 1][0]
        if array[i][1] == -1:   #falls es keine gültige Monatsangabe ist, wird diese aus den benachbarten Werten ermittelt
            if array[i - 1][1] == 12:
                array[i][1] = 1
            else:
                array[i][1] = 12
        if array[i][2] == 0.0: #falls es kein gültiger Datenpunkt ist, wird der zeitlich naheliegenste Wert angenommen
            if array[i][1] == 1:
                array[i][2] = array[i - 1][2]
            else:
                array[i][2] = array[i + 1][2]
        i += 1
        
def outputToFile(fileName, array, beschreibung):
    i = 0
    beschreibungEinzeln = beschreibung.split(";")
    file = open(fileName, 'w')
    file.write("")
    file.close()
    file = open(fileName, 'a')
    while i < len(array[0]):
        temp = []
        for content in array:
            temp.append(content[i])
        
        file.write("%s\nModus: %d\narithmetischer Mittelwert: %.3f\nMedian: %.3f\nSpannweite: %d\nMittlere Abweichung vom Median: %.3f\nStichprobenvarianz: %.3f\nVariationskoeffizient: %.3f\nKovarianz: %.3f\n" % (beschreibungEinzeln[i], mode(temp), np.mean(temp), np.median(temp), max(temp) - min(temp), abweichungMedian(temp), np.var(temp), variationsKoeffizient(temp), np.cov(temp)))
        quartiles = quartile(temp)
        file.write("Quartilsabstand: %d" % (quartiles[2] - quartiles[0]))
        file.write("\nQuartile: ")
        intTemp = 1
        for data in quartiles:
            file.write("q%d: %d, " % (intTemp * 25, data))
            intTemp += 1
        file.write("\nDezile: ")
        intTemp = 1
        for data in dezile(temp):
            file.write("d%d: %d, " % (intTemp, data))
            intTemp += 1
        file.write("\n\n\n")
        i += 1
    file.close()
            
    
def boxWhiskerPlot(filePath, fileName, data, yLabel):
    i = 0
    while i < len(data[0]):
        temp = []
        newfileName = filePath
        newfileName += fileName[i] 
        newfileName += '.jpg'
        for content in data:
            if (i > 1) and ((filePath == 'output/dataset-1/boxWhiskerPlot-') or (filePath == 'output/dataset-3/boxWhiskerPlot-')):
                temp.append(content[i] / 1000000)
            else:
                temp.append(content[i])
        plt.boxplot(temp)
        plt.title(fileName[i])
        plt.ylabel(yLabel[i])
        plt.savefig(newfileName, dpi = 5000)
        plt.show()
        i += 1
    #boxWhiskerPlot('output/dataset-1/boxWhiskerPlot-', ['Jahr-', 'Monat-', 'Elektrizizaetserzeugung-'], data1Array)
        
def scatterPlot(fileName, data, title, yLabel):
    time = []
    value = []
    if len(data[0]) > 3:
        value2 = []
    for content in data:
        time.append(content[0] + (content[1] / 12))
        if fileName != 'output/dataset-2/scatterPlot.jpg':
            value.append(content[2] / 1000000)
        else:
            value.append(content[2])
        if len(data[0]) > 3:
            value2.append(content[3] / 1000000)

    plt.scatter(time, value, color = 'blue', label = 'Ankuenfte')
    if len(data[0]) > 3:
        plt.scatter(time, value2, color = 'red', label = 'Uebernachtungen')
        
        #Curvefitting
        # Initial guess for the parameters [A, B, C, D]
        initial_guess = [4, 6.99, -1991, 7]
        
        # Perform the curve fitting
        params, covariance = curve_fit(sine_function, time, value, p0=initial_guess)

        # Extract the fitted parameters
        A_fit, B_fit, C_fit, D_fit = params
        
        print(f"Fitted parameters: A={A_fit}, B={B_fit}, C={C_fit}, D={D_fit}")
        # Generate y values using the fitted parameters
        new_y = []
        for l in time:
            new_y.append(sine_function(l, A_fit, B_fit, C_fit, D_fit))
        
        label1 = ("Curvefit mit: %.3f * sin(%.3f * x + %.3f) + %.3f" % (A_fit, B_fit, C_fit, D_fit))
        plt.plot(time, new_y, color = 'orange', label = label1)
        
        # Initial guess for the parameters [A, B, C, D]
        initial_guess = [-12, 6.74, -1992, 28]
        
        # Perform the curve fitting
        params, covariance = curve_fit(sine_function, time, value2, p0=initial_guess)
        
        # Extract the fitted parameters
        A_fit, B_fit, C_fit, D_fit = params
        
        print(f"Fitted parameters: A={A_fit}, B={B_fit}, C={C_fit}, D={D_fit}")
        # Generate y values using the fitted parameters
        
        new_y2 = []
        for l in time:
            new_y2.append(sine_function(l, A_fit, B_fit, C_fit, D_fit))
        label2 = ("Curvefit mit: %.3f * sin(%.3f * x + %.3f) + %.3f" % (A_fit, B_fit, C_fit, D_fit))
        plt.plot(time, new_y2, color = 'green', label = label2)
        
        plt.legend(['Ankuenfte', 'Uebernachtungen'])#, loc = 'upper center', bbox_to_anchor = (0.5, -0.1), ncol = 2)
        plt.legend(['Ankuenfte', 'Uebernachtungen', label1, label2], loc = 'upper center', bbox_to_anchor = (1.5, 0.7), ncol = 1)
        
    plt.title(title)
        
    
    plt.xlabel('Jahr')
    plt.xlim(min(time) - 1, max(time) + 1)
    
    plt.ylabel(yLabel)
    #plt.ylim(min(value) * 0.8 , max(value) * 1.1)
    plt.savefig(fileName, bbox_inches = 'tight', dpi = 5000)
    plt.show()
    
    if fileName == 'output/dataset-2/scatterPlot.jpg':
        plt.plot(time, value, color = 'blue', label = 'Beschaeftigte')
        plt.title(title)
        plt.xlabel('Jahr')
        plt.xlim(min(time) - 1, max(time) + 1)
        plt.ylabel(yLabel)
        plt.savefig(fileName[:-15] + 'linePlot.jpg', dpi = 5000)
        plt.show()
        
#scatterPlot('output/dataset-3/scatterPlot.jpg', data3Array)
        
def urlist(filePath, data, fileName):
    i = 0
    while i < len(data[0]):
        newfileName = filePath
        newfileName += fileName[i]
        newfileName += '.csv'
        with open(newfileName, 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow([fileName[i]])
            for content in data:
                writer.writerow([str(content[i])])
        i += 1
        
def ranglist(filePath, data, fileName):
    i = 0
    while i < len(data[0]):
        newfileName = filePath
        newfileName += fileName[i]
        newfileName += '.csv'
        with open(newfileName, 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow([fileName[i]])
            temp = []
            for content in data:
                temp.append(content[i])
            temp.sort()
            for content in temp:
                writer.writerow([str(content)])
        i += 1
        
def histogram(data, fileName):
    jahresDurchschnitt = []
    jahre = []
    i = 0
    j = 0
    while i < len(data):
        if (i != 0):
            if (data[i][0] != data[i-1][0]):
                j += 1
                jahresDurchschnitt.append(data[i][2])
                jahre.append(data[i][0])
            else:
                jahresDurchschnitt[j] += data[i][2]
        else:
            jahre.append(data[i][0])
            jahresDurchschnitt.append(data[i][2])
        print("i: %d" % (i))
        i += 1
    i = 0
    while i < len(jahresDurchschnitt):
        jahresDurchschnitt[i] = jahresDurchschnitt[i] / 3 / 1000000
        i += 1
    plt.bar(jahre, jahresDurchschnitt)
    plt.title("Energieerzeugung im Schnitt pro Jahr durch Steinkohle")
    plt.xlabel("Jahre")
    plt.ylabel("Energieerzeugung in TWh")
    plt.savefig(fileName, dpi = 5000)
    plt.show()
    
def sine_function(x, A, B, C, D):
    return A * np.sin(B * x + C) + D
    


# statistic Funktionen https://www.python4data.science/de/latest/workspace/pandas/descriptive-statistics.html

# bestimmen des Modus durch mode() wenn nur der erste Modus bestimmt werden soll, multimode() wenn eine Liste aller Modus bestimmt werden soll
    
data1Array = []
data2Array = []
data3Array = []
data3bArray = []
data4Array = []

data = open('Dataset-1/data-1.csv', 'r')
readFromDataToArray(data, data1Array, 1)
data.close()
data1Array.sort()

data = open('Dataset-2/data-2.csv', 'r')
readFromDataToArray(data, data2Array, 2)
data.close()
clean(data2Array)

data = open('Dataset-3/data-3-a.csv', 'r')
readFromDataToArray(data, data3Array, 3)
data.close()

data = open('Dataset-3/data-3-b.csv', 'r')
readFromDataToArray(data, data3bArray, 31)
data.close()

data = open('Dataset-4/data-4.csv', 'r')
readFromDataToArray(data, data4Array, 4)
data.close()



#beide Teile von Datensatz 3 kombinieren
i = -1
for teilA in data3Array:
    i += 1
    for teilB in data3bArray:
        if teilA[0] == teilB[0]:
            teilA += teilB[1:]
            del teilA[0]
            break

data3Array.sort()


histogram(data1Array, 'output/dataset-1/histogramm.jpg')

urlist('output/dataset-1/urliste-', data1Array, ['Jahr', 'Monat', 'Elektrizitaetserzeugung'])
urlist('output/dataset-2/urliste-', data2Array, ['Jahr', 'Monat', 'Beschaeftigte'])
urlist('output/dataset-3/urliste-', data3Array, ['Jahr', 'Monat', 'Ankuenfte', 'Uebernachtungen'])
urlist('output/dataset-4/urliste-', data4Array, ['Zeit', 'Lux'])

ranglist('output/dataset-1/rangliste-', data1Array, ['Jahr', 'Monat', 'Elektrizitaetserzeugung'])
ranglist('output/dataset-2/rangliste-', data2Array, ['Jahr', 'Monat', 'Beschaeftigte'])
ranglist('output/dataset-3/rangliste-', data3Array, ['Jahr', 'Monat', 'Ankuenfte', 'Uebernachtungen'])
ranglist('output/dataset-4/rangliste-', data4Array, ['Zeit', 'Lux'])

boxWhiskerPlot('output/dataset-1/boxWhiskerPlot-', ['Jahr', 'Monat', 'Elektrizizaetserzeugung'], data1Array, ['', '', 'in TWh'])
boxWhiskerPlot('output/dataset-2/boxWhiskerPlot-', ['Jahr', 'Monat', 'Beschäftigte'], data2Array, ['', '', 'prozentual zu 2015'])
boxWhiskerPlot('output/dataset-3/boxWhiskerPlot-', ['Jahr', 'Monat', 'AnzahlAnkuenfte', 'AnzahlUebernachtungen'], data3Array, ['', '', 'in Mio', 'in Mio'])
boxWhiskerPlot('output/dataset-4/boxWhiskerPlot-', ['Zeit', 'Lux'], data4Array, ['', '', 'Lichtstärke in Lux'])

scatterPlot('output/dataset-1/scatterPlot.jpg', data1Array, 'Energieerzeugung aus Steinkohle nach Jahren', 'Energieerzeugung in TWh')
scatterPlot('output/dataset-2/scatterPlot.jpg', data2Array, 'Beschäftige im Einzelhandel im Vergleich zu 2015 nach Jahren', 'Beschaeftigte prozentual zu 2015')
scatterPlot('output/dataset-3/scatterPlot.jpg', data3Array, 'Ankuenfte und Uebernachtungen in Beherbergungsbetrieben nach Jahren', 'Anzahl in Mio')

outputToFile('output/dataset-1/content.txt', data1Array, "Variable Jahr: ;Variable Monat: ;Variable Elektrizizaetserzeugung netto in MWh: ")
outputToFile('output/dataset-2/content.txt', data2Array, "Variable Jahr: ;Variable Monat: ;Variable Beschaeftigte prozentual zu 2015: ")
outputToFile('output/dataset-3/content.txt', data3Array, "Variable Jahr: ;Variable Monat: ;Variable Anzahl an Unterkünften: ;Variable Anzahl an Uebernachtugnen: ")
outputToFile('output/dataset-4/content.txt', data4Array, "Variable Zeit: ;Variable lux: ")




with open('output/dataset-3/konsolidiert.csv', 'w', newline = '') as file:
    writer = csv.writer(file, delimiter = ',')
    for content in data3Array:
        writer.writerow([str(content[0]), intToMonth(content[1]), str(content[2]), str(content[3])])
    i += 1
