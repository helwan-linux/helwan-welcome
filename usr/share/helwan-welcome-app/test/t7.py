import sys
import smtplib
from email.mime.text import MIMEText
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QTextEdit, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import gettext

# === تحميل الترجمة ===
def load_translation(lang_code):
    try:
        translation = gettext.translation('app', localedir='locales', languages=[lang_code])
        translation.install()
        _ = translation.gettext
    except FileNotFoundError:
        gettext.install('app')
        _ = gettext.gettext
    return _

# === البريد الإلكتروني المرسل ===
EMAIL_SENDER = "helwanlinux@gmail.com"
EMAIL_PASSWORD = "APP_PASSWORD_HERE"  # لازم تجيب App Password من إعداد Gmail

# === إرسال البريد الإلكتروني ===
def send_email(subject, message, sender_email):
    try:
        msg = MIMEText(f"From: {sender_email}\n\n{message}")
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_SENDER

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_SENDER, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# === نموذج التواصل ===
class ContactForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(_("Contact Us"))
        self.setGeometry(200, 200, 400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(_("Your Name"))
        layout.addWidget(self.name_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText(_("Your Email"))
        layout.addWidget(self.email_input)

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText(_("Subject"))
        layout.addWidget(self.subject_input)

        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText(_("Your Message"))
        layout.addWidget(self.message_input)

        send_button = QPushButton(_("Send"))
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        self.setLayout(layout)

    def send_message(self):
        name = self.name_input.text()
        email = self.email_input.text()
        subject = self.subject_input.text()
        message = self.message_input.toPlainText()

        if not (name and email and subject and message):
            QMessageBox.warning(self, _("Warning"), _("Please fill all fields"))
            return

        full_message = f"Name: {name}\nEmail: {email}\n\n{message}"
        success = send_email(subject, full_message, email)
        if success:
            QMessageBox.information(self, _("Success"), _("Message sent successfully!"))
            self.close()
        else:
            QMessageBox.critical(self, _("Error"), _("Failed to send message. Please try again."))

# === التطبيق الرئيسي ===
class HelwanLinuxApp(QWidget):
    def __init__(self):
        super().__init__()
        self.language_code = 'en'
        global _
        _ = load_translation(self.language_code)
        self.setWindowTitle(_("Helwan Linux Welcome App"))
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        layout = self.main_layout
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel(_("Welcome to Helwan Linux"))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        language_label = QLabel(_("Select Language:"))
        layout.addWidget(language_label)

        self.language_combo = QComboBox()
        self.language_combo.addItem("English", 'en')
        self.language_combo.addItem("Arabic", 'ar')
        self.language_combo.setCurrentIndex(0)
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        layout.addWidget(self.language_combo)

        contact_button = QPushButton(_("Contact Us"))
        contact_button.clicked.connect(self.open_contact_form)
        layout.addWidget(contact_button)

        exit_button = QPushButton(_("Exit"))
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    def on_language_changed(self):
        lang_code = self.language_combo.currentData()
        self.change_language(lang_code)

    def change_language(self, lang_code):
        global _
        _ = load_translation(lang_code)
        self.language_code = lang_code
        self.rebuild_ui()

    def rebuild_ui(self):
        # مسح الواجهة القديمة
        for i in reversed(range(self.main_layout.count())):
            widget_item = self.main_layout.itemAt(i)
            if widget_item is not None:
                item_widget = widget_item.widget()
                if item_widget is not None:
                    item_widget.setParent(None)

        # بناء الواجهة الجديدة
        self.init_ui()

    def open_contact_form(self):
        self.contact_form = ContactForm(self)
        self.contact_form.show()

# === تشغيل البرنامج ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HelwanLinuxApp()
    window.show()
    sys.exit(app.exec_())
