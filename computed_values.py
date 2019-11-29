import pymysql
import os
import data_load

class Computed:
    def __init__(self, dataset_file_name, cursor):
        self.dataset_file_name = dataset_file_name
        self.cursor = cursor
      
    def save_computing(self, item_key, comp_func):
        item_value = comp_func()
        self.save_computed(item_key, item_value)

    def save_computed(self, item_key, item_value):
        values_tablename = os.path.splitext(os.path.basename(self.dataset_file_name))[0]+"_values"
        insert_qry = "INSERT INTO `" + values_tablename + "`(`item_key`,`item_value`) VALUES ('"+ item_key+"',"+str(item_value) + ") ;"
        self.cursor.execute(insert_qry)
        print(self.cursor.rowcount, "Record inserted successfully into values table")
        self.cursor.execute("commit")

    def get_computed(self, item_key):
        values_tablename = os.path.splitext(os.path.basename(self.dataset_file_name))[0]+"_values"
        select_qry = "SELECT `item_value` FROM `" + values_tablename + "` WHERE `item_key`='"+item_key+"';"
        self.cursor.execute(select_qry)
        item_value = self.cursor.fetchone()[0]
        print(item_value, "Retrieved successfully from values table")
        return item_value


'''def main():
    dataset_file_name = "/Users/saalex/Documents/weather_data_test.csv"
    db = pymysql.connect("localhost", "root", "toortoor", "analytics")
    cursor = db.cursor()
    #save_computed(cursor,dataset_file_name, "abcdefg",178.90)
    get_computed(cursor,dataset_file_name, "abcdefg")

main()'''