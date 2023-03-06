from enum import Enum

from kivy.uix.label import Label

from configs import colors


class LabelType(Enum):
    """
    Enum class for the different types of text labels.

    HEADING1: Heading 1 label type
    HEADING2: Heading 2 label type
    PARAGRAPH: Paragraph label type
    ADDITION: Addition label type
    """

    HEADING1 = "h1"
    HEADING2 = "h2"
    PARAGRAPH = "p"
    ADDITION = "a"


class TextLabel(Label):
    """
    A custom label class with text style properties.
    """

    def __init__(
        self,
        text: str,
        color=colors.FOREGROUND,
        label_type=LabelType.PARAGRAPH,
        halign="left",
        max_lines=1,
        size_hint=(1, None),
        show_warning=False,
        warning_text="required",
        show_ref=False,
        ref_text="help",
        **kwargs,
    ):
        super(TextLabel, self).__init__(**kwargs)
        self.markup = True
        self.text = (
            text + f"[color={colors.ERROR_COLOR}] ({warning_text})[/color]"
            if show_warning
            else text
        )
        if show_ref:
            self.text += f" [u][color={colors.WORKING_COLOR}][ref={ref_text}]{ref_text}[/ref][/color][/u]"

        self.font_name = "Default"
        self.size_hint = size_hint
        self.label_type = label_type
        self.color = color
        self.halign = halign
        self.max_lines = max_lines
        self._set_type()

        self.bind(size=self._set_text_width)
        self.height = self.font_size * self.max_lines + 2
        self.texture_update()

    def _set_text_width(self, *_):
        self.text_size[0] = self.size[0]

    def _set_type(self, *_):
        """
        Helper function that sets the font size and
        font weight of the label based on its type.
        """
        if self.label_type == LabelType.HEADING1:
            self.font_size = 24
            self.bold = True

        elif self.label_type == LabelType.HEADING2:
            self.font_size = 20

        elif self.label_type == LabelType.PARAGRAPH:
            self.font_size = 15

        elif self.label_type == LabelType.ADDITION:
            self.font_size = 13
            self.color = colors.FOREGROUND_DARKER
