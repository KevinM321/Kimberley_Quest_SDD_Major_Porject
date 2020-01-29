from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from tinydb import TinyDB, Query


class LoginScreenLayout(BoxLayout):
    passenger = ''

    def __init__(self, **kwargs):
        super(LoginScreenLayout, self).__init__(**kwargs)

    # def login(self):
    #     LoginScreenLayout.customer = passenger_functions.Passenger(self.usr_name_input.text_input.text,
    #                                                                self.psw_input.psw_input.text_input.text)
    #     msg = LoginScreenLayout.customer.check()


class MyButton(Button):
    pass


class PasswordMask(MyButton):

    # on press show/hide password
    def on_release(self):
        self.psw_input.password = not self.psw_input.password
        self.text = "Hide" if self.text == "Show" else "Show"

