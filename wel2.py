import os
import webbrowser
import gettext
import subprocess
import socket
import threading
from PIL import Image, ImageTk
from gi.repository import Gtk, Gdk, GLib

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

class WelcomeApp:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("interface.glade")  # تأكد من أن لديك واجهة GTK ملف XML
        self.window = self.builder.get_object("main_window")
        self.window.set_title(_("Welcome to Helwan Linux"))
        self.window.set_default_size(800, 600)

        self.startup_file = os.path.join(os.path.expanduser("~"), ".helwan_welcome_shown")
        self.show_on_startup = not os.path.exists(self.startup_file)

        self.logo = self.load_logo()
        if self.logo:
            logo_image = self.builder.get_object("logo_image")
            logo_image.set_from_pixbuf(self.logo)

        self.language_combo = self.builder.get_object("language_combo")
        self.language_combo.set_active_id(language_code)
        self.language_combo.connect("changed", self.on_language_changed)

        self.startup_checkbutton = self.builder.get_object("startup_checkbutton")
        self.startup_checkbutton.set_active(self.show_on_startup)
        self.startup_checkbutton.connect("toggled", self.toggle_startup)

        self.builder.get_object("update_pacman_button").connect("clicked", lambda w: self.update_system("pacman"))
        self.builder.get_object("update_yay_button").connect("clicked", lambda w: self.update_system("yay"))
        self.builder.get_object("documentation_button").connect("clicked", self.open_documentation)
        self.builder.get_object("youtube_button").connect("clicked", self.open_youtube_channel)
        self.builder.get_object("system_info_button").connect("clicked", self.show_system_info)
        self.builder.get_object("performance_monitor_button").connect("clicked", self.show_performance)

        if self.show_on_startup:
            self.mark_as_shown()

        self.window.show_all()

    def load_logo(self):
        try:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources", "logo.png")
            logo = Image.open(logo_path).resize((150, 150))
            return Gdk.pixbuf_new_from_file_at_size(logo_path, 150, 150)
        except Exception as e:
            print(f"Error loading logo: {e}")
            return None

    def on_language_changed(self, combo):
        language_code = combo.get_active_id()
        global _
        _ = set_language(language_code)
        self.update_ui()

    def update_ui(self):
        self.window.set_title(_("Welcome to Helwan Linux"))
        # تحديث بقية الواجهة بناءً على اللغة الجديدة

    def update_system(self, manager):
        if not self.check_internet_connection():
            self.show_error(_("Error"), _("No internet connection."))
            return

        dialog = Gtk.MessageDialog(self.window, Gtk.DialogFlags.MODAL, Gtk.MessageType.INFO, Gtk.ButtonsType.CANCEL, _("Updating system, please wait..."))
        dialog.show()

        def run_update():
            command = ["xterm", "-e"]
            if manager == "pacman":
                command.append("bash -c 'sudo pacman -Syu; echo; echo Press Enter to close...; read'")
            else:
                command.append("bash -c 'yay -Syu; echo; echo Press Enter to close...; read'")

            try:
                subprocess.Popen(command)
                dialog.destroy()
                self.show_info(_("Update Complete"), _("System updated successfully."))
            except Exception as e:
                dialog.destroy()
                self.show_error(_("Error"), str(e))

        threading.Thread(target=run_update).start()

    def check_internet_connection(self):
        try:
            socket.create_connection(("www.google.com", 80), timeout=5)
            return True
        except OSError:
            return False

    def open_documentation(self, button):
        webbrowser.open("https://helwan-linux.mystrikingly.com/documentation")

    def open_youtube_channel(self, button):
        webbrowser.open("https://www.youtube.com/channel/UCKlFDMjrzkVFzw-erYKVibQ")

    def show_system_info(self, button):
        info = ""
        info += "Kernel: " + self.run_command("uname -r")
        info += "CPU Info:\n" + self.run_command("lscpu | grep 'Model name'")
        info += "Memory:\n" + self.run_command("free -h")
        info += "Disk Usage:\n" + self.run_command("df -h --total | grep total")
        info += "Graphics:\n" + self.run_command("lspci | grep -i vga")
        self.show_output("System Info", info)

    def show_performance(self, button):
        info = ""
        info += "CPU Usage:\n" + self.run_command("top -bn1 | grep 'Cpu(s)'")
        info += "Memory Usage:\n" + self.run_command("free -h")
        info += "\nTop 5 Processes:\n" + self.run_command("ps aux --sort=-%mem | head -n 6")
        self.show_output("Performance Monitor", info)

    def show_output(self, title, content):
        dialog = Gtk.Dialog(title, self.window, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        textview = Gtk.TextView()
        textview.set_wrap_mode(Gtk.WrapMode.WORD)
        textview.get_buffer().set_text(content)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(textview)
        dialog.vbox.pack_start(scrolled_window, True, True, 0)
        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def run_command(self, command):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr

    def show_info(self, title, message):
        dialog = Gtk.MessageDialog(self.window, Gtk.DialogFlags.MODAL, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, message)
        dialog.run()
        dialog.destroy()

    def show_error(self, title, message):
        dialog = Gtk.MessageDialog(self.window, Gtk.DialogFlags.MODAL, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, message)
        dialog.run()
        dialog.destroy()

    def mark_as_shown(self):
        try:
            with open(self.startup_file, "w") as f:
                f.write("shown")
        except Exception as e:
            print(f"Error creating startup file: {e}")

    def toggle_startup(self, button):
        if self.startup_checkbutton.get_active():
            self.mark_as_shown()
        else:
            self.mark_as_not_shown()

    def mark_as_not_shown(self):
        try:
            os.remove(self.startup_file)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error removing startup file: {e}")


# تهيئة الواجهة
app = WelcomeApp()
Gtk.main()
