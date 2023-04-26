import psycopg2
import configparser
from psycopg2 import Error
from datetime import datetime as dt

config = configparser.ConfigParser()
config.read("settings.ini")

# con = psycopg2.connect(
#     database=config["Database"]["database"],
#     user=config["Database"]["user"],
#     password=config["Database"]["password"],
#     host=config["Database"]["host"],
#     port=config["Database"]["port"]
# )


def createNewIssue(channel_msg_id, chat_id, opener_msg_id, issuer_msg_id, room, content):

    con = psycopg2.connect(
        database=config["Database"]["database"],
        user=config["Database"]["user"],
        password=config["Database"]["password"],
        host=config["Database"]["host"],
        port=config["Database"]["port"]
    )

    cursor = con.cursor()
    now = dt.now()

    # Преобразование объекта datetime в строку с помощью метода strftime()
    timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')
    sql_insert_query = """INSERT INTO applications (channel_msg_id, chat_id, opener_msg_id, issuer_msg_id, room, content, opening_time) 
                         VALUES (%s,%s,%s,%s,%s,%s,TIMESTAMP %s)"""
    record_to_insert = (channel_msg_id, chat_id, opener_msg_id, issuer_msg_id, room, content, timestamp_str)
    cursor.execute(sql_insert_query, record_to_insert)
    con.commit()
    cursor.close()
    con.close()

    return


def acceptIssue(message_chat_id, user_id, bot_accept_id):
    con = psycopg2.connect(
        database=config["Database"]["database"],
        user=config["Database"]["user"],
        password=config["Database"]["password"],
        host=config["Database"]["host"],
        port=config["Database"]["port"]
    )
    try:
        cursor = con.cursor()
        # print("Таблица до обновления записи")
        print("message_chat_id", message_chat_id)
        sql_select_query = """select * from applications where issuer_msg_id  = %s"""
        cursor.execute(sql_select_query, (message_chat_id,))
        record = cursor.fetchone()
        print(record)

        # Обновление отдельной записи
        sql_update_query = """Update applications set issuer = %s, bot_accept_id = %s where issuer_msg_id = %s"""
        cursor.execute(sql_update_query, (user_id, bot_accept_id, message_chat_id))
        con.commit()
        print("Заказ быд принять сотрудником АСУ")

        # print("Таблица после обновления записи")
        sql_select_query = """select * from applications where issuer_msg_id = %s"""
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


def closeApplications(issuer_msg_id, closer, solution):
    con = psycopg2.connect(
        database=config["Database"]["database"],
        user=config["Database"]["user"],
        password=config["Database"]["password"],
        host=config["Database"]["host"],
        port=config["Database"]["port"]
    )
    try:
        now = dt.now()
        # Преобразование объекта datetime в строку с помощью метода strftime()
        timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')

        cursor = con.cursor()
        # Обновление отдельной записи
        sql_update_query = """Update applications set closer =%s, solution=%s, status = %s, closed_time = TIMESTAMP %s where issuer_msg_id = %s"""
        cursor.execute(sql_update_query, (closer, solution, True, timestamp_str, issuer_msg_id))
        con.commit()
        print("Заявка закрыта")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if con:
            cursor.close()
            con.close()
            print("Соединение с PostgreSQL закрыто")


# def getNewIdForApplication():
#     con = psycopg2.connect(
#         database=config["Database"]["database"],
#         user=config["Database"]["user"],
#         password=config["Database"]["password"],
#         host=config["Database"]["host"],
#         port=config["Database"]["port"]
#     )
#     cursor = con.cursor()
#     sql_select_query = """SELECT MAX(issuer_msg_id) FROM applications"""
#     cursor.execute(sql_select_query)
#     id = cursor.fetchone()
#     cursor.close()
#     con.close()
#     return id[0]


# acceptIssue(1654, 123)
# closeApplications(1655)
# now = dt.now()
#
# # Преобразование объекта datetime в строку с помощью метода strftime()
# timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')
#
# createNewIssue(1654, 654856, 84654, 846564685, 46868465, "89746", "5458", "5443543", "453452", timestamp_str)
#
#
# print(dt.now())

def isAccepted(issuer_msg_id):
    con = psycopg2.connect(
        database=config["Database"]["database"],
        user=config["Database"]["user"],
        password=config["Database"]["password"],
        host=config["Database"]["host"],
        port=config["Database"]["port"]
    )
    cursor = con.cursor()
    sql_select_query = """select status from applications where issuer_msg_id  = %s"""
    cursor.execute(sql_select_query, (issuer_msg_id,))
    check = cursor.fetchone()
    cursor.close()
    con.close()
    return check[0]


def permissionToCloseApplication(issuer_msg_id):
    con = psycopg2.connect(
        database=config["Database"]["database"],
        user=config["Database"]["user"],
        password=config["Database"]["password"],
        host=config["Database"]["host"],
        port=config["Database"]["port"]
    )
    cursor = con.cursor()
    print("issuer_msg_id", issuer_msg_id)
    sql_select_query = """select status from applications where issuer_msg_id  = %s"""
    cursor.execute(sql_select_query, (issuer_msg_id,))
    isStatus = cursor.fetchone()[0]
    print(isStatus)
    sql_select_query = """select issuer from applications where issuer_msg_id  = %s"""
    cursor.execute(sql_select_query, (issuer_msg_id,))
    isIssuer = cursor.fetchone()[0]
    print(isIssuer)
    cursor.close()
    con.close()
    return not (isIssuer is None) and not isStatus


def getBotAcceptId(issuer_msg_id):
    con = psycopg2.connect(
        database=config["Database"]["database"],
        user=config["Database"]["user"],
        password=config["Database"]["password"],
        host=config["Database"]["host"],
        port=config["Database"]["port"]
    )
    cursor = con.cursor()
    sql_select_query = """select bot_accept_id from applications where issuer_msg_id  = %s"""
    cursor.execute(sql_select_query, (issuer_msg_id,))
    check = cursor.fetchone()
    cursor.close()
    con.close()
    return check[0]

def getContent(issuer_msg_id):
    con = psycopg2.connect(
        database=config["Database"]["database"],
        user=config["Database"]["user"],
        password=config["Database"]["password"],
        host=config["Database"]["host"],
        port=config["Database"]["port"]
    )
    cursor = con.cursor()
    sql_select_query = """select content from applications where issuer_msg_id  = %s"""
    cursor.execute(sql_select_query, (issuer_msg_id,))
    check = cursor.fetchone()
    cursor.close()
    con.close()
    return check[0]


def getOpenerMsgId(issuer_msg_id):
    con = psycopg2.connect(
        database=config["Database"]["database"],
        user=config["Database"]["user"],
        password=config["Database"]["password"],
        host=config["Database"]["host"],
        port=config["Database"]["port"]
    )
    cursor = con.cursor()
    sql_select_query = """select opener_msg_id from applications where issuer_msg_id  = %s"""
    cursor.execute(sql_select_query, (issuer_msg_id,))
    check = cursor.fetchone()
    cursor.close()
    con.close()
    return check[0]
