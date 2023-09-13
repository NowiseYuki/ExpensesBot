import datetime
import psycopg2
from finance import Finance
from env_conf import DB_PARAMS


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

    # ADD FINANCE
    def insert_query(self, finance):
        try:
            connection = psycopg2.connect(**self.__dict__)
            cursor = connection.cursor()
            try:
                isIncome, amount, from_to, description = finance.get_params()
                INSERT_QUERY = f"""
                                INSERT INTO finances (isIncome, amount, from_to, description_)
                                VALUES ('{isIncome}', {amount}, '{from_to}', '{description}');
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

    # param = 0 (all finances for today)
    # param = 1 (all finances for specific date)
    # param = 2 (all finances for week)
    # param = 3 (all finances for month)
    def select_query(self):
        data = None
        try:
            connection = psycopg2.connect(**self.__dict__)
            cursor = connection.cursor()
            try:
                SELECT_QUERY = f"""
                                SELECT isIncome, amount, from_to, description_, TO_CHAR(dt, 'HH24:MI:SS') AS datetime 
                                FROM finances 
                                WHERE DATE(dt) = CURRENT_DATE;
                                """
                cursor.execute(SELECT_QUERY)
                data = cursor.fetchone()
                print(data)

            except psycopg2.Error:
                print("select_query_EXECUTE ERROR")
        except psycopg2.Error:
            print("select_query_CONNECTION/CURSOR ERROR")
        else:
            try:
                connection.commit()
                cursor.close()
                connection.close()
            except psycopg2.Error:
                print("select_query_CONNECTION/CURSOR CLOSE ERROR")
        return data

    def select_today_query(self):
        data = []
        try:
            connection = psycopg2.connect(**self.__dict__)
            cursor = connection.cursor()
            try:
                SELECT_QUERY = f"""
                                SELECT isIncome, amount, from_to, description_, dt 
                                FROM finances 
                                WHERE DATE(dt) = CURRENT_DATE and isIncome = TRUE
                                ORDER BY dt, amount;
                                """
                cursor.execute(SELECT_QUERY)
                data.append(cursor.fetchall())
                SELECT_QUERY = f"""
                                SELECT isIncome, amount, from_to, description_, dt 
                                FROM finances 
                                WHERE DATE(dt) = CURRENT_DATE and isIncome = FALSE
                                ORDER BY dt, amount;
                                """
                cursor.execute(SELECT_QUERY)
                data.append(cursor.fetchall())
            except psycopg2.Error:
                print("select_today_query_EXECUTE ERROR")
        except psycopg2.Error:
            print("select_today_query_CONNECTION/CURSOR ERROR")
        else:
            try:
                connection.commit()
                cursor.close()
                connection.close()
            except psycopg2.Error:
                print("select_today_query_CONNECTION/CURSOR CLOSE ERROR")
        return data


    def __str__(self):
        for key, value in self.__dict__.items():
            print(key, value)
