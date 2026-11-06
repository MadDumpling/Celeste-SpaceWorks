import dearpygui.dearpygui as dpg


def _apply_space_theme():
    with dpg.theme() as theme, dpg.theme_component(dpg.mvAll):
        for color, value in (
            (dpg.mvThemeCol_WindowBg, (10, 15, 30, 255)),
            (dpg.mvThemeCol_ChildBg, (15, 23, 42, 255)),
            (dpg.mvThemeCol_PopupBg, (19, 29, 52, 255)),
            (dpg.mvThemeCol_Text, (229, 238, 250, 255)),
            (dpg.mvThemeCol_Border, (52, 73, 105, 255)),
            (dpg.mvThemeCol_FrameBg, (23, 36, 61, 255)),
            (dpg.mvThemeCol_FrameBgHovered, (35, 57, 91, 255)),
            (dpg.mvThemeCol_FrameBgActive, (45, 75, 111, 255)),
            (dpg.mvThemeCol_TitleBg, (10, 15, 30, 255)),
            (dpg.mvThemeCol_TitleBgActive, (19, 31, 56, 255)),
            (dpg.mvThemeCol_Button, (25, 57, 82, 255)),
            (dpg.mvThemeCol_ButtonHovered, (31, 105, 126, 255)),
            (dpg.mvThemeCol_ButtonActive, (38, 133, 145, 255)),
            (dpg.mvThemeCol_Header, (20, 49, 73, 255)),
            (dpg.mvThemeCol_HeaderHovered, (29, 78, 105, 255)),
            (dpg.mvThemeCol_HeaderActive, (35, 99, 119, 255)),
            (dpg.mvThemeCol_Tab, (16, 27, 49, 255)),
            (dpg.mvThemeCol_TabHovered, (27, 71, 94, 255)),
            (dpg.mvThemeCol_TabActive, (25, 79, 98, 255)),
            (dpg.mvThemeCol_CheckMark, (80, 226, 190, 255)),
            (dpg.mvThemeCol_SliderGrab, (80, 226, 190, 255)),
            (dpg.mvThemeCol_SliderGrabActive, (126, 245, 207, 255)),
        ):
            dpg.add_theme_color(color, value)
        for style, value in (
            (dpg.mvStyleVar_WindowRounding, 11),
            (dpg.mvStyleVar_FrameRounding, 7),
            (dpg.mvStyleVar_GrabRounding, 5),
            (dpg.mvStyleVar_TabRounding, 7),
            (dpg.mvStyleVar_WindowPadding, (14, 14)),
            (dpg.mvStyleVar_FramePadding, (9, 6)),
            (dpg.mvStyleVar_ItemSpacing, (9, 8)),
        ):
            if isinstance(value, tuple):
                dpg.add_theme_style(style, *value)
            else:
                dpg.add_theme_style(style, value)
    dpg.bind_theme(theme)


def create_dockspace():
    _apply_space_theme()
    with dpg.viewport_menu_bar(), dpg.menu(label="File"):
        dpg.add_menu_item(
            label="Exit",
            callback=dpg.stop_dearpygui,
        )

    with dpg.window(
        tag="primary_window",
        no_background=True,
        no_title_bar=True,
        no_move=True,
        no_resize=True,
        no_close=True,
        no_collapse=True,
    ):
        pass

    with dpg.window(
        label="Viewport",
        tag="viewport_window",
        pos=(525, 28),
        width=1385,
        height=1025,
    ):
        with dpg.texture_registry():
            dpg.add_dynamic_texture(
                width=1280,
                height=720,
                default_value=[0.0] * (1280 * 720 * 4),
                tag="viewport_texture",
            )

        dpg.add_text(
            "Left-drag orbit · Right/middle-drag pan · Wheel zoom · "
            "Click select · F frame · R reset",
            color=(150, 165, 185),
        )
        dpg.add_text(
            "No component selected",
            tag="viewport_component_title",
            color=(255, 190, 80),
        )
        dpg.add_text(
            "Select a part to inspect its mass and modeled hardware ratings.",
            tag="viewport_component_details",
            color=(195, 205, 220),
        )
        dpg.add_text(" ", tag="mission_banner", wrap=1320)
        dpg.add_image(
            "viewport_texture",
            tag="viewport_image",
            width=1280,
            height=720,
        )
        dpg.add_text(
            "",
            tag="fps_text",
            color=(150, 165, 185),
        )
