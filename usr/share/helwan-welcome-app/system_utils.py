import os
import subprocess
import webbrowser
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
import platform
import psutil

def check_startup_enabled():
    autostart_dir = os.path.expanduser("~/.config/autostart")
    startup_file_path = os.path.join(autostart_dir, "helwan_welcome.desktop")
    return os.path.exists(startup_file_path)

def update_startup_file(parent, state):
    try:
        autostart_dir = os.path.expanduser("~/.config/autostart")
        if not os.path.exists(autostart_dir):
            os.makedirs(autostart_dir)

        startup_file_path = os.path.join(autostart_dir, "helwan_welcome.desktop")
        current_file_path = os.path.abspath(__file__)  # يجب تعديل هذا إذا كان main.py في مكان آخر

        if state == Qt.Checked:
            if not os.path.exists(startup_file_path):
                with open(startup_file_path, "w") as f:
                    f.write(f"""[Desktop Entry]
Name=Helwan Welcome App
Exec=python3 {current_file_path.replace('system_utils.py', 'main.py')}
Type=Application
X-GNOME-Autostart-enabled=true
Comment=Welcome screen for Helwan Linux
Icon={os.path.join(os.path.dirname(current_file_path), "sources", "logo.png")}
Terminal=false""")
                return True
        else:
            if os.path.exists(startup_file_path):
                os.remove(startup_file_path)
                return True
        return False
    except Exception as e:
        QMessageBox.warning(parent, _("Error"), f"{_('Could not update startup file:')} {e}")
        return False

def open_url(parent, url):
    try:
        webbrowser.open(url)
    except Exception as e:
        QMessageBox.warning(parent, _("Error"), f"{_('Could not open URL:')} {e}")

def run_terminal_cmd(parent, cmd):
    try:
        subprocess.Popen(["xterm", "-hold", "-e", f"{cmd}; echo; echo Press Enter to exit..."])
    except FileNotFoundError:
        QMessageBox.critical(parent, _("Error"), _("xterm is not installed. Please install xterm."))

def apply_system_language(parent, lang):
    try:
        process = subprocess.Popen(["pkexec", "localectl", "set-locale", f"LANG={lang}"],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            QMessageBox.information(parent, _("System Language"), _("System language applied successfully. You might need to restart your system for the changes to take full effect."))
            return True
        else:
            QMessageBox.critical(parent, _("Error"), f"{_('Failed to apply system language:')} {stderr.decode()}")
            return False
    except FileNotFoundError:
        QMessageBox.critical(parent, _("Error"), _("pkexec command not found. Ensure polkit is installed."))
        return False
    except Exception as e:
        QMessageBox.critical(parent, _("Error"), f"{_('An error occurred while applying system language:')} {e}")
        return False

def install_linux_lts(parent):
    _install_kernel(parent, "linux-lts", "linux-lts-headers")

def install_linux_zen(parent):
    _install_kernel(parent, "linux-zen", "linux-zen-headers")

def _install_kernel(parent, kernel_package, headers_package):
    command = f"sudo pacman -S --needed {kernel_package} {headers_package}"
    try:
        subprocess.Popen(["xterm", "-hold", "-e", f"{command}; sudo grub-mkconfig -o /boot/grub/grub.cfg; echo; echo Press Enter to exit..."])
    except FileNotFoundError:
        QMessageBox.critical(parent, _("Error"), _("xterm is not installed. Please install xterm."))
    except Exception as e:
        QMessageBox.critical(parent, _("Error"), f"{_('An error occurred during kernel installation:')} {e}")

def check_disk_space(parent):
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
                        parent.disk_space_status.setText(_("Low ({} / {})").format(available, total))
                        parent.disk_space_status.setStyleSheet("color: red;")
                    elif used_percentage > 80:
                        parent.disk_space_status.setText(_("Warning ({} / {})").format(available, total))
                        parent.disk_space_status.setStyleSheet("color: orange;")
                    else:
                        parent.disk_space_status.setText(_("OK ({} / {})").format(available, total))
                        parent.disk_space_status.setStyleSheet("color: green;")
                    return
            parent.disk_space_status.setText(_("N/A"))
            parent.disk_space_status.setStyleSheet("")
        else:
            print(f"Error executing df: Return code {process.returncode}, Stderr: {stderr}")
            parent.disk_space_status.setText(_("Error"))
            parent.disk_space_status.setStyleSheet("color: red;")
    except FileNotFoundError:
        parent.disk_space_status.setText(_("N/A (df not found)"))
        parent.disk_space_status.setStyleSheet("")
    except Exception as e:
        print(f"Exception in check_disk_space: {e}")
        parent.disk_space_status.setText(_("Error"))
        parent.disk_space_status.setStyleSheet("color: red;")

def update_system_info(parent):
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

    parent.processor_info.setText(processor_info)

    # Memory Info
    try:
        mem = psutil.virtual_memory()
        total_memory_gb = round(mem.total / (1024 ** 3), 2)
        parent.memory_info.setText(f"{total_memory_gb} GB")
    except Exception as e:
        print(f"Error getting memory info: {e}")
        parent.memory_info.setText(_("N/A"))

def is_yay_installed():
    try:
        subprocess.run(["yay", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        return True # يعتبر مثبت إذا لم يظهر خطأ في عدم العثور عليه
