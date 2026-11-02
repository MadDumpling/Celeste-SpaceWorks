"""Qt-owned OpenGL surface for the spacecraft viewport."""
from __future__ import annotations

try:
    import moderngl
    from PySide6.QtOpenGLWidgets import QOpenGLWidget
except ImportError:
    moderngl = None
    QOpenGLWidget = object


class QtOpenGLViewport(QOpenGLWidget):
    """Native Qt surface that renders directly into Qt's default FBO."""

    def __init__(self, render_scene, parent=None):
        super().__init__(parent)
        self._render_scene = render_scene
        self.renderer = None
        self._qt_framebuffer = None
        self.setMinimumSize(1, 1)

    def initializeGL(self):
        if moderngl is None:
            return
        from rendering import OpenGLRenderer

        # Qt has made its context current and bound QOpenGLWidget's private
        # default FBO at this point.  ModernGL must use that FBO; framebuffer 0
        # is not the paint target of a QOpenGLWidget.
        context = moderngl.create_context()
        self._qt_framebuffer = context.detect_framebuffer()
        self.renderer = OpenGLRenderer(
            context=context,
            qt_framebuffer=self._qt_framebuffer,
        )
        self.renderer.resize(self.width(), self.height())

    def paintGL(self):
        if self.renderer is None:
            return
        self.renderer.set_qt_framebuffer(self._qt_framebuffer)
        self.renderer.begin_frame()
        self._render_scene(self.renderer)
        self.renderer.end_frame()

    def resizeGL(self, width, height):
        if self.renderer is not None:
            self._qt_framebuffer = self.renderer.ctx.detect_framebuffer()
            self.renderer.set_qt_framebuffer(self._qt_framebuffer)
            self.renderer.resize(width, height)
