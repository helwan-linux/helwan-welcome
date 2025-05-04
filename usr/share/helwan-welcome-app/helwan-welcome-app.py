#!/usr/bin/env python3

import sys
import os
import webbrowser
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox,
    QComboBox, QProgressBar, QDialog, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import gettext

# === إعداد الترجمة ===
def load_translation(language_code):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    locale_path = os.path.join(current_dir, 'locales')
    try:
        translation = gettext.translation('base', localedir=locale_path, languages=[language_code])
        translation.install()
        return translation.gettext
    except FileNotFoundError:
        return lambda s: s

DEFAULT_LANGUAGE_CODE = 'en'
_ = load_translation(DEFAULT_LANGUAGE_CODE)

class WelcomeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.language_code = DEFAULT_LANGUAGE_CODE
        self.show_on_startup = self.check_startup_enabled()

        self.setWindowTitle(_("Welcome to Helwan Linux"))
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet(self.load_styles())
        self.logo = self.load_logo()

        self.init_ui()

    def check_startup_enabled(self):
        autostart_dir = os.path.expanduser("~/.config/autostart")
        startup_file_path = os.path.join(autostart_dir, "helwan_welcome.desktop")
        return os.path.exists(startup_file_path)

    def load_styles(self):
        return """
            QWidget { background-color: #f5f5f5; font-family: 'Segoe UI'; font-size: 13px; }
            QLabel { color: #333; }
            QPushButton { background-color: #e0e0e0; color: #333; border: 1px solid #ccc; border-radius: 5px; padding: 8px 15px; margin-top: 5px; }
            QPushButton:hover { background-color: #d0d0d0; }
            QCheckBox { color: #333; margin-top: 8px; }
            QComboBox { background-color: #fff; color: #333; border: 1px solid #ccc; border-radius: 3px; padding: 6px; margin-top: 5px; }
        """

    def load_logo(self):
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources", "logo.png")
        if os.path.exists(logo_path):
            logo = QPixmap(logo_path)
            return logo.scaledToWidth(120, Qt.SmoothTransformation) if not logo.isNull() else None
        else:
            print(f"Warning: Logo not found at {logo_path}")
            return None

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        if self.logo:
            logo_label = QLabel(self)
            logo_label.setPixmap(self.logo)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)

        greeting = QLabel(_("Welcome to the world of Helwan Linux! ❤️\nWe are here to help you build your dreams on the strongest foundation!"))
        greeting.setAlignment(Qt.AlignCenter)
        greeting.setStyleSheet("font-size: 15px; margin-top: 15px; margin-bottom: 25px; color: #555;")
        layout.addWidget(greeting)

        controls = QVBoxLayout()
        controls.setSpacing(12)
        layout.addLayout(controls)

        controls.addLayout(self.create_labeled_combobox(
            _("Application Language:"),
            ['en', 'ar', 'es', 'pt'],
            self.language_code,
            self.change_language
        ))

        self.startup_check = QCheckBox(_("Show on startup"))
        self.startup_check.setChecked(self.show_on_startup)
        self.startup_check.stateChanged.connect(self.update_startup_file)
        controls.addWidget(self.startup_check)

        update_row = QHBoxLayout()
        update_row.addWidget(self.create_button(_("Update System (Pacman)"), lambda: self.run_terminal_cmd("sudo pacman -Syu")))
        update_row.addWidget(self.create_button(_("Update System (Yay)"), lambda: self.run_terminal_cmd("yay -Syu")))
        controls.addLayout(update_row)

        controls.addLayout(self.create_labeled_combobox(
            _("System Language:"),
            ['ar_EG.UTF-8', 'en_US.UTF-8', 'es_ES.UTF-8', 'pt_PT.UTF-8'],
            'ar_EG.UTF-8',
            None,
            attr_name="system_language_combobox"
        ))

        controls.addWidget(self.create_button(_("Apply System Language"), self.apply_system_language))

        docs_row = QHBoxLayout()
        docs_row.addWidget(self.create_button(_("Open Documentation"), lambda: self.open_url("https://helwan-linux.mystrikingly.com/documentation")))
        docs_row.addWidget(self.create_button(_("Open YouTube Channel"), lambda: self.open_url("https://www.youtube.com/your_channel_here")))
        controls.addLayout(docs_row)

        sysinfo_row = QHBoxLayout()
        sysinfo_row.addWidget(self.create_button(_("Show System Info"), lambda: self.run_terminal_cmd("neofetch")))
        sysinfo_row.addWidget(self.create_button(_("Performance Monitor"), lambda: self.run_terminal_cmd("htop")))
        controls.addLayout(sysinfo_row)

    def create_button(self, text, action):
        button = QPushButton(text)
        button.clicked.connect(action)
        return button

    def create_labeled_combobox(self, label_text, items, default, on_change, attr_name=None):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)
        layout.addStretch(1)

        combo = QComboBox()
        combo.addItems(items)
        combo.setCurrentText(default)
        if on_change:
            combo.currentTextChanged.connect(on_change)
        layout.addWidget(combo)

        if attr_name:
            setattr(self, attr_name, combo)
        return layout

    def change_language(self, lang_code):
        global _
        _ = load_translation(lang_code)
        self.language_code = lang_code
        self.retranslate_ui()
        QMessageBox.information(self, _("Language Changed"), _("Language has been changed successfully."))

    def retranslate_ui(self):
        self.setWindowTitle(_("Welcome to Helwan Linux"))
        self.startup_check.setText(_("Show on startup"))
        # تحتاج هنا لتحديث نصوص العناصر الأخرى في الواجهة إذا كانت مترجمة

    def update_startup_file(self, state):
        try:
            autostart_dir = os.path.expanduser("~/.config/autostart")
            if not os.path.exists(autostart_dir):
                os.makedirs(autostart_dir)

            startup_file_path = os.path.join(autostart_dir, "helwan_welcome.desktop")

            if state == Qt.Checked:
                if not os.path.exists(startup_file_path):
                    with open(startup_file_path, "w") as f:
                        f.write(f"""[Desktop Entry]
Name=Helwan Welcome App
Exec={sys.executable} {os.path.abspath(__file__)}
Type=Application
X-GNOME-Autostart-enabled=true
Comment=Welcome screen for Helwan Linux
Icon={os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources", "logo.png")}
Terminal=false""")
                self.show_on_startup = True
            else:
                if os.path.exists(startup_file_path):
                    os.remove(startup_file_path)
                self.show_on_startup = False

        except Exception as e:
            QMessageBox.warning(self, _("Error"), f"{_('Could not update startup file:')} {e}")

    def open_url(self, url):
        try:
            webbrowser.open(url)
        except Exception as e:
            QMessageBox.warning(self, _("Error"), f"{_('Could not open URL:')} {e}")

    def run_terminal_cmd(self, cmd):
        try:
            subprocess.Popen(["xterm", "-hold", "-e", f"{cmd}; echo; echo Press Enter to exit..."])
        except FileNotFoundError:
            QMessageBox.critical(self, _("Error"), _("xterm is not installed. Please install xterm."))

    def apply_system_language(self):
        lang = self.system_language_combobox.currentText()
        try:
            process = subprocess.Popen(["sudo", "localectl", "set-locale", f"LANG={lang}"],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                QMessageBox.information(self, _("System Language"), _("System language applied successfully. You might need to restart your system for the changes to take full effect."))
            else:
                QMessageBox.critical(self, _("Error"), f"{_('Failed to apply system language:')} {stderr.decode()}")
        except FileNotFoundError:
            QMessageBox.critical(self, _("Error"), _("localectl command not found. Ensure systemd is installed."))
        except Exception as e:
            QMessageBox.critical(self, _("Error"), f"{_('An error occurred while applying system language:')} {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelcomeApp()
    window.show()
    sys.exit(app.exec_())
