import pytest

from ui.qt_widgets import QApplication, QDockWidget, QTableWidget, qt


@pytest.fixture
def qt_window():
    qt.create_context()
    qt.create_viewport(width=900, height=600)
    yield qt
    qt.destroy_context()


def test_native_docks_are_registered_and_parented(qt_window):
    with qt_window.window(tag="spacecraft_designer_window"):
        qt_window.add_text("Designer", tag="designer_label")
    with qt_window.window(tag="viewport_window"):
        qt_window.add_text("Viewport", tag="viewport_label")

    assert isinstance(qt_window.items["spacecraft_designer_window"].widget, QDockWidget)
    assert isinstance(qt_window.items["viewport_window"].widget, QDockWidget)
    assert qt_window.items["designer_label"].widget.text() == "Designer"


def test_children_only_deletion_preserves_parent(qt_window):
    with qt_window.window(tag="viewport_window"):
        qt_window.add_text("First", tag="first")
        qt_window.add_text("Second", tag="second")

    parent = qt_window.items["viewport_window"].widget.widget()
    qt_window.delete_item("viewport_window", children_only=True)

    assert "viewport_window" in qt_window.items
    assert parent.layout().count() == 0
    assert "first" not in qt_window.items
    assert "second" not in qt_window.items


def test_replacing_viewport_keeps_single_expanding_widget(qt_window):
    with qt_window.window(tag="viewport_window"):
        qt_window.add_text("placeholder", tag="viewport_image")

    replacement = QTableWidget()
    qt_window.replace_widget("viewport_image", replacement)

    item = qt_window.items["viewport_image"]
    assert item.widget is replacement
    assert replacement.parentWidget() is not None
    assert replacement.sizePolicy().expandingDirections()


def test_plot_series_are_data_backed(qt_window):
    with qt_window.window(tag="viewport_window"):
        with qt_window.plot(tag="plot"):
            qt_window.add_bar_series([0], [1.5], label="Dry mass", tag="series")

    assert qt_window.items["series"].data == {"x": [0], "y": [1.5], "label": "Dry mass"}
