from collections.abc import Generator

import pyads
from pyads import Connection
from pyqtconsole.console import PythonConsole
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class ConsoleWindow(QMainWindow):
    """Qt Window class for the main application."""

    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_NET_ID = "127.0.0.1.1.1"
    DEFAULT_PORT = pyads.PORT_TC3PLC1

    def __init__(self) -> None:
        super().__init__()

        self.plc: Connection | None = None

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        inputs_layout = QHBoxLayout()
        main_layout.addLayout(inputs_layout)

        self.input_host = QLineEdit(placeholderText=self.DEFAULT_HOST)
        self.input_ams_id = QLineEdit(placeholderText=self.DEFAULT_NET_ID)
        self.input_ams_port = QLineEdit(placeholderText=str(self.DEFAULT_PORT))
        self.check_connect = QCheckBox("Connect")

        self.input_host.setToolTip("Host")
        self.input_ams_id.setToolTip("AMS Net ID")
        self.input_ams_port.setToolTip("AMS Port")
        self.check_connect.setToolTip("Check to make the connection")

        self.input_ams_port.setValidator(QIntValidator())

        for edit in self.inputs:
            layout_col = QVBoxLayout()
            layout_col.addWidget(
                QLabel(edit.toolTip().title() + ":"),
            )
            layout_col.addWidget(edit)
            inputs_layout.addLayout(layout_col)

        inputs_layout.addWidget(self.check_connect)

        self.check_connect.stateChanged.connect(self.on_connect_changed)

        main_layout.addWidget(QLabel("Use the 'plc' variable for the local connection"))

        self.console = PythonConsole()
        main_layout.addWidget(self.console)
        self.console.eval_in_thread()

        self.console.interpreter.locals["clear"] = self.console.clear

        self.on_connect_changed(False)  # Initialize states by triggering the event

        self.show()

    def closeEvent(self, event) -> None:
        """Catch the 'exit' event to first shut down the console."""
        self.console.exit()

    @property
    def inputs(self) -> Generator[QLineEdit, None, None]:
        yield self.input_host
        yield self.input_ams_id
        yield self.input_ams_port

    @Slot()
    def on_connect_changed(self, state) -> None:
        """Callback when the checkbox gets (un)checked."""
        self.update_connect(Qt.CheckState(state) == Qt.CheckState.Checked)

    def update_connect(self, is_checked: bool) -> None:
        """Change the connected state."""
        for inp in self.inputs:
            inp.setDisabled(is_checked)

        self.console.setDisabled(not is_checked)

        if is_checked:
            host = self.input_host.text()
            net_id = self.input_ams_id.text()
            if not host and not net_id:
                host = self.DEFAULT_HOST
                net_id = self.DEFAULT_NET_ID
            if host and not net_id:
                net_id = f"{host}.1.1"
            elif not host and net_id:
                host = ".".join(net_id.split(".")[:4])

            port = int(self.input_ams_port.text() or self.DEFAULT_PORT)

            self.plc = Connection(net_id, port, host)
            self.plc.open()

            self.console.interpreter.locals["plc"] = self.plc
        else:
            if self.plc:
                self.plc.close()
            self.plc = None
            self.console.interpreter.locals["plc"] = None
