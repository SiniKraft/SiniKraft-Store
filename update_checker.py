import datetime
import json
import os.path
import os
import subprocess
import sys
import threading
import time
import urllib.request
import winreg

from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QMessageBox, QApplication, QSystemTrayIcon

import ui_sinikraft_launcher_rc  # type: ignore


def find_apps():
    app_list = []
    hkeys = [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]
    for hkey in hkeys:
        with winreg.OpenKey(hkey, r"Software\Microsoft\Windows\CurrentVersion\Uninstall") as h_apps:
            for idx in range(winreg.QueryInfoKey(h_apps)[0]):
                try:
                    with winreg.OpenKeyEx(h_apps, winreg.EnumKey(h_apps, idx)) as h_app_info:
                        def get_value(key):
                            try:
                                return winreg.QueryValueEx(h_app_info, key)[0]
                            except Exception as e:
                                return ""

                        if get_value("Publisher").__contains__("SiniKraft") or get_value("Publisher") == "Nicklor":
                            installer_path = get_value("InstallLocation")
                            if os.path.exists(str(installer_path)):
                                try:
                                    icon_str = get_value("DisplayIcon")
                                except Exception as e:
                                    icon_str = ""
                                date = get_value("InstallDate")
                                date = date[6] + date[7] + "/" + date[4] + date[5] + "/" + date[0] + date[1] + \
                                       date[2] + date[3]
                                app_list.append((get_value("DisplayName").split(" version")[0], icon_str,
                                                 get_value("DisplayVersion"), date,
                                                 get_value("UninstallString"), 'start /wait "" ' +
                                                 get_value("QuietUninstallString").replace("/SILENT", "/VERYSILENT"),
                                                 (str(round(get_value("EstimatedSize") / 1024, 2)) + " Mo")
                                                 .replace(".", ",")))
                        elif get_value("Publisher") == "UNKNOWN":
                            if get_value("DisplayName") == "Discord Spammer":
                                installer_path = get_value("InstallLocation")
                                if os.path.exists(str(installer_path)):
                                    try:
                                        icon_str = get_value("DisplayIcon")
                                    except Exception as e:
                                        icon_str = ""
                                date = get_value("InstallDate")
                                date = date[6] + date[7] + "/" + date[4] + date[5] + "/" + date[0] + date[1] + \
                                       date[2] + date[3]
                                app_list.append((get_value("DisplayName").split(" version")[0], icon_str,
                                                 get_value("DisplayVersion"), date,
                                                 get_value("UninstallString"), "start /wait " +
                                                 get_value("UninstallString").replace("/I", "/X") + " /QUIET",
                                                 (str(round(get_value("EstimatedSize") / 1024, 2)) + " Mo")
                                                 .replace(".", ",")))

                except (WindowsError, KeyError, ValueError):
                    continue

    return app_list


def check_update_main():
    e = None
    a = {"": ""}
    try:
        with urllib.request.urlopen("https://raw.githubusercontent.com/SiniKraft/SiniKraft-Store/master/update.json") \
                as url:
            a = json.loads(url.read().decode())
    except Exception as _e:
        e = _e
    return a, e


def log(text: str):
    print(text[1:])
    with open("update_checker.log", "a") as file:
        file.write(text)


def write_to_task(_dict: dict):
    with open("task.json", "w") as file:
        json.dump(_dict, file, indent=4)


def get_tasks():
    if not os.path.isfile("task.json"):
        write_to_task({"current_task": None, "current_state": None, "queued_work": []})
    try:
        with open("task.json", "r") as file:
            _dict = json.load(file)
    except json.JSONDecodeError:
        _dict = {"current_task": None, "current_state": None, "queued_work": []}
        write_to_task(_dict)
    return _dict


