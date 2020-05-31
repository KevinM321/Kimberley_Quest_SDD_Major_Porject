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
import activityscreen

# Kimberley Quest cuisine information
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

dietary_requirements = 'Vegetarian food only'


# contains the layout for the meal selection screen
class MealScreenLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(MealScreenLayout, self).__init__(**kwargs)
        MealScreenLayout.body = self

    # display a popup containing information about the cuisine
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


# class containing three instances (Breakfast/Lunch/Dinner)
class MealPanelItem(TabbedPanelItem):

    def __init__(self, **kwargs):
        super(MealPanelItem, self).__init__(**kwargs)
        MealPanelItem.body = self
        MealPanelItem.selected = 'Breakfast'
        MealPanelItem.selected_main_meal = ''

    # extract today's menu from 'menu', then create items and add into each section
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

    # find the stored item's instance in the main meal layout and store that instance
    def find_stored(self):
        for each in self.meal_box.main_meal.children[:-1]:
            if each.name.text == loginscreen.LoginScreenLayout.body.user.extract_meals(MealPanelItem.selected)[0]:
                MealPanelItem.selected_main_meal = each

    # remove all widgets of each section
    def remove_menu(self):
        for each in self.meal_box.main_meal.children[:-1]:
            self.meal_box.main_meal.remove_widget(each)
        for each in self.meal_box.snacks.children[:-1]:
            self.meal_box.snacks.remove_widget(each)
        for each in self.meal_box.drinks.children[:-1]:
            self.meal_box.drinks.remove_widget(each)

    # find the selected item in each section of an instance of this class, and update each selected item into 'bookings'
    def update_selection(self):
        user = loginscreen.LoginScreenLayout.body.user
        # loop for finding the selected time (Breakfast/Lunch/Dinner)
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

    # find the selected item from a section and return its position
    @staticmethod
    def find_selected(menu_list):
        i = 1
        for each in menu_list:
            if each.checkbox_group.state == 'down':
                return i
            i += 1
        return None

    # refresh the menu by selecting the items that has been extracted from the 'bookings' file for each section
    def update_menu(self):
        user = loginscreen.LoginScreenLayout.body.user
        selected = user.extract_meals(self.text)
        num = 0
        # loop through three sections (main meal, snacks, drinks)
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

    # when an instance of this class is called, refresh that instance then store that instance
    def on_release(self, *largs):
        super(MealPanelItem, self).on_release(*largs)
        self.update_menu()
        MealPanelItem.selected = self.text
        self.find_stored()


# class containing and grouping the three MealPanelItem instances
class MealTabs(TabbedPanel):

    def __init__(self, **kwargs):
        super(MealTabs, self).__init__(**kwargs)
        MealTabs.body = self


# class containing the layout for each MealPanelItem
class MealBox(BoxLayout):
    pass


# class containing the layout for each selectable item
class MenuItem(BoxLayout):

    def __init__(self, **kwargs):
        super(MenuItem, self).__init__(**kwargs)


# class for the update button
class UpdateButton(Button):

    selected = ''

    # when pressed check if update is possible and updates
    def on_release(self):
        # check if the current user has dietary requirements
        if loginscreen.LoginScreenLayout.body.user.special_notes == dietary_requirements:
            if self.check():
                # warning for choosing a non-dietary meal
                content = activityscreen.WarningLayout(text='The selected main meal is not Vegetarian\n'
                                                            'Do you wish to proceed?')
                popup = Popup(size_hint=(.45, .55),
                              separator_color=(.1, .1, 1, .775),
                              content=content,
                              title='Warning',
                              auto_dismiss=False,
                              title_size=30,
                              title_color=(0, 0, 0, 1),
                              pos_hint={'x': .375, 'y': .2125},
                              background='res/system/white_background.jpg')
                content.proceed_btn.bind(on_release=popup.dismiss)
                content.stop_btn.bind(on_release=popup.dismiss)
                content.proceed_btn.bind(on_release=self.proceed)
                content.stop_btn.bind(on_release=self.stop)
                popup.open()
            else:
                MealPanelItem.body.update_selection()
        else:
            MealPanelItem.body.update_selection()

    # continue update of non-dietary meal
    @staticmethod
    def proceed(args):
        MealPanelItem.body.update_selection()

    # stop update of non-dietary meal
    def stop(self, args):
        if MealPanelItem.body.selected_main_meal:
            MealPanelItem.body.selected_main_meal.checkbox_group.state = 'down'
        else:
            self.selected.checkbox_group.state = 'normal'

    # check if the selected meal fits dietary requirements or not
    @staticmethod
    def check():
        for each in MealPanelItem.get_widgets('panel'):
            if each.state == 'down':
                time = each.text
                selected_panel = each
        selected = MealPanelItem.find_selected(selected_panel.meal_box.main_meal.children[0:3])
        # check if any meal is selected or not
        if selected:
            UpdateButton.selected = selected_panel.meal_box.main_meal.children[selected-1]
            if 'Vegetarian' not in selected_panel.meal_box.main_meal.children[selected-1].name.text:
                return True
            else:
                return False
