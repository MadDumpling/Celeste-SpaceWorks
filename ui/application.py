from .qt_widgets import qt
try:
    from PySide6.QtCore import QTimer
except ImportError:
    QTimer = None


class Application:

    def initialize(self):

        qt.create_context()

        qt.configure_app(
            docking=True,
            docking_space=True,
            # Qt delivers widget signals on the GUI thread.
        )

        qt.create_viewport(
            title="Spacecraft Configurator",
            width=1920,
            height=1080,
        )

        qt.setup()
        qt.show_viewport()

    def running(self):
        return qt.is_running()

    @staticmethod
    def run_callbacks():
        """Run queued widget callbacks on this (the main) thread."""
        qt.process_events()

    def render(self):
        self.run_callbacks()

    def run(self, designer_app):
        if QTimer is None:
            return
        timer = QTimer()
        timer.timeout.connect(designer_app.update)
        timer.start(16)
        return qt.application.exec()

    def shutdown(self):
        qt.destroy_context()
