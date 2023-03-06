import json
import threading
from functools import partial
from time import sleep
from tkinter import Tk, filedialog

from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from configs import config
from utils.functions import get_all_dates
from widgets.push_button import PushButton
from widgets.sized_box import SizedBox
from widgets.spacer import Spacer
from widgets.text_label import TextLabel, LabelType


class ResultScreen(Screen):
    model = StringProperty()
    car_name = StringProperty()
    body_type = StringProperty()
    first_registration = StringProperty()
    vin = StringProperty()
    registration_number = StringProperty()
    mileage = StringProperty()

    def __init__(self, root):
        super().__init__()
        self.name = "result_screen"
        self.dialog = None
        self.thread = None

        self.main_layout = BoxLayout()
        self.main_layout.orientation = "vertical"
        self.main_layout.padding = config.PADDING
        self.main_layout.spacing = 10

        self.bind(model=self._change_text)
        self.bind(car_name=self._change_text)
        self.bind(body_type=self._change_text)
        self.bind(first_registration=self._change_text)
        self.bind(vin=self._change_text)
        self.bind(registration_number=self._change_text)
        self.bind(mileage=self._change_text)

        # Main label
        self.model_and_name_label = TextLabel(
            text="",
            label_type=LabelType.HEADING2,
            halign="center",
        )

        self.vin_label = TextLabel(text="")
        self.registration_number_label = TextLabel(text="")
        self.body_type_label = TextLabel(text="")
        self.first_registration_label = TextLabel(text="")
        self.mileage_label = TextLabel(text="")

        self.back_button = PushButton(text="Back", on_click=root.back_to_home)
        self.save_button = PushButton(text="Save JSON", on_click=self._save_json)

        self.main_layout.add_widget(self.model_and_name_label)
        self.main_layout.add_widget(SizedBox(height=10))
        self.main_layout.add_widget(self.vin_label)
        self.main_layout.add_widget(self.registration_number_label)
        self.main_layout.add_widget(self.body_type_label)
        self.main_layout.add_widget(self.first_registration_label)
        self.main_layout.add_widget(self.mileage_label)

        self.main_layout.add_widget(Spacer())
        self.main_layout.add_widget(self.back_button)
        self.main_layout.add_widget(self.save_button)
        self.add_widget(self.main_layout)

    def _change_text(self, *_):
        self.model_and_name_label.text = f"{self.car_name}, {self.model}"
        self.vin_label.text = f"VIN: {self.vin}"
        self.registration_number_label.text = (
            f"Registration number: {self.registration_number}"
        )
        self.mileage_label.text = f"Mileage: {self.mileage}"
        self.body_type_label.text = f"Body type: {self.body_type}"
        self.first_registration_label.text = (
            f"Date of first registration: {self.first_registration}"
        )

    def _save_json(self, *_):
        tk = Tk()
        tk.withdraw()
        file = filedialog.asksaveasfile(
            filetypes=[("JSON File", "*.json")], defaultextension="*.json"
        )
        if file:
            json.dump(
                {
                    "name": self.car_name,
                    "model": self.model,
                    "vin": self.vin,
                    "registration_number": self.registration_number,
                    "mileage": self.mileage,
                    "body_type": self.body_type,
                    "first_registration_date": self.first_registration,
                },
                file,
                indent=4,
            )
            file.close()
