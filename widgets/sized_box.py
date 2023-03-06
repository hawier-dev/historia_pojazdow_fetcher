from kivy.uix.widget import Widget


class SizedBox(Widget):
    """
    Class to create a widget with a fixed size.
    """

    def __init__(self, width=0, height=0):
        super().__init__()

        self.size_hint_y = None
        self.size_hint_x = None
        self.width = width
        self.height = height
