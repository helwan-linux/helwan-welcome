#!/usr/bin/env python3

import sys
import os
import webbrowser
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox,
    QComboBox, QProgressBar, QDialog, QHBoxLayout, QMessageBox, QInputDialog, QLineEdit
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

# قائمة بلغات النظام المدعومة (يجب أن تكون هذه اللغات مثبتة على النظام)
SYSTEM_LANGUAGES = [
    'ar_EG.UTF-8',
    'en_US.UTF-8',
    'es_ES.UTF-8',
    'pt_PT.UTF-8',
    'de_DE.UTF-8',
    'fr_FR.UTF-8',
    'ru_RU.UTF-8',
    'zh_CN.UTF-8'
]

class WelcomeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.language_code = DEFAULT_LANGUAGE_CODE
        self.show_on_startup = self.check_startup_enabled()

        self.setWindowTitle(_("Welcome to Helwan Linux"))
        self.setGeometry(100, 100, 400, 700)  # زيادة الارتفاع لاستيعاب الأزرار الجديدة
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

        self.greeting = QLabel()
        self.greeting.setAlignment(Qt.AlignCenter)
        self.greeting.setStyleSheet("font-size: 15px; margin-top: 15px; margin-bottom: 25px; color: #555;")
        layout.addWidget(self.greeting)

        controls = QVBoxLayout()
        controls.setSpacing(12)
        layout.addLayout(controls)

        # Application Language ComboBox
        controls.addLayout(self.create_labeled_combobox(
            label_attr='app_lang_label',
            combo_attr='app_lang_combobox',
            label_text=_("Application Language:"),
            items=['en', 'ar', 'es', 'pt', 'de', 'fr', 'ru', 'zh_CN'],
            default=self.language_code,
            on_change=self.change_language
        ))

        # Show on Startup Checkbox
        self.startup_check = QCheckBox()
        self.startup_check.setChecked(self.show_on_startup)
        self.startup_check.stateChanged.connect(self.update_startup_file)
        controls.addWidget(self.startup_check)

        # System Update Buttons
        update_row = QHBoxLayout()
        self.pacman_btn = self.create_button(_("Update System (Pacman)"), lambda: self.run_terminal_cmd("sudo pacman -Syu"))
        self.yay_btn = self.create_button(_("Update System (Yay)"), lambda: self.run_terminal_cmd("yay -Syu"))
        update_row.addWidget(self.pacman_btn)
        update_row.addWidget(self.yay_btn)
        controls.addLayout(update_row)

        # Kernel Installation Buttons
        kernel_row1 = QHBoxLayout()
        self.install_lts_btn = self.create_button(_("Install Linux LTS"), self.install_linux_lts)
        self.install_zen_btn = self.create_button(_("Install Linux Zen"), self.install_linux_zen)
        kernel_row1.addWidget(self.install_lts_btn)
        kernel_row1.addWidget(self.install_zen_btn)
        controls.addLayout(kernel_row1)

        # System Language ComboBox
        controls.addLayout(self.create_labeled_combobox(
            label_attr='sys_lang_label',
            combo_attr='system_language_combobox',
            label_text=_("System Language:"),
            items=SYSTEM_LANGUAGES,
            default='en_US.UTF-8' if 'en_US.UTF-8' in SYSTEM_LANGUAGES else SYSTEM_LANGUAGES[0] if SYSTEM_LANGUAGES else '',
            on_change=None
        ))

        # Apply System Language Button
        self.apply_lang_btn = self.create_button(_("Apply System Language"), self.apply_system_language)
        controls.addWidget(self.apply_lang_btn)

        # Docs Buttons
        docs_row = QHBoxLayout()
        self.docs_btn = self.create_button(_("Open Documentation"), lambda: self.open_url("https://helwan-linux.mystrikingly.com/documentation"))
        self.youtube_btn = self.create_button(_("Open YouTube Channel"), lambda: self.open_url("https://www.youtube.com/@HelwanO.S"))
        docs_row.addWidget(self.docs_btn)
        docs_row.addWidget(self.youtube_btn)
        controls.addLayout(docs_row)

        # System Info Buttons
        sysinfo_row = QHBoxLayout()
        self.neofetch_btn = self.create_button(_("Show System Info"), lambda: self.run_terminal_cmd("neofetch"))
        self.htop_btn = self.create_button(_("Performance Monitor"), lambda: self.run_terminal_cmd("htop"))
        sysinfo_row.addWidget(self.neofetch_btn)
        sysinfo_row.addWidget(self.htop_btn)
        controls.addLayout(sysinfo_row)

        # أول تعريب للواجهة
        self.retranslate_ui()

    def create_button(self, text, action):
        button = QPushButton(text)
        button.clicked.connect(action)
        return button

    def create_labeled_combobox(self, label_attr, combo_attr, label_text, items, default, on_change):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        setattr(self, label_attr, label)
        layout.addWidget(label)
        layout.addStretch(1)

        combo = QComboBox()
        combo.addItems(items)
        combo.setCurrentText(default)
        if on_change:
            combo.currentTextChanged.connect(on_change)
        setattr(self, combo_attr, combo)
        layout.addWidget(combo)
        return layout

    def change_language(self, lang_code):
        global _
        _ = load_translation(lang_code)
        self.language_code = lang_code
        self.retranslate_ui()
        QMessageBox.information(self, _("Language Changed"), _("Language has been changed successfully."))

    def retranslate_ui(self):
        self.setWindowTitle(_("Welcome to Helwan Linux"))
        self.greeting.setText(_("Welcome to the world of Helwan Linux! ❤️\nWe are here to help you build your dreams on the strongest foundation!"))
        self.app_lang_label.setText(_("Application Language:"))
        self.startup_check.setText(_("Show on startup"))
        self.pacman_btn.setText(_("Update System (Pacman)"))
        self.yay_btn.setText(_("Update System (Yay)"))
        self.install_lts_btn.setText(_("Install Linux LTS"))
        self.install_zen_btn.setText(_("Install Linux Zen"))
        self.sys_lang_label.setText(_("System Language:"))
        self.apply_lang_btn.setText(_("Apply System Language"))
        self.docs_btn.setText(_("Open Documentation"))
        self.youtube_btn.setText(_("Open YouTube Channel"))
        self.neofetch_btn.setText(_("Show System Info"))
        self.htop_btn.setText(_("Performance Monitor"))

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
            process = subprocess.Popen(["pkexec", "localectl", "set-locale", f"LANG={lang}"],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                QMessageBox.information(self, _("System Language"), _("System language applied successfully. You might need to restart your system for the changes to take full effect."))
            else:
                QMessageBox.critical(self, _("Error"), f"{_('Failed to apply system language:')} {stderr.decode()}")
        except FileNotFoundError:
            QMessageBox.critical(self, _("Error"), _("pkexec command not found. Ensure polkit is installed."))
        except Exception as e:
            QMessageBox.critical(self, _("Error"), f"{_('An error occurred while applying system language:')} {e}")

    def install_linux_lts(self):
        self._install_kernel("linux-lts", "linux-lts-headers")

    def install_linux_zen(self):
        self._install_kernel("linux-zen", "linux-zen-headers")

    def _install_kernel(self, kernel_package, headers_package):
        command = f"sudo pacman -S --needed {kernel_package} {headers_package}"
        try:
            subprocess.Popen(["xterm", "-hold", "-e", f"{command}; sudo grub-mkconfig -o /boot/grub/grub.cfg; echo; echo Press Enter to exit..."])
        except FileNotFoundError:
            QMessageBox.critical(self, _("Error"), _("xterm is not installed. Please install xterm."))
        except Exception as e:
            QMessageBox.critical(self, _("Error"), f"{_('An error occurred during kernel installation:')} {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelcomeApp()
    window.show()
    sys.exit(app.exec_())
