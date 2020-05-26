from kivy.uix.relativelayout import RelativeLayout
import loginscreen
import user_manager
import re

string_pattern = r"[A-Za-z]+$"
number_pattern = r"[0-9]+$"


class RegisterScreenLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(RegisterScreenLayout, self).__init__(**kwargs)
        RegisterScreenLayout.body = self

    def confirm(self):
        register_info = {}
        input_box = self.register_input.children[1:8]
        input_box.reverse()
        incorrect = False
        invalid_name = False
        required_empty = False
        invalid_age = False
        invalid_password = False
        for each in input_box:
            if each.l_text[:-1] == 'Name':
                register_info[each.l_text[:-1].lower()] = (each.text_input1.text, each.text_input2.text)
            elif each.l_text[:-1] == 'Sex':
                for i in each.sex_button.children:
                    if i.state == 'down':
                        selected = i
                register_info[each.l_text[:-1].lower()] = selected.text.lower()
            elif each.l_text[:-1] == 'Password':
                register_info[each.l_text[:-1].lower()] = each.psw_input.text
            else:
                register_info[each.l_text[:-1].lower()] = each.text_input.text
        for each in register_info:
            if each != 'special notes':
                if not register_info[each]:
                    incorrect = True
                    required_empty = True
                if each == 'name':
                    if register_info[each][0] == '' and register_info[each][1] == '':
                        required_empty = True
                    else:
                        if not (re.match(string_pattern, register_info[each][0]) and
                                re.match(string_pattern, register_info[each][1])):
                            incorrect = True
                            invalid_name = True
                if each == 'password':
                    if ' ' in register_info[each]:
                        incorrect = True
                        invalid_password = True
                if each == 'age':
                    if register_info[each]:
                        if re.match(number_pattern, register_info[each]):
                            if int(register_info[each]) > 125:
                                incorrect = True
                                invalid_age = True
                        else:
                            incorrect = True
                            invalid_age = True
        if not incorrect:
            loginscreen.LoginScreenLayout.body.to_login(user_manager.User.register(register_info))
        if invalid_name:
            loginscreen.ErrorPopup.display('Name invalid', '')
        if invalid_age:
            loginscreen.ErrorPopup.display('Age invalid', 'must be less than 125')
        if invalid_password:
            loginscreen.ErrorPopup.display('Password invalid', '')
        if required_empty:
            loginscreen.ErrorPopup.display('Please fill in all required', '')

    @staticmethod
    def cancel():
        loginscreen.LoginScreenLayout.body.to_login()
