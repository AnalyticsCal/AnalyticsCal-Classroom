import csv

def preprocess_csv(file_name):  
    csvHeader = [] # Stores header of the csv File
    csvRows = [] # Stores Rest of the rows - values

    # Read CSV file
    csvFileObj = open(file_name) # reads csv file
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

    return csvHeader, csvList