def perform(parent=None, show_msg=False):
    no_notif = False
    if parent is not None:
        no_notif = True
    show_msg = False
    parent = None
    with open("checking", "w") as file:
        file.write("\n")
        file.close()
    if os.path.isfile("update_checker.log"):
        try:
            os.remove("update_checker.log")
        except Exception as e:
            pass
    if parent is not None:
        to_write = ("Starting Update Checking at %s from %s" % (
            str(datetime.datetime.now()), "SiniKraft STORE app"))
    else:
        to_write = ("Starting Update Checking at %s from %s" % (str(datetime.datetime.now()),
                                                                "Update Checker Service"))
    _continue = True
    result = check_update_main()
    if result[1] is not None:
        if show_msg:
            msg = QMessageBox(parent)
            msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
            msg.setWindowTitle("Failed to Check for Updates !")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("An error occured while checking for updates : " + str(result[1]))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        log(to_write + "\nError : " + str(result[1]))
        _continue = False
    if _continue:
        json = result[0]
        found = False
        app_list = find_apps()
        for x in range(0, len(app_list)):
            if json[app_list[x][0]][0] != app_list[x][2]:
                found = True
                log(to_write + "\nFound Update for %s : New version : %s, old : %s" % (
                    app_list[x][0], json[app_list[x][0]][0],
                    app_list[x][2]))
                _u = list(app_list[x])
                _u.append(json[app_list[x][0]][1])
                __dict = get_tasks()
                __dict["queued_work"].append(_u)
                write_to_task(__dict)
        if found and show_msg:
            msg = QMessageBox(parent)
            msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
            msg.setWindowTitle("Updates Avaible !")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Updates were found ! Installing them now ...")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        if not found:
            if no_notif or ("-launched-from-store" in sys.argv):
                notifies("No Updates !", "You are up-to-date !")
                time.sleep(10)
            if show_msg:
                msg = QMessageBox(parent)
                msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
                msg.setWindowTitle("No Updates Avaible !")
                msg.setIcon(QMessageBox.Information)
                msg.setText("No Updates were found ! You are up-to-date !")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
            try:
                os.remove("checking")
            except:
                pass
            appp = QApplication.instance()
            appp.exit(0)
        else:
            manage_tasks()


def manage_tasks():
    """
    # Sort:
    1. Download
    2. Uninstall
    3. Install
    4; Finished
    :return:
    """
    # Let's first check if a task was running ...
    _dict_ = get_tasks()
    if _dict_["current_state"] is None:
        _dict_["current_task"] = _dict_["queued_work"][-1]
        _dict_["current_state"] = 1  # type: ignore
        _dict_["queued_work"].pop()
        write_to_task(_dict_)
    try:
        process(_dict_)
    except Exception as e:
        msg = QMessageBox(None)
        msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
        msg.setWindowTitle("Failed to Check for Updates !")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("An error occured while checking for updates : " + str(e))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    while len(_dict_["queued_work"]) > 0:
        _dict_["current_task"] = _dict_["queued_work"][-1]
        _dict_["current_state"] = 1  # type: ignore
        _dict_["queued_work"].pop()
        write_to_task(_dict_)
        try:
            process(_dict_)
        except Exception as e:
            msg = QMessageBox(None)
            msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
            msg.setWindowTitle("Failed to Check for Updates !")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("An error occured while checking for updates : " + str(e))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
    try:
        process(_dict_)
    except Exception as e:
        msg = QMessageBox(None)
        msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
        msg.setWindowTitle("Failed to Check for Updates !")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("An error occured while checking for updates : " + str(e))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()



def notifies(title, message):
    icon = QIcon(":/images/SiniKraft-STORE-icon.png")
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    tray.setToolTip("SiniKraft STORE")
    tray.showMessage(title, message, icon, 10)


