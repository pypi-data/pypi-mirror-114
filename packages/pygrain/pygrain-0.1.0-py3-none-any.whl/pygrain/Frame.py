from .Component import Component


class Frame(Component):
    """
    Class for a collection of components.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.components = []
        parent.switch_frame(self)

    def event(self, events):
        """
        Pass event to all sub-components inside the frame.
        :param events:
        :return: if event was valid for any component
        """

        for component in self.components[::-1]:
            if component.event(events):
                return True

        return super().event(events)

    def draw(self, screen):
        """
        Draw frame and all sub-components from bottom to top order.
        :param screen:
        :return: None
        """
        super().draw(screen)
        for component in self.components:
            component.draw(screen)

    def add_component(self, component):
        """
        Add new component to the front of list.
        :param component: Component
        :return: None
        """
        self.components.append(component)

    def update(self):
        """
        Update parent component (or App).
        :return:
        """
        self.parent.update()

