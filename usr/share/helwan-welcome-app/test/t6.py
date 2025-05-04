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
import shutil

# === إعداد الترجمة ===
def load_translation(language_code):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    locale_path = os.path.join(current_dir, 'locales')
    try:
        translation = gettext.translation('base', localedir=locale_path, languages=[language_code])
        translation.install()
        return translation.gettext
    except FileNotFoundError:
        # Fallback to English if locale not found
        try:
            translation = gettext.translation('base', localedir=locale_path, languages=['en'])
            translation.install()
            return translation.gettext
        except FileNotFoundError:
            # If even English translation is not found, fallback to using original strings and show a warning
            print("Warning: English translation file not found. Using default strings.")
            return lambda s: s

# اللغة الافتراضية عند بدء التشغيل
DEFAULT_LANGUAGE_CODE = 'en'
_ = load_translation(DEFAULT_LANGUAGE_CODE)

# === التطبيق ===
class WelcomeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.language_code = DEFAULT_LANGUAGE_CODE
        self.startup_file = os.path.join(os.path.expanduser("~"), ".helwan_welcome_shown")
        self.show_on_startup = not os.path.exists(self.startup_file)

        self.setWindowTitle(_("Welcome to Helwan Linux"))
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet(self.load_styles())
        self.logo = self.load_logo()

        self.init_ui()

        if self.show_on_startup:
            self.mark_as_shown()

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

        # إضافة الشعار
        if self.logo:
            logo_label = QLabel(self)
            logo_label.setPixmap(self.logo)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)

        # رسالة الترحيب
        greeting = QLabel(_("Welcome to the world of Helwan Linux! ❤️\nWe are here to help you build your dreams on the strongest foundation!"))
        greeting.setAlignment(Qt.AlignCenter)
        greeting.setStyleSheet("font-size: 15px; margin-top: 15px; margin-bottom: 25px; color: #555;")
        layout.addWidget(greeting)

        # --- عناصر التحكم ---
        controls = QVBoxLayout()
        controls.setSpacing(12)
        layout.addLayout(controls)

        # لغة التطبيق
        controls.addLayout(self.create_labeled_combobox(
            _("Application Language:"),
            ['en', 'ar', 'es', 'pt'],
            self.language_code,
            self.change_language
        ))

        # إظهار عند بدء التشغيل
        self.startup_check = QCheckBox(_("Show on startup"))
        self.startup_check.setChecked(self.show_on_startup)
        self.startup_check.stateChanged.connect(self.toggle_startup)
        controls.addWidget(self.startup_check)

        # تحديث النظام
        update_row = QHBoxLayout()
        update_row.addWidget(self.create_button(_("Update System (Pacman)"), lambda: self._run_terminal_cmd("sudo pacman -Syu", _("Updating System (Pacman)..."))))
        update_row.addWidget(self.create_button(_("Update System (Yay)"), lambda: self._run_terminal_cmd("yay -Syu", _("Updating System (Yay)..."))))
        controls.addLayout(update_row)

        # لغة النظام
        controls.addLayout(self.create_labeled_combobox(
            _("System Language:"),
            ['ar_EG.UTF-8', 'en_US.UTF-8', 'es_ES.UTF-8', 'pt_PT.UTF-8'],
            'ar_EG.UTF-8',
            None,
            attr_name="system_language_combobox"
        ))

        controls.addWidget(self.create_button(_("Apply System Language"), self.apply_system_language))

        # الوثائق ويوتيوب
        docs_row = QHBoxLayout()
        docs_row.addWidget(self.create_button(_("Open Documentation"), lambda: self.open_url("https://helwan-linux.mystrikingly.com/documentation")))
        docs_row.addWidget(self.create_button(_("Open YouTube Channel"), lambda: self.open_url("https://www.youtube.com/your_channel_url"))) # استبدل بعنوان URL الصحيح لقناتك
        controls.addLayout(docs_row)

        # معلومات النظام والمراقبة
        sysinfo_row = QHBoxLayout()
        sysinfo_row.addWidget(self.create_button(_("Show System Info"), lambda: self._run_terminal_cmd("neofetch", _("Showing System Info..."))))
        sysinfo_row.addWidget(self.create_button(_("Performance Monitor"), lambda: self._run_terminal_cmd("htop", _("Running Performance Monitor..."))))
        controls.addLayout(sysinfo_row)

    # === أدوات المساعدة لواجهة المستخدم ===
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

    # === وظائف التفاعل ===
    def change_language(self, lang_code):
        global _
        _ = load_translation(lang_code)
        self.language_code = lang_code
        QMessageBox.information(self, _("Language Changed"), _("Please restart the application to apply language changes."))

    def toggle_startup(self, state):
        if state == Qt.Checked:
            if os.path.exists(self.startup_file):
                os.remove(self.startup_file)
        else:
            self.mark_as_shown()

    def mark_as_shown(self):
        try:
            with open(self.startup_file, "w") as f:
                f.write("shown")
        except Exception as e:
            QMessageBox.warning(self, _("Error"), f"{_('Could not write startup file:')} {e}")

    def open_url(self, url):
        try:
            webbrowser.open(url)
        except Exception as e:
            QMessageBox.warning(self, _("Error"), f"{_('Could not open URL:')} {e}")

    def _run_terminal_cmd(self, cmd, message):
        xterm_path = shutil.which('xterm')
        if xterm_path:
            try:
                subprocess.Popen([xterm_path, "-hold", "-e", f"{cmd}; echo; echo Press Enter to exit..."])
            except Exception as e:
                QMessageBox.critical(self, _("Error"), f"{_('Could not run terminal command:')} {e}")
        else:
            QMessageBox.critical(self, _("Error"), _("xterm is not installed. Please install xterm to use this feature."))

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

# === تشغيل التطبيق ===
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelcomeApp()
    window.show()
    sys.exit(app.exec_())