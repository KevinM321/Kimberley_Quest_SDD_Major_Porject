from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from tinydb import TinyDB, Query
from kivy.clock import Clock
import loginscreen


class MealScreenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MealScreenLayout, self).__init__(**kwargs)


class MealPanelItem(TabbedPanelItem):

    def __init__(self, **kwargs):
        super(MealPanelItem, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.build_menu(), 0.5)
        MealPanelItem.selected = 'Breakfast'

    def build_menu(self):
        menu_data = TinyDB('menu', indent=2).all()[0]
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
                num += 1

    def on_release(self, *largs):
        super(MealPanelItem, self).on_release(*largs)
        self.update_menu()
        MealPanelItem.selected = self.text


class MealTabs(TabbedPanel):

    def __init__(self, **kwargs):
        super(MealTabs, self).__init__(**kwargs)


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


class UpdateButton(Button):

    def on_release(self):
        MealPanelItem.body.update_selection()
