from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import loginscreen
import activityscreen


class HomeScreenLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(HomeScreenLayout, self).__init__(**kwargs)
        HomeScreenLayout.body = self

    def update_activity_today(self):
        user = loginscreen.LoginScreenLayout.body.user
        activity = user.extract_activity(activityscreen.ActivityScreenLayout.body.today)
        if activity:
            activity_info = activityscreen.activity_names[activity]
            self.activity_img.source = activity
            self.activity_name.text = activity_info[0] + ' (' + activity_info[1] + ')'
        else:
            self.activity_img.source = 'res/system/no_activity.png'
            self.activity_name.text = 'None'

    def update_profile(self, user):
        self.profile.clear_widgets()
        profile_info = list(user.extract_profile().items())
        index = 0
        for each in range(3):
            row = BoxLayout()
            for i in range(2):
                section = ProfileInfo()
                section.type.text = str(profile_info[index][0]).upper()
                if str(profile_info[index][0]) == 'special notes':
                    section.info.text = str(profile_info[index][1])
                else:
                    section.info.text = str(profile_info[index][1])
                row.add_widget(section)
                index += 1
            self.profile.add_widget(row)


class ProfileImage(Image):
    pass


class SideBar(BoxLayout):

    sidebars = []

    def __init__(self, **kwargs):
        super(SideBar, self).__init__(**kwargs)
        self.sidebars.append(self)

    @classmethod
    def display_date(cls, date):
        for each in cls.sidebars:
            each.day.text = 'DAY: ' + date


class KimberleyInfo(Button):

    last_screen = ''

    def __init__(self, **kwargs):
        super(KimberleyInfo, self).__init__(**kwargs)

    def on_release(self):
        self.last_screen = HomeScreenLayout.body.screen_manager.current
        HomeScreenLayout.body.screen_manager.current = 'help_screen'


class ProfileInfo(BoxLayout):
    pass


class HomeScreenButton(Button):

    def change_password(self):
        pass

    @staticmethod
    def view_receipt():
        content = ReceiptLayout(orientation='vertical')
        empty = 7
        overall = 0
        for each in loginscreen.LoginScreenLayout.body.user.extract_activities():
            if each:
                receipt_row = BoxLayout()
                receipt_row.add_widget(ReceiptLabel(text=activityscreen.activity_names[each][0]))
                receipt_row.add_widget(ReceiptLabel(text='$' + activityscreen.activity_names[each][2]))
                content.receipt_rows.add_widget(receipt_row)
                empty -= 1
                overall += int(activityscreen.activity_names[each][2])
        for each in range(empty):
            content.receipt_rows.add_widget(Label())
        content.sum.text = '$' + str(overall)
        popup = Popup(size_hint=(.6, .6),
                      separator_color=(.1, .1, 1, .775),
                      content=content,
                      title='Receipt',
                      title_size=30,
                      title_color=(0, 0, 0, 1),
                      pos_hint={'x': .3, 'y': .2},
                      background='res/system/white_background.jpg')
        popup.open()

    @staticmethod
    def change_profile():
        content = ChangeProfileLayout()
        popup = Popup(size_hint=(.6, .6),
                      separator_color=(.1, .1, 1, .775),
                      content=content,
                      title='Change Profile',
                      title_size=30,
                      title_color=(0, 0, 0, 1),
                      pos_hint={'x': .3, 'y': .2},
                      background='res/system/white_background.jpg',
                      auto_dismiss=False)
        content.cancel_button.bind(on_release=popup.dismiss)
        content.confirm_button.bind(on_release=popup.dismiss)
        content.confirm_button.bind(on_release=lambda dt: content.confirm_update())
        popup.open()


class ReceiptLabel(Label):
    pass


class ReceiptLayout(BoxLayout):
    pass


class ChangeProfileLayout(BoxLayout):

    def confirm_update(self):
        new_profile = {}
        for each in self.children[1:5]:
            if each.text_input.text:
                pass
                new_profile[each.l_text[:-1].lower()] = each.text_input.text
        if new_profile:
            loginscreen.LoginScreenLayout.body.user.update_profile(new_profile)
            HomeScreenLayout.body.update_profile(loginscreen.LoginScreenLayout.body.user)
