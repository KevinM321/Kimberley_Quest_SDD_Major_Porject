from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button


class HomeScreenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(HomeScreenLayout, self).__init__(**kwargs)


class ProfileImage(Image):
    pass


class KimberleyInfo(Button):

    def __init__(self, **kwargs):
        super(KimberleyInfo, self).__init__(**kwargs)
