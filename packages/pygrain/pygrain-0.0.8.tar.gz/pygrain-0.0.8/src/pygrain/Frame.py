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
        super().event(events)
        done = False
        for component in self.components:
            done = component.event(events) or done

        return done

    def draw(self, screen):
        """
        Draw frame and all sub-components from bottom to top order.
        :param screen:
        :return: None
        """
        super().draw(screen)
        for component in self.components[::-1]:
            component.draw(screen)

    def add_component(self, component):
        """
        Add new component to the front of list.
        :param component: Component
        :return: None
        """
        self.components.insert(0, component)

    def update(self):
        """
        Update parent component (or App).
        :return:
        """
        self.parent.update()

