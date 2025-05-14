#!/usr/bin/env python3
# CREATED BY Saeed Badrelden <saeedbadrelden2021@gmail.com>
import sys
import os
import webbrowser
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox,
    QComboBox, QProgressBar, QDialog, QHBoxLayout, QMessageBox, QInputDialog,
    QLineEdit, QGroupBox, QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer, QSettings
from PyQt5.QtGui import QPixmap
import gettext
import platform
import psutil
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
        return lambda s: s

DEFAULT_LANGUAGE_CODE = 'en'
_ = load_translation(DEFAULT_LANGUAGE_CODE)

# قائمة بلغات النظام المدعومة مع الأسماء المقابلة
SYSTEM_LANGUAGES = {
    'ar_EG.UTF-8': 'العربية (مصر)',
    'en_US.UTF-8': 'English (US)',
    'es_ES.UTF-8': 'Español (España)',
    'pt_PT.UTF-8': 'Português (Portugal)',
    'de_DE.UTF-8': 'Deutsch (Deutschland)',
    'fr_FR.UTF-8': 'Français (France)',
    'ru_RU.UTF-8': 'Русский (Россия)',
    'zh_CN.UTF-8': '中文 (简体)',
    'ja_JP.UTF-8': '日本語',
    'it_IT.UTF-8': 'Italiano',
    'pl_PL.UTF-8': 'Polski',
    'ro_RO.UTF-8': 'Română',
    'ur_PK.UTF-8': 'اردو',
    'fa_IR.UTF-8': 'فارسی'
}

# قائمة لغة التطبيق بنفس الطريقة
APP_LANGUAGES = {
    'en': 'English',
    'ar': 'العربية',
    'es': 'Español',
    'pt': 'Português',
    'de': 'Deutsch',
    'fr': 'Français',
    'ru': 'Русский',
    'zh_CN': '中文',
    'ja': '日本語',
    'it': 'Italiano',
    'pl': 'Polski',
    'ro': 'Română',
    'ur': 'اردو',
    'fa': 'فارسی'
}

