from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
import loginscreen
import activityscreen

sidebars = []


class HomeScreenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(HomeScreenLayout, self).__init__(**kwargs)
        HomeScreenLayout.body = self

    def update_activity_today(self):
        user = loginscreen.LoginScreenLayout.body.user
        activity = user.extract_activity(activityscreen.ActivityScreenLayout.body.today)
        if activity:
            activity_info = activityscreen.activity_names[activity]
            self.activity_img.source = activity
            self.activity_name.text = "Today's  Activity:        " + activity_info[0] + ' (' + activity_info[1] + ')'
        else:
            self.activity_img.source = 'res/system/no_activity.png'
            self.activity_name.text = "Today's  Activity:        " + 'None'


class ProfileImage(Image):
    pass


class SideBar(BoxLayout):

    def __init__(self, **kwargs):
        super(SideBar, self).__init__(**kwargs)
        sidebars.append(self)

    @staticmethod
    def display_date(date):
        for each in sidebars:
            each.day.text = 'DAY: ' + date


class KimberleyInfo(Button):

    def __init__(self, **kwargs):
        super(KimberleyInfo, self).__init__(**kwargs)

    def on_release(self):
        pass


class ProfileInfo(BoxLayout):
    pass
