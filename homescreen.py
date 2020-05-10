from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock


class HomeScreenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(HomeScreenLayout, self).__init__(**kwargs)


class ProfileImage(Image):
    pass


class SideBar(BoxLayout):

    def __init__(self, **kwargs):
        super(SideBar, self).__init__(**kwargs)
        SideBar.body = self

    def display_date(self, date):
        self.day.text = 'DAY: ' + date


class KimberleyInfo(Button):

    def __init__(self, **kwargs):
        super(KimberleyInfo, self).__init__(**kwargs)

    def on_release(self):
        pass
