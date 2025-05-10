from PyQt5.QtWidgets import QWidget

def load_theme(widget: QWidget, theme_name: str):
    if theme_name == "Default":
        widget.setStyleSheet("""
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
        widget.setStyleSheet("""
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
        widget.setStyleSheet("""
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
        widget.setStyleSheet("""
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
