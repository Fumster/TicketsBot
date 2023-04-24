import psycopg2
import configparser

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


def acceptIssue():
    return

