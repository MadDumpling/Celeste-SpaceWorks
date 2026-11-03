"""Qt-owned OpenGL surface for the spacecraft viewport."""
from __future__ import annotations

try:
    import moderngl
    from PySide6.QtCore import Qt
    from PySide6.QtOpenGLWidgets import QOpenGLWidget
except ImportError:
    moderngl = None
    Qt = None
    QOpenGLWidget = object


class QtOpenGLViewport(QOpenGLWidget):
    """Native Qt surface that renders directly into Qt's default FBO."""

    def __init__(self, render_scene, parent=None):
        super().__init__(parent)
        self._render_scene = render_scene
        self.renderer = None
        self._qt_framebuffer = None
        self._input_source = None
        self.setMinimumSize(1, 1)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus if Qt is not None else 0)

    def set_input_source(self, input_source):
        self._input_source = input_source

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
        dpr = self.devicePixelRatioF()

        self.renderer.resize(
            int(self.width() * dpr),
            int(self.height() * dpr),
        )
        print(context.fbo)
        print(context.screen)
        print(self._qt_framebuffer)

    def paintGL(self):
        if self.renderer is None:
            return

        current_fbo = self.renderer.ctx.detect_framebuffer()

        self.renderer.set_qt_framebuffer(current_fbo)

        self.renderer.begin_frame()
        self._render_scene(self.renderer)
        self.renderer.end_frame()

    def resizeGL(self, width, height):
        if self.renderer is not None:
            self._qt_framebuffer = self.renderer.ctx.detect_framebuffer()

            self.renderer.set_qt_framebuffer(
                self.renderer.ctx.detect_framebuffer()
            )

            dpr = self.devicePixelRatioF()

            self.renderer.resize(
                int(self.width() * dpr),
                int(self.height() * dpr),
            )


    def mouseMoveEvent(self, event):
        if self._input_source is not None:
            self._input_source.mouse_move(event.position().x(), event.position().y())
        self.update()
        event.accept()

    def mousePressEvent(self, event):
        if self._input_source is not None:
            self._input_source.mouse_move(event.position().x(), event.position().y())
            self._input_source.mouse_press(self._button_name(event.button()))
        self.setFocus()
        event.accept()

    def mouseReleaseEvent(self, event):
        if self._input_source is not None:
            self._input_source.mouse_move(event.position().x(), event.position().y())
            self._input_source.mouse_release(self._button_name(event.button()))
        event.accept()

    def wheelEvent(self, event):
        if self._input_source is not None:
            self._input_source.on_wheel(event.angleDelta().y() / 120.0)
        event.accept()

    def enterEvent(self, event):
        if self._input_source is not None:
            self._input_source.enter()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self._input_source is not None:
            self._input_source.leave()
        super().leaveEvent(event)

    def keyPressEvent(self, event):
        if self._input_source is not None:
            self._input_source.key_press(event.text())
        event.accept()

    @staticmethod
    def _button_name(button):
        return {
            Qt.LeftButton: "left",
            Qt.RightButton: "right",
            Qt.MiddleButton: "middle",
        }.get(button, "")
