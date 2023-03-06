import threading
from kivy.clock import mainthread
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from configs import config
from utils.functions import get_all_dates
from widgets.push_button import PushButton
from widgets.sized_box import SizedBox
from widgets.spacer import Spacer
from widgets.text_field import TextField
from widgets.text_label import TextLabel, LabelType

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class HomeScreen(Screen):
    can_start_task = BooleanProperty(False)
    running = BooleanProperty(False)

    def __init__(self, root):
        super().__init__()
        self.name = "home_screen"
        self.dialog = None
        self.thread = None
        self.root = root
        self.bind(can_start_task=self.disable_start_button)

        self.main_layout = BoxLayout()
        self.main_layout.orientation = "vertical"
        self.main_layout.padding = config.PADDING
        self.main_layout.spacing = 10

        # Main label
        self.main_label = TextLabel(
            text="First registration date fetcher",
            label_type=LabelType.HEADING2,
            halign="center",
        )

        # VIN Number
        self.vin_field = TextField(hint_text="VIN")
        self.vin_description = TextLabel(
            text="Vehicle Identification Number (VIN)", label_type=LabelType.ADDITION
        )
        self.vin_field.bind(text=self.check_for_text)
        # License plate
        self.registration_number_field = TextField(hint_text="Registration number")
        self.registration_number_description = TextLabel(
            text="Vehicle registration number", label_type=LabelType.ADDITION
        )
        self.registration_number_field.bind(text=self.check_for_text)
        # Year
        self.year_field = TextField(hint_text="Year", max_chars=4)
        self.year_field.input_filter = "int"
        self.year_description = TextLabel(
            text="Vehicle year of production", label_type=LabelType.ADDITION
        )
        self.year_field.bind(text=self.check_for_text)

        self.start_button = PushButton(text="Start", on_click=self.run_process)

        self.main_layout.add_widget(self.main_label)

        self.main_layout.add_widget(SizedBox(height=10))

        self.main_layout.add_widget(self.vin_field)
        self.main_layout.add_widget(self.vin_description)

        self.main_layout.add_widget(SizedBox(height=10))

        self.main_layout.add_widget(self.registration_number_field)
        self.main_layout.add_widget(self.registration_number_description)

        self.main_layout.add_widget(SizedBox(height=10))

        self.main_layout.add_widget(self.year_field)
        self.main_layout.add_widget(self.year_description)

        self.main_layout.add_widget(Spacer())
        self.main_layout.add_widget(self.start_button)
        self.add_widget(self.main_layout)
        self.disable_start_button(True, False)

    def check_for_text(self, *_):
        if (
            not self.running
            and self.vin_field.text
            and self.year_field.text
            and self.registration_number_field.text
        ):
            self.can_start_task = True
        else:
            self.can_start_task = False

    def disable_start_button(self, _, value: bool):
        self.start_button.set_disabled(not value)

    def run_process(self, *_):
        self.thread = threading.Thread(target=self.main_task, args=[])
        self.thread.daemon = True
        self.thread.start()

    def main_task(self):
        self.can_start_task = False
        self.running = True

        year = self.year_field.text
        vin = self.vin_field.text
        registration_number = self.registration_number_field.text
        self.start_button.text = "Searching..."

        if not year or not vin or not registration_number:
            print("You need to specify: vin, year and registration number")
            self.start_button.text = "Start"
            self.can_start_task = True
            self.running = False
            return

        try:
            url = "https://historiapojazdu.gov.pl/"

            browser = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install())
            )

            browser.get(url)

            dates = get_all_dates(int(year))

            for date in dates:
                vin_field = browser.find_element(
                    By.ID, "_historiapojazduportlet_WAR_historiapojazduportlet_:vin"
                )
                vin_field.send_keys(vin)

                plate_field = browser.find_element(
                    By.ID, "_historiapojazduportlet_WAR_historiapojazduportlet_:rej"
                )
                plate_field.send_keys(registration_number)

                date_field = browser.find_element(
                    By.ID, "_historiapojazduportlet_WAR_historiapojazduportlet_:data"
                )
                date_field.click()
                date_field.send_keys(date)

                submit_button = browser.find_element(
                    By.ID,
                    "_historiapojazduportlet_WAR_historiapojazduportlet_:btnSprawdz",
                )
                submit_button.click()

                browser.implicitly_wait(3)
                try:
                    abroad_data_button = browser.find_element(
                        By.ID, "raport-content-template-dane-zagraniczne-button"
                    )
                    abroad_data_button.click()

                    name_text = browser.find_element(
                        By.ID,
                        "_historiapojazduportlet_WAR_historiapojazduportlet_:j_idt10:marka",
                    )
                    model_text = browser.find_element(
                        By.ID,
                        "_historiapojazduportlet_WAR_historiapojazduportlet_:j_idt10:model",
                    )
                    type_text = browser.find_element(
                        By.ID,
                        "_historiapojazduportlet_WAR_historiapojazduportlet_:j_idt10:podrodzaj",
                    )
                    mileage_text = browser.find_element(
                        By.CLASS_NAME,
                        "km",
                    ).find_element(By.CLASS_NAME, "strong")

                    print(f"Found {name_text.text}, {model_text.text}")
                    print("-------")
                    print(f"Body type: {type_text.text}")
                    print(f"Date of first registration: {date}")
                    print(f"VIN: {vin}")
                    print(f"Registration number: {registration_number}")
                    print(f"Mileage: {mileage_text.text}")
                    self.go_to_results(
                        model=model_text.text,
                        name=name_text.text,
                        body_type=type_text.text,
                        first_registration=date,
                        vin=vin,
                        mileage=mileage_text.text,
                        registration_number=registration_number,
                    )
                    break

                except NoSuchElementException:
                    browser.get(url)
                    continue

            browser.close()

        except Exception as e:
            print(e)
            self.start_button.text = "Start"
            self.can_start_task = True
            self.running = False

        self.can_start_task = True
        self.start_button.text = "Start"
        self.running = False

    @mainthread
    def go_to_results(
        self,
        model: str,
        name: str,
        body_type: str,
        first_registration: str,
        vin: str,
        mileage: str,
        registration_number: str,
    ):
        self.root.change_screen_to_result(
            model=model,
            name=name,
            body_type=body_type,
            first_registration=first_registration,
            vin=vin,
            mileage=mileage,
            registration_number=registration_number,
        )
