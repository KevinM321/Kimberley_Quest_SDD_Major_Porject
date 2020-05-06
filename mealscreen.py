from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from tinydb import TinyDB, Query
from kivy.clock import Clock


class MealScreenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MealScreenLayout, self).__init__(**kwargs)


class MealPanelItem(TabbedPanelItem):

    def __init__(self, **kwargs):
        super(MealPanelItem, self).__init__(**kwargs)

    def on_release(self):
        MealBox.body.generate_menu(self.text)


class MealTabs(TabbedPanel):
    pass


class MealBox(BoxLayout):

    def __init__(self, **kwargs):
        super(MealBox, self).__init__(**kwargs)
        MealBox.body = self

    def generate_menu(self, meal):
        menu_data = TinyDB('menu', indent=2)
        menu = menu_data.all()[0][meal]
        self.main_meal.add_widget(Button(text='lol'))
