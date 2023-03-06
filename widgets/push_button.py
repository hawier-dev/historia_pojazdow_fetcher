from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.button import Button

from configs import colors


class PushButton(Button):
    """
    Custom button widget with stylized appearance and hover/click behavior.
    """

    def __init__(
        self,
        text="",
        primary_color=colors.PRIMARY,
        hover_color=colors.PRIMARY_HOVER,
        clicked_color=colors.PRIMARY_CLICKED,
        foreground_color=colors.FOREGROUND,
        height=38,
        width=120,
        font_size=14,
        size_hint_x=None,
        on_click=None,
        **kwargs,
    ):
        super(PushButton, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_over)

        self.markup = True
        self.primary_color = primary_color
        self.hover_color = hover_color
        self.clicked_color = clicked_color

        self.background_color = self.primary_color
        self.background_normal = self.primary_color
        self.background_down = self.hover_color
        self.foreground_color = foreground_color
        self.size_hint_y = None
        self.size_hint_x = size_hint_x
        self.height = height
        self.width = width
        self.font_name = "Default"
        self.text = text
        self.font_size = font_size
        self.pos_hint = {"center_x": 0.5}
        self.on_click = on_click
        self.padding_x = 10
        self.auto_resize()

    def auto_resize(self, *args):
        while self.texture_size[0] > self.width:
            self.font_size -= 1
            self.texture_update()

    def on_press(self):
        """
        This method is called when the button is pressed by the user.
        It sets the background color of the button to the color specified as 'clicked_color'
        in the constructor and calls the 'on_click' function.
        """
        self.background_color = self.clicked_color
        self.background_normal = self.clicked_color
        if self.on_click:
            self.on_click()

    def on_release(self):
        """
        Handle button release event.
        This method sets the background color of the button to the primary color.
        """
        self.background_color = self.primary_color
        self.background_normal = self.primary_color

    def on_mouse_over(self, window, pos):
        """
        Event handler that changes the background color of the button
        when the mouse is over.

        :param window: The window where the button is displayed
        :type window: kivy.core.window.Window
        :param pos: The current mouse position
        :type pos: tuple of int
        """
        if self.collide_point(*pos):
            self.background_color = self.hover_color
            self.background_normal = self.hover_color

        else:
            self.background_color = self.primary_color
            self.background_normal = self.primary_color
