from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.graphics import Line, Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
import loginscreen
import datetime

activity = {1: '', 2: '', 3: '',
            4: ['res/activity/glass_bottom_boat.jpg', 'res/activity/fishing.jpg', 'res/activity/scuba_diving.jpg'],
            5: ['res/activity/lying_in_stream.jpg', 'res/activity/paddleboarding.jpg',
                'res/activity/catch_and_cook.jpg'],
            6: '',
            7: ['res/activity/relax_on_the_beach.jpg', 'res/activity/bushwalking.jpg',
                'res/activity/holding_a_large_fish_and_taking_a_photo.jpg'],
            8: ['res/activity/glass_bottom_boat.jpg', 'res/activity/heli_ride.jpg', 'res/activity/kayak.jpg'],
            9: ['res/activity/boat_ride.jpg', 'res/activity/bushwalking.jpg', 'res/activity/catch_and_cook.jpg'],
            10: '',
            11: ['res/activity/relax_on_the_beach.jpg', 'res/activity/heli_ride.jpg', 'res/activity/scuba_diving.jpg'],
            12: '',
            13: ['res/activity/boat_ride.jpg', 'res/activity/paddleboarding.jpg', 'res/activity/kayak.jpg'],
            14: ''}
activity_names = {'res/activity/scuba_diving.jpg': ['Scuba Dive', 'Physical challenge', '160',
                                                    'Enjoy the whole day out in a SCUBA diving adventure. \n'
                                                    'You will be transferred from the Kimberley Quest \n'
                                                    'to a purpose-built pontoon, \n'
                                                    'where you will dive and lunch in style. \n'
                                                    '(Participants must be PADI \n'
                                                    'certified for Open Water Diving).'],
                  'res/activity/glass_bottom_boat.jpg': ['Glass Bottom Boat ride', 'Easy going', '120',
                                                         'Experience a day on the reef and a \n'
                                                         'short walk on one of the many remote beaches. \n'
                                                         'Our glass bottom boat experience is second to none.'],
                  'res/activity/fishing.jpg': ['Fishing', 'Moderate', '40',
                                               'Walk to a fishing spot where the fish are always biting. \n'
                                               'Lunch will be the fish caught and cooked on the spot.'],
                  'res/activity/lying_in_stream.jpg': ['Lying In Stream', 'Easy going', '300', ''],
                  'res/activity/holding_a_large_fish_and_taking_a_photo.jpg': ['Holding A Large Fish And Taking A Photo'
                                                                               , 'Physical challenge', '300',
                                                                               'Enjoy the once in a '
                                                                               'life time experience\n'
                                                                               'of taking a photo '
                                                                               'while holding a fish\n'
                                                                               'larger than your head!'],
                  'res/activity/boat_ride.jpg': ['Landscape Exploration Boat ride', 'Easy going', '120', ''],
                  'res/activity/bushwalking.jpg': ['Bushwalking', 'Moderate', '40', ''],
                  'res/activity/relax_on_the_beach.jpg': ['Relax On The Beach', 'Easy going', '10', ''],
                  'res/activity/catch_and_cook.jpg': ['Catch And Cook', 'Physical challenge', '60', ''],
                  'res/activity/paddleboarding.jpg': ['Paddleboarding', 'Moderate', '60', ''],
                  'res/activity/heli_ride.jpg': ['Helicopter Ride', 'Moderate', '300',
                                                 'Take our helicopter and enjoy an amazing ride \n'
                                                 'showcasing unique and beautiful scenery of '],
                  'res/activity/kayak.jpg': ['Kayaking', 'Physical challenge', '60', '']}

physically_challenged = ('Difficulty walking long distances', 'Pacemaker \u2013 Heart Issues')


class ActivityScreenLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(ActivityScreenLayout, self).__init__(**kwargs)
        ActivityScreenLayout.body = self
        self.initiated = 0
        self.booked_activity = ''
        self.today = ''
        self.no_activity = ''
        self.end_booking = ''
        self.color = (Color(rgba=(.25, .25, .25, .7)))
        self.chosen_day = ''
        self.can_book = True
        Clock.schedule_once(lambda dt: self.build_no_activity(), .5)

    def build_no_activity(self):
        self.no_activity = Rectangle(size=self.activities.size, pos=self.activities.pos)

    def load(self, *args, **kwargs):
        day = kwargs.pop("day")
        if (self.no_activity and self.color) in self.activities.canvas.children:
            self.activities.canvas.remove(self.no_activity)
            self.activities.canvas.remove(self.color)
        self.booked_activity = loginscreen.LoginScreenLayout.body.user.extract_activity(day)
        activity_today = activity[int(day)]
        self.activities.clear_widgets()
        self.name.clear_widgets()
        self.info.clear_widgets()
        ActivityMainScreen.body.select.clear_widgets()
        if activity_today:
            self.activities.add_widget(Label(size_hint_x=0.15))
            self.name.add_widget(Label(size_hint_x=0.15))
            self.info.add_widget(Label(size_hint_x=0.15))
            for each in activity_today:
                self.activities.add_widget(ActivityImage(source=each))
                self.name.add_widget(ActivityName(text=activity_names[each][0]))
                self.info.add_widget(ActivityInfo(source=each, name=activity_names[each][0]))
            self.activities.add_widget(Label(size_hint_x=0.0))
            self.name.add_widget(Label(size_hint_x=0.01))
            self.info.add_widget(Label(size_hint_x=0.01))
            Clock.schedule_once(self.select_saved)
            if int(loginscreen.LoginScreenLayout.body.user.extract_date()) + 3 > int(self.chosen_day):
                if self.initiated > 1:
                    self.display_reminder('Booking has ended')
                else:
                    Clock.schedule_once(lambda dt: self.set_reminder())
                    self.display_reminder('Booking has ended')
        else:
            if self.initiated > 1:
                self.display_reminder('No activities today')
            else:
                Clock.schedule_once(lambda dt: self.set_reminder())
                self.display_reminder('No activities today')

    def select_saved(self, *args):
        for each in self.activities.children[1: 4]:
            if each.source == self.booked_activity:
                each.state = 'down'

    def display_reminder(self, text):
        BookingButton.body.disabled = True
        if (self.no_activity and self.color) in self.activities.canvas.children:
            self.activities.clear_widgets()
            self.activities.add_widget(Label(text=text))
        else:
            self.set_reminder()
            self.activities.canvas.add(self.color)
            self.activities.canvas.add(self.no_activity)
            self.activities.clear_widgets()
            self.activities.add_widget(Label(text=text))

    def set_reminder(self):
        self.no_activity.size = self.activities.size
        self.no_activity.pos = self.activities.pos


class ActivityImage(ToggleButton):

    source = StringProperty()

    def __init__(self, **kwargs):
        super(ActivityImage, self).__init__(**kwargs)
        self.source = kwargs.pop('source')
        with self.canvas:
            Color(rgba=(.1, .1, .8, 1))
        ActivityImage.popup_opened = False
        self.last_position = [0, 0]
        self.pressed_shape = Line(width=5, rectangle=(self.x, self.y, self.width, self.height))
        self.hover_color = Color(rgba=(.8, .8, .8, .25))
        self.hover_shape = Rectangle(size=(self.width - 5.5, self.height - 5.5),
                                     pos=(self.x + 3, self.y + 3))
        Window.bind(mouse_pos=lambda w, p: self.mouse_hover(p))

    def on_state(self, instance, value):
        user = loginscreen.LoginScreenLayout.body.user
        booked = self.check_activity()
        if booked:
            if self == booked:
                BookingButton.body.disabled = True
        else:
            if booked == ActivityScreenLayout.body.booked_activity:
                BookingButton.body.disabled = True
        if value == "normal":
            self.canvas.remove(self.pressed_shape)
            ActivityMainScreen.body.select.clear_widgets()
            if self.source == user.extract_activity(str(ActivityScreenLayout.body.chosen_day)):
                BookingButton.body.disabled = False
        else:
            if self.source == user.extract_activity(str(ActivityScreenLayout.body.chosen_day)):
                BookingButton.body.disabled = True
            else:
                BookingButton.body.disabled = False
            self.mouse_hover([0, 0])
            self.pressed_shape = Line(width=5, rectangle=(self.x, self.y, self.width, self.height))
            self.canvas.add(self.pressed_shape)
            self.mouse_hover(self.last_position)
            select_label = SelectedLabel(pos=ActivityMainScreen.body.select.pos)
            ActivityMainScreen.body.select.add_widget(Label(size_hint=(None, None),
                                                            width=(self.width/2 + (self.x-ActivityMainScreen.body.x -
                                                                                   (select_label.width/2)))))
            ActivityMainScreen.body.select.add_widget(select_label)

    @staticmethod
    def check_activity():
        for each in ToggleButton.get_widgets('activities'):
            if each.source == ActivityScreenLayout.body.booked_activity:
                return each
        return ''

    def mouse_hover(self, position):
        if not ActivityImage.popup_opened:
            if self.collide_point(*position):
                if hasattr(self, "hover_color") and\
                        not (self.hover_color and self.hover_shape) in self.canvas.children:
                    self.last_position = position
                    self.hover_color = Color(rgba=(.8, .8, .8, .25))
                    self.hover_shape = Rectangle(size=(self.width - 5.5, self.height - 5.5),
                                                 pos=(self.x + 3, self.y + 3))
                    self.canvas.add(self.hover_color)
                    self.canvas.add(self.hover_shape)
            else:
                if (self.hover_color and self.hover_shape) in self.canvas.children:
                    self.canvas.remove(self.hover_shape)
                    self.canvas.remove(self.hover_color)


