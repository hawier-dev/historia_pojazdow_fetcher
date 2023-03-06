import os
from tkinter import Tk

import kivy
from kivy import Config

from screens.result_screen import ResultScreen

kivy.require("2.1.0")

from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.app import App
from kivy.core.text import LabelBase

from configs import colors, config
from screens.home_screen import HomeScreen

os.environ["SDL_MOUSE_FOCUS_CLICKTHROUGH"] = "1"


class FirstRegistrationDateFetcher(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.result_screen = ResultScreen(self)
        self.screen_manager = ScreenManager()

    def build(self):
        self.title = config.APP_NAME
        tk = Tk()
        tk.withdraw()
        # Window settings
        Window.size = (400, 450)
        Window.minimum_width, Window.minimum_height = Window.size
        Window.clearcolor = colors.BACKGROUND

        # Set icon
        Config.set("kivy", "window_icon", "assets/logo.ico")
        Config.set("kivy", "exit_on_escape", "0")
        Config.set("input", "mouse", "mouse,disable_multitouch")
        Config.write()

        self.screen_manager.transition = FadeTransition()
        self.screen_manager.transition.duration = 0.4

        home_screen = HomeScreen(self)

        self.screen_manager.add_widget(home_screen)
        self.screen_manager.add_widget(self.result_screen)

        return self.screen_manager

    def change_screen_to_result(
        self,
        model: str,
        name: str,
        body_type: str,
        first_registration: str,
        vin: str,
        mileage: str,
        registration_number: str,
    ):
        self.result_screen.model = model
        self.result_screen.car_name = name
        self.result_screen.body_type = body_type
        self.result_screen.first_registration = first_registration
        self.result_screen.vin = vin
        self.result_screen.mileage = mileage
        self.result_screen.registration_number = registration_number
        self.screen_manager.current = "result_screen"

    def back_to_home(self):
        self.screen_manager.current = "home_screen"


if __name__ == "__main__":
    LabelBase.register(
        name="Default",
        fn_regular="fonts/Inter-Medium.ttf",
        fn_bold="fonts/Inter-Bold.ttf",
    )

    app = FirstRegistrationDateFetcher()
    app.run()