def process(dict_: dict):
    params_dict = load_params()
    if dict_["current_state"] == 1:
        # Downloading
        try:
            path_to_save = os.path.expandvars("%TEMP%") + "\\" + "tmp_installer.exe"
            url = dict_["current_task"][-1]
            extension = url[-4:]
            if extension == ".msi":
                path_to_save = path_to_save[:-4] + ".msi"
            notifies("Starting Download ...", "Starting downloading update for %s ..." % (dict_["current_task"][0]))
            log("\nStarting downloading '%s' to '%s'" % (url, path_to_save))
            urllib.request.urlretrieve(url, path_to_save)
            log("\nFinished Downloading !")
            if params_dict["notifications"]["finish_download"] and not params_dict["automating"]["install_when_download"
                                                                                                 "ed"]:
                notifies("Download Finished !", "The Update for %s is now downloaded !" % (dict_["current_task"][0]))
            dict_["current_state"] = 2
            write_to_task(dict_)
        except Exception as e:
            log("\nException when downloading : %s" % str(e))

    if dict_["current_state"] == 2:
        if not params_dict["automating"]["install_when_downloaded"]:
            time.sleep(10)
            notifies("Waiting confirmation ...", "Update is ready to install. Please open SiniKraft STORE to confirm in"
                                                 "stalling.")
            time.sleep(5)
        else:
            # Processing 2
            if params_dict["notifications"]["finish_download"] and params_dict["automating"]["install_when_downloaded"]:
                notifies("Download Finished !", "The Update for %s is now downloaded ! Installing Update now" % (
                    dict_["current_task"][0]))
            uninstall_cmd = dict_["current_task"][5]
            log("\nCalling " + "cmd /c " + uninstall_cmd)
            if params_dict["notifications"]["start_install"]:
                notifies("Installing Update", "%s will be fist uninstalled and then reinstalled." % (dict_["current_tas"
                                                                                                           "k"][0]))
            a = subprocess.check_output("cmd /c " + uninstall_cmd, shell=False)
            log("\nUninstalling cmd returned exit code 0 with output : " + a.decode())
            dict_["current_state"] = 3
            write_to_task(dict_)

    if dict_["current_state"] == 3:
        extension = dict_["current_task"][4][:-1][-4:]
        if extension == ".exe":
            path = os.path.expandvars("%TEMP%") + "\\" + "tmp_installer.exe"
            log("\nInstalling now ... with command '%s'" % (str(path + " /VERYSILENT")))
            a = subprocess.check_output(path + " /VERYSILENT")
            log("\nInstalling process returned exit code 0 and output : %s" % a.decode())
        else:
            path = os.path.expandvars("%TEMP%") + "\\" + "tmp_installer.msi"
            log("\nInstalling now ... with command '%s'" % (str('msiexec /I "' + path + '" /QUIET')))
            a = subprocess.check_output('msiexec /I "' + path + '" /QUIET')
            log("\nInstalling process returned exit code 0 and output : %s" % a.decode())

        try:
            os.remove(path)
        except Exception as e:
            log("\nFailed to remove tmp file '%s' : %s" % (path, str(e)))
        dict_["current_state"] = None
        __tmp_name__ = dict_["current_task"][0]
        dict_["current_task"] = None
        write_to_task(dict_)
        try:
            os.remove("checking")
        except FileNotFoundError:
            pass
        if params_dict["notifications"]["finish_install"]:
            notifies("Finished Updating", "%s is now Updated ! Enjoy !" % __tmp_name__)
            time.sleep(10)

    _app = QApplication.instance()
    _app.shutdown()
    os._exit(0)  # type: ignore


def load_params():
    with open("config.json", "r") as file:
        ___tmp__ = json.load(file)
    return ___tmp__


def run(parent=None, show_msg=False):
    already_app = True
    app = QApplication.instance()
    if app is None:
        already_app = False
        app = QApplication(sys.argv)
    _dict = get_tasks()
    if _dict["current_state"] is None:
        t = threading.Thread(target=perform, args=(parent, show_msg,))
    else:
        t = threading.Thread(target=process, args=(_dict,))

    try:
        t.start()
    except Exception as e:
        msg = QMessageBox(None)
        msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
        msg.setWindowTitle("Failed to Check for Updates !")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("An error occured while checking for updates : " + str(e))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    if not already_app:
        icon = QIcon(":/images/SiniKraft-STORE-icon.png")
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)
        tray.setToolTip("SiniKraft STORE")
        app.exec_()
        sys.exit(0)


if __name__ == "__main__":
    run()
