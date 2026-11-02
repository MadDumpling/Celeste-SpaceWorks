from .qt_widgets import qt


def _apply_space_theme():
    with qt.theme() as theme, qt.theme_component(qt.mvAll):
        for color, value in (
            (qt.mvThemeCol_WindowBg, (13, 19, 31, 255)),
            (qt.mvThemeCol_ChildBg, (17, 26, 42, 255)),
            (qt.mvThemeCol_PopupBg, (20, 30, 48, 255)),
            (qt.mvThemeCol_Text, (225, 233, 244, 255)),
            (qt.mvThemeCol_Border, (50, 67, 91, 255)),
            (qt.mvThemeCol_FrameBg, (26, 39, 59, 255)),
            (qt.mvThemeCol_FrameBgHovered, (38, 58, 84, 255)),
            (qt.mvThemeCol_FrameBgActive, (48, 72, 101, 255)),
            (qt.mvThemeCol_TitleBg, (13, 19, 31, 255)),
            (qt.mvThemeCol_TitleBgActive, (22, 34, 54, 255)),
            (qt.mvThemeCol_Button, (31, 55, 81, 255)),
            (qt.mvThemeCol_ButtonHovered, (43, 82, 116, 255)),
            (qt.mvThemeCol_ButtonActive, (50, 104, 141, 255)),
            (qt.mvThemeCol_Header, (24, 48, 72, 255)),
            (qt.mvThemeCol_HeaderHovered, (34, 69, 100, 255)),
            (qt.mvThemeCol_HeaderActive, (42, 87, 120, 255)),
            (qt.mvThemeCol_Tab, (21, 34, 53, 255)),
            (qt.mvThemeCol_TabHovered, (40, 76, 107, 255)),
            (qt.mvThemeCol_TabActive, (32, 63, 91, 255)),
            (qt.mvThemeCol_CheckMark, (255, 170, 64, 255)),
            (qt.mvThemeCol_SliderGrab, (255, 170, 64, 255)),
            (qt.mvThemeCol_SliderGrabActive, (255, 195, 105, 255)),
        ):
            qt.add_theme_color(color, value)
        for style, value in (
            (qt.mvStyleVar_WindowRounding, 8),
            (qt.mvStyleVar_FrameRounding, 5),
            (qt.mvStyleVar_GrabRounding, 5),
            (qt.mvStyleVar_TabRounding, 5),
            (qt.mvStyleVar_WindowPadding, (12, 12)),
            (qt.mvStyleVar_FramePadding, (8, 5)),
            (qt.mvStyleVar_ItemSpacing, (8, 7)),
        ):
            if isinstance(value, tuple):
                qt.add_theme_style(style, *value)
            else:
                qt.add_theme_style(style, value)
    qt.bind_theme(theme)


def create_dockspace():
    _apply_space_theme()
    with qt.viewport_menu_bar(), qt.menu(label="File"):
        qt.add_menu_item(
            label="Exit",
            callback=qt.stop,
        )

    with qt.window(
        tag="primary_window",
        no_background=True,
        no_title_bar=True,
        no_move=True,
        no_resize=True,
        no_close=True,
        no_collapse=True,
    ):
        pass

    with qt.window(
        label="Viewport",
        tag="viewport_window",
        pos=(525, 28),
        width=1385,
        height=1025,
    ):
        qt.add_text(
            "Left-drag orbit · Right/middle-drag pan · Wheel zoom · "
            "Click select · F frame · R reset",
            color=(150, 165, 185),
        )
        qt.add_text(
            "No component selected",
            tag="viewport_component_title",
            color=(255, 190, 80),
        )
        qt.add_text(
            "Select a part to inspect its mass and modeled hardware ratings.",
            tag="viewport_component_details",
            color=(195, 205, 220),
        )
        qt.add_text(" ", tag="mission_banner", wrap=1320)
        qt.add_text(
            "OpenGL viewport",
            tag="viewport_image",
            width=1280,
        )
        qt.add_text(
            "",
            tag="fps_text",
            color=(150, 165, 185),
        )

