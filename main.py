from kivy.config import Config
# Config.set('graphics', 'resizable', False)
# Config.set('graphics', 'width', '1440')
# Config.set('graphics', 'height', '855')

from loginscreen import *
from homescreen import *
from activityscreen import *
from locationscreen import *
from mealscreen import *
from registerscreen import *
from helpscreen import *

import kivy
# from kivy.core.window import Window
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
kivy.require("1.11.1")

# load the screen files
Builder.load_file('loginscreen.kv')
Builder.load_file('homescreen.kv')
Builder.load_file('activityscreen.kv')
Builder.load_file('locationscreen.kv')
Builder.load_file('mealscreen.kv')
Builder.load_file('registerscreen.kv')
Builder.load_file('helpscreen.kv')


# class  containing the screenmanger of all screens
class KQScreenManager(ScreenManager):

    # detect screen change and call related functions
    def on_current(self, instance, value):
        super(KQScreenManager, self).on_current(instance, value)
        if value == 'activity_screen':
            del ErrorPopup.single
            if DropDownMenu.body.dropped:
                DropDownMenu.body.drop_down()
            body = ActivityScreenLayout.body
            body.add_widget(ErrorPopup())
            body.initiated += 1
            body.load(day=str(body.chosen_day))
        if value == 'login_screen':
            LoginScreenLayout.body.login_box.psw_button.text = 'Show'
            LoginScreenLayout.body.login_box.psw_input.password = True
            LoginScreenLayout.body.add_widget(ErrorPopup())
        if value == 'meal_screen':
            del ErrorPopup.single
            MealScreenLayout.body.add_widget(ErrorPopup())
            for each in MealPanelItem.get_widgets('panel'):
                Clock.schedule_once(lambda dt: each.update_menu(),.1)
                if each.text == MealPanelItem.selected:
                    selected = each
            Clock.schedule_once(lambda dt: selected.update_menu(), .125)
            for each in MealPanelItem.get_widgets('panel'):
                Clock.schedule_once(lambda dt: each.find_stored(), .25)
        if value == 'home_screen':
            del ErrorPopup.single
            HomeScreenLayout.body.add_widget(ErrorPopup())
            HomeScreenLayout.body.update_activity_today()


# creates the program and run it
class KimberleyQuestApp(App):

    def build(self):
        self.title = 'Kimberley Quest'
        self.icon = 'res/system/jojo_icon.png'
        return KQScreenManager()


home = KimberleyQuestApp()
home.run()
