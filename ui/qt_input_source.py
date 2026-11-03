class QtInputSource:
    """Input state collected directly from the native viewport widget."""

    def __init__(self, viewport=None):
        self.viewport = None
        self._scroll = 0.0
        self._mouse = (0.0, 0.0)
        self._last_mouse = (0.0, 0.0)
        self._over = False
        self._buttons = set()
        self._clicked = set()
        self._pressed = set()
        if viewport is not None:
            self.bind(viewport)

    def bind(self, viewport):
        self.viewport = viewport
        viewport.set_input_source(self)

    def mouse_move(self, x, y):
        self._mouse = (float(x), float(y))

    def mouse_press(self, button):
        self._buttons.add(button)
        self._clicked.add(button)

    def mouse_release(self, button):
        self._buttons.discard(button)

    def enter(self):
        self._over = True

    def leave(self):
        self._over = False

    def key_press(self, key):
        self._pressed.add(key)

    def key_release(self, key):
        pass

    def on_wheel(self, amount):
        self._scroll += amount

    def consume_scroll(self):
        scroll, self._scroll = self._scroll, 0.0
        return scroll

    def is_cursor_over_viewport(self):
        return self._over

    def get_cursor_pos(self):
        if self.viewport is None:
            return (0.5, 0.5)
        mouse_x, mouse_y = self._mouse
        width = max(1.0, float(self.viewport.width()))
        height = max(1.0, float(self.viewport.height()))
        x = min(1.0, max(0.0, mouse_x / width))
        y = min(1.0, max(0.0, 1.0 - mouse_y / height))
        return (x, y)

    def get_window_shape(self):
        if self.viewport is None:
            return (1.0, 1.0)
        return (max(1.0, float(self.viewport.width())), max(1.0, float(self.viewport.height())))

    def mouse_delta(self):
        last, self._last_mouse = self._last_mouse, self._mouse
        return (self._mouse[0] - last[0], self._mouse[1] - last[1])

    def is_down(self, button):
        return button in self._buttons

    def is_clicked(self, button):
        if button in self._clicked:
            self._clicked.discard(button)
            return True
        return False

    def is_pressed(self, key):
        key = key.lower()
        if key in self._pressed:
            self._pressed.discard(key)
            return True
        return False




