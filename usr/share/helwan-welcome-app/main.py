#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication
from welcome_window import WelcomeApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelcomeApp()
    window.show()
    sys.exit(app.exec_())
