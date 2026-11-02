import numpy as np
import pytest

from spacecraft.geometry import primitive, scale
from rendering import (
    OpenGLRenderer,
)
from rendering import opengl_renderer
from viewport.orbit_camera import OrbitCamera


def test_opengl_context_created():

    renderer = (
        OpenGLRenderer()
    )

    assert (
        renderer.ctx
        is not None
    )


def test_fbo_created():

    renderer = (
        OpenGLRenderer()
    )

    assert (
        renderer.fbo
        is not None
    )


def test_texture_created():

    renderer = (
        OpenGLRenderer()
    )

    assert (
        renderer.texture
        is not None
    )


def test_end_frame_does_not_read_back_a_full_frame(monkeypatch):
    renderer = OpenGLRenderer.__new__(OpenGLRenderer)
    renderer.width = 2
    renderer.height = 2

    read_calls = []

    class FakeTexture:
        def read(self):
            read_calls.append(True)
            return bytes(16)

    renderer.texture = FakeTexture()
    renderer.end_frame()

    assert read_calls == []


def test_end_frame_has_no_ui_texture_dependency():
    renderer = OpenGLRenderer.__new__(OpenGLRenderer)
    renderer.width = 1
    renderer.height = 1
    renderer.texture = type(
        "FakeTexture",
        (),
        {"read": lambda self: bytes((0, 0, 0, 255))},
    )()
    renderer.end_frame()


@pytest.fixture(scope="module")
def shared_renderer():
    return OpenGLRenderer()


def _camera_looking_down_z(renderer):
    camera = OrbitCamera()
    camera.yaw = 0.0
    camera.pitch = 0.0
    camera.distance = 6.0
    renderer.set_camera(
        camera.view_projection(renderer.aspect),
        camera.eye,
    )


def test_draw_mesh_renders_pixels_and_picks_id(shared_renderer):
    renderer = shared_renderer
    _camera_looking_down_z(renderer)
    renderer.begin_frame()
    renderer.draw_mesh(
        "box",
        primitive("box"),
        scale(2.0, 2.0, 2.0),
        (1.0, 0.2, 0.2),
        pick_id=7,
    )

    assert renderer.pick(0.5, 0.5) == 7
    assert renderer.pick(0.02, 0.02) == 0
    assert renderer.pick(2.0, 0.5) == 0

    renderer.end_frame()
    centre = np.frombuffer(renderer.texture.read(), dtype=np.uint8).reshape(
        (renderer.height, renderer.width, 4)
    )[renderer.height // 2, renderer.width // 2]
    assert centre[0] > centre[2]


def test_draw_lines_3d_accepts_segments(shared_renderer):
    renderer = shared_renderer
    _camera_looking_down_z(renderer)
    renderer.begin_frame()
    renderer.draw_lines_3d(
        np.array([(-1, 0, 0), (1, 0, 0)], dtype=np.float32),
        (1.0, 1.0, 1.0, 1.0),
    )
    renderer.draw_lines_3d(np.empty((0, 3), dtype=np.float32), (1, 1, 1))
    renderer.end_frame()
