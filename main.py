import kivy
import loginscreen

from kivy.config import Config
# from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
kivy.require("1.11.1")

# open when finished
# Config.set('graphics', 'resizable', False)
# Config.set('graphics', 'width', '1440')
# Config.set('graphics', 'height', '790')
# Window.clearcolor = (1, 1, 1, 1)
Builder.load_file('loginscreen.kv')


class LoginScreenLayout(BoxLayout):
    pass


class KimberlyQuestApp(App):

    def build(self):
        return LoginScreenLayout()


home = KimberlyQuestApp()
home.run()
