from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from tinydb import TinyDB, Query
from kivy.uix.screenmanager import FadeTransition
from passlib.hash import pbkdf2_sha256
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.animation import Animation
import user_manager
import activityscreen

accounts = TinyDB('account', indent=2)


class LoginScreenLayout(RelativeLayout):
    passenger = ''

    def __init__(self, **kwargs):
        super(LoginScreenLayout, self).__init__(**kwargs)
        LoginScreenLayout.body = self
        Clock.schedule_once(lambda dt: OpenAnimation.body.animate(), 3)

    def login(self):
        activityscreen_body = activityscreen.ActivityScreenLayout.body
        self.login_box.usr_name_input.input_box.text = 'LuffyM9'
        self.login_box.psw_input.input_box.text = '1234'
        LoginScreenLayout.body.account = accounts.search(Query().username == self.login_box.usr_name_input.input_box.text)
        if LoginScreenLayout.body.account:
            if self.login_box.psw_input.input_box.text:
                if pbkdf2_sha256.verify(self.login_box.psw_input.input_box.text,
                                        LoginScreenLayout.body.account[0]['password']):
                    self.screen_manager.transition = FadeTransition()
                    LoginScreenLayout.body.user = user_manager.User(self.login_box.usr_name_input.input_box.text)
                    day_passed = LoginScreenLayout.body.user.extract_date()
                    if day_passed == '1':
                        activityscreen_body.today = day_passed
                        activityscreen_body.chosen_day = day_passed
                    else:
                        activityscreen_body.today = str(day_passed + 1)
                        activityscreen_body.chosen_day = str(day_passed + 1)
                    activityscreen.ActivityMainScreen.body.chosen_day.text = 'Day ' + activityscreen_body.chosen_day
                    activityscreen.ActivityMainScreen.body.today.text = 'Day ' + activityscreen_body.today
                    self.login_box.usr_name_input.input_box.text = ''
                    self.login_box.psw_input.input_box.text = ''
                    self.screen_manager.current = 'activity_screen'
                else:
                    ErrorPopup.display('Incorrect password')
            else:
                ErrorPopup.display('Password is empty')
        elif self.login_box.usr_name_input.input_box.text == '':
            ErrorPopup.display('Username is empty')
        else:
            ErrorPopup.display('Username does not exist')


class ErrorPopup(RelativeLayout):

    single = None

    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs.pop('name')
        super(ErrorPopup, self).__init__(**kwargs)
        ErrorPopup.single = self

    @classmethod
    def display(cls, text):
        if not cls.single.children:
            popup = ErrorLabel(text=text,
                               pos=(1050, 650),
                               size_hint=(None, None),
                               size=(500, 125))
            cls.single.add_widget(popup)
        else:
            cls.single.clear_widgets()
            cls.single.display(text)


class ErrorLabel(Label):

    def __init__(self, **kwargs):
        super(ErrorLabel, self).__init__(**kwargs)
        self.animation = ''
        self.move_left()

    def move_left(self):
        self.animation = Animation(x=565, duration=0.75)
        self.animation.start(self)
        Clock.schedule_once(lambda dt: self.wait(), 3)

    def move_right(self):
        self.animation = Animation(x=1050, duration=0.75)
        self.animation.start(self)

    def wait(self):
        Clock.schedule_once(lambda dt: self.move_right())


class OpenAnimation(Image):

    def __init__(self, **kwargs):
        super(OpenAnimation, self).__init__(**kwargs)
        OpenAnimation.body = self
        self.animation = ''

    def animate(self):
        self.animation = Animation(x=1050, duration=4, transition='out_cubic')
        self.animation.start(OpenAnimation.body)
