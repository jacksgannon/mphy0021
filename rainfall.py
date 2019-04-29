import json
import numpy as np
import math
import matplotlib.pyplot as plt


def parseData(fileName, startyear, endyear):
    """
    Function that parses the data in a file and returns it as a dictionary.
    :param fileName: name of File containing original data
    :param startyear: first year in data set
    :param endyear: last year in data set
    :return:  tot_data: dictionary where key= 'year' (int), value = dict > key = 'day' (int), value='rainfall' (float)
    """
    file = np.genfromtxt(fileName, delimiter=',', names=['year', 'day', 'rainfall'], dtype=[int, int, float])
    tot_data = {}  # dict to contain all data
    while startyear <= endyear:
        rainfall_by_year = {}  # dict to contain rainfall each day in year
        for row in file:
            if row[0] == startyear:  # row[0] is year on the file
                day = int(row[1])
                rainfall = float(row[2])
                rainfall_by_year[day] = rainfall
        tot_data[int(startyear)] = rainfall_by_year
        startyear += 1
#     jsondata = json.dumps(tot_data, sort_keys=True, indent=4)  # convert dict to json
#     diskJson = open('rainfall_data.json', 'w+')
#     diskJson.write(jsondata)  # write json to disk
    
    with open('new_file.json', 'w') as file:
        json.dump(tot_data, file, indent=4)
    
    return tot_data


file = parseData('python_language_1_data.csv', 1937, 2012)


def plotRainfallYear(jsonFile, year, colour):
    """
    Function which plots a time series of the daily measured rainfall for a given year
    :param jsonFile: file containing data as json
    :param year: year to be plotted
    :param colour:  colour of line
    :return:
    """
    xpoints = []  # lists to be plotted
    ypoints = []
    file = open(jsonFile, 'r')
    data_as_string = file.read()  # data in jsonFile in str form
    py_data_object = json.loads(data_as_string)  # convert to dict object
    rainfall_data = py_data_object[year]  # get rainfall data for specific year
    for day, rainfall in rainfall_data.items():
        xpoints.append(int(day))
        ypoints.append(float(rainfall))
    plt.plot(xpoints, ypoints, colour)
    plt.ylabel('Rainfall (mm/day)')
    plt.xlabel('Day')
    plt.title('Daily rainfall measurement in {0}'.format(year))
    plt.savefig('Rainfall_plot_1998.png')
    plt.clf()

plotRainfallYear('rainfall_data.json', '1998', 'r')


def plotAnnualRainfall(jsonFile, startyear, endyear):
    """
    Function to plot the mean annual rainfall each year from startyear to endyear
    :param jsonFile: file containing data as json
    :param startyear: first year in range of plotting mean annual rainfall
    :param endyear: last year in range of plotting mean annual rainfall
    :return:
    """
    istartyear = int(startyear)  # convert startyear and endyear to int
    iendyear = int(endyear)
    file = open(jsonFile, 'r')
    data_as_string = file.read()  # data in jsonFile in str form
    py_data_object = json.loads(data_as_string)  # convert to dict object

        
    xpoints = []
    ypoints = []  # lists to be plotted
    while istartyear <= iendyear:
        rainfall_data = py_data_object[str(istartyear)]  # get rainfall data for specific year
        tot_rainfall = 0
        for day, rainfall in rainfall_data.items():
            tot_rainfall += float(rainfall)  # getting total rainfall
        mean_rainfall = tot_rainfall/len(rainfall_data.items())
        ypoints.append(mean_rainfall)
        xpoints.append(int(istartyear))
        istartyear+=1
    plt.plot(xpoints, ypoints, 'bo-')
    plt.ylabel('Mean Annual Rainfall (mm/day)')
    plt.xlabel('Year')
    plt.title('Mean Annual Rainfall measurements, {0} - {1}'.format(startyear, endyear))
    plt.savefig('Rainfall_plot_1988_2000.png')
    plt.clf()


plotAnnualRainfall('rainfall_data.json', '1988', '2000')


def applyCorrection(rainfall_val):
    correct_val = rainfall_val * math.pow(1.2, np.sqrt(2))
    return correct_val


def applyCorrectionLoop(jsonFile, year):
    """
    Function that applies the applyCorrection() method to all values of rainfall in a specified year using a loop
    :param jsonFile:  file containing data as json
    :param year: year for data to be corrected
    :return: corrected_rainfall_list (list) : contains all corrected rainfall values
    """
    corrected_rainfall_list =[]
    file = open(jsonFile, 'r')
    data_as_string = file.read()  # data in jsonFile in str form
    py_data_object = json.loads(data_as_string)  # convert to dict object
    rainfall_data = py_data_object[year]  # get rainfall data for specific year
    for day, rainfall in rainfall_data.items():
        correct_rainfall = applyCorrection(rainfall)
        corrected_rainfall_list.append(correct_rainfall)
    return corrected_rainfall_list


correct_data_loop = applyCorrectionLoop('rainfall_data.json', '2000')


def applyCorrectionComp(jsonFile, year):
    """
    Function that applies the applyCorrection() method to all rainfall values in a specified year using comprehenion
    :param jsonFile:  file containing data as json
    :param year: year for data to be corrected
    :return: corrected_rainfall_list (list) : contains all corrected rainfall values

    Advantages of using comprehension - considered more readable, achieves the same output in less lines of
                                        code, faster in terms of performance.
    Disadvantages of using comprehension - Does not increase the capabilities of the language

    Advantages of using loop - Perhaps easier to understand
    Disadvantage of using loop - less readable, takes more lines of code, slower in terms of performance.
    """
    file = open(jsonFile, 'r')
    data_as_string = file.read()  # data in jsonFile in str form
    py_data_object = json.loads(data_as_string)  # convert to dict object
    rainfall_data = py_data_object[year]  # get rainfall data for specific year
    return [applyCorrection(rainfall) for day, rainfall in rainfall_data.items()]


correct_data_comp = applyCorrectionComp('rainfall_data.json', '2000')
