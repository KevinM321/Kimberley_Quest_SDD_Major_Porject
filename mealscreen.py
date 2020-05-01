from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem


class MealScreenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MealScreenLayout, self).__init__(**kwargs)


class MealPanelItem(TabbedPanelItem):

    def on_release(self):
        pass


class MealTabs(TabbedPanel):

    def generate_breakfast(self):
        pass

    def generate_lunch(self):
        pass

    def generate_dinner(self):
        pass


class MealBox(BoxLayout):
    pass
