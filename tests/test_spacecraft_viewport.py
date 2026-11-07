import numpy as np
import pytest

from rendering import OpenGLRenderer
from spacecraft.presets import load_spacecraft
from spacecraft.vehicle import Spacecraft
from ui.spacecraft_designer import DEFAULT_PRESET
from viewport import SpacecraftViewport


@pytest.fixture(scope="module")
def renderer():
    return OpenGLRenderer()


def _render(viewport, renderer):
    renderer.begin_frame()
    viewport.render(renderer)


def test_viewport_renders_and_picks_components(renderer):
    craft = load_spacecraft(DEFAULT_PRESET)
    viewport = SpacecraftViewport(lambda: craft)

    _render(viewport, renderer)

    found = set()
    for ix in range(10, 90, 2):
        for iy in range(5, 95, 2):
            picked = viewport.pick(renderer, ix / 100, iy / 100)
            if picked:
                found.add(picked)
    assert found
    assert found <= {c.id for c in craft.components}
    assert viewport.pick(renderer, 0.0, 0.0) is None


def test_viewport_handles_empty_design_and_stale_selection(renderer):
    craft = Spacecraft()
    viewport = SpacecraftViewport(lambda: craft)
    viewport.selected_id = "missing"

    _render(viewport, renderer)

    assert viewport.layout.parts == []


def test_selecting_component_does_not_change_camera_framing():
    craft = load_spacecraft(DEFAULT_PRESET)
    viewport = SpacecraftViewport(lambda: craft)
    viewport._refresh_layout()
    center = viewport.layout.camera_center.copy()
    distance = viewport.camera.distance

    viewport.selected_id = craft.components[0].id
    viewport.update(1.0)

    np.testing.assert_array_equal(viewport.camera.target, center)
    assert viewport.camera.distance == distance


def test_invalidate_keeps_pending_reframe():
    viewport = SpacecraftViewport(lambda: Spacecraft())

    viewport.invalidate(reframe=False)

    assert viewport._reframe is True
