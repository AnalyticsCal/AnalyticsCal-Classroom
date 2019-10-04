import csv

def csvToDict(fileName):
    """
    This fucntion converts csv file into a python dictionary object\
    returns a tuple--> (dict, headerList, valueList)
    For Ex:
    csv file: abc.csv is converted to dictionary: out_dict 

    abc.csv:
        x,y,z
        1,7.50,42720.54
        2,44.31,43306.38
        3,60.80,44774.76
        4,148.97,45364.04

        |
        |becomes
        v
        
    out_dict:
    {'x': ['1', '2', '3', '4'], 'y': ['7.50', '44.31', '60.80', '148.97'], 'z': ['42720.54', '43306.38', '44774.76', '45364.04']}
    headerList:
    ['x','y','z']
    valueList:
    [['1', '2', '3', '4'], ['7.50', '44.31', '60.80', '148.97'],  ['42720.54', '43306.38', '44774.76', '45364.04']]
    

    As the csv file treats everything as a string the key-value pairs' datatype is string.
    """
    csvHeader = [] # Stores header of the csv File
    csvRows = [] # Stores Rest of the rows - values

    # Read CSV file
    csvFileObj = open(fileName) # reads csv file 
    readerObj = csv.reader(csvFileObj) # creates a reader object

    # Separate header row and other rows in different lists
    for row in readerObj:
        if readerObj.line_num == 1: # line #1 corresponds to header 
            csvHeader = row # store header in a list csvHeader
        else:
            csvRows.append(row) # stores the values in list csvRows
    csvFileObj.close()


    csvList = [] #stores list of column vectors([x1],[x2],[x3]...,[xn],[y])

    # Create list of column vectors
    for i in range(len(csvHeader)):
        csvList.append([row[i] for row in csvRows]) 

    out_dict = dict(zip(csvHeader, csvList)) # convert csvList into dictionary
    # print('out_dict = ', out_dict)
    return out_dict, csvHeader, csvList

fileName = 'Sub_Division_IMD_2017.csv' # Path of csv file
dataDict, dataHeader, dataValues = csvToDict(fileName) # unwraping tuple into dict and list
