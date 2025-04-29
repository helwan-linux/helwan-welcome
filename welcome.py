import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import os
import webbrowser
from PIL import Image, ImageTk
import gettext
import subprocess
import socket
import threading

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
    def __init__(self, root):
        self.root = root
        self.root.title(_("Welcome to Helwan Linux"))
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.startup_file = os.path.join(os.path.expanduser("~"), ".helwan_welcome_shown")
        self.show_on_startup = not os.path.exists(self.startup_file)

        self.logo = self.load_logo()
        if self.logo:
            self.logo_label = tk.Label(self.root, image=self.logo, bg="#f0f0f0")
            self.logo_label.pack(pady=10)

        self.greeting_label = tk.Label(self.root,
                                     text=_("Welcome to the world of Helwan Linux! ❤️\nWe are here to help you build your dreams on the strongest foundation!"),
                                     font=("Arial", 14),
                                     bg="#f0f0f0", justify="center")
        self.greeting_label.pack(pady=10)

        self.buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.buttons_frame.pack(pady=10)

        self.language_label_app = tk.Label(self.buttons_frame, text=_("Application Language:"), font=("Arial", 10), bg="#f0f0f0")
        self.language_label_app.grid(row=0, column=0, padx=5, pady=5)

        self.language_var_app = tk.StringVar(value=language_code)
        self.language_menu_app = ttk.OptionMenu(self.buttons_frame, self.language_var_app, language_code, *['en', 'ar', 'es', 'pt'], command=self.change_language)
        self.language_menu_app.grid(row=0, column=1, padx=5, pady=5)

        self.startup_var = tk.BooleanVar(value=self.show_on_startup)
        self.startup_checkbutton = tk.Checkbutton(self.buttons_frame, text=_("Show on startup"), variable=self.startup_var, command=self.toggle_startup, bg="#f0f0f0")
        self.startup_checkbutton.grid(row=0, column=2, padx=5, pady=5)

        self.update_pacman_button = tk.Button(self.buttons_frame, text=_("Update System (Pacman)"), command=lambda: self.update_system("pacman"))
        self.update_pacman_button.grid(row=1, column=0, padx=10, pady=10)

        self.update_yay_button = tk.Button(self.buttons_frame, text=_("Update System (Yay)"), command=lambda: self.update_system("yay"))
        self.update_yay_button.grid(row=1, column=1, padx=10, pady=10)

        # استبدال الزر بقائمة منسدلة لتغيير لغة النظام
        self.system_language_label = tk.Label(self.buttons_frame, text=_("System Language:"), font=("Arial", 10), bg="#f0f0f0")
        self.system_language_label.grid(row=2, column=0, padx=5, pady=5)

        self.system_language_var = tk.StringVar()
        self.system_language_choices = ['ar_EG.UTF-8', 'en_US.UTF-8', 'es_ES.UTF-8', 'pt_PT.UTF-8']
        self.system_language_combobox = ttk.Combobox(self.buttons_frame, textvariable=self.system_language_var, values=self.system_language_choices)
        self.system_language_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.system_language_combobox.set('ar_EG.UTF-8')  # تعيين اللغة العربية كلغة افتراضية في القائمة
        self.change_system_language_button = tk.Button(self.buttons_frame, text=_("Apply System Language"), command=self.apply_system_language)
        self.change_system_language_button.grid(row=2, column=2, padx=10, pady=10)

        self.documentation_button = tk.Button(self.buttons_frame, text=_("Open Documentation"), command=self.open_documentation)
        self.documentation_button.grid(row=3, column=0, padx=10, pady=10)

        self.youtube_button = tk.Button(self.buttons_frame, text=_("Open YouTube Channel"), command=self.open_youtube_channel)
        self.youtube_button.grid(row=3, column=1, padx=10, pady=10)

        # إضافة أزرار جديدة لتحليل النظام ومراقبة الأداء
        self.system_info_button = tk.Button(self.buttons_frame, text=_("Show System Info"), command=self.show_system_info)
        self.system_info_button.grid(row=4, column=0, padx=10, pady=10)

        self.performance_monitor_button = tk.Button(self.buttons_frame, text=_("Performance Monitor"), command=self.show_performance)
        self.performance_monitor_button.grid(row=4, column=1, padx=10, pady=10)

        if self.show_on_startup:
            self.mark_as_shown()

    def load_logo(self):
        try:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources", "logo.png")
            logo = Image.open(logo_path).resize((150, 150))
            return ImageTk.PhotoImage(logo)
        except Exception as e:
            messagebox.showwarning(_("Logo Not Found"), str(e))
            return None

    def change_language(self, language_code):
        global _
        _ = set_language(language_code)
        self.update_ui()

    def update_ui(self):
        self.root.title(_("Welcome to Helwan Linux"))
        self.greeting_label.config(text=_("Welcome to the world of Helwan Linux! ❤️\nWe are here to help you build your dreams on the strongest foundation!"))
        self.language_label_app.config(text=_("Application Language:"))
        self.update_pacman_button.config(text=_("Update System (Pacman)"))
        self.update_yay_button.config(text=_("Update System (Yay)"))
        self.system_language_label.config(text=_("System Language:"))
        self.change_system_language_button.config(text=_("Apply System Language"))
        self.documentation_button.config(text=_("Open Documentation"))
        self.youtube_button.config(text=_("Open YouTube Channel"))
        self.startup_checkbutton.config(text=_("Show on startup"))
        self.system_info_button.config(text=_("Show System Info"))
        self.performance_monitor_button.config(text=_("Performance Monitor"))

    def open_documentation(self):
        webbrowser.open("https://helwan-linux.mystrikingly.com/documentation")

    def open_youtube_channel(self):
        webbrowser.open("https://www.youtube.com/channel/UCKlFDMjrzkVFzw-erYKVibQ")

    def update_system(self, manager):
        if not self.check_internet_connection():
            messagebox.showerror(_("Error"), _("No internet connection."))
            return

        # إنشاء شريط التقدم
        progress_window = tk.Toplevel(self.root)
        progress_window.title(_("Updating System"))
        progress_window.geometry("400x100")
        progress_label = tk.Label(progress_window, text=_("Updating system, please wait..."))
        progress_label.pack(pady=10)

        progress = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="indeterminate")
        progress.pack(pady=10)
        progress.start()

        # بدء التحديث في خيط منفصل لعدم تعطيل واجهة المستخدم
        def run_update():
            command = ["xterm", "-e"]
            if manager == "pacman":
                command.append("bash -c 'sudo pacman -Syu; echo; echo Press Enter to close...; read'")
            else:
                command.append("bash -c 'yay -Syu; echo; echo Press Enter to close...; read'")

            try:
                subprocess.Popen(command)
                progress.stop()
                progress_window.destroy()
                messagebox.showinfo(_("Update Complete"), _("System updated successfully."))
            except Exception as e:
                progress.stop()
                progress_window.destroy()
                messagebox.showerror(_("Error"), str(e))

        threading.Thread(target=run_update).start()

    def check_internet_connection(self):
        try:
            socket.create_connection(("www.google.com", 80), timeout=5)
            return True
        except OSError:
            return False

    def apply_system_language(self):
        selected_language = self.system_language_var.get()
        try:
            messagebox.showinfo(_("Language Change"), _(f"System will be configured to {selected_language} now."))
            subprocess.run(["localectl", "set-locale", f"LANG={selected_language}"], check=True)
            subprocess.run(["sudo", "locale-gen"], check=True)
            messagebox.showinfo(_("Done"), _("System language changed. Please log out and log in again."))
        except subprocess.CalledProcessError as e:
            messagebox.showerror(_("Error"), str(e))

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
        if self.startup_var.get():
            self.mark_as_shown()
        else:
            self.mark_as_not_shown()

    # إضافة وظيفة لعرض معلومات النظام
    def show_system_info(self):
        info = ""
        info += "Kernel: " + self.run_command("uname -r")
        info += "CPU Info:\n" + self.run_command("lscpu | grep 'Model name'")
        info += "Memory:\n" + self.run_command("free -h")
        info += "Disk Usage:\n" + self.run_command("df -h --total | grep total")
        info += "Graphics:\n" + self.run_command("lspci | grep -i vga")
        self.show_output("System Info", info)

    # إضافة وظيفة لمراقبة الأداء
    def show_performance(self):
        info = ""
        info += "CPU Usage:\n" + self.run_command("top -bn1 | grep 'Cpu(s)'")
        info += "Memory Usage:\n" + self.run_command("free -h")
        info += "\nTop 5 Processes:\n" + self.run_command("ps aux --sort=-%mem | head -n 6")
        self.show_output("Performance Monitor", info)

    def show_output(self, title, content):
        output_window = tk.Toplevel(self.root)
        output_window.title(title)
        text_box = tk.Text(output_window, wrap="word", bg="black", fg="lime", font=("Courier", 10))
        text_box.pack(expand=True, fill="both")
        text_box.insert("1.0", content)
        text_box.config(state="disabled")

    # تنفيذ الأوامر عبر shell
    def run_command(self, command):
        try:
            return subprocess.check_output(command, shell=True, text=True)
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"

# تشغيل التطبيق
if __name__ == "__main__":
    root = tk.Tk()
    app = WelcomeApp(root)
    root.mainloop()
