from kivy.uix.boxlayout import BoxLayout
from tinydb import TinyDB, Query
# passenger_profile = TinyDB('profile')
# passenger_profile.insert({'name': 'Kevin'})
# print(passenger_profile.all())


class LoginScreenLayout(BoxLayout):
    customer = ''

    def __init__(self, **kwargs):
        super(LoginScreenLayout, self).__init__(**kwargs)

    # called when login button pressed
    def login(self):
        # create an instance of a customer using customer_functions and saves it as customer in LoginScreenLayout
        LoginScreenLayout.customer = customer_functions.Customer(self.usr_name_input.text_input.text,
                                                                 self.psw_input.psw_input.text_input.text)
        # use the Customer class function check() using username and password input
        msg = LoginScreenLayout.customer.check()
        # if login not successful create a popup containing the error message
        if msg:
            Popup(title='', content=Label(text=msg), size_hint=(.5, .5)).open()
        # else clear the login screen input box texts, change screen transition and screen
        else:
            self.screen_manager.transition = CardTransition(direction='up', mode='pop')
            self.usr_name_input.text_input.text = ''
            self.psw_input.psw_input.text_input.text = ''
            self.screen_manager.current = 'shop_screen'
            # check if a week has passed since last lucky draw, if so enable lucky draw
            if LoginScreenLayout.customer.details[6] != 'lucky_draw_date':
                date_now = datetime.now().date()
                drawn_date = LoginScreenLayout.customer.details[6].date()
                delta = date_now - drawn_date
                if delta.days >= 7:
                    LoginScreenLayout.customer.update_account('', '', '', '', True, '')