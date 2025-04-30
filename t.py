import sys
import os
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QComboBox, QProgressBar, QDialog, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
import subprocess
import socket
import threading
import gettext

# تعيين اللغة الافتراضية وتبديلها
def set_language(language_code):
    try:
        language = gettext.translation('base', localedir='locales', languages=[language_code])
        language.install()
        return language.gettext
    except FileNotFoundError:
        print(f"Error: Locale files for '{language_code}' not found. Falling back to English.")
        language = gettext.translation('base', localedir='locales', languages=['en'])
        language.install()
        return language.gettext

# اللغة الافتراضية
language_code = 'en'
_ = set_language(language_code)

class WelcomeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(_("Welcome to Helwan Linux"))
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0; font-family: Arial, sans-serif;")

        self.startup_file = os.path.join(os.path.expanduser("~"), ".helwan_welcome_shown")
        self.show_on_startup = not os.path.exists(self.startup_file)

        self.logo = self.load_logo()
        self.init_ui()

    def load_logo(self):
        try:
            # تأكد من أن المسار يحتوي على الصورة
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources", "logo.png")
            # إذا كانت الصورة موجودة وقابلة للتحميل
            if os.path.exists(logo_path):
                logo = QPixmap(logo_path)  # تحميل الصورة مباشرة كـ QPixmap
                if not logo.isNull():
                    return logo
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

        if self.logo:
            self.logo_label = QLabel(self)
            self.logo_label.setPixmap(self.logo)
            self.logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.logo_label)

        self.greeting_label = QLabel(_("Welcome to the world of Helwan Linux! ❤️\nWe are here to help you build your dreams on the strongest foundation!"))
        self.greeting_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.greeting_label)

        self.buttons_frame = QVBoxLayout()
        layout.addLayout(self.buttons_frame)

        self.language_label_app = QLabel(_("Application Language:"))
        self.buttons_frame.addWidget(self.language_label_app)

        self.language_menu_app = QComboBox(self)
        self.language_menu_app.addItems(['en', 'ar', 'es', 'pt'])
        self.language_menu_app.setCurrentText(language_code)
        self.language_menu_app.currentTextChanged.connect(self.change_language)
        self.buttons_frame.addWidget(self.language_menu_app)

        self.startup_checkbutton = QCheckBox(_("Show on startup"))
        self.startup_checkbutton.setChecked(self.show_on_startup)
        self.startup_checkbutton.stateChanged.connect(self.toggle_startup)
        self.buttons_frame.addWidget(self.startup_checkbutton)

        self.update_pacman_button = QPushButton(_("Update System (Pacman)"), self)
        self.update_pacman_button.clicked.connect(lambda: self.update_system("pacman"))
        self.buttons_frame.addWidget(self.update_pacman_button)

        self.update_yay_button = QPushButton(_("Update System (Yay)"), self)
        self.update_yay_button.clicked.connect(lambda: self.update_system("yay"))
        self.buttons_frame.addWidget(self.update_yay_button)

        self.system_language_combobox = QComboBox(self)
        self.system_language_combobox.addItems(['ar_EG.UTF-8', 'en_US.UTF-8', 'es_ES.UTF-8', 'pt_PT.UTF-8'])
        self.system_language_combobox.setCurrentText('ar_EG.UTF-8')
        self.change_system_language_button = QPushButton(_("Apply System Language"), self)
        self.change_system_language_button.clicked.connect(self.apply_system_language)
        self.buttons_frame.addWidget(self.system_language_combobox)
        self.buttons_frame.addWidget(self.change_system_language_button)

        self.documentation_button = QPushButton(_("Open Documentation"), self)
        self.documentation_button.clicked.connect(self.open_documentation)
        layout.addWidget(self.documentation_button)

        self.youtube_button = QPushButton(_("Open YouTube Channel"), self)
        self.youtube_button.clicked.connect(self.open_youtube_channel)
        layout.addWidget(self.youtube_button)

        self.system_info_button = QPushButton(_("Show System Info"), self)
        self.system_info_button.clicked.connect(self.show_system_info)
        layout.addWidget(self.system_info_button)

        self.performance_monitor_button = QPushButton(_("Performance Monitor"), self)
        self.performance_monitor_button.clicked.connect(self.show_performance)
        layout.addWidget(self.performance_monitor_button)

        if self.show_on_startup:
            self.mark_as_shown()

    def change_language(self, language_code):
        global _
        _ = set_language(language_code)
        self.update_ui()

    def update_ui(self):
        self.setWindowTitle(_("Welcome to Helwan Linux"))
        self.greeting_label.setText(_("Welcome to the world of Helwan Linux! ❤️\nWe are here to help you build your dreams on the strongest foundation!"))
        self.language_label_app.setText(_("Application Language:"))
        self.update_pacman_button.setText(_("Update System (Pacman)"))
        self.update_yay_button.setText(_("Update System (Yay)"))
        self.change_system_language_button.setText(_("Apply System Language"))
        self.documentation_button.setText(_("Open Documentation"))
        self.youtube_button.setText(_("Open YouTube Channel"))
        self.startup_checkbutton.setText(_("Show on startup"))
        self.system_info_button.setText(_("Show System Info"))
        self.performance_monitor_button.setText(_("Performance Monitor"))

    def open_documentation(self):
        webbrowser.open("https://helwan-linux.mystrikingly.com/documentation")

    def open_youtube_channel(self):
        webbrowser.open("https://www.youtube.com/channel/UCKlFDMjrzkVFzw-erYKVibQ")

    def update_system(self, manager):
        if not self.check_internet_connection():
            self.show_message(_("Error"), _("No internet connection."))
            return

        progress_window = QDialog(self)
        progress_window.setWindowTitle(_("Updating System"))
        progress_window.setFixedSize(400, 100)
        progress_layout = QVBoxLayout(progress_window)
        progress_label = QLabel(_("Updating system, please wait..."), progress_window)
        progress_layout.addWidget(progress_label)

        progress = QProgressBar(progress_window)
        progress.setRange(0, 0)
        progress_layout.addWidget(progress)

        progress_window.show()

        def run_update():
            command = ["xterm", "-e"]
            if manager == "pacman":
                command.append("bash -c 'sudo pacman -Syu; echo; echo Press Enter to close...; read'")
            else:
                command.append("bash -c 'yay -Syu; echo; echo Press Enter to close...; read'")

            try:
                subprocess.Popen(command)
                progress_window.accept()
                self.show_message(_("Update Complete"), _("System updated successfully."))
            except Exception as e:
                progress_window.accept()
                self.show_message(_("Error"), str(e))

        threading.Thread(target=run_update).start()

    def check_internet_connection(self):
        try:
            socket.create_connection(("www.google.com", 80), timeout=5)
            return True
        except OSError:
            return False

    def apply_system_language(self):
        selected_language = self.system_language_combobox.currentText()
        try:
            self.show_message(_("Language Change"), _(f"System will be configured to {selected_language} now."))
            subprocess.run(["localectl", "set-locale", f"LANG={selected_language}"], check=True)
            subprocess.run(["sudo", "locale-gen"], check=True)
            self.show_message(_("Done"), _("System language changed. Please log out and log in again."))
        except subprocess.CalledProcessError as e:
            self.show_message(_("Error"), str(e))

    def mark_as_shown(self):
        try:
            with open(self.startup_file, "w") as f:
                f.write("shown")
        except Exception as e:
            print(f"Error creating startup file: {e}")

    def mark_as_not_shown(self):
        try:
            os.remove(self.startup_file)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error removing startup file: {e}")

    def toggle_startup(self):
        if self.startup_checkbutton.isChecked():
            self.mark_as_shown()
        else:
            self.mark_as_not_shown()

    def show_system_info(self):
        info = ""
        info += "Kernel: " + self.run_command("uname -r")
        info += "CPU Info:\n" + self.run_command("lscpu | grep 'Model name'")
        info += "Memory:\n" + self.run_command("free -h")
        info += "Disk Usage:\n" + self.run_command("df -h --total | grep total")
        info += "Graphics:\n" + self.run_command("lspci | grep -i vga")
        self.show_message(_("System Information"), info)

    def run_command(self, command):
        try:
            return subprocess.check_output(command, shell=True, text=True)
        except subprocess.CalledProcessError as e:
            return str(e)

    def show_performance(self):
        # قم بفتح نافذة لمراقبة الأداء هنا
        self.show_message(_("Performance Monitor"), _("This feature will open a performance monitoring tool."))

    def show_message(self, title, message):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setFixedSize(400, 200)
        dialog_layout = QVBoxLayout(dialog)
        dialog_label = QLabel(message, dialog)
        dialog_layout.addWidget(dialog_label)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomeApp()
    window.show()
    sys.exit(app.exec_())
