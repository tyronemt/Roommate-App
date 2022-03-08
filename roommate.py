from re import U
import calend
users = []


class Roommate:
  def __init__(self, name, username, password, birthday):
    self.name = name
    self.birthday = birthday
    self.username = username
    self.password = password
    self.calendar = calend.Calendar()

def login(username, password):
  for i in users:
    if i.username == username and i.password == password:
      return (True, i)
  return (False, "Wrong email or password!")

def register(name, username, password, birthday):
  if len(name) == 0 or len(username) == 0 or len(password) == 0 or len(birthday) == 0:
    return "One or more parameters is empty!"
  if len(birthday) != 8:
    return "Birthday is invalid!"
  for i in users:
    if i.username == username and i.password == password:
      return "User already exist!"
  try:
      month = int(birthday[0:2])
      day  = int(birthday[2:4])
      year = int(birthday[4:8])
      if month > 0 and month <= 12:
        if day > 0 and day <= 31:
          if year > 0:
            temp = Roommate(name, username, password, birthday)
            users.append(temp)
            return True
      return "Invalid Date!"
  except:
    return "Error!"




