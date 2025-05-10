from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox,
    QComboBox, QHBoxLayout, QMessageBox, QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
import os
import webbrowser
import subprocess
import platform
import psutil
import gettext
from theme_manager import load_theme  # استيراد دالة إدارة السمات
from language_manager import load_translation  # استيراد دالة إدارة اللغة
from system_utils import (
    check_startup_enabled, update_startup_file, open_url, run_terminal_cmd,
    apply_system_language, install_linux_lts, install_linux_zen,
    check_disk_space, update_system_info, is_yay_installed
)
import sys

DEFAULT_LANGUAGE_CODE = 'en'
_ = load_translation(DEFAULT_LANGUAGE_CODE)

# قائمة بلغات النظام المدعومة
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
        self.show_on_startup = check_startup_enabled()
        self.current_theme = "Default" # السمة الافتراضية

        self.setWindowTitle(_("Welcome to Helwan Linux"))
        self.setGeometry(100, 100, 600, 650)
        load_theme(self, self.current_theme) # تحميل السمة الافتراضية عند البدء
        self.logo = self.load_logo()

        self.app_lang_label = None
        self.app_lang_combobox = None
        self.startup_check = None
        self.pacman_btn = None
        self.yay_btn = None
        self.install_lts_btn = None
        self.install_zen_btn = None
        self.sys_lang_label = None
        self.system_language_combobox = None
        self.apply_lang_btn = None
        self.docs_btn = None
        self.youtube_btn = None
        self.neofetch_btn = None
        self.htop_btn = None
        self.system_info_group = None
        self.disk_space_label = None
        self.disk_space_status = None
        self.processor_label = None
        self.processor_info = None
        self.memory_label = None
        self.memory_info = None
        self.theme_label = None
        self.theme_combobox = None

        self.init_ui()
        check_disk_space(self)
        update_system_info(self)

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: check_disk_space(self))
        self.timer.start(5000)

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
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(1)

        if self.logo:
            logo_label = QLabel(self)
            logo_label.setPixmap(self.logo)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)

        self.greeting = QLabel()
        self.greeting.setAlignment(Qt.AlignCenter)
        self.greeting.setStyleSheet("font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #555;")
        layout.addWidget(self.greeting)

        controls = QVBoxLayout()
        controls.setSpacing(8)
        layout.addLayout(controls)

        # Theme Selection
        theme_layout = QHBoxLayout()
        self.theme_label = QLabel(_("Application Theme:"))
        theme_layout.addWidget(self.theme_label)
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(["Default", "Sky Blue", "Light Black", "Light Purple"])
        self.theme_combobox.setCurrentText(self.current_theme)
        self.theme_combobox.currentTextChanged.connect(lambda text: load_theme(self, text))
        theme_layout.addWidget(self.theme_combobox)
        controls.addLayout(theme_layout)

        # Application Language
        app_lang_layout = self.create_labeled_combobox(
            label_attr='app_lang_label',
            combo_attr='app_lang_combobox',
            label_text=_("Application Language:"),
            items=['en', 'ar', 'es', 'pt', 'de', 'fr', 'ru', 'zh_CN'],
            default=self.language_code,
            on_change=self.change_language
        )
        controls.addLayout(app_lang_layout)

        # Startup Settings
        startup_layout = QHBoxLayout()
        self.startup_check = QCheckBox(_("Show on startup"))
        self.startup_check.setChecked(self.show_on_startup)
        self.startup_check.stateChanged.connect(self.update_startup_file)
        startup_layout.addWidget(self.startup_check)
        controls.addLayout(startup_layout)

        # System Update Buttons
        update_layout = QHBoxLayout()
        self.pacman_btn = self.create_button(_("Update System (Pacman)"), lambda: run_terminal_cmd(self, "sudo pacman -Syu"))
        update_layout.addWidget(self.pacman_btn)
        if is_yay_installed():
            self.yay_btn = self.create_button(_("Update System (Yay)"), lambda: run_terminal_cmd(self, "yay -Syu"))
            update_layout.addWidget(self.yay_btn)
        controls.addLayout(update_layout)

        # Kernel Installation Buttons
        kernel_layout = QHBoxLayout()
        self.install_lts_btn = self.create_button(_("Install Linux LTS"), self.install_linux_lts)
        kernel_layout.addWidget(self.install_lts_btn)
        self.install_zen_btn = self.create_button(_("Install Linux Zen"), self.install_linux_zen)
        kernel_layout.addWidget(self.install_zen_btn)
        controls.addLayout(kernel_layout)

        # System Language
        sys_lang_layout = QHBoxLayout()
        self.sys_lang_label = QLabel(_("System Language:"))
        sys_lang_layout.addWidget(self.sys_lang_label)
        self.system_language_combobox = QComboBox()
        self.system_language_combobox.addItems(SYSTEM_LANGUAGES)
        self.system_language_combobox.setCurrentText('en_US.UTF-8' if 'en_US.UTF-8' in SYSTEM_LANGUAGES else SYSTEM_LANGUAGES[0] if SYSTEM_LANGUAGES else '')
        sys_lang_layout.addWidget(self.system_language_combobox)
        controls.addLayout(sys_lang_layout)

        self.apply_lang_btn = self.create_button(_("Apply System Language"), self.apply_system_language)
        controls.addWidget(self.apply_lang_btn)

        # Documentation and Support
        docs_layout = QHBoxLayout()
        self.docs_btn = self.create_button(_("Open Documentation"), lambda: open_url(self, "https://helwan-linux.mystrikingly.com/documentation"))
        docs_layout.addWidget(self.docs_btn)
        self.youtube_btn = self.create_button(_("Open YouTube Channel"), lambda: open_url(self, "https://www.youtube.com/@HelwanO.S"))
        docs_layout.addWidget(self.youtube_btn)
        controls.addLayout(docs_layout)

        # System Information Group
        self.system_info_group = QGroupBox(_("System Information"))
        system_info_layout = QGridLayout()

        # Disk Space
        self.disk_space_label = QLabel(_("Available Disk Space:"))
        self.disk_space_status = QLabel()
        self.disk_space_status.setObjectName("disk_space_status")
        system_info_layout.addWidget(self.disk_space_label, 0, 0)
        system_info_layout.addWidget(self.disk_space_status, 0, 1)

        # Processor
        self.processor_label = QLabel(_("Processor:"))
        self.processor_info = QLabel()
        self.processor_info.setObjectName("system_info")
        system_info_layout.addWidget(self.processor_label, 1, 0)
        system_info_layout.addWidget(self.processor_info, 1, 1)

        # Memory
        self.memory_label = QLabel(_("RAM:"))
        self.memory_info = QLabel()
        self.memory_info.setObjectName("system_info")
        system_info_layout.addWidget(self.memory_label, 2, 0)
        system_info_layout.addWidget(self.memory_info, 2, 1)

        self.system_info_group.setLayout(system_info_layout)
        controls.addWidget(self.system_info_group)

        # System Information Buttons (Neofetch, Htop)
        sysinfo_layout = QHBoxLayout()
        self.neofetch_btn = self.create_button(_("Show System Info Details"), lambda: run_terminal_cmd(self, "neofetch"))
        sysinfo_layout.addWidget(self.neofetch_btn)
        self.htop_btn = self.create_button(_("Performance Monitor"), lambda: run_terminal_cmd(self, "htop"))
        sysinfo_layout.addWidget(self.htop_btn)
        controls.addLayout(sysinfo_layout)

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
        if self.theme_label:
            self.theme_label.setText(_("Application Theme:"))
        if self.app_lang_label:
            self.app_lang_label.setText(_("Application Language:"))
        if self.startup_check:
            self.startup_check.setText(_("Show on startup"))
        if self.pacman_btn:
            self.pacman_btn.setText(_("Update System (Pacman)"))
        if hasattr(self, 'yay_btn') and self.yay_btn:
            self.yay_btn.setText(_("Update System (Yay)"))
        if self.install_lts_btn:
            self.install_lts_btn.setText(_("Install Linux LTS"))
        if self.install_zen_btn:
            self.install_zen_btn.setText(_("Install Linux Zen"))
        if self.sys_lang_label:
            self.sys_lang_label.setText(_("System Language:"))
        if self.apply_lang_btn:
            self.apply_lang_btn.setText(_("Apply System Language"))
        if self.docs_btn:
            self.docs_btn.setText(_("Open Documentation"))
        if self.youtube_btn:
            self.youtube_btn.setText(_("Open YouTube Channel"))
        if self.neofetch_btn:
            self.neofetch_btn.setText(_("Show System Info Details"))
        if self.htop_btn:
            self.htop_btn.setText(_("Performance Monitor"))
        if self.system_info_group:
            self.system_info_group.setTitle(_("System Information"))
            if self.disk_space_label:
                self.disk_space_label.setText(_("Available Disk Space:"))
            if self.processor_label:
                self.processor_label.setText(_("Processor:"))
            if self.memory_label:
                self.memory_label.setText(_("RAM:"))

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