class ActivityLayout(BoxLayout):

    def __init__(self, **kwargs):
        self.source = kwargs.pop('source')
        self.name = kwargs.pop('name')
        self.price = kwargs.pop('price')
        self.level = kwargs.pop('level')
        self.desc = kwargs.pop('desc')
        super(ActivityLayout, self).__init__(**kwargs)


class ActivityName(Label):
    pass


class ActivityMainScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(ActivityMainScreen, self).__init__(**kwargs)
        ActivityMainScreen.body = self


class ActivityInfo(BoxLayout):

    def __init__(self, **kwargs):
        self.source = kwargs.pop('source')
        self.name = kwargs.pop('name')
        super(ActivityInfo, self).__init__(**kwargs)

    def popup(self):
        popup_content = ActivityLayout(source=self.source,
                                       name=self.name,
                                       level=activity_names[self.source][1],
                                       price=activity_names[self.source][2],
                                       desc=activity_names[self.source][3])
        popup = ActivityPopup(size_hint=(.6, .6),
                              content=popup_content,
                              separator_color=(.1, .1, 1, .775),
                              title=self.name,
                              title_size=30,
                              title_color=(0, 0, 0, 1),
                              pos_hint={'x': .3, 'y': .2},
                              background='res/system/white_background.jpg')
        popup.open()


class WarningLayout(BoxLayout):

    text = StringProperty()

    def __init__(self, **kwargs):
        super(WarningLayout, self).__init__(**kwargs)
        self.txt = kwargs.pop('text')


class ActivityPopup(Popup):

    def __init__(self, **kwargs):
        super(ActivityPopup, self).__init__(**kwargs)

    def on_open(self):
        ActivityImage.popup_opened = True

    def on_dismiss(self):
        ActivityImage.popup_opened = False


class SelectedLabel(Label):
    pass


class DropDownMenu(BoxLayout):

    def __init__(self, **kwargs):
        super(DropDownMenu, self).__init__(**kwargs)
        DropDownMenu.body = self
        self.dropped = False
        self.drop_down_background = Color(rgba=(0, 0, 0, 1))
        self.color = Rectangle(size=self.size, pos=self.pos)

    def drop_down(self):
        if not self.children:
            self.dropped = True
            self.canvas.add(self.color)
            self.canvas.add(self.drop_down_background)
            for i in range(1, 15):
                days_button = DayButton(text=str(i), allow_no_selection=False)
                self.add_widget(days_button)
                if i == int(ActivityScreenLayout.body.chosen_day):
                    days_button.on_release()
                    days_button.state = 'down'
        else:
            self.dropped = False
            self.clear_widgets()
            self.canvas.remove(self.color)
            self.canvas.remove(self.drop_down_background)


class DayButton(ToggleButton):

    def __init__(self, **kwargs):
        super(DayButton, self).__init__(**kwargs)
        self.day = self.text
        self.text = 'Day ' + self.day

    def on_release(self):
        super(DayButton, self).on_release()
        ActivityMainScreen.body.chosen_day.text = 'Day ' + self.day
        ActivityScreenLayout.body.chosen_day = int(self.day)
        ActivityScreenLayout.body.load(day=self.day)
        ActivityScreenLayout.body.chosen_button = self


class DropDownButton(Button):

    def __init__(self, **kwargs):
        super(DropDownButton, self).__init__(**kwargs)
        DropDownButton.body = self


class BookingButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.disabled = False
        BookingButton.body = self

    def proceed(self, args):
        self.book_activity()

    @staticmethod
    def stop(button):
        button.state = 'normal'
        ActivityScreenLayout.body.select_saved('')
        BookingButton.body.disabled = True
        loginscreen.ErrorPopup.display('Booking cancel successful', '')

    def on_release(self):
        user = loginscreen.LoginScreenLayout.body.user
        if user.special_notes in physically_challenged:
            for each in ToggleButton.get_widgets('activities'):
                if each.state == 'down':
                    if activity_names[each.source][1] == 'Physical challenge':
                        content = WarningLayout(text='The activity may be physically challenging\n'
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
                        content.stop_btn.bind(on_release=(lambda dt: self.stop(each)))
                        popup.open()
                        return
                    else:
                        self.book_activity()
            self.book_activity()
        else:
            self.book_activity()

    def book_activity(self):
        user = loginscreen.LoginScreenLayout.body.user
        activity_images = ToggleButton.get_widgets('activities')
        for each in activity_images:
            if each.state == 'down':
                user.book_activity(str(ActivityScreenLayout.body.chosen_day), each.source)
                ActivityScreenLayout.body.booked_activity = each.source
                break
        else:
            user.book_activity(str(ActivityScreenLayout.body.chosen_day), '')
            ActivityScreenLayout.body.booked_activity = ''
        self.disabled = True
