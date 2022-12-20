import mysql.connector
import datetime
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

  cursor.execute("CREATE TABLE IF NOT EXISTS EVENTS (code varchar(255) NOT NULL, name varchar(255) NOT NULL, d DATE NOT NULL);")

  cursor.execute("CREATE TABLE IF NOT EXISTS BIRTHDAYS (code varchar(255) NOT NULL, name varchar(255) NOT NULL, d DATE NOT NULL);")
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
  date = y + '-' + m + '-' + d
  cursor.execute("USE roommate;")
  query = "INSERT INTO USERS(phoneNumber, name, birthday) VALUES ('%s', '%s', '%s');" % (phone_number, name, date)
  cursor.execute(query)
  mydb.commit()
  print(cursor.rowcount, "record inserted.")
  cursor.close()

def add_birthday(phone_number, name, date):
  cursor = mydb.cursor()
  cursor.execute("USE roommate;")
  code = check_member(phone_number)
  query = 'INSERT INTO BIRTHDAYS(code, NAME, d) VALUES ("%s", "%s", "%s");' % (code,name,date)
  print(query)
  cursor.execute(query)
  mydb.commit()
  print(cursor.rowcount, "record inserted.")
  cursor.close()

def add_event(phone_number, name, date):
  cursor = mydb.cursor()
  cursor.execute("USE roommate;")
  code = check_member(phone_number)
  m = date[0:2]
  d = date[2:4]
  y = date[4:8]
  da = y + '-' + m + '-' + d
  query = 'INSERT INTO EVENTS(code, NAME, d) VALUES ("%s", "%s", "%s");' % (code,name,da)
  print(query)
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

def check_member(phone_number):
  cursor = mydb.cursor()
  cursor.execute("USE roommate;")
  query = "SELECT code FROM MEMBERS WHERE phoneNumber = '%s';" %phone_number
  cursor.execute(query)
  myresult = cursor.fetchall()
  for i in myresult:
    return i[0]
  return None


def add_member(phone_number, group_id):
  cursor = mydb.cursor()
  if check_group(group_id):
    cursor.execute("USE roommate;")
    query = "INSERT INTO MEMBERS(code, phoneNumber) VALUES ('%s', '%s');" % (group_id, phone_number)
    try:
      cursor.execute(query)
      mydb.commit()
      insert_birthday(phone_number, group_id)
      result = True
    except:
      result = False
    cursor.close()
    return result
  else:
    result = False
    return False

def insert_birthday(phone_number, group_id):
    cursor = mydb.cursor()
    cursor.execute("USE roommate;")
    query = "SELECT name, birthday FROM USERS WHERE phoneNumber = %s;" %(phone_number)
    cursor.execute(query)
    myresult = cursor.fetchall()
    for i in myresult:
      name = i[0]
      birthday = i[1]
    

    n = name + "'s Birthday"
    add_birthday(phone_number, n, birthday)
    cursor.close()

def get_events(phone_number):
  lst = []  
  cursor = mydb.cursor()
  cursor.execute("USE roommate;")
  today = datetime.date.today()
  code = check_member(phone_number)
  later = today + datetime.timedelta(days=7)
  query = "SELECT * FROM EVENTS WHERE code = '%s' AND d >= '%s' AND d <= '%s';" %(code, today, later)
  cursor.execute(query)
  myresult = cursor.fetchall()
  for i in myresult:
    lst.append(i)
  return lst

def get_birthdays(phone_number):
  lst = []  
  cursor = mydb.cursor()
  cursor.execute("USE roommate;")
  code = check_member(phone_number)
  today = datetime.date.today()
  for i in range(7):
    later = today + datetime.timedelta(days=i)
    query = "SELECT * FROM BIRTHDAYS WHERE code = '%s' AND MONTH(d) = %d AND DAY(d) = %d;" %(code, later.month, later.day)
    cursor.execute(query)
    myresult = cursor.fetchall()
    for i in myresult:
      lst.append(i)
  return lst


if __name__ == '__main__':
  drop_db()
  create_db()