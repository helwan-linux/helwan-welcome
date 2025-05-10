#!/usr/bin/env python3

import sys
import os
import webbrowser
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox,
    QComboBox, QProgressBar, QDialog, QHBoxLayout, QMessageBox, QInputDialog, QLineEdit,
    QGroupBox, QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
import gettext
import platform
import psutil

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
        self.current_theme = "Default" # السمة الافتراضية

        self.setWindowTitle(_("Welcome to Helwan Linux"))
        self.setGeometry(100, 100, 600, 650) # زيادة الارتفاع لاستيعاب معلومات النظام
        self.load_theme(self.current_theme) # تحميل السمة الافتراضية عند البدء
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
        self.system_info_group = None # المجموعة الجديدة لمعلومات النظام
        self.disk_space_label = None
        self.disk_space_status = None
        self.processor_label = None
        self.processor_info = None
        self.memory_label = None
        self.memory_info = None
        self.theme_label = None
        self.theme_combobox = None

        self.init_ui()
        self.check_disk_space()
        self.update_system_info() # جلب معلومات النظام عند البدء

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_disk_space)
        self.timer.start(5000)

    def check_startup_enabled(self):
        autostart_dir = os.path.expanduser("~/.config/autostart")
        startup_file_path = os.path.join(autostart_dir, "helwan_welcome.desktop")
        return os.path.exists(startup_file_path)

    def load_theme(self, theme_name):
        if theme_name == "Default":
            self.setStyleSheet("""
                QWidget { background-color: #f5f5f5; font-family: 'Segoe UI'; font-size: 13px; color: #333; }
                QLabel { color: #333; margin-bottom: 5px; }
                QPushButton { background-color: #e0e0e0; color: #333; border: 1px solid #ccc; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 12px; }
                QPushButton:hover { background-color: #d0d0d0; }
                QCheckBox { color: #333; margin-top: 5px; margin-bottom: 5px; }
                QComboBox { background-color: #fff; color: #333; border: 1px solid #ccc; border-radius: 3px; padding: 6px; margin-top: 3px; margin-bottom: 3px; }
                QGroupBox { border: 1px solid #ccc; border-radius: 5px; margin-top: 10px; padding: 10px; }
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #555; }
                QLabel#disk_space_status { font-weight: bold; }
                QLabel#disk_space_status_ok { color: green; }
                QLabel#disk_space_status_warning { color: orange; }
                QLabel#disk_space_status_error { color: red; }
                QLabel#system_info { margin-bottom: 2px; }
            """)
        elif theme_name == "Sky Blue":
            self.setStyleSheet("""
                QWidget { background-color: #e0f7fa; font-family: 'Segoe UI'; font-size: 13px; color: #212121; }
                QLabel { color: #212121; margin-bottom: 5px; }
                QPushButton { background-color: #81d4fa; color: #212121; border: 1px solid #4fc3f7; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 12px; }
                QPushButton:hover { background-color: #4fc3f7; }
                QCheckBox { color: #212121; margin-top: 5px; margin-bottom: 5px; }
                QComboBox { background-color: #b3e5fc; color: #212121; border: 1px solid #81d4fa; border-radius: 3px; padding: 6px; margin-top: 3px; margin-bottom: 3px; }
                QGroupBox { border: 1px solid #4fc3f7; border-radius: 5px; margin-top: 10px; padding: 10px; }
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #0277bd; }
                QLabel#disk_space_status { font-weight: bold; color: #212121; }
                QLabel#disk_space_status_ok { color: darkgreen; }
                QLabel#disk_space_status_warning { color: darkorange; }
                QLabel#disk_space_status_error { color: darkred; }
                QLabel#system_info { margin-bottom: 2px; }
            """)
        elif theme_name == "Light Black":
            self.setStyleSheet("""
                QWidget { background-color: #303030; font-family: 'Segoe UI'; font-size: 13px; color: #f0f0f0; }
                QLabel { color: #f0f0f0; margin-bottom: 5px; }
                QPushButton { background-color: #505050; color: #f0f0f0; border: 1px solid #707070; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 12px; }
                QPushButton:hover { background-color: #707070; }
                QCheckBox { color: #f0f0f0; margin-top: 5px; margin-bottom: 5px; }
                QComboBox { background-color: #404040; color: #f0f0f0; border: 1px solid #606060; border-radius: 3px; padding: 6px; margin-top: 3px; margin-bottom: 3px; }
                QGroupBox { border: 1px solid #606060; border-radius: 5px; margin-top: 10px; padding: 10px; }
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #a0a0a0; }
                QLabel#disk_space_status { font-weight: bold; color: #f0f0f0; }
                QLabel#disk_space_status_ok { color: lightgreen; }
                QLabel#disk_space_status_warning { color: yellow; }
                QLabel#disk_space_status_error { color: red; }
                QLabel#system_info { margin-bottom: 2px; }
            """)
            
        elif theme_name == "Light Purple":  # Light purple theme
            self.setStyleSheet("""
                QWidget { background-color: #e6ccff; font-family: 'Segoe UI'; font-size: 13px; color: #4d194d; } /* بنفسجي فاتح للخلفية، بنفسجي داكن للنص */
                QLabel { color: #4d194d; margin-bottom: 5px; }
                QPushButton { background-color: #f0d9ff; color: #4d194d; border: 1px solid #b388eb; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 12px; }
                QPushButton:hover { background-color: #b388eb; }
                QCheckBox { color: #4d194d; margin-top: 5px; margin-bottom: 5px; }
                QComboBox { background-color: #f3e5f5; color: #4d194d; border: 1px solid #ce93d8; border-radius: 3px; padding: 6px; margin-top: 3px; margin-bottom: 3px; }
                QGroupBox { border: 1px solid #ce93d8; border-radius: 5px; margin-top: 10px; padding: 10px; color: #4d194d; }
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #8e24aa; } /* بنفسجي أغمق لعنوان المجموعة */
                QLabel#disk_space_status { font-weight: bold; color: #4d194d; }
                QLabel#disk_space_status_ok { color: darkgreen; }
                QLabel#disk_space_status_warning { color: darkorange; }
                QLabel#disk_space_status_error { color: darkred; }
                QLabel#system_info { margin-bottom: 2px; color: #4d194d; }
            """)

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
        layout.setAlignment(Qt.AlignTop) # محاذاة العناصر في الأعلى
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
        self.theme_combobox.currentTextChanged.connect(self.load_theme)
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
        self.pacman_btn = self.create_button(_("Update System (Pacman)"), lambda: self.run_terminal_cmd("sudo pacman -Syu"))
        update_layout.addWidget(self.pacman_btn)
        if self.is_yay_installed():
            self.yay_btn = self.create_button(_("Update System (Yay)"), lambda: self.run_terminal_cmd("yay -Syu"))
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
        self.docs_btn = self.create_button(_("Open Documentation"), lambda: self.open_url("https://helwan-linux.mystrikingly.com/documentation"))
        docs_layout.addWidget(self.docs_btn)
        self.youtube_btn = self.create_button(_("Open YouTube Channel"), lambda: self.open_url("https://www.youtube.com/@HelwanO.S"))
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

        # System Information Buttons (Neofetch, Htop) - نقلناها أسفل معلومات النظام
        sysinfo_layout = QHBoxLayout()
        self.neofetch_btn = self.create_button(_("Show System Info Details"), lambda: self.run_terminal_cmd("neofetch"))
        sysinfo_layout.addWidget(self.neofetch_btn)
        self.htop_btn = self.create_button(_("Performance Monitor"), lambda: self.run_terminal_cmd("htop"))
        sysinfo_layout.addWidget(self.htop_btn)
        controls.addLayout(sysinfo_layout)

        # أول تعريب للواجهة
        self.retranslate_ui()

    def is_yay_installed(self):
        try:
            subprocess.run(["yay", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False
        except subprocess.CalledProcessError:
            return True # يعتبر مثبت إذا لم يظهر خطأ في عدم العثور عليه

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

    def check_disk_space(self):
        try:
            process = subprocess.Popen(["df", "-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                lines = stdout.strip().split('\n')[1:]
                for line in lines:
                    parts = line.split()
                    if parts[5] == '/' : # نفترض أن القسم الجذر هو المثبت على /
                        available = parts[3]
                        total = parts[1]
                        used_percentage = int(float(parts[4][:-1]))
                        if used_percentage > 90:
                            self.disk_space_status.setText(_("Low ({} / {})").format(available, total))
                            self.disk_space_status.setStyleSheet("color: red;")
                        elif used_percentage > 80:
                            self.disk_space_status.setText(_("Warning ({} / {})").format(available, total))
                            self.disk_space_status.setStyleSheet("color: orange;")
                        else:
                            self.disk_space_status.setText(_("OK ({} / {})").format(available, total))
                            self.disk_space_status.setStyleSheet("color: green;")
                        return
                self.disk_space_status.setText(_("N/A"))
                self.disk_space_status.setStyleSheet("")
            else:
                print(f"Error executing df: Return code {process.returncode}, Stderr: {stderr}")
                self.disk_space_status.setText(_("Error"))
                self.disk_space_status.setStyleSheet("color: red;")
        except FileNotFoundError:
            self.disk_space_status.setText(_("N/A (df not found)"))
            self.disk_space_status.setStyleSheet("")
        except Exception as e:
            print(f"Exception in check_disk_space: {e}")
            self.disk_space_status.setText(_("Error"))
            self.disk_space_status.setStyleSheet("color: red;")

    def update_system_info(self):
        processor_info = None
        if platform.system() == "Linux":
            try:
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            processor_info = line.split(":")[1].strip()
                            break
            except FileNotFoundError:
                print("Error: /proc/cpuinfo not found.")
            except Exception as e:
                print(f"Error reading /proc/cpuinfo: {e}")

        if not processor_info:
            processor_info = platform.processor() or _("N/A")

        self.processor_info.setText(processor_info)

        # Memory Info
        try:
            mem = psutil.virtual_memory()
            total_memory_gb = round(mem.total / (1024 ** 3), 2)
            self.memory_info.setText(f"{total_memory_gb} GB")
        except Exception as e:
            print(f"Error getting memory info: {e}")
            self.memory_info.setText(_("N/A"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelcomeApp()
    window.show()
    sys.exit(app.exec_())

