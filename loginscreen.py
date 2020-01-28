from kivy.uix.boxlayout import BoxLayout
from tinydb import TinyDB, Query



class LoginScreenLayout(BoxLayout):
    customer = ''

    def __init__(self, **kwargs):
        super(LoginScreenLayout, self).__init__(**kwargs)

    def login(self):
        LoginScreenLayout.customer = customer_functions.Customer(self.usr_name_input.text_input.text,
                                                                 self.psw_input.psw_input.text_input.text)
        msg = LoginScreenLayout.customer.check()
