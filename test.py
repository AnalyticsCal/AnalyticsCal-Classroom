import pymysql
import os

import data_load
from data_load import load_and_filter_data_opeartion


dataset_file_name = "/home/archit/Documents/STUDY/CCE_IISC/BasicsofDataAnalytics/dataset/delhi_weather_test.csv"
db = pymysql.connect("localhost", "root", "toortoor", "analytics")
cursor = db.cursor()


ret_value = load_and_filter_data_opeartion(cursor,dataset_file_name)
if ret_value == 0:
    print("Data loaded into Database, Do further processing...")
else:
    print("Error : "+str(ret_value))


