from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from tinydb import TinyDB, Query


class LoginScreenLayout(AnchorLayout):
    passenger = ''

    def __init__(self, **kwargs):
        super(LoginScreenLayout, self).__init__(**kwargs)

    def login(self):
        accounts = TinyDB('account')
        user = accounts.search(Query().username == self.usr_name_input.text_input.text)
        if user:
            if self.psw_input.psw_input.text_input.text == user[0]['password']:
                print('Login successful')
            else:
                print('Incorrect password')
        elif self.usr_name_input.text_input.text == '':
            print('Username is empty')
        else:
            print('Username does not exist')


class MyButton(Button):
    pass


class PasswordMask(MyButton):

    # on press show/hide password
    def on_release(self):
        self.psw_input.password = not self.psw_input.password
        self.text = "Hide" if self.text == "Show" else "Show"

