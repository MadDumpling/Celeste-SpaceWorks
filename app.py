from ui import Application, DesignerApplication


def main():
    app = Application()
    app.initialize()

    designer_app = DesignerApplication()
    designer_app.initialize()

    try:
        app.run(designer_app)
    finally:
        designer_app.shutdown()
        app.shutdown()


if __name__ == "__main__":
    main()