from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.label import Label
from tinydb import TinyDB
from kivy.clock import Clock
import loginscreen

about_cuisine = "Cuisine on board Kimberley Quest II is simply delicious.\n" \
                "All meals are prepared by our talented chef in the fully equipped gourmet galley, \n" \
                "offering an array of fresh fish, seafood, the highest quality meats, \n" \
                "freshly baked breads and some of the best local produce. \n\n" \
                "The menu is designed with variety in mind and you can expect\n" \
                "a minimum of three meals each day with tasty treats and snacks in between meals.\n" \
                "When our guests catch fresh fish, oysters or crabs, you can expect to see them on the menu!\n\n" \
                "With both indoor and outdoor dining areas, \n" \
                "you can relax while enjoying the amazing cuisine and the ever-changing backdrop. \n" \
                "The air conditioned indoor dining area offers a large open dining/lounge space\n" \
                "and is an excellent location to sit down and enjoy a delicious meal\n" \
                "with views through our full length windows,\n" \
                "whilst the outdoor dining area offers a relaxed environment complete with a soft ocean breeze.\n\n" \
                "We cater for all dietary requirements and special needs.\n" \
                "We have endless fresh drinking water, tea,\n" \
                "coffee and an espresso machine available 24 hours a day.\n\n" \
                "Kimberley Quest II is a fully licenced vessel and\n" \
                "beverages can be pre-ordered prior to your departures. BYO is also an option."


class MealScreenLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(MealScreenLayout, self).__init__(**kwargs)
        MealScreenLayout.body = self

    @staticmethod
    def info_popup():
        popup = Popup(size_hint=(.6, .6),
                      content=Label(text=about_cuisine,
                                    color=(0, 0, 0, 1),
                                    font_size=16.75),
                      separator_color=(.1, .1, 1, .775),
                      title='Cuisine',
                      title_size=30,
                      title_color=(0, 0, 0, 1),
                      pos_hint={'x': .3, 'y': .2},
                      background='res/system/white_background.jpg')
        popup.open()


class MealPanelItem(TabbedPanelItem):

    def __init__(self, **kwargs):
        super(MealPanelItem, self).__init__(**kwargs)
        MealPanelItem.body = self
        MealPanelItem.selected = 'Breakfast'

    def build_menu(self, menu):
        menu_data = TinyDB('menu', indent=2).all()[int(menu)-1]
        menu_meal = menu_data[self.text]
        for each in menu_meal:
            item = MenuItem()
            item.name.text = each
            item.desc.text = menu_meal[each]
            item.checkbox_group.group = 'main_meal'
            self.meal_box.main_meal.add_widget(item)
        menu_snack = menu_data['Snacks']
        for each in menu_snack:
            item = MenuItem()
            item.name.text = each
            item.desc.text = menu_snack[each]
            item.checkbox_group.group = 'snacks'
            self.meal_box.snacks.add_widget(item)
        menu_drink = menu_data['Drinks']
        for each in menu_drink:
            item = MenuItem()
            item.name.text = each
            item.desc.text = menu_drink[each]
            item.checkbox_group.group = 'drinks'
            self.meal_box.drinks.add_widget(item)
        MealPanelItem.body = self

    def remove_menu(self):
        for each in self.meal_box.main_meal.children[:-1]:
            self.meal_box.main_meal.remove_widget(each)
        for each in self.meal_box.snacks.children[:-1]:
            self.meal_box.snacks.remove_widget(each)
        for each in self.meal_box.drinks.children[:-1]:
            self.meal_box.drinks.remove_widget(each)

    def update_selection(self):
        user = loginscreen.LoginScreenLayout.body.user
        for each in self.get_widgets('panel'):
            if each.state == 'down':
                time = each.text
                selected_panel = each
        selected = self.find_selected(selected_panel.meal_box.main_meal.children[0:3])
        if selected:
            selected_item = selected_panel.meal_box.main_meal.children[selected-1].name.text
        else:
            selected_item = ''
        user.book_meals(time, 'main_meal', selected_item)
        selected = self.find_selected(selected_panel.meal_box.snacks.children[0:3])
        if selected:
            selected_item = selected_panel.meal_box.snacks.children[selected - 1].name.text
        else:
            selected_item = ''
        user.book_meals(time, 'snacks', selected_item)
        selected = self.find_selected(selected_panel.meal_box.drinks.children[0:3])
        if selected:
            selected_item = selected_panel.meal_box.drinks.children[selected - 1].name.text
        else:
            selected_item = ''
        user.book_meals(time, 'drinks', selected_item)

    @staticmethod
    def find_selected(menu_list):
        i = 1
        for each in menu_list:
            if each.checkbox_group.state == 'down':
                return i
            i += 1
        return None

    def update_menu(self):
        user = loginscreen.LoginScreenLayout.body.user
        selected = user.extract_meals(self.text)
        num = 0
        for each in self.meal_box.children:
            part = each.children[0:3]
            part.reverse()
            for i in part:
                section = i.children[0:3]
                section.reverse()
                for e in section:
                    if e.name.text == selected[num]:
                        if e.checkbox_group.state != 'down':
                            e.checkbox_group.state = 'down'
                    else:
                        e.checkbox_group.state = 'normal'
                num += 1

    def on_release(self, *largs):
        super(MealPanelItem, self).on_release(*largs)
        self.update_menu()
        MealPanelItem.selected = self.text


class MealTabs(TabbedPanel):

    def __init__(self, **kwargs):
        super(MealTabs, self).__init__(**kwargs)
        MealTabs.body = self


class MealBox(BoxLayout):
    pass


class MenuItem(BoxLayout):

    def __init__(self, **kwargs):
        super(MenuItem, self).__init__(**kwargs)


class UpdateButton(Button):

    def on_release(self):
        MealPanelItem.body.update_selection()
