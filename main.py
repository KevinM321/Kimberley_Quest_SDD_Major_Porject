from kivy.config import Config
from loginscreen import *
from homescreen import *
from activityscreen import *
from loginscreen import *

import kivy
# from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
kivy.require("1.11.1")

# open when finished
# Config.set('graphics', 'resizable', False)
# Config.set('graphics', 'width', '1440')
# Config.set('graphics', 'height', '790')
# Window.clearcolor = (1, 1, 1, 1)
Builder.load_file('loginscreen.kv')
Builder.load_file('homescreen.kv')
Builder.load_file('activityscreen.kv')
Builder.load_file('locationscreen.kv')
Builder.load_file('mealscreen.kv')


# class KQScreenManager(ScreenManager):
#     pass


class KimberlyQuestApp(App):

    def build(self):
        return HomeScreenLayout()


home = KimberlyQuestApp()
home.run()
