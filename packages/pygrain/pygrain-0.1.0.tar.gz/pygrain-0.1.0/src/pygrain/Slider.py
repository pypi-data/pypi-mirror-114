from .Component import Component
from .util import show_text


class Slider(Component):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)