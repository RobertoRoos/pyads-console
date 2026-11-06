import sys

from PySide6.QtWidgets import QApplication

from pyads_console.application import ConsoleWindow


def main() -> int:
    app = QApplication(sys.argv)

    _ = ConsoleWindow()

    return app.exec()


if __name__ == "__main__":
    code = main()
    sys.exit(code)
