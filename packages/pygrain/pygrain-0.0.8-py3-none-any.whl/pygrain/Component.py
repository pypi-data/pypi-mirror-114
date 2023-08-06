import pygame


class Component:
    """
    Superclass for UI components.
    """
    def __init__(self, parent, x=0, y=0, font_color=(0, 0, 0),
                 bg_colour=(255, 255, 255), border_color=(0, 0, 0),
                 border_thickness=1, font_size=20, width=1, height=1,
                 colour=(0, 0, 0), draggable=False):
        self.parent = parent
        self.parent.add_component(self)
        self.x = x
        self.y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_colour = font_color
        self.bg_colour = bg_colour
        self.border_colour = border_color
        self.border_thickness = border_thickness
        self.font_size = font_size
        self.colour = colour
        self.actions = {}
        self.dragging = False
        self.drag_offset_x, self.drag_offset_y = 0, 0
        if draggable:
            self.initialise_dragging()

    def get_parent(self):
        """
        Return this component's parent component (or App)
        :return: parent component
        """
        return self.parent

    def draw(self, screen):
        """
        Draw component based on defined properties.
        :param screen:
        :return: None
        """
        x, y = self.get_x(), self.get_y()
        # Background rectangle
        pygame.draw.rect(screen, self.bg_colour,
                         (x, y, self.width, self.height))
        # Border
        pygame.draw.rect(screen, self.border_colour,
                         (x, y, self.width, self.height),
                         width=self.border_thickness)

    def valid_event(self, events):
        """
        Return true if event is intended for this component.
        :param events: set of event names
        :return: bool
        """
        for name in events:
            if 'click' in name and not self.mouseover():
                return False

        return True

    def event(self, event):
        """
        Call callback function for a given binding that is a subset of the
        current event.
        :param event: set of event names
        :return: None
        """
        event = frozenset(event)
        called = False
        for curr in self.actions:
            if curr.issubset(event) and self.valid_event(event):
                for action in self.actions[curr]:
                    action(self)

                called = True

        return called

    def get_x(self):
        """
        Calculate absolute x coordinate of component.
        :return: int/float
        """
        return self.get_parent().get_x() + self.x

    def get_y(self):
        """
        Calculate absolute y coordinate of component.
        :return: int/float
        """
        return self.get_parent().get_y() + self.y

    def set_width(self, width):
        """
        Set width of component and signal parent component to update display.
        :param width:
        :return: None
        """
        self.width = width
        self.parent.update()

    def get_property(self, name):
        """
        Return value of property given name.
        :param name:
        :return:
        """
        prop = self.__getattribute__(name)
        if callable(prop):
            prop = prop()

        return prop

    def set_property(self, name, value):
        """
        Set value of property given name and signal parent to update display.
        :param name:
        :param value:
        :return:
        """
        self.__setattr__(name, value)
        self.parent.update()

    def get_action(self, events):
        """
        Return callback function associated with event combination.
        :param events: set of event names
        :return:
        """
        return self.actions[events]

    def bind(self, events, func):
        """
        Add mapping for event combination in actions dict.
        :param self:
        :param events: set of event names
        :param func: callback function when event occurs
        :return:
        """
        if frozenset(events) not in self.actions:
            self.actions[frozenset(events)] = []

        self.actions[frozenset(events)].append(func)

    def mouseover(self):
        """
        Return true if mouse is inside component's region.
        :return:
        """
        x, y = pygame.mouse.get_pos()
        return (
                self.get_x() <= x <= self.get_x() + self.width and
                self.get_y() <= y <= self.get_y() + self.height
        )

    def set_dragging(self):
        """
        Calculate distances between current position of mouse and
        top left (or centre) of the component.
        :return:
        """
        self.dragging = True
        x, y = pygame.mouse.get_pos()
        self.drag_offset_x = x - self.get_x()
        self.drag_offset_y = y - self.get_y()

    def reset_dragging(self):
        self.dragging = False

    def drag_position(self):
        """
        If component is being dragged then the relative x, y coordinates
        are set using the current position of the mouse and the offsets of
        the mouse from the component when the user clicked on the component.
        :return:
        """
        if not self.dragging:
            return
        x, y = pygame.mouse.get_pos()
        self.x = x - self.get_parent().get_x() - self.drag_offset_x
        self.y = y - self.get_parent().get_y() - self.drag_offset_y
        self.parent.update()

    def initialise_dragging(self):
        """
        Binds actions for dragging component.
        :return:
        """
        self.bind({'left click'}, lambda target: self.set_dragging())
        self.bind({'left up'}, lambda target: self.reset_dragging())
        self.bind({'mousemotion'}, lambda target: self.drag_position())

