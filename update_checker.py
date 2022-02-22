import datetime
import json
import os.path
import urllib.request
import winreg

from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QMessageBox


def find_apps():
    app_list = []
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall") as h_apps:
        for idx in range(winreg.QueryInfoKey(h_apps)[0]):
            try:
                with winreg.OpenKeyEx(h_apps, winreg.EnumKey(h_apps, idx)) as h_app_info:
                    def get_value(key):
                        return winreg.QueryValueEx(h_app_info, key)[0]

                    if get_value("Publisher") == "SiniKraft" or get_value("Publisher") == "Nicklor":
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
                                             get_value("UninstallString"), get_value("QuietUninstallString"),
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
    with open("update_checker.log", "a") as file:
        file.write(text)
    change = False
    with open("update_checker.log", "r") as file:
        if file.readlines()[0][0] == '\n':
            change = True
            content = file.read()
    if change:
        with open("update_checker.log", "w") as file:
            file.write(content[-1:])
            file.close()


def perform(parent=None, show_msg=False):
    if os.path.isfile("update_checker.log"):
        try:
            os.remove("update_checker.log")
        except:
            pass
    if parent is not None:
        log("Starting Update Checking at %s from %s" % (datetime.datetime.now().isocalendar(), "SiniKraft STORE app"))
    else:
        log("Starting Update Checking at %s from %s" % (datetime.datetime.now().isocalendar(), "Update Checker Service"))
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
        log("\nError : " + str(result[1]))
        _continue = False
    if _continue:
        json = result[0]
        found = False
        app_list = find_apps()
        for x in range(0, len(app_list)):
            if json[app_list[x][0]][0] != app_list[x][2]:
                found = True
                log("\nFound Update for %s : New version : %s, old : %s" % (app_list[x][0], json[app_list[x][0]][0],
                                                                          app_list[x][2]))
        if found and show_msg:
            msg = QMessageBox(parent)
            msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
            msg.setWindowTitle("Updates Avaible !")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Updates were found ! Installing them now ...")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        if not found:
            log("\nNo Updates !")
            if show_msg:
                msg = QMessageBox(parent)
                msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
                msg.setWindowTitle("No Updates Avaible !")
                msg.setIcon(QMessageBox.Information)
                msg.setText("No Updates were found ! You are up-to-date !")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()


if __name__ == "__main__":
    perform()
