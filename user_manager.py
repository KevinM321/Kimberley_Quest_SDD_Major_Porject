from tinydb import TinyDB, Query
from datetime import date, datetime
from passlib.hash import pbkdf2_sha256
import activityscreen

user_query = Query()
user_bookings = TinyDB('bookings', indent=2)
user_account = TinyDB('account', indent=2)
user_profile = TinyDB('profile', indent=2)

# format for the meal bookings in 'bookings'
meal_day = {
           "Breakfast": {
             "main_meal": "",
             "snacks": "",
             "drinks": ""
           },
           "Lunch": {
             "main_meal": "",
             "snacks": "",
             "drinks": ""
           },
           "Dinner": {
             "main_meal": "",
             "snacks": "",
             "drinks": ""
           }
          }


# class for each instances of an user
class User:

    # set attributes for later use
    def __init__(self, username):
        self.username = username
        self.bookings = user_bookings.search(user_query.username == self.username)
        self.account = user_account.search(user_query.username == self.username)
        self.profile = user_profile.search(user_query.username == self.username)
        self.special_notes = ''
        self.extract_profile()
        self.sex = ''

    # extract the number of registered users
    @staticmethod
    def extract_passenger_number():
        return len(user_account.all())

    # extract the current user's booked activity for the given day
    def extract_activity(self, day):
        bookings = self.bookings[0]['activities'][day]
        return bookings

    # insert the new booked activity data into 'bookings'
    def book_activity(self, day, activity):
        bookings = self.bookings[0]['activities']
        bookings[day] = activity
        user_bookings.update({'activities': bookings}, user_query.username == self.username)

    # insert the new booked meals data into 'bookings'
    def book_meals(self, time, section, meal):
        bookings = self.bookings[0]['meals']
        bookings[activityscreen.ActivityScreenLayout.body.today][time][section] = meal
        user_bookings.update({'meals': bookings}, user_query.username == self.username)

    # extract the current user's booked meals for the given time (Breakfast/Lunch/Dinner)
    def extract_meals(self, time):
        bookings = self.bookings[0]['meals'][activityscreen.ActivityScreenLayout.body.today][time]
        bookings_list = []
        for each in bookings:
            bookings_list.append(bookings[each])
        return bookings_list

    # calculate and return how many day has passed since the start date of the current user
    def extract_date(self):
        if self.account[0]['start_date']:
            today = datetime.today()
            start_date = datetime.strptime(self.account[0]['start_date'], '%d-%m-%y')
            day_passed = (today - start_date).days
            return day_passed
        else:
            start_date = date.today().strftime('%d-%m-%y')
            user_account.update({'start_date': start_date, 'day': '1'}, user_query.username == self.username)
            return '1'

    # extract personal data of the current user from 'profile'
    def extract_profile(self):
        for each in user_profile.all():
            name = each['name'].split(' ')
            if (name[1] + name[0][0] + str(each['cabin number'])) == self.username:
                user = each
                # set attributes for later use
                self.special_notes = user['special notes']
                self.sex = user['sex']
                return user

    # extract the current user's booked activity for all of the days
    def extract_activities(self):
        bookings = self.bookings[0]['activities']
        return list(bookings.values())

    # update and insert new profile data from current user into 'profile'
    def update_profile(self, info):
        name = self.extract_profile()['name']
        user_profile.update(info, user_query.name == name)

    # update and insert new password data from current user into 'account'
    def update_password(self, psw):
        self.account[0]['password'] = pbkdf2_sha256.hash(psw)
        user_account.update(self.account[0], user_query.username == self.username)

    # register a new user from extracted inputs
    @staticmethod
    def register(info):
        f_name, l_name = info['name']
        username = f_name.capitalize() + l_name[0].upper() + info['cabin number']
        # check if username already exists or not
        if user_account.search(user_query.username == username):
            return
        profile = info
        account = {'username': username,
                   'password': pbkdf2_sha256.hash(info['password']),
                   'start_date': "",
                   'day': "",
                   'menu': ""}
        profile.pop('password')
        profile['name'] = l_name.capitalize() + ' ' + f_name.capitalize()
        activities = {}
        meals = {}
        for i in range(1, 15):
            activities[str(i)] = ""
            meals[str(i)] = meal_day
        bookings = {'username': account['username'],
                    'activities': activities,
                    'meals': meals}
        user_profile.insert(profile)
        user_account.insert(account)
        user_bookings.insert(bookings)
        # return generated account name for display
        return account['username']
