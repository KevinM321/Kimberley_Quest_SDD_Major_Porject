from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from tinydb import TinyDB, Query
from kivy.uix.screenmanager import FadeTransition
from passlib.hash import pbkdf2_sha256
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.animation import Animation
from random import randint
import user_manager
import activityscreen
import homescreen
import mealscreen


class LoginScreenLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(LoginScreenLayout, self).__init__(**kwargs)
        LoginScreenLayout.body = self
        Clock.schedule_once(lambda dt: OpenAnimation.body.animate(), 3)
        Clock.schedule_once(lambda dt: self.body.login_box.register_button.bind(on_release=self.to_register), .25)
        self.ls_animation = ''
        self.rs_animation = ''

    def to_register(self, args):
        self.ls_animation = Animation(x=-1250, duration=0.75)
        self.rs_animation = Animation(x=0, duration=0.75)
        self.ls_animation.start(LoginScreenLayout.body.login_screen_layout)
        self.rs_animation.start(LoginScreenLayout.body.register_screen_layout)

    def to_login(self, username):
        self.ls_animation = Animation(x=0, duration=0.75)
        self.rs_animation = Animation(x=1250, duration=0.75)
        self.ls_animation.start(LoginScreenLayout.body.login_screen_layout)
        self.rs_animation.start(LoginScreenLayout.body.register_screen_layout)
        if username:
            Clock.schedule_once(lambda dt: self.register_successful(username), 0.8)

    @staticmethod
    def register_successful(username):
        content = RegisterSuccessfulLayout(username=username)
        popup = Popup(title='Register Successful',
                      content=content,
                      separator_color=(.1, .1, 1, .775),
                      title_size=30,
                      size_hint=(.4, .5),
                      title_color=(0, 0, 0, 1),
                      background='res/system/white_background.jpg',
                      auto_dismiss=False)
        content.btn.bind(on_release=popup.dismiss)
        popup.open()

    def login(self):
        activityscreen_body = activityscreen.ActivityScreenLayout.body
        # self.login_box.usr_name_input.input_box.text = 'PeterS1'
        # self.login_box.psw_input.input_box.text = '1234'
        accounts = TinyDB('account', indent=2)
        self.body.account = accounts.search(Query().username == self.login_box.usr_name_input.input_box.text)
        if LoginScreenLayout.body.account:
            if self.login_box.psw_input.input_box.text:
                if pbkdf2_sha256.verify(self.login_box.psw_input.input_box.text,
                                        LoginScreenLayout.body.account[0]['password']):
                    self.body.user = user_manager.User(self.login_box.usr_name_input.input_box.text)
                    day_passed = LoginScreenLayout.body.user.extract_date()
                    if day_passed == '1':
                        activityscreen_body.today = day_passed
                        activityscreen_body.chosen_day = day_passed
                    else:
                        activityscreen_body.today = str(day_passed + 1)
                        activityscreen_body.chosen_day = str(day_passed + 1)
                        if (day_passed + 1) > 14:
                            Popup(title='Kimberley Quest',
                                  content=Label(text='Your Trip Has Ended',
                                                font_size=35,
                                                bold=True,
                                                color=(0, 0, 0, 1)),
                                  separator_color=(.1, .1, 1, .775),
                                  title_size=30,
                                  size_hint=(.4, .5),
                                  title_color=(0, 0, 0, 1),
                                  background='res/system/white_background.jpg').open()
                            return
                    activityscreen.ActivityMainScreen.body.chosen_day.text = 'Day ' + activityscreen_body.chosen_day
                    activityscreen.ActivityMainScreen.body.today.text = 'Day ' + activityscreen_body.today
                    self.login_box.usr_name_input.input_box.text = ''
                    self.login_box.psw_input.input_box.text = ''
                    self.screen_manager.transition = FadeTransition()
                    self.screen_manager.current = 'home_screen'
                    account = accounts.search(Query().username == LoginScreenLayout.body.user.username)[0]
                    if account['day'] == activityscreen_body.today:
                        for each in mealscreen.MealPanelItem.get_widgets('panel'):
                            each.build_menu(account['menu'])
                    else:
                        account['day'] = activityscreen_body.today
                        account['menu'] = str(randint(1, 5))
                        accounts.update(account, Query().username == LoginScreenLayout.body.user.username)
                        for each in mealscreen.MealPanelItem.get_widgets('panel'):
                            each.build_menu(account['menu'])
                    homescreen.HomeScreenLayout.body.update_profile(self.body.user)
                    homescreen.ProfileImage.body.build()
                    homescreen.SideBar.display_date(activityscreen_body.today)
                else:
                    ErrorPopup.display('Incorrect password', '')
            else:
                ErrorPopup.display('Password is empty', '')
        elif self.login_box.usr_name_input.input_box.text == '':
            ErrorPopup.display('Username is empty', '')
        else:
            ErrorPopup.display('Username does not exist', '')


class RegisterSuccessfulLayout(BoxLayout):

    username = StringProperty()

    def __init__(self, **kwargs):
        super(RegisterSuccessfulLayout, self).__init__(**kwargs)
        self.usr_label.text = kwargs.pop('username')


class ErrorPopup(RelativeLayout):

    single = None

    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs.pop('name')
        super(ErrorPopup, self).__init__(**kwargs)
        ErrorPopup.single = self

    @classmethod
    def display(cls, text, subtext):
        popup = ErrorLabel(pos=(1050, 700),
                           size_hint=(None, None),
                           size=(500, 125))
        popup.error_text.text = text
        if subtext:
            popup.sub_text.text = subtext
        cls.single.add_widget(popup)


class ErrorLabel(BoxLayout):

    def __init__(self, **kwargs):
        super(ErrorLabel, self).__init__(**kwargs)
        self.animation = ''
        Clock.schedule_once(lambda dt: self.move_left(), .25)

    def move_left(self):
        self.animation = Animation(x=565, duration=0.75)
        self.animation.start(self)
        Clock.schedule_once(lambda dt: self.wait(), 3)

    def move_right(self):
        self.animation = Animation(x=1050, duration=0.75)
        self.animation.start(self)

    def wait(self):
        self.move_right()


class OpenAnimation(Image):

    def __init__(self, **kwargs):
        super(OpenAnimation, self).__init__(**kwargs)
        OpenAnimation.body = self
        self.animation = ''

    def animate(self):
        self.animation = Animation(x=1050, duration=4, transition='out_cubic')
        self.animation.start(OpenAnimation.body)