class WelcomeApp(QWidget):

    def __init__(self):
        super().__init__()
        self.language_code = DEFAULT_LANGUAGE_CODE
        self.show_on_startup = self.check_startup_enabled()
        self.current_theme = "Default"  # السمة الافتراضية

        self.settings = QSettings("Helwan", "WelcomeApp")  # هنا غير "Helwan" باسم مؤسستك
        self.logo = self.load_logo()

        self.app_lang_label = None
        self.app_lang_combobox = None
        self.startup_check = None
        self.pacman_btn = None
        self.yay_btn = None   # هنا ضفنا تعريف yay_btn
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

        self.init_ui()  # قم بتهيئة واجهة المستخدم أولاً
        self.load_theme(self.current_theme) # ثم قم بتحميل الثيم الذي يعتمد على عناصر الواجهة

        self.load_settings() # ثم قم بتحميل الإعدادات التي تعتمد عليها

        self.check_disk_space()
        self.update_system_info()

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_disk_space)
        self.timer.start(5000)

    def load_settings(self):
        # استرجاع اللغة المحفوظة وتطبيقها
        saved_language_index = self.settings.value("language_index", 0, type=int)
        if self.app_lang_combobox:
            self.app_lang_combobox.setCurrentIndex(saved_language_index)
            self.change_language(self.app_lang_combobox.currentText())

        # استرجاع السمة المحفوظة وتطبيقها
        saved_theme = self.settings.value("theme", "Default", type=str)
        if self.theme_combobox:
            index = self.theme_combobox.findText(saved_theme)
            if index != -1:
                self.theme_combobox.setCurrentIndex(index)
            self.load_theme(saved_theme)

    def check_startup_enabled(self):
        autostart_dir = os.path.expanduser("~/.config/autostart")
        startup_file_path = os.path.join(autostart_dir, "helwan_welcome.desktop")
        return os.path.exists(startup_file_path)

    def load_theme(self, theme_name):
        if theme_name == "Default":
            self.setStyleSheet("""
                QWidget { background-color: #f5f5f5; font-family: 'Segoe UI'; font-size: 13px; color: #333; }
                QLabel { color: #333; margin-bottom: 5px; }
                QPushButton { background-color: #e0e0e0; color: #333; border: 1px solid #ccc; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
                QPushButton:hover { background-color: #d0d0d0; }
                QCheckBox { color: #333; margin-top: 5px; margin-bottom: 5px; }
                QComboBox { background-color: #fff; color: #333; border: 1px solid #ccc; border-radius: 3px; padding: 4px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
                QGroupBox { border: 1px solid #ccc; border-radius: 5px; margin-top: 10px; padding: 10px; }
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #555; }
                QLabel#disk_space_status { font-weight: bold; }
                QLabel#disk_space_status_ok { color: green; }
                QLabel#disk_space_status_warning { color: orange; }
                QLabel#disk_space_status_error { color: red; }
                QLabel#system_info { margin-bottom: 2px; }
            """)
            if self.greeting:
                self.greeting.setStyleSheet("font-size: 15px; margin-top: 1px; margin-bottom: 1px; color: #555;") # لون النص الافتراضي
        elif theme_name == "Sky Blue":
            self.setStyleSheet("""
                QWidget { background-color: #e0f7fa; font-family: 'Segoe UI'; font-size: 13px; color: #212121; }
                QLabel { color: #212121; margin-bottom: 5px; }
                QPushButton { background-color: #81d4fa; color: #212121; border: 1px solid #4fc3f7; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
                QPushButton:hover { background-color: #4fc3f7; }
                QCheckBox { color: #212121; margin-top: 5px; margin-bottom: 5px; }
                QComboBox { background-color: #b3e5fc; color: #212121; border: 1px solid #81d4fa; border-radius: 3px; padding: 4px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
                QGroupBox { border: 1px solid #4fc3f7; border-radius: 5px; margin-top: 10px; padding: 10px; }
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #0277bd; }
                QLabel#disk_space_status { font-weight: bold; color: #212121; }
                QLabel#disk_space_status_ok { color: darkgreen; }
                QLabel#disk_space_status_warning { color: darkorange; }
                QLabel#disk_space_status_error { color: darkred; }
                QLabel#system_info { margin-bottom: 2px; }
            """)
            if self.greeting:
                self.greeting.setStyleSheet("font-size: 15px; margin-top: 1px; margin-bottom: 1px; color: #212121;") # لون النص للسمة الزرقاء
        elif theme_name == "Light Black":  # اسم جديد للسمة اللوكس
            self.setStyleSheet("""
                QWidget { background-color: #666666; font-family: 'Segoe UI'; font-size: 13px; color: #d0d0d0; } /* خلفية رمادي غامق، نص رمادي فاتح */
                QLabel { color: #d0d0d0; margin-bottom: 5px; }
                QPushButton { background-color: #808080; color: #d0d0d0; border: 1px solid #a0a0a0; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; } /* أزرار رمادي متوسط */
                QPushButton:hover { background-color: #a0a0a0; } /* هوفر أفتح للأزرار */
                QCheckBox { color: #d0d0d0; margin-top: 5px; margin-bottom: 5px; }
                QComboBox { background-color: #737373; color: #d0d0d0; border: 1px solid #999999; border-radius: 3px; padding: 4px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; } /* قوائم منسدلة أغمق شوية */
                QGroupBox { border: 1px solid #999999; border-radius: 5px; margin-top: 10px; padding: 10px; color: #d0d0d0; }
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #cccccc; } /* عنوان المجموعة أفتح */
                QLabel#disk_space_status { font-weight: bold; color: #d0d0d0; }
                QLabel#disk_space_status_ok { color: lightgreen; }
                QLabel#disk_space_status_warning { color: yellow; }
                QLabel#disk_space_status_error { color: red; }
                QLabel#system_info { margin-bottom: 2px; color: #d0d0d0; }
            """)
            if self.greeting:
                self.greeting.setStyleSheet("font-size: 15px; margin-top: 1px; margin-bottom: 1px; color: #d0d0d0;") # لون نص الترحيب للسمة اللوكس
        elif theme_name == "Light Purple":
            self.setStyleSheet("""
                QWidget { background-color: #e6ccff; font-family: 'Segoe UI'; font-size: 13px; color: #4d194d; } /* بنفسجي فاتح للخلفية، بنفسجي داكن للنص */
                QLabel { color: #4d194d; margin-bottom: 5px; }
                QPushButton { background-color: #f0d9ff; color: #4d194d; border: 1px solid #b388eb; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
                QPushButton:hover { background-color: #b388eb; }
                QCheckBox { color: #4d194d; margin-top: 5px; margin-bottom: 5px; }
                QComboBox { background-color: #f3e5f5; color: #4d194d; border: 1px solid #ce93d8; border-radius: 3px; padding: 4px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
                QGroupBox { border: 1px solid #ce93d8; border-radius: 5px; margin-top: 10px; padding: 10px; color: #4d194d; }
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #8e24aa; } /* بنفسجي أغمق لعنوان المجموعة */
                QLabel#disk_space_status { font-weight: bold; color: #4d194d; }
                QLabel#disk_space_status_ok { color: darkgreen; }
                QLabel#disk_space_status_warning { color: darkorange; }
                QLabel#disk_space_status_error { color: darkred; }
                QLabel#system_info { margin-bottom: 2px; color: #4d194d; }
            """)
            if self.greeting:
                self.greeting.setStyleSheet("font-size: 15px; margin-top: 1px; margin-bottom: 1px; color: #4d194d;") # لون النص للسمة البنفسجية
        elif theme_name == "Light Black (Faded)":
            self.setStyleSheet("""
                QWidget { background-color: #505050; font-family: 'Segoe UI'; font-size: 13px; color: #e0e0e0; } /* افتحنا الخلفية والنص */
                QLabel { color: #e0e0e0; margin-bottom: 5px; }
                QPushButton { background-color: #707070; color: #e0e0e0; border: 1px solid #909090; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; } /* افتحنا الأزرار */
                QPushButton:hover { background-color: #909090; } /* افتحنا لونHover للأزرار */
                QCheckBox { color: #e0e0e0; margin-top: 5px; margin-bottom: 5px; }
                QComboBox { background-color: #606060; color: #e0e0e0; border: 1px solid #808080; border-radius: 3px; padding: 4px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; } /* افتحنا القوائم المنسدلة */
                QGroupBox { border: 1px solid #808080; border-radius: 5px; margin-top: 10px; padding: 10px; color: #e0e0e0; } /* افتحنا حدود وعنوان المجموعات */
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #c0c0c0; } /* افتحنا لون عنوان المجموعة */
                QLabel#disk_space_status { font-weight: bold; color: #e0e0e0; }
                QLabel#disk_space_status_ok { color: lightgreen; }
                QLabel#disk_space_status_warning { color: yellow; }
                QLabel#disk_space_status_error { color: red; }
                QLabel#system_info { margin-bottom: 2px; color: #e0e0e0; }
            """)
            if self.greeting:
                self.greeting.setStyleSheet("font-size: 15px; margin-top: 1px; margin-bottom: 1px; color: #e0e0e0;") # لون النص للسمة السوداء الفاتحة)

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
        layout.setSpacing(10)

        if self.logo:
            logo_label = QLabel(self)
            logo_label.setPixmap(self.logo)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)

        self.greeting = QLabel()
        self.greeting.setAlignment(Qt.AlignCenter)
        self.greeting.setStyleSheet("font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #e0e0e0;")
        layout.addWidget(self.greeting)

        controls = QVBoxLayout()
        controls.setSpacing(8)
        layout.addLayout(controls)

        # System Updates Group - نقلناها إلى هنا وأضفنا أزرار التثبيت
        update_group = QGroupBox(_("System Updates"))
        update_layout = QVBoxLayout() # استخدم QVBoxLayout لترتيب رأسي
        update_layout_buttons = QHBoxLayout() # صف للأزرار الأفقية
        self.pacman_btn_bottom = self.create_button(_("Update System (Pacman)"), lambda: self.run_terminal_cmd("sudo pacman -Syu"))
        update_layout_buttons.addWidget(self.pacman_btn_bottom)
        self.yay_btn_bottom = self.create_button(_("Update System (Yay)"), lambda: self.run_terminal_cmd("yay -Syu"))
        if not self.is_yay_installed():
            self.yay_btn_bottom.setEnabled(False)
            self.yay_btn_bottom.setToolTip(_("Yay is not installed."))
        update_layout_buttons.addWidget(self.yay_btn_bottom)
        update_layout.addLayout(update_layout_buttons) # إضافة صف أزرار التحديث

        # أزرار تثبيت النواة
        kernel_install_layout = QHBoxLayout()
        self.install_lts_btn = self.create_button(_("Install Linux LTS"), self.install_linux_lts)
        kernel_install_layout.addWidget(self.install_lts_btn)
        self.install_zen_btn = self.create_button(_("Install Linux Zen"), self.install_linux_zen)
        kernel_install_layout.addWidget(self.install_zen_btn)
        update_layout.addLayout(kernel_install_layout) # إضافة صف أزرار تثبيت النواة

        update_group.setLayout(update_layout)
        controls.addWidget(update_group)

        # Theme Selection
        theme_layout = QHBoxLayout()
        self.theme_label = QLabel(_("Application Theme:"))
        theme_layout.addWidget(self.theme_label)
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(["Default", "Sky Blue", "Light Black", "Light Purple"])
        self.theme_combobox.setCurrentText(self.current_theme)
        self.theme_combobox.currentTextChanged.connect(self.save_theme)
        self.theme_combobox.setStyleSheet("font-size: 10px; padding: 4px;") # تصغير حجم خط قائمة الثيمات
        theme_layout.addWidget(self.theme_combobox)
        controls.addLayout(theme_layout)

        # Application Language
        app_lang_layout = self.create_labeled_combobox(
            label_attr='app_lang_label',
            combo_attr='app_lang_combobox',
            label_text=_("Application Language:"),
            items=list(APP_LANGUAGES.values()),  # استخدام أسماء اللغات
            default=APP_LANGUAGES.get(self.language_code, 'English'), # البحث عن الاسم باستخدام الكود
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

        # System Language
        sys_lang_layout = QHBoxLayout()
        self.sys_lang_label = QLabel(_("System Language:"))
        sys_lang_layout.addWidget(self.sys_lang_label)
        self.system_language_combobox = QComboBox()
        self.system_language_combobox.addItems(list(SYSTEM_LANGUAGES.values()))
        self.system_language_combobox.setCurrentText('en_US.UTF-8' if 'en_US.UTF-8' in SYSTEM_LANGUAGES else list(SYSTEM_LANGUAGES.keys())[0] if SYSTEM_LANGUAGES else '')
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
        self.disk_space_label = QLabel(_("Available Disk Space:"))
        self.disk_space_status = QLabel()
        self.disk_space_status.setObjectName("disk_space_status")
        system_info_layout.addWidget(self.disk_space_label, 0, 0)
        system_info_layout.addWidget(self.disk_space_status, 0, 1)
        self.processor_label = QLabel(_("Processor:"))
        self.processor_info = QLabel()
        self.processor_info.setObjectName("system_info")
        system_info_layout.addWidget(self.processor_label, 1, 0)
        system_info_layout.addWidget(self.processor_info, 1, 1)
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

        layout.addStretch(1) # إضافة تمدد في نهاية التخطيط الرئيسي

        # أول تعريب للواجهة
        self.retranslate_ui()

    def create_labeled_combobox(self, label_attr, combo_attr, label_text, items, default, on_change=None):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        combo = QComboBox()
        combo.addItems(items)
        index = combo.findText(default)
        if index != -1:
            combo.setCurrentIndex(index)
        if on_change:
            combo.currentTextChanged.connect(on_change)
        # تصغير حجم خط القائمة المنسدلة وتعديل الحشو
        combo.setStyleSheet("font-size: 10px; padding: 4px;")
        setattr(self, label_attr, label)
        setattr(self, combo_attr, combo)
        layout.addWidget(label)
        layout.addWidget(combo)
        return layout

    def create_button(self, text, on_click):
        button = QPushButton(text)
        button.clicked.connect(on_click)
        # يمكنك هنا محاولة تصغير حجم الخط أو تغيير أبعاد الزر
        button.setStyleSheet("font-size: 10px; padding: 4px 8px;") # تقليل حجم الخط والحشو
        return button

    def update_startup_file(self, state):
        autostart_dir = os.path.expanduser("~/.config/autostart")
        startup_file_path = os.path.join(autostart_dir, "helwan_welcome.desktop")
        if state == Qt.Checked:
            if not os.path.exists(autostart_dir):
                os.makedirs(autostart_dir, exist_ok=True)
            with open(startup_file_path, "w") as f:
                f.write("[Desktop Entry]\n")
                f.write("Type=Application\n")
                f.write(f"Exec={sys.executable} {os.path.abspath(__file__)}\n")
                f.write("Hidden=false\n")
                f.write("X-GNOME-Autostart-enabled=true\n")
                f.write("Name=Helwan Welcome\n")
                f.write("Comment=Welcome application for Helwan Linux\n")
                if self.logo:
                    # افتراض أن الشعار موجود في نفس دليل السكريبت أو يمكنك توفير مسار مطلق
                    logo_base_name = os.path.basename(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources", "logo.png"))
                    f.write(f"Icon={os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sources', logo_base_name)}\n")
        else:
            if os.path.exists(startup_file_path):
                os.remove(startup_file_path)
        self.show_on_startup = state == Qt.Checked

    def change_language(self, language_name):
        for code, name in APP_LANGUAGES.items():
            if name == language_name:
                new_gettext = load_translation(code)
                global _
                _ = new_gettext
                self.language_code = code
                self.retranslate_ui()
                self.settings.setValue("language_index", self.app_lang_combobox.currentIndex())
                QMessageBox.information(self, _("Language Changed"), _("Application language has been changed. Some changes may require an application restart."))
                return
        print(f"Warning: Language code not found for {language_name}")

    def save_theme(self, theme_name):
        self.current_theme = theme_name
        self.load_theme(theme_name)
        self.settings.setValue("theme", theme_name)

    def is_yay_installed(self):
        try:
            process = subprocess.run(['yay', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return process.returncode == 0
        except FileNotFoundError:
            return False

    def install_linux_lts(self):
        self.run_terminal_cmd("sudo pacman -S --needed linux-lts linux-lts-headers")

    def install_linux_zen(self):
        self.run_terminal_cmd("sudo pacman -S --needed linux-zen linux-zen-headers")

    def apply_system_language(self):
        selected_lang_name = self.system_language_combobox.currentText()
        lang_code = None
        for code, name in SYSTEM_LANGUAGES.items():
            if name == selected_lang_name:
                lang_code = code
                break

        if lang_code:
            try:
                process = subprocess.Popen(["pkexec", "localectl", "set-locale", f"LANG={lang_code}"],
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
        else:  # <-- هذا هو السطر 432
            QMessageBox.critical(self, _("Error"), _("Invalid system language selected."))

        def open_url(self, url):
            webbrowser.open(url)

    def run_terminal_cmd(self, command, title=_("Running Command")):
        try:
            subprocess.Popen(["xterm", "-hold", "-T", title, "-e", f"{command}; echo; echo Press Enter to exit..."])
        except FileNotFoundError:
            QMessageBox.critical(self, _("Error"), _("xterm is not installed. Please install xterm."))
            
    def open_url(self, url):
        webbrowser.open(url)

    def _execute_command(self, command, dialog):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        dialog.close()
        if process.returncode == 0:
            QMessageBox.information(self, _("Success"), stdout.decode())
        else:
            QMessageBox.critical(self, _("Error"), stderr.decode())

    def check_disk_space(self):
        try:
            total, used, free = shutil.disk_usage("/")
            free_gb = free // (2**30)
            warning_threshold = 10  # GB
            error_threshold = 5   # GB

            self.disk_space_status.setText(f"{free_gb} GB {_('Free')}")
            if free_gb < error_threshold:
                self.disk_space_status.setStyleSheet("font-weight: bold; color: red;")
            elif free_gb < warning_threshold:
                self.disk_space_status.setStyleSheet("font-weight: bold; color: orange;")
            else:
                self.disk_space_status.setStyleSheet("font-weight: bold; color: green;")
        except Exception as e:
            print(f"Error checking disk space: {e}")
            self.disk_space_status.setText(_("N/A"))

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

    def retranslate_ui(self):
        self.setWindowTitle(_("Welcome to Helwan Linux"))
        if self.app_lang_label:
            self.app_lang_label.setText(_("Application Language:"))
        if self.startup_check:
            self.startup_check.setText(_("Show on startup"))
        if self.pacman_btn_bottom:
            self.pacman_btn_bottom.setText(_("Update System (Pacman)"))
        if self.yay_btn_bottom:
            self.yay_btn_bottom.setText(_("Update System (Yay)"))
            if not self.is_yay_installed():
                self.yay_btn_bottom.setToolTip(_("Yay is not installed."))
            else:
                self.yay_btn_bottom.setToolTip("")
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
        if self.system_info_group:
            self.system_info_group.setTitle(_("System Information"))
        if self.disk_space_label:
            self.disk_space_label.setText(_("Available Disk Space:"))
        if self.processor_label:
            self.processor_label.setText(_("Processor:"))
        if self.memory_label:
            self.memory_label.setText(_("RAM:"))
        if self.neofetch_btn:
            self.neofetch_btn.setText(_("Show System Info Details"))
        if self.htop_btn:
            self.htop_btn.setText(_("Performance Monitor"))
        if self.theme_label:
            self.theme_label.setText(_("Application Theme:"))
        self.greeting.setText(_("Welcome to the world of Helwan Linux! ❤️\nWe are here to help you build your dreams on the strongest foundation!"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WelcomeApp()
    window.setWindowTitle("Welcome to Helwan Linux")
    window.show()
    sys.exit(app.exec_())
