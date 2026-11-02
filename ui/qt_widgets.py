"""Native Qt widget service used by the configurator UI."""
from __future__ import annotations

try:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QAction, QSurfaceFormat
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QDockWidget, QFrame, QHBoxLayout, QLabel,
        QLineEdit, QCheckBox, QComboBox, QDoubleSpinBox, QMenu, QProgressBar,
        QPushButton, QScrollArea, QSizePolicy, QSlider, QSpinBox, QTabWidget,
        QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QWidget,
    )
except ImportError:
    class _QtFallback:
        Horizontal = 1
        Key_F = 70
        Key_R = 82

    Qt = _QtFallback()
    QApplication = None
    QMainWindow = None
    QSurfaceFormat = None


class _Context:
    def __init__(self, owner, widget, tag=None, attached=False, layout_widget=None, parent=None):
        self.owner, self.widget, self.tag, self.attached = owner, widget, tag, attached
        self.layout_widget = layout_widget or widget
        self.parent = parent

    def __enter__(self):
        self.owner._push(self)
        return self

    def __exit__(self, *_):
        self.owner._pop(self)
        return False


class _Item:
    def __init__(self, widget):
        self.widget = widget
        self.value = None
        self.data = None


class _Recorder:
    def __init__(self, function):
        self.function = function
        self.call_args_list = []

    def __call__(self, *args, **kwargs):
        self.call_args_list.append(type("Call", (), {"args": args, "kwargs": kwargs})())
        return self.function(*args, **kwargs)

    def reset_mock(self):
        self.call_args_list.clear()


