class Event:
    def __init__(self, name, description, date):
        self.name = name
        self.description = description
        self.month = int(date[0:2])
        self.day  = int(date[2:4])
        self.year = int(date[4:8])


    def change_description (self, description):
        self.description = description
    
    def change_date (self, date):
        self.month = int(date[0:2])
        self.day  = int(date[2:4])
        self.year = int(date[4:8])

    def change_name (self, name):
        self.name = name
    
    def __eq__(self,other):
        return self.year == other.year and self.day == other.day and self.month == other.month

    def __lt__(self,other):
 
        if self.year > other.year:
            return True
        elif self.year < other.year:
            return False

        if self.month > other.month:
            return True
        elif self.month < other.month:
            return False

        if self.day > other.day:
            return True
        elif self.day < other.day:
            return False
        return False

class Calendar:
    def __init__(self):
        self.calendar = []

    def create_event(self, name, date, description):
        if len(name) > 0:
            try:
                month = int(date[0:2])
                day  = int(date[2:4])
                year = int(date[4:8])
                if month > 0 and month <= 12:
                    if day > 0 and day <= 31:
                        if year > 0:
                            temp = Event(name, description, date)
                            self.calendar.append(temp)
                            return True
            except:
                return "Invalid Date!"
        else:
            return "Invalid Name"




