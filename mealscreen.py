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
        Clock.schedule_once(lambda dt: self.build_menu(), 0.5)

    def build_menu(self):
        menu_data = TinyDB('menu', indent=2).all()[0]
        menu_meal = menu_data[self.text]
        for each in menu_meal:
            item = MenuItem()
            item.name.text = each
            item.desc.text = menu_meal[each]
            self.meal_box.main_meal.add_widget(item)
        menu_snack = menu_data['Snacks']
        for each in menu_snack:
            item = MenuItem()
            item.name.text = each
            item.desc.text = menu_snack[each]
            self.meal_box.snacks.add_widget(item)
        menu_drink = menu_data['Drinks']
        for each in menu_drink:
            item = MenuItem()
            item.name.text = each
            item.desc.text = menu_drink[each]
            self.meal_box.drinks.add_widget(item)


class MealTabs(TabbedPanel):
    pass


class MealBox(BoxLayout):
    pass
    # def __init__(self, **kwargs):
    #     super(MealBox, self).__init__(**kwargs)
    #     MealBox.body = self
    #
    # def generate_menu(self, meal):
    #     menu_data = TinyDB('menu', indent=2)
    #     menu = menu_data.all()[0][meal]
    #     self.main_meal.add_widget(Button(text='lol'))


class MenuItem(BoxLayout):

    def __init__(self, **kwargs):
        super(MenuItem, self).__init__(**kwargs)
