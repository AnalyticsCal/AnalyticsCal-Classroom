import csv
import pymysql
import os

def load_csv_file(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        temp_list = list(reader)
    return temp_list

def filter_data(temp_data):
    length = len(temp_data)
    i = 0
    while i < length:
        temp_data[i].append(0)
        temp_data[i].append(0)
        i += 1
    return temp_data

def create_structured_data(row_data):
    column_name = row_data[0]
    row_data.pop(0)
    for i in range(len(row_data)):
        for j in range(len(row_data[0])):
            if (row_data[i][j] == ''):
                row_data[i][j] = 'NULL'
    return column_name, row_data

def check_if_exists(cursor,data_tablename):
    check_table_str = "show tables like \"" + data_tablename + "\";"
    table_count = cursor.execute(check_table_str)
    return table_count

def create_data_table(cursor, column_name,data_tablename):
    columns = " DOUBLE,".join(column_name) + " DOUBLE"
    create_table_str = "CREATE TABLE IF NOT EXISTS " + data_tablename + "(id int  NOT NULL AUTO_INCREMENT," + columns + ",PRIMARY KEY (id));"
    print ("create table query : "+create_table_str)
    cursor.execute(create_table_str)

def insert_data_to_db(cursor, structured_data, column_name,data_tablename):
    count = 0
    columns = "`" + "`,`".join(column_name) + "`"
    for list in structured_data:
        values = ",".join(list)
        temp_str = "INSERT INTO `" + data_tablename + "` ( " + columns + ") VALUES (" + values + ") ;"
        cursor.execute(temp_str)
        count = count + 1
    cursor.execute("commit")
    return count


def load_and_filter_data_opeartion(cursor, dataset_file_name):
    cursor=get_connection()
    data_tablename = os.path.splitext(os.path.basename(dataset_file_name))[0]
    row_data = load_csv_file(dataset_file_name)
    column_name, structured_data = create_structured_data(row_data)
    print("column name " + str(column_name))
    if (check_if_exists(cursor,data_tablename)):
        print("The table already exists. Overwriting content ...")
        delete_table_content = "DELETE FROM "+ data_tablename +";"
        cursor.execute(delete_table_content)
    else:
        create_data_table(cursor,column_name,data_tablename)
        print("Table created: " + data_tablename)
    inserted_rows_count = insert_data_to_db(cursor, structured_data, column_name,data_tablename)
    print("Number of rows inserted :" + str(inserted_rows_count))
    create_computation_table(cursor,dataset_file_name)
    cursor.execute("commit")

def create_computation_table(cursor, dataset_file_name):
    values_tablename = os.path.splitext(os.path.basename(dataset_file_name))[0]+"_values"
    if (check_if_exists(cursor,values_tablename)):
        print("The values_table already exists. Clearing content ...")
        delete_all_content = "DELETE FROM "+ values_tablename +";"
        print ("delete content query : "+delete_all_content)
        cursor.execute(delete_all_content)
        print("Table content cleared: " + values_tablename)
    else:
        create_val_table_str = "CREATE TABLE IF NOT EXISTS " + values_tablename + "(id INT NOT NULL AUTO_INCREMENT,item_key VARCHAR(200) NOT NULL UNIQUE,item_value DOUBLE,PRIMARY KEY (id));"
        print ("create table query : "+create_val_table_str)
        cursor.execute(create_val_table_str)
        print("Table created: " + values_tablename)

def get_connection():
    db = pymysql.connect("localhost", "root", "toortoor", "analytics")
    return db.cursor()


'''def main():
    dataset_file_name = "/Users/saalex/Documents/weather_data_test.csv"
    load_and_filter_data_opeartion(dataset_file_name)

main()'''