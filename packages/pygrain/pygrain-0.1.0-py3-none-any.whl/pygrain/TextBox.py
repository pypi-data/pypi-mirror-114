from .Component import Component
from .util import show_text


class TextBox(Component):
    """
    Component to display text.
    """
    def __init__(self, parent, text='', **kwargs):
        super().__init__(parent, **kwargs)
        self.text = text

    def draw(self, screen):
        """
        Draw textbox with text.
        :param screen:
        :return:
        """
        x, y = self.get_x(), self.get_y()
        super().draw(screen)
        show_text(screen, self.get_text(), x + self.width / 2, y + self.height / 2,
                  font_size=self.font_size)
        return self

    def get_text(self):
        """
        Return text if it is a string or call function that returns text.
        :return:
        """
        text = self.text
        if callable(text):
            text = text()

        return text


