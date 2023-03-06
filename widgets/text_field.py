from kivy.uix.textinput import TextInput

from configs import colors


class TextField(TextInput):
    """
    Custom implementation of TextInput widget from kivy.uix.textinput.TextInput.
    """

    def __init__(
        self,
        hint_text="",
        cursor_color=colors.PRIMARY,
        background_color=colors.SURFACE,
        foreground_color=colors.FOREGROUND,
        multiline=False,
        height=48,
        font_size=14,
        size_hint_x=1,
        input_filter=None,
        max_chars=255,
        **kwargs,
    ):
        super(TextField, self).__init__(**kwargs)
        self.background_color = background_color
        self.background_normal = background_color
        self.foreground_color = foreground_color
        self.cursor_color = cursor_color
        self.size_hint_y = None
        self.height = height
        self.font_name = "Default"
        self.hint_text = hint_text
        self.multiline = multiline
        self.write_tab = False
        self.font_size = font_size
        self.padding = (10, self.height / 2 - self.font_size / 2, 10, 10)
        self.size_hint_x = size_hint_x
        self.pos_hint = {"center_x": 0.5}
        self.input_filter = input_filter
        self.max_chars = max_chars
        self.bind(text=self._check_for_max)

    def _check_for_max(self, *_):
        self.text = (
            self.text[0 : self.max_chars]
            if len(self.text) > self.max_chars
            else self.text
        )
