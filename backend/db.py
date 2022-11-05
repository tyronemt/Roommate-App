import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "password"
)

cursor = mydb.cursor()


def create_table():
  
  cursor.execute("CREATE DATABASE IF NOT EXISTS roommate")

  cursor.execute("USE roommate")

  cursor.execute("CREATE TABLE IF NOT EXISTS USERS (phoneNumber varchar(255) NOT NULL, name varchar(255) NOT NULL, birthday DATE NOT NULL);")

def check_user(phone_number):
  cursor.execute("USE roommate")
  query = "SELECT phoneNumber FROM USERS WHERE phoneNumber = '%s';" %phone_number 
  cursor.execute(query)

  for phoneNumber in cursor:
    return True
  return False


create_table()