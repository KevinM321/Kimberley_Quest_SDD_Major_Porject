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
        invalid_name = False
        required_empty = False
        invalid_cabin_number = False
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
            elif each.l_text[:-1] == 'Special Notes':
                if each.text_input.text:
                    if each.text_input.text.isspace():
                        register_info[each.l_text[:-1].lower()] = 'None'
                    else:
                        register_info[each.l_text[:-1].lower()] = each.text_input.text
                else:
                    register_info[each.l_text[:-1].lower()] = 'None'
            else:
                register_info[each.l_text[:-1].lower()] = each.text_input.text
        for each in register_info:
            if each != 'special notes':
                if not register_info[each]:
                    required_empty = True
                if each == 'name':
                    if register_info[each][0] == '' and register_info[each][1] == '':
                        required_empty = True
                    else:
                        if not (re.match(string_pattern, register_info[each][0]) and
                                re.match(string_pattern, register_info[each][1])):
                            invalid_name = True
                if each == 'cabin number':
                    if register_info[each]:
                        if re.match(number_pattern, register_info[each]):
                            if not (1 <= int(register_info[each]) <= 13):
                                invalid_cabin_number = True
                        else:
                            invalid_cabin_number = True
                if each == 'password':
                    if ' ' in register_info[each]:
                        invalid_password = True
                if each == 'age':
                    if register_info[each]:
                        if re.match(number_pattern, register_info[each]):
                            if not (1 <= int(register_info[each]) <= 125):
                                invalid_age = True
                        else:
                            invalid_age = True
        if invalid_name:
            loginscreen.ErrorPopup.display('Name invalid', '')
        elif invalid_password:
            loginscreen.ErrorPopup.display('Password invalid', 'cannot contain space')
        elif invalid_age:
            loginscreen.ErrorPopup.display('Age invalid', 'must be a number <= 125')
        elif invalid_cabin_number:
            loginscreen.ErrorPopup.display('Cabin number invalid', 'must be a number <= 13')
        elif required_empty:
            loginscreen.ErrorPopup.display('Please fill in all required', '')
        else:
            loginscreen.LoginScreenLayout.body.to_login(user_manager.User.register(register_info))
            RegisterScreenLayout.body.clear_inputs()

    @staticmethod
    def cancel():
        RegisterScreenLayout.body.clear_inputs()
        loginscreen.LoginScreenLayout.body.to_login('')

    def clear_inputs(self):
        for each in self.register_input.children[1:8]:
            if each.l_text[:-1] == 'Name':
                each.text_input1.text = ''
                each.text_input2.text = ''
            elif each.l_text[:-1] == 'Sex':
                each.sex_button.children[1].state = 'down'
            elif each.l_text[:-1] == 'Password':
                each.password = True
                each.psw_button.text = 'Show'
                each.psw_input.text = ''
            else:
                each.text_input.text = ''
