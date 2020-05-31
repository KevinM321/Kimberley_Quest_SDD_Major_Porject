from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
import homescreen


# class for the help screen
class HelpScreenLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(HelpScreenLayout, self).__init__(**kwargs)

    # move back to the screen on which the help button was pressed
    def back(self):
        self.screen_manager.current = homescreen.KimberleyInfo.last_screen

    # creates a popup and displays the screen help image in it
    @staticmethod
    def popup_help(source):
        popup = HelpPopup(size_hint=(.825, .8))
        content = HelpPopupLayout()
        content.add_widget(Image(source=source,
                                 size=content.size,
                                 pos=content.pos))
        popup.add_widget(content)
        popup.open()


# class for the popup in help screen
class HelpPopup(ModalView):
    pass


# class for the layout of the popup
class HelpPopupLayout(BoxLayout):
    pass
