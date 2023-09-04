import mysql.connector
from application.model.item import Item

class MysqlAdapter:
    host = ""
    user = ""
    password = ""
    database = ""
    connection = None

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.item_apibase = database
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.item_apibase
            )
            print("mysql connection established successfully...")
        except Exception as ex:
            print("connection failed...")
            print(ex)
    
    def write(self, item):
        try:
            cursor = self.connection.cursor()
            sql = "REPLACE INTO item (site, id, price, start_time, category_name, currency_description, seller_nickname) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, item.getValues())
            print(cursor.rowcount, "record inserted.")
            self.connection.commit()
        except Exception as ex:
            print("error inserting record...")
            print(ex)
    
    def write_many(self, items):
        try:
            print("inserting record... write many", items)
            cursor = self.connection.cursor()
            sql = "REPLACE INTO item (site, id, price, start_time, category_name, currency_description, seller_nickname) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, items)
            print(cursor.rowcount, "record inserted.")
            self.connection.commit()
        except Exception as ex:
            print("error inserting record...")
            print(ex)
    
    def close(self):
        self.connection.close()