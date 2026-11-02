# Copilot Instructions

## Project Guidelines
- The app is a spacecraft configurator: the Qt designer panel edits a `Spacecraft`, and `viewport.SpacecraftViewport` draws it with the OpenGL renderer in the Qt application.
- Keep `spacecraft/` (domain, geometry) free of UI and GL imports so it stays testable headlessly.
