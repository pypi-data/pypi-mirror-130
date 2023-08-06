import sys

from PyQt5.QtWidgets import QApplication, QDesktopWidget

from .src.control.controller import Controller
from .src.view.gui import GUI


def main():

    print("Showing GUI...")
    app = QApplication(sys.argv)

    # Setup Model-View-Control structure
    control = Controller()
    view = GUI(control)

    # Install event filter to catch user interventions
    app.installEventFilter(view)

    # Start GUI
    view.show()

    print("Showing GUI...")

    app.setStyle("Fusion")

    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - view.width()) / 2
    height = (desktop.height() - view.height()) / 2
    view.move(width, height)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