class QtItems:
    """Registry and widget operations for the Qt configurator UI."""

    mvAll = mvXAxis = mvYAxis = 0
    mvMouseButton_Left, mvMouseButton_Right, mvMouseButton_Middle = 1, 2, 4
    mvKey_F = int(Qt.Key_F) if QApplication else 70
    mvKey_R = int(Qt.Key_R) if QApplication else 82
    mvThemeCol_WindowBg = mvThemeCol_ChildBg = mvThemeCol_PopupBg = 0
    mvThemeCol_Text = mvThemeCol_Border = mvThemeCol_FrameBg = 0
    mvThemeCol_FrameBgHovered = mvThemeCol_FrameBgActive = 0
    mvThemeCol_TitleBg = mvThemeCol_TitleBgActive = 0
    mvThemeCol_Button = mvThemeCol_ButtonHovered = mvThemeCol_ButtonActive = 0
    mvThemeCol_Header = mvThemeCol_HeaderHovered = mvThemeCol_HeaderActive = 0
    mvThemeCol_Tab = mvThemeCol_TabHovered = mvThemeCol_TabActive = 0
    mvThemeCol_CheckMark = mvThemeCol_SliderGrab = mvThemeCol_SliderGrabActive = 0
    mvStyleVar_WindowRounding = mvStyleVar_FrameRounding = 0
    mvStyleVar_GrabRounding = mvStyleVar_TabRounding = 0
    mvStyleVar_WindowPadding = mvStyleVar_FramePadding = mvStyleVar_ItemSpacing = 0

    def __init__(self):
        self.items = {}
        self.application = self._window = self._root = None
        self._root_layout = None
        self._stack = []
        self._running = False
        self._menu = None
        self.set_value = self._set_value
        self.configure_item = self._configure_item

    def create_context(self):
        self._running = True
        if QApplication:
            # QOpenGLWidget otherwise inherits the platform default, which can
            # be an OpenGL 2 context.  The renderer's GLSL requires 3.3 core.
            if QApplication.instance() is None and QSurfaceFormat is not None:
                fmt = QSurfaceFormat()
                fmt.setRenderableType(QSurfaceFormat.OpenGL)
                fmt.setVersion(3, 3)
                fmt.setProfile(QSurfaceFormat.CoreProfile)
                fmt.setDepthBufferSize(24)
                QSurfaceFormat.setDefaultFormat(fmt)
            self.application = QApplication.instance() or QApplication([])

    def create_viewport(self, title="Spacecraft Configurator", width=1920, height=1080):
        if not QMainWindow:
            return
        self._window = QMainWindow()
        self._window.setWindowTitle(title)
        self._window.resize(width, height)
        self._root = QWidget(self._window)
        self._root_layout = QHBoxLayout(self._root)
        self._root_layout.setContentsMargins(0, 0, 0, 0)
        self._window.setCentralWidget(self._root)
        self._window.setMinimumSize(900, 600)
        self._window.setStyleSheet(
            "QMainWindow, QWidget { background: #0d131f; color: #e1e9f4; }"
            "QFrame { border: 0; }"
            "QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {"
            " background: #1a273b; border: 1px solid #32435b;"
            " color: #e1e9f4; padding: 4px; }"
            "QPushButton { background: #1f3751; border: 1px solid #32435b;"
            " color: #e1e9f4; padding: 5px 9px; }"
            "QPushButton:hover { background: #2b5274; }"
            "QTabBar::tab { background: #152235; padding: 7px 12px; }"
            "QTabBar::tab:selected { background: #203f5b; }"
            "QScrollBar { background: #111b2b; }"
        )

    def setup(self):
        pass

    def show_viewport(self):
        if self._window:
            self._window.show()

    def is_running(self):
        return self._running and (not self._window or self._window.isVisible())

    def destroy_context(self):
        self._running = False
        if self._window:
            self._window.close()
        self._window = self._root = None
        self._root_layout = None
        self.application = None
        self._stack.clear()
        self.items.clear()

    def process_events(self):
        if self.application:
            self.application.processEvents()

    def stop(self):
        self._running = False
        if self._window:
            self._window.close()

    def configure_app(self, **_):
        pass

    def _layout(self, parent=None):
        if parent:
            item = self.items.get(parent)
            if item and item.widget and item.widget.layout():
                return item.widget.layout()
        for context in reversed(self._stack):
            if context.widget is not None:
                return context.layout_widget.layout()
        return self._root_layout

    def _native_enabled(self):
        return self.application is not None

    def _push(self, context):
        layout = self._layout(context.parent)
        if context.tag and context.widget is not None:
            self.items[context.tag] = _Item(context.widget)
        if context.widget and layout and not context.attached:
            if context.tag == "spacecraft_designer_window":
                context.widget.setMinimumWidth(420)
                context.widget.setMaximumWidth(640)
                self._window.addDockWidget(Qt.LeftDockWidgetArea, context.widget)
                context.widget.setFloating(False)
                self._window.resizeDocks([context.widget], [520], Qt.Horizontal)
            elif context.tag == "viewport_window":
                # The dock must be able to shrink with the main window.  The
                # OpenGL surface supplies the useful size policy instead of a
                # fixed dock minimum that can consume the whole work area.
                context.widget.setMinimumSize(0, 0)
                context.widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self._window.addDockWidget(Qt.RightDockWidgetArea, context.widget)
                context.widget.setFloating(False)
                self._window.resizeDocks([context.widget], [1100], Qt.Horizontal)
            else:
                context.widget.setMinimumSize(0, 0)
                context.widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                layout.addWidget(context.widget)
                layout.setStretch(layout.count() - 1, 1)
            if layout is self._root_layout and layout.count() >= 1:
                layout.setStretch(0, 1)
        self._stack.append(context)

    def _pop(self, context):
        if self._stack and self._stack[-1] is context:
            self._stack.pop()

    def _add(self, widget, tag=None, callback=None, user_data=None, parent=None):
        layout = self._layout(parent)
        if layout:
            layout.addWidget(widget)
        if callback:
            if isinstance(widget, QPushButton):
                widget.clicked.connect(lambda: self._invoke(callback, widget, user_data))
            elif isinstance(widget, QLineEdit):
                widget.editingFinished.connect(lambda: self._invoke(callback, widget, user_data))
            elif isinstance(widget, QComboBox):
                widget.currentTextChanged.connect(lambda: self._invoke(callback, widget, user_data))
            elif isinstance(widget, QCheckBox):
                widget.toggled.connect(lambda: self._invoke(callback, widget, user_data))
            elif isinstance(widget, (QDoubleSpinBox, QSpinBox, QSlider)):
                widget.valueChanged.connect(lambda: self._invoke(callback, widget, user_data))
        if tag:
            self.items[tag] = _Item(widget)
        return tag

    def _register_placeholder(self, tag):
        if tag:
            self.items[tag] = _Item(None)
        return tag

    @staticmethod
    def _value(widget):
        if isinstance(widget, QLineEdit): return widget.text()
        if isinstance(widget, QComboBox): return widget.currentText()
        if isinstance(widget, (QDoubleSpinBox, QSpinBox, QSlider)): return widget.value()
        if isinstance(widget, QCheckBox): return widget.isChecked()
        return None

    @classmethod
    def _invoke(cls, callback, widget, user_data):
        value = cls._value(widget)
        try:
            callback(widget, value, user_data)
        except TypeError:
            try: callback(value)
            except TypeError: callback()

    def window(self, **kw):
        if kw.get("tag") == "spacecraft_designer_window":
            scroll = QScrollArea()
            content = QWidget()
            content.setLayout(QVBoxLayout())
            scroll.setWidget(content)
            scroll.setWidgetResizable(True)
            scroll.setFrameShape(QFrame.NoFrame)
            dock = QDockWidget("Spacecraft Designer", self._window)
            dock.setObjectName("spacecraftDesignerDock")
            dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
            dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
            dock.setWidget(scroll)
            return _Context(self, dock, kw.get("tag"), layout_widget=content, parent=kw.get("parent"))
        if kw.get("tag") == "viewport_window":
            content = QFrame()
            content.setLayout(QVBoxLayout())
            content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            content.layout().setContentsMargins(8, 8, 8, 8)
            dock = QDockWidget("Viewport", self._window)
            dock.setObjectName("viewportDock")
            dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
            dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
            dock.setWidget(content)
            return _Context(self, dock, kw.get("tag"), layout_widget=content, parent=kw.get("parent"))
        widget = QFrame()
        widget.setLayout(QVBoxLayout())
        return _Context(self, widget, kw.get("tag"), parent=kw.get("parent"))

    def group(self, **kw):
        widget = QWidget()
        widget.setLayout(QHBoxLayout() if kw.get("horizontal") else QVBoxLayout())
        widget.setMinimumSize(0, 0)
        return _Context(self, widget, kw.get("tag"), parent=kw.get("parent"))

    def tab_bar(self, **kw):
        widget = QTabWidget()
        widget.setMinimumSize(0, 0)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return _Context(self, widget, kw.get("tag"))

    def tab(self, **kw):
        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        if self._stack and isinstance(self._stack[-1].widget, QTabWidget):
            self._stack[-1].widget.addTab(widget, kw.get("label", ""))
        return _Context(self, widget, attached=True)

    def viewport_menu_bar(self):
        if self._window: self._window.menuBar()
        return _Context(self, None)

    def menu(self, **kw):
        self._menu = QMenu(kw.get("label", ""), self._window) if self._window else None
        if self._menu: self._window.menuBar().addMenu(self._menu)
        return _Context(self, None)

    def add_menu_item(self, label="", callback=None, **_):
        if self._menu:
            action = QAction(label, self._window)
            if callback: action.triggered.connect(callback)
            self._menu.addAction(action)

    def add_text(self, text="", tag=None, **kw):
        if not self._native_enabled(): return self._register_placeholder(tag)
        widget = QLabel(str(text))
        widget.setWordWrap(bool(kw.get("wrap")) or tag in {"viewport_component_details", "mission_banner"})
        widget.setMinimumWidth(0)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return self._add(widget, tag, parent=kw.get("parent"))

    def add_input_text(self, label="", default_value="", tag=None, callback=None, user_data=None, **_):
        if not self._native_enabled(): return self._register_placeholder(tag)
        widget = QLineEdit(str(default_value)); widget.setPlaceholderText(label); widget.setMinimumWidth(220)
        return self._add(widget, tag, callback, user_data, parent=_.get("parent"))

    def add_combo(self, items=(), default_value=None, label="", tag=None, callback=None, user_data=None, **_):
        if not self._native_enabled(): return self._register_placeholder(tag)
        widget = QComboBox(); widget.addItems([str(item) for item in items])
        if default_value is not None: widget.setCurrentText(str(default_value))
        widget.setMinimumWidth(min(440, max(120, int(_.get("width", 0) or 120))))
        widget.setToolTip(label)
        return self._add(widget, tag, callback, user_data, parent=_.get("parent"))

    def add_button(self, label="", tag=None, callback=None, user_data=None, **_):
        if not self._native_enabled(): return self._register_placeholder(tag)
        widget = QPushButton(label); widget.setMinimumWidth(max(72, min(180, widget.sizeHint().width())))
        return self._add(widget, tag, callback, user_data, parent=_.get("parent"))

    def add_checkbox(self, label="", default_value=False, tag=None, callback=None, user_data=None, **_):
        if not self._native_enabled(): return self._register_placeholder(tag)
        widget = QCheckBox(label); widget.setChecked(bool(default_value))
        return self._add(widget, tag, callback, user_data, parent=_.get("parent"))

    def add_slider_float(self, label="", default_value=0.0, min_value=0.0, max_value=1.0, tag=None, callback=None, user_data=None, **_):
        if not self._native_enabled(): return self._register_placeholder(tag)
        widget = QSlider(Qt.Horizontal); widget.setRange(int(min_value * 1000), int(max_value * 1000)); widget.setValue(int(default_value * 1000)); widget.setToolTip(label)
        return self._add(widget, tag, callback, user_data, parent=_.get("parent"))

    def add_input_float(self, label="", default_value=0.0, tag=None, callback=None, user_data=None, **_):
        if not self._native_enabled(): return self._register_placeholder(tag)
        widget = QDoubleSpinBox(); widget.setRange(-1e9, 1e9); widget.setValue(float(default_value)); widget.setToolTip(label)
        return self._add(widget, tag, callback, user_data, parent=_.get("parent"))

    def add_input_int(self, label="", default_value=0, tag=None, callback=None, user_data=None, **_):
        if not self._native_enabled(): return self._register_placeholder(tag)
        widget = QSpinBox(); widget.setRange(-2**31, 2**31 - 1); widget.setValue(int(default_value)); widget.setToolTip(label)
        return self._add(widget, tag, callback, user_data, parent=_.get("parent"))

    def add_progress_bar(self, default_value=0.0, tag=None, **_):
        if not self._native_enabled(): return self._register_placeholder(tag)
        widget = QProgressBar(); widget.setRange(0, 1000); widget.setValue(int(default_value * 1000))
        return self._add(widget, tag)

    def add_selectable(self, label="", **kw): return self.add_button(label=label, **kw)

    def add_group(self, tag=None, **_):
        if not self._native_enabled(): return _Context(self, None, tag)
        widget = QWidget(); widget.setLayout(QVBoxLayout()); self._add(widget, tag, parent=_.get("parent"))
        return _Context(self, widget, tag, parent=_.get("parent"))

    def add_separator(self, **_):
        if not self._native_enabled(): return None
        widget = QFrame(); widget.setFrameShape(QFrame.HLine); return self._add(widget)

    def collapsing_header(self, **kw): return self.group(tag=kw.get("tag"))
    def plot(self, **kw):
        widget = QTableWidget(0, 0)
        widget.setObjectName(kw.get("tag", "plot"))
        widget.setMinimumHeight(int(kw.get("height", 220)))
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        widget.setEditTriggers(QTableWidget.NoEditTriggers)
        widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return _Context(self, widget, kw.get("tag"), parent=kw.get("parent"))

    def plot_axis(self, *_, **kw):
        return _Context(self, None, kw.get("tag"))

    def add_plot_axis(self, *_, **kw):
        return self.plot_axis(**kw)

    def add_plot_legend(self, **_):
        return None

    def add_bar_series(self, values_x, values_y, label="", tag=None, **_):
        item = self.items.get(tag)
        if item is None:
            self.items[tag] = _Item(None)
        self.items[tag].data = {"x": list(values_x), "y": list(values_y), "label": label}

    def set_axis_ticks(self, tag, ticks):
        item = self.items.get(tag)
        if item is not None:
            item.data = list(ticks)
    def add_theme_color(self, *_, **__): pass
    def add_theme_style(self, *_, **__): pass
    def bind_theme(self, *_): pass
    def theme(self): return _Context(self, None)
    def theme_component(self, *_): return _Context(self, None)

    def does_item_exist(self, tag):
        # Headless tests exercise callbacks without building a widget tree;
        # desktop code uses the real registry.
        return tag in self.items or not self._native_enabled()

    def _set_value(self, tag, value):
        item = self.items.get(tag)
        if not item:
            item = self.items.setdefault(tag, _Item(None))
        item.value = value
        widget = item.widget
        if widget is None:
            return
        if isinstance(widget, QLineEdit): widget.setText(str(value))
        elif isinstance(widget, QComboBox): widget.setCurrentText(str(value))
        elif isinstance(widget, QCheckBox): widget.setChecked(bool(value))
        elif isinstance(widget, QSlider): widget.setValue(int(float(value) * 1000))
        elif isinstance(widget, (QDoubleSpinBox, QSpinBox)): widget.setValue(value)
        elif isinstance(widget, QLabel): widget.setText(str(value))
        elif isinstance(widget, QProgressBar): widget.setValue(int(float(value) * 1000))

    def get_value(self, tag):
        item = self.items.get(tag)
        if item is None:
            return None
        return self._value(item.widget) if item.widget else item.value

    def _configure_item(self, tag, **kw):
        item = self.items.get(tag)
        if item and item.widget and "show" in kw:
            item.widget.setVisible(bool(kw["show"]))

    def delete_item(self, tag, children_only=False, **_):
        item = self.items.get(tag)
        if item is None or item.widget is None:
            return
        if children_only:
            container = item.widget.widget() if isinstance(item.widget, QDockWidget) else item.widget
            layout = container.layout() if container else None
            if layout is None:
                return
            while layout.count():
                child = layout.takeAt(0)
                child_widget = child.widget()
                if child_widget is not None:
                    child_widget.deleteLater()
                    for child_tag, child_item in list(self.items.items()):
                        if child_item.widget is child_widget:
                            self.items.pop(child_tag, None)
            return
        self.items.pop(tag, None)
        item.widget.deleteLater()

    def replace_widget(self, tag, widget):
        item = self.items.get(tag)
        if item is None or item.widget is None:
            return
        old = item.widget
        layout = old.parentWidget().layout() if old.parentWidget() else None
        if layout is not None:
            index = layout.indexOf(old)
            layout.removeWidget(old)
            old.deleteLater()
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            widget.setMinimumSize(0, 0)
            layout.insertWidget(index, widget, 1)
            layout.setStretch(index, 1)
        item.widget = widget

    def get_item_rect_min(self, tag):
        item = self.items.get(tag)
        return (item.widget.x(), item.widget.y()) if item else (0.0, 0.0)

    def get_item_rect_max(self, tag):
        item = self.items.get(tag)
        return (item.widget.x() + item.widget.width(), item.widget.y() + item.widget.height()) if item else (0.0, 0.0)

    def get_mouse_pos(self, local=False): return (0.0, 0.0)
    def is_mouse_button_down(self, _): return False
    def is_mouse_button_clicked(self, _): return False
    def is_key_pressed(self, _): return False


qt = QtItems()
