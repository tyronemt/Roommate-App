import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "password"
)


def drop_db():
  cursor = mydb.cursor()
  cursor.execute("DROP DATABASE `roommate`;")

def create_db():

  cursor = mydb.cursor()
  cursor.execute("CREATE DATABASE IF NOT EXISTS roommate;")

  cursor.execute("USE roommate;")

  cursor.execute("CREATE TABLE IF NOT EXISTS USERS (phoneNumber varchar(255) NOT NULL, name varchar(255) NOT NULL, birthday DATE NOT NULL, UNIQUE (`phoneNumber`));")
  
  cursor.execute("CREATE TABLE IF NOT EXISTS HOUSE (code varchar(255) NOT NULL, name varchar(255) NOT NULL, UNIQUE (`code`));")

  cursor.execute("CREATE TABLE IF NOT EXISTS MEMBERS (code varchar(255) NOT NULL, phoneNumber varchar(255) NOT NULL, UNIQUE (`phoneNumber`));")

  print(cursor.rowcount, "record inserted.")

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

def create_group(phone_number, name, group_id):
  cursor = mydb.cursor()
  cursor.execute("USE roommate;")
  query = "INSERT INTO HOUSE(code, name) VALUES ('%s', '%s');" % (group_id, name)
  cursor.execute(query)
  mydb.commit()
  print(cursor.rowcount, "record inserted.")
  cursor.close()
  add_member(phone_number, group_id)

def check_group(group_id):
  cursor = mydb.cursor()
  res = False
  cursor.execute("USE roommate;")
  query = "SELECT * FROM HOUSE WHERE code = '%s';" %group_id
  cursor.execute(query)

  myresult = cursor.fetchall()

  for i in myresult:
    res = True
  cursor.close()
  return res


def add_member(phone_number, group_id):
  cursor = mydb.cursor()
  if check_group(group_id):
    cursor.execute("USE roommate;")
    query = "INSERT INTO MEMBERS(code, phoneNumber) VALUES ('%s', '%s');" % (group_id, phone_number)
    try:
      cursor.execute(query)
      mydb.commit()
      result = True
    except:
      result = False
    cursor.close()
    return result
  else:
    result = False
    return False

if __name__ == '__main__':
  drop_db()
  create_db()