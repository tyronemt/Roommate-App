import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "password"
)


def create_table():

  cursor = mydb.cursor()
  cursor.execute("CREATE DATABASE IF NOT EXISTS roommate")

  cursor.execute("USE roommate;")

  cursor.execute("CREATE TABLE IF NOT EXISTS USERS (phoneNumber varchar(255) NOT NULL, name varchar(255) NOT NULL, birthday DATE NOT NULL, UNIQUE (`phoneNumber`));")
  cursor.close()

def check_user(phone_number):

  cursor = mydb.cursor()
  res = False
  cursor.execute("USE roommate;")
  query = "SELECT phoneNumber FROM USERS WHERE phoneNumber = '%s';" %phone_number 
  cursor.execute(query)

  myresult = cursor.fetchall()

  for phoneNumber in myresult:
    res = True
  cursor.close()
  return res

def create_user(phone_number, name, birthday):

  cursor = mydb.cursor()
  m = birthday[0:2]
  d = birthday[2:4]
  y = birthday[4:8]
  cursor.execute("USE roommate;")
  query = "INSERT INTO USERS(phoneNumber, name, birthday) VALUES ('%s', '%s', '%s');" % (phone_number, name, y + '-' + m + '-' + d)
  cursor.execute(query)
  mydb.commit()
  print(cursor.rowcount, "record inserted.")
  cursor.close()

create_table()