from kivy.config import Config
# Config.set('graphics', 'resizable', False)
# Config.set('graphics', 'width', '1440')
# Config.set('graphics', 'height', '855')

from kivy.config import Config
from loginscreen import *
from homescreen import *
from activityscreen import *
from locationscreen import *
from mealscreen import *

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


class KQScreenManager(ScreenManager):

    def on_current(self, instance, value):
        super(KQScreenManager, self).on_current(instance, value)
        system_popup = ErrorPopup()
        if value == 'activity_screen':
            LoginScreenLayout.body.remove_widget(system_popup)
            ActivityScreenLayout.body.add_widget(system_popup)
            ActivityScreenLayout.body.load(day=str(ActivityScreenLayout.body.today))
        if value == 'login_screen':
            LoginScreenLayout.body.add_widget(system_popup)


class KimberleyQuestApp(App):

    def build(self):
        self.title = 'Kimberley Quest'
        self.icon = 'res/system/jojo_icon.png'
        return KQScreenManager()


home = KimberleyQuestApp()
home.run()
