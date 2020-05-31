from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import StringProperty
from passlib.hash import pbkdf2_sha256
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import re
import mealscreen
import loginscreen
import activityscreen

number_pattern = r"[0-9]+$"


# class for the layout of the home screen
class HomeScreenLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(HomeScreenLayout, self).__init__(**kwargs)
        HomeScreenLayout.body = self

    # display the user's booked activity for today
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

    # display the user's stored profile information
    def update_profile(self, user):
        self.profile.clear_widgets()
        profile_info = list(user.extract_profile().items())
        index = 0
        for each in range(3):
            row = BoxLayout()
            for i in range(2):
                section = ProfileInfo()
                section.type.text = str(profile_info[index][0]).upper()
                if str(profile_info[index][0]) == 'name':
                    section.info.text = str(profile_info[index][1].split(' ')[1]) \
                                        + ' ' + \
                                        str(profile_info[index][1].split(' ')[0])
                else:
                    section.info.text = str(profile_info[index][1])
                row.add_widget(section)
                index += 1
            self.profile.add_widget(row)
        ProfileImage.body.build()


# class for the profile image on home screen
class ProfileImage(Image):

    def __init__(self, **kwargs):
        super(ProfileImage, self).__init__(**kwargs)
        ProfileImage.body = self

    # display appropriate image based on the stored gender of the user
    def build(self):
        if loginscreen.LoginScreenLayout.body.user.sex == 'male':
            self.source = 'res/system/male_profile.jpg'
        else:
            self.source = 'res/system/female_profile.jpg'


# class for the layout of the side bar on the left side of each screen
class SideBar(BoxLayout):

    sidebars = []

    def __init__(self, **kwargs):
        super(SideBar, self).__init__(**kwargs)
        self.sidebars.append(self)

    # display the user's trip day
    @classmethod
    def display_date(cls, date):
        for each in cls.sidebars:
            each.day.text = 'DAY: ' + date


# class for the help button on the bottom left of the sidebar
class KimberleyInfo(Button):

    last_screen = ''

    def __init__(self, **kwargs):
        super(KimberleyInfo, self).__init__(**kwargs)

    def on_release(self):
        KimberleyInfo.last_screen = HomeScreenLayout.body.screen_manager.current  # store the screen of pressed button
        HomeScreenLayout.body.screen_manager.current = 'help_screen'  # change to help screen


# class of the layout for displaying user profile information
class ProfileInfo(BoxLayout):
    pass


# class for the 3 buttons on the bottom right of the home screen
class HomeScreenButton(Button):

    psw_popup = ''

    @staticmethod
    def change_password():  # create a popup for changing password
        content = ChangePasswordLayout()
        popup = Popup(size_hint=(.6, .6),
                      separator_color=(.1, .1, 1, .775),
                      content=content,
                      title='Change Password',
                      title_size=30,
                      title_color=(0, 0, 0, 1),
                      pos_hint={'x': .3, 'y': .2},
                      background='res/system/white_background.jpg',
                      auto_dismiss=False)
        content.cancel_button.bind(on_release=popup.dismiss)
        content.confirm_button.bind(on_release=lambda dt: content.check())
        HomeScreenButton.psw_popup = popup
        popup.open()

    @staticmethod
    def logout():  # logout of the current user
        body = activityscreen.ActivityScreenLayout.body
        body.chosen_day = body.today
        HomeScreenLayout.body.screen_manager.transition = FadeTransition()
        HomeScreenLayout.body.screen_manager.current = 'login_screen'
        for each in mealscreen.MealPanelItem.get_widgets('panel'):
            if each.text == 'Breakfast':
                each.on_release()
            each.remove_menu()

    @staticmethod
    def view_receipt():  # create a popup displaying all the booked activities and the sum of prices
        content = ReceiptLayout(orientation='vertical')
        empty = 7
        overall = 0
        for each in loginscreen.LoginScreenLayout.body.user.extract_activities():  # extract booked activities and add
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
    def change_profile():  # create a popup for changing profile information
        content = ChangeProfileLayout()
        for each in content.gender.children:  # select the button corresponding to the user's gender
            if each.text.lower() == loginscreen.LoginScreenLayout.body.user.sex:
                each.state = 'down'
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
        content.confirm_button.bind(on_release=lambda dt: content.confirm_update(popup))
        popup.open()


# class for the layout of each row of  booked activity
class ReceiptLabel(Label):
    pass


# class for the layout of the displayed receipt popup
class ReceiptLayout(BoxLayout):
    pass


# class for the layout of the change password popup
class ChangePasswordLayout(BoxLayout):

    # called when confirm button pressed
    def check(self):
        content = ''
        if self.new_psw.text_input.text and self.old_psw.text_input.text:  # check if new password matches the old
            if pbkdf2_sha256.verify(self.old_psw.text_input.text,  # check if the input old password is correct
                                    loginscreen.LoginScreenLayout.body.user.account[0]['password']):
                if ' ' in self.new_psw.text_input.text:  # check if there is a input for new password
                    content = WarningBox(message='New Password Invalid')
                else:
                    HomeScreenButton.psw_popup.dismiss()  # close the popup and update new password to 'account'
                    loginscreen.LoginScreenLayout.body.user.update_password(self.new_psw.text_input.text)
                    loginscreen.ErrorPopup.display('Update successful', '')
            else:
                content = WarningBox(message='Original Password Incorrect')
        else:
            content = WarningBox(message='Input Empty')
        if content:  # create a warning if the above tests failed
            Popup(title='Warning',
                  content=content,
                  separator_color=(.1, .1, 1, .775),
                  title_size=30,
                  size_hint=(.4, .525),
                  title_color=(0, 0, 0, 1),
                  pos_hint={'x': .4125, 'y': .25},
                  background='res/system/white_background.jpg').open()


# class for the layout of the warning popup
class WarningBox(BoxLayout):

    message = StringProperty()

    def __init__(self, **kwargs):
        super(WarningBox, self).__init__(**kwargs)
        self.warning_label.text = kwargs.pop('message')


# class for the layout of the change profile popup
class ChangeProfileLayout(BoxLayout):

    def confirm_update(self, popup):  # called when confirm button pressed
        new_profile = {}
        for each in self.children[1:5]:  # check for input of new profile info and add to 'new_profile'
            if each.l_text == 'Sex:':  # extracted the selected gender button
                for i in each.gender.children:
                    if i.state == 'down':
                        new_profile['sex'] = i.text.lower()
            elif each.l_text == 'Age:':  # check if entered age is valid
                if each.text_input.text:
                    if re.match(number_pattern, each.text_input.text) and (1 <= int(each.text_input.text) <= 125):
                        new_profile[each.l_text[:-1].lower()] = each.text_input.text
                    else:
                        Popup(title='Warning',
                              content=WarningBox(message='Age invalid'),
                              separator_color=(.1, .1, 1, .775),
                              title_size=30,
                              size_hint=(.4, .525),
                              title_color=(0, 0, 0, 1),
                              pos_hint={'x': .4125, 'y': .25},
                              background='res/system/white_background.jpg').open()
                        return
            else:
                if each.text_input.text:
                    new_profile[each.l_text[:-1].lower()] = each.text_input.text
        if new_profile:  # if there are new profile info then update the user's profile
            loginscreen.LoginScreenLayout.body.user.update_profile(new_profile)
            HomeScreenLayout.body.update_profile(loginscreen.LoginScreenLayout.body.user)
            loginscreen.ErrorPopup.display('Update successful', '')
            popup.dismiss()
