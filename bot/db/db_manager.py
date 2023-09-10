import datetime

import psycopg2
from dotenv import dotenv_values
from bot.utils import Spending


# CREATE_QUERY = ("CREATE TABLE spendings ("
#                 "id SERIAL PRIMARY KEY, "
#                 "title VARCHAR(255), "
#                 "price INTEGER, "
#                 "dt TIMESTAMPTZ"
#                 ");")

# title = "Бургер"
# price = 100
# dt = datetime.datetime.now()

# config_dict = {**dotenv_values('../.env')}
# DB_NAME = config_dict["DB_NAME"]
# DB_HOST = config_dict["DB_HOST"]
# DB_PORT = config_dict["DB_PORT"]
# DB_USER = config_dict["DB_USER"]
# DB_USER_PWD = config_dict["DB_USER_PWD"]

# connection = psycopg2.connect(
#     dbname=DB_NAME,
#     user=DB_USER,
#     password=DB_USER_PWD,
#     host=DB_HOST,
#     port=DB_PORT
# )

# params = {"dbname": DB_NAME,
#           "user": DB_USER,
#           "password": DB_USER_PWD,
#           "host": DB_HOST,
#           "port": DB_PORT}


# connection = psycopg2.connect(**params)
#
# cursor = connection.cursor()
# cursor.execute(INSERT_QUERY)
#
# connection.commit()
# cursor.close()
# connection.close()


# def connect(db_manager, func):
#     def wrapper():
#         try:
#             connection = psycopg2.connect(**db_manager.__dict__)
#             cursor = connection.cursor()
#             try:
#                 func()
#             except psycopg2.Error:
#                 print("EXECUTE ERROR")
#         except psycopg2.Error:
#             print("CONNECTION/CURSOR ERROR")
#         else:
#             try:
#                 connection.commit()
#                 cursor.close()
#                 connection.close()
#             except psycopg2.Error:
#                 print("CONNECTION/CURSOR CLOSE ERROR")
#         return
#     return wrapper


class DBmanager:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def create_query(self):
        try:
            connection = psycopg2.connect(**self.__dict__)
            cursor = connection.cursor()
            try:
                CREATE_QUERY = ("CREATE TABLE spendings ("
                                "id SERIAL PRIMARY KEY, "
                                "title VARCHAR(255), "
                                "price INTEGER, "
                                "dt TIMESTAMPTZ"
                                ");")
                cursor.execute(CREATE_QUERY)
            except psycopg2.Error:
                print("create_query_EXECUTE ERROR")
        except psycopg2.Error:
            print("insert_query_CONNECTION/CURSOR ERROR")
        else:
            try:
                connection.commit()
                cursor.close()
                connection.close()
            except psycopg2.Error:
                print("create_query_CONNECTION/CURSOR CLOSE ERROR")

    def insert_query(self, spending):
        try:
            connection = psycopg2.connect(**self.__dict__)
            cursor = connection.cursor()
            try:
                title, price, dt = spending.get_params()
                INSERT_QUERY = f"""
                                INSERT INTO spendings (title, price, dt)
                                VALUES ('{title}', {price}, '{dt}');
                                """
                cursor.execute(INSERT_QUERY)
            except psycopg2.Error:
                print("insert_query_EXECUTE ERROR")
        except psycopg2.Error:
            print("insert_query_CONNECTION/CURSOR ERROR")
        else:
            try:
                connection.commit()
                cursor.close()
                connection.close()
            except psycopg2.Error:
                print("insert_query_CONNECTION/CURSOR CLOSE ERROR")

    # 0 - day
    # 1 - week
    # 2 - month
    # 3 - year
    def select_query(self, param=0):
        data = None
        try:
            connection = psycopg2.connect(**self.__dict__)
            cursor = connection.cursor()
            try:
                match param:
                    case 0:
                        SELECT_QUERY = f"""
                                        SELECT title, price, TO_CHAR(dt, 'HH24:MI:SS') AS datetime 
                                        FROM spendings 
                                        WHERE DATE(dt) = CURRENT_DATE;
                                        """
                        cursor.execute(SELECT_QUERY)
                        data = cursor.fetchone()
                        print(data)
                    case [1, 2, 3]:
                        SELECT_QUERY = f"""
                                        SELECT 
                                        """
                    case _:
                        print("No Params")
            except psycopg2.Error:
                print("insert_query_EXECUTE ERROR")
        except psycopg2.Error:
            print("insert_query_CONNECTION/CURSOR ERROR")
        else:
            try:
                connection.commit()
                cursor.close()
                connection.close()
            except psycopg2.Error:
                print("insert_query_CONNECTION/CURSOR CLOSE ERROR")
        return data

    def __str__(self):
        for key, value in self.__dict__.items():
            print(key, value)

# sp = Spending("Продукты", 500)
# manager = DBmanager(**params)
# manager.create_query()
# manager.insert_query(sp)
