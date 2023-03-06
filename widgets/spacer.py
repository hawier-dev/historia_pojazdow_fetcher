from kivy.uix.widget import Widget


class Spacer(Widget):
    """A Widget to add space between other widgets.

    Attributes:
    orientation: str, optional (default="vertical")
        The orientation of the spacer, either "vertical" or "horizontal".
    """

    def __init__(self, orientation="vertical"):
        super().__init__()
        if orientation == "vertical":
            self.size_hint_y = 1.0
            self.size_hint_x = None

        elif orientation == "horizontal":
            self.size_hint_y = None
            self.size_hint_x = 1.0
