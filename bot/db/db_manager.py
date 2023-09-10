import datetime

import psycopg2
from bot.utils import Spending


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
