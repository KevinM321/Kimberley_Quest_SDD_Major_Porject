import kivy

from kivy.config import Config
# from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
kivy.require("1.11.1")

Config.set('graphics', 'resizable', False)
# set to 1440 when finished
Config.set('graphics', 'width', '1000')
# set to 790 when finished
Config.set('graphics', 'height', '600')
# Window.clearcolor = (1, 1, 1, 1)
Builder.load_file('loginscreen.kv')


class LoginScreenLayout(BoxLayout):
    pass


class KimberlyQuestApp(App):

    def build(self):
        return LoginScreenLayout()


home = KimberlyQuestApp()
home.run()
