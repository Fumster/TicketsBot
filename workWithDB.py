import psycopg2
import configparser
from psycopg2 import Error
from datetime import datetime as dt

config = configparser.ConfigParser()
config.read("settings.ini")

con = psycopg2.connect(
    database=config["Database"]["database"],
    user=config["Database"]["user"],
    password=config["Database"]["password"],
    host=config["Database"]["host"],
    port=config["Database"]["port"]
)


def createNewIssue():
    return


def acceptIssue(message_chat_id, user_id):
    try:
        cursor = con.cursor()
        # print("Таблица до обновления записи")
        sql_select_query = """select * from applications where channel_msg_id  = %s"""
        cursor.execute(sql_select_query, (message_chat_id,))
        record = cursor.fetchone()
        print(record)

        # Обновление отдельной записи
        sql_update_query = """Update applications set issuer = %s where channel_msg_id = %s"""
        cursor.execute(sql_update_query, (user_id,message_chat_id))
        con.commit()
        print("Заказ быд принять сотрудником АСУ")

        # print("Таблица после обновления записи")
        sql_select_query = """select * from applications where channel_msg_id = %s"""
        cursor.execute(sql_select_query, (message_chat_id,))
        record = cursor.fetchone()
        print(record)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if con:
            cursor.close()
            con.close()
            print("Соединение с PostgreSQL закрыто")

def closeApplications(channel_msg_id):
    try:
        now = dt.now()

        # Преобразование объекта datetime в строку с помощью метода strftime()
        timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')

        cursor = con.cursor()
        # Обновление отдельной записи
        sql_update_query = """Update applications set status = %s, closed_time = TIMESTAMP %s where channel_msg_id = %s"""
        cursor.execute(sql_update_query, (True, timestamp_str, channel_msg_id))
        con.commit()
        print("Заявка закрыта")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if con:
            cursor.close()
            con.close()
            print("Соединение с PostgreSQL закрыто")
# acceptIssue(1654, 123)
closeApplications(1655)
