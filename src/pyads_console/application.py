from PySide6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QWidget


class ConsoleWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        main_layout.addWidget(QLabel("Hello world"))

        self.show()
