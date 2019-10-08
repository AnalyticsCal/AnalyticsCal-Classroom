import csv
import pymysql

# global variable
dataset_file_name = "/home/archit/Documents/STUDY/CCE_IISC/BasicsofDataAnalytics/delhi-weather-data_test.csv"


db = pymysql.connect("localhost", "root", "toortoor", "analytics")
cursor = db.cursor()

class Wheather:

    def __init__(self):
        return

    def load_csv_file(self,filename):
        with open(filename , 'r') as f:
            reader = csv.reader(f)
            temp_list = list(reader)
        return temp_list

    def filter_data(self,temp_data):
        length = len(temp_data)
        i = 0
        while i < length:
            temp_data[i].append(0)
            temp_data[i].append(0)
            i += 1
        return temp_data

    def create_structured_data(self,row_data):
        column_name = row_data[0]
        row_data.pop(0)
        for i in range(len(row_data)) :
            for j in range(len(row_data[0])):
                if(row_data[i][j] == ''):
                    row_data[i][j] = 'NULL'
        return column_name, row_data

# INSERT INTO delhi_weather (datetime_utc, _conds, _dewptm, _fog, _hail, _heatindexm, _hum, _precipm, _pressurem, _rain, _snow, _tempm, _thunder, _tornado, _vism,	_wdird, _wdire,	_wgustm, _windchillm, _wspdm )
# VALUES ('1996-11-01 12:00','Smoke',10,0,0,NULL,32,NULL,-9999,0,0,28,0,0,NULL,0,'North',NULL,NULL,NULL);

    def insert_data_to_db(self,structured_data,column_name):
        cnt = 0
        columns = ",".join(column_name)
        for list in structured_data:
            # values = str(list)[1:-1
            value1 = ",".join(list[2:16])
            value2 = ",".join(list[17:20])
            temp_str = "INSERT INTO delhi_weather (" + columns + ") VALUES ( '" + list[0] + "','" + list[1] + "'," +value1 +",'"+list[16]+"',"+value2 +") ;"
            print(temp_str)
            cursor.execute(temp_str)
            cnt = cnt + 1
        cursor.execute("commit")
        return cnt

    # values = ",".join(list)
    # values = str(list)[1:-1]

if __name__ == '__main__':
    my_weather = Wheather()
    row_data = my_weather.load_csv_file(dataset_file_name)
    column_name, structured_data = my_weather.create_structured_data(row_data)
    # print(structured_data)
    inserted_rows_count = my_weather.insert_data_to_db(structured_data, column_name)
    print("number of rows inserted " + str(inserted_rows_count))
    # print(column_name)
    # data = my_weather.filter_data(data)
    # print(data)

# db = pymysql.connect("localhost", "root", "toortoor", "analytics")
# cursor = db.cursor()
# cursor.execute("SELECT VERSION()")
# db_version = cursor.fetchone()
# print(db_version)
