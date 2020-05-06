from tinydb import TinyDB, Query
from datetime import date, datetime

user_query = Query()
user_bookings = TinyDB('bookings', indent=2)
user_account = TinyDB('account', indent=2)


class User:

    def __init__(self, username):
        self.username = username
        self.bookings = user_bookings.search(user_query.username == self.username)
        self.account = user_account.search(user_query.username == self.username)

    def extract_activity(self, day):
        bookings = self.bookings[0]['activities'][day]
        return bookings

    def book_activity(self, day, activity):
        bookings = self.bookings[0]['activities']
        bookings[day] = activity
        user_bookings.update({'activities': bookings}, user_query.username == self.username)

    def book_meals(self, day, meals):
        pass

    def extract_date(self):
        if self.account[0]['start_date']:
            today = datetime.today()
            start_date = datetime.strptime(self.account[0]['start_date'], '%d-%m-%y')
            day_passed = (today - start_date).days
            return day_passed
        else:
            start_date = date.today().strftime('%d-%m-%y')
            user_account.update({'start_date': start_date}, user_query.username == self.username)
            return '1'
