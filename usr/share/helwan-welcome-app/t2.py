#!/usr/bin/env python3

import sys
import os
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QComboBox, QProgressBar, QDialog, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
import subprocess
import socket
import threading
import gettext

# تعيين اللغة الافتراضية وتبديلها
def set_language(language_code):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))  # المسار الحالي للملف
        lang_path = os.path.join(current_dir, 'locales')  # مسار ملفات الترجمة
        language = gettext.translation('base', localedir=lang_path, languages=[language_code])
        language.install()
        return language.gettext
    except FileNotFoundError:
        print(f"Error: Locale files for '{language_code}' not found. Falling back to English.")
        language = gettext.translation('base', localedir=lang_path, languages=['en'])
        language.install()
        return language.gettext

# اللغة الافتراضية
language_code = 'en'
_ = set_language(language_code)

class Worker(QObject):
    finished = pyqtSignal(str)
    progress = pyqtSignal(int)
    error = pyqtSignal(str)
    operation_completed = pyqtSignal(str, str) # operation, message

    def __init__(self, parent=None):
        super().__init__(parent)
        self.command = []
        self.operation_name = ""

    def set_command(self, command, operation_name):
        self.command = command
        self.operation_name = operation_name

    def run(self):
        try:
            process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                print(output.strip())  # يمكنك هنا معالجة المخرجات لعرض التقدم بشكل أدق إذا كان ذلك ممكنًا

            return_code = process.wait()
            if return_code == 0:
                self.operation_completed.emit(self.operation_name, _("{} completed successfully.").format(self.operation_name))
            else:
                error_output = process.stderr.read()
                self.error.emit(_("Failed to {}.").format(self.operation_name) + f"\n{error_output}")
        except FileNotFoundError:
            self.error.emit(_("Error: Command not found."))
        except Exception as e:
            self.error.emit(f"An unexpected error occurred: {e}")
        finally:
            self.finished.emit("Done")

class WelcomeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(_("Welcome to Helwan Linux"))
        self.setGeometry(100, 100, 400, 750)  # زيادة الطول لاستيعاب العناصر الجديدة
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #e0e0e0;
                color: #333;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px 15px;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QCheckBox {
                color: #333;
                margin-top: 8px;
            }
            QComboBox {
                background-color: #fff;
                color: #333;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 6px;
                margin-top: 5px;
            }
            QProgressBar {
                margin-top: 10px;
            }
        """)

        self.startup_file = os.path.join(os.path.expanduser("~"), ".helwan_welcome_shown")
        self.show_on_startup = not os.path.exists(self.startup_file)

        self.logo = self.load_logo()
        self.init_ui()

        self.worker_thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.operation_completed.connect(self.show_operation_completed_message)
        self.worker.error.connect(self.show_error_message)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

    def load_logo(self):
        try:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources", "logo.png")
            if os.path.exists(logo_path):
                logo = QPixmap(logo_path)
                if not logo.isNull():
                    scaled_logo = logo.scaledToWidth(120, Qt.SmoothTransformation)
                    return scaled_logo
                else:
                    print(f"Error: Image at {logo_path} is invalid.")
                    return None
            else:
                print(f"Error: Logo image not found at {logo_path}")
                return None
        except Exception as e:
            print(f"Error loading logo: {e}")
            return None

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        if self.logo:
            logo_label = QLabel(self)
            logo_label.setPixmap(self.logo)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)

        self.greeting_label = QLabel(_("Welcome to the world of Helwan Linux! ❤️\nWe are here to help you build your dreams on the strongest foundation!"))
        self.greeting_label.setAlignment(Qt.AlignCenter)
        self.greeting_label.setStyleSheet("font-size: 15px; margin-top: 15px; margin-bottom: 25px; color: #555;")
        layout.addWidget(self.greeting_label)

        self.controls_layout = QVBoxLayout()
        self.controls_layout.setSpacing(12)
        layout.addLayout(self.controls_layout)

        # Application Language
        language_hbox = QHBoxLayout()
        self.app_language_label = QLabel(_("Application Language:"))
        language_hbox.addWidget(self.app_language_label)
        language_hbox.addStretch(1)
        self.language_menu_app = QComboBox(self)
        self.language_menu_app.addItems(['en', 'ar', 'es', 'pt'])
        self.language_menu_app.setCurrentText(language_code)
        self.language_menu_app.currentTextChanged.connect(self.change_language)
        language_hbox.addWidget(self.language_menu_app)
        self.controls_layout.addLayout(language_hbox)

        # Show on startup
        self.startup_checkbutton = QCheckBox(_("Show on startup"))
        self.startup_checkbutton.setChecked(self.show_on_startup)
        self.startup_checkbutton.stateChanged.connect(self.toggle_startup)
        self.controls_layout.addWidget(self.startup_checkbutton)

        # Update Buttons
        update_buttons_row1 = QHBoxLayout()
        self.update_pacman_button = QPushButton(_("Update System (Pacman)"), self)
        self.update_pacman_button.clicked.connect(lambda: self.start_operation(["sudo", "pacman", "-Syu", "--noconfirm"], _("System Update (Pacman)")))
        update_buttons_row1.addWidget(self.update_pacman_button)

        self.update_yay_button = QPushButton(_("Update System (Yay)"), self)
        self.update_yay_button.clicked.connect(lambda: self.start_operation(["yay", "-Syu", "--noconfirm"], _("System Update (Yay)")))
        update_buttons_row1.addWidget(self.update_yay_button)
        self.controls_layout.addLayout(update_buttons_row1)

        # System Language
        system_language_hbox = QHBoxLayout()
        self.system_language_label = QLabel(_("System Language:"))
        system_language_hbox.addWidget(self.system_language_label)
        system_language_hbox.addStretch(1)
        self.system_language_combobox = QComboBox(self)
        self.system_language_combobox.addItems(['ar_EG.UTF-8', 'en_US.UTF-8', 'es_ES.UTF-8', 'pt_PT.UTF-8'])
        self.system_language_combobox.setCurrentText('ar_EG.UTF-8')
        system_language_hbox.addWidget(self.system_language_combobox)
        self.controls_layout.addLayout(system_language_hbox)

        self.change_system_language_button = QPushButton(_("Apply System Language"), self)
        self.change_system_language_button.clicked.connect(self.apply_system_language)
        self.controls_layout.addWidget(self.change_system_language_button)

        # Kernel Installation
        kernel_hbox = QHBoxLayout()
        self.kernel_label = QLabel(_("Install Kernel:"))
        kernel_hbox.addWidget(self.kernel_label)
        kernel_hbox.addStretch(1)
        self.kernel_combobox = QComboBox(self)
        self.kernel_combobox.addItems(['linux-lts', 'linux-zen', 'linux-hardened'])
        kernel_hbox.addWidget(self.kernel_combobox)
        self.controls_layout.addLayout(kernel_hbox)

        self.install_kernel_button = QPushButton(_("Install Selected Kernel"), self)
        self.install_kernel_button.clicked.connect(self.install_selected_kernel)
        self.controls_layout.addWidget(self.install_kernel_button)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0) # الوضع المشغول افتراضيًا
        self.progress_bar.hide()
        self.controls_layout.addWidget(self.progress_bar)

        # Other Buttons
        other_buttons_row = QHBoxLayout()
        self.documentation_button = QPushButton(_("Open Documentation"), self)
        self.documentation_button.clicked.connect(self.open_documentation)
        other_buttons_row.addWidget(self.documentation_button)

        self.quit_button = QPushButton(_("Quit"), self)
        self.quit_button.clicked.connect(self.close)
        other_buttons_row.addWidget(self.quit_button)
        self.controls_layout.addLayout(other_buttons_row)

    def change_language(self, language_code):
        global _
        _ = set_language(language_code)
        self.greeting_label.setText(_("Welcome to the world of Helwan Linux! ❤️\nWe are here to help you build your dreams on the strongest foundation!"))

    def toggle_startup(self, state):
        if state == Qt.Checked:
            os.system("echo '@python3 {0}/helwan_startup.py' >> ~/.config/autostart/helwan.desktop".format(os.path.expanduser("~")))
            with open(self.startup_file, "w"): pass
        else:
            os.remove(self.startup_file)
            os.system("rm ~/.config/autostart/helwan.desktop")

    def start_operation(self, command, operation_name):
        self.worker.set_command(command, operation_name)
        self.worker_thread.start()

    def show_operation_completed_message(self, operation, message):
        QMessageBox.information(self, operation, message)

    def show_error_message(self, error_message):
        QMessageBox.critical(self, _("Error"), error_message)

    def apply_system_language(self):
        system_language = self.system_language_combobox.currentText()
        confirmation = QMessageBox.question(self, _("Confirm System Language Change"), _("Are you sure you want to change system language to {}?".format(system_language)), QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            self.start_operation(["sudo", "localectl", "set-locale", "LANG=" + system_language], _("System Language Change"))

    def install_selected_kernel(self):
        selected_kernel = self.kernel_combobox.currentText()
        confirmation = QMessageBox.question(self, _("Confirm Kernel Installation"), _("Are you sure you want to install the selected kernel: {}?".format(selected_kernel)), QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            self.start_operation(["sudo", "pacman", "-S", selected_kernel, "--noconfirm"], _("Kernel Installation"))

    def open_documentation(self):
        url = "https://www.archlinux.org/doc/"
        webbrowser.open(url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelcomeApp()
    window.show()
    sys.exit(app.exec_())
