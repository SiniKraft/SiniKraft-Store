import json
import sys
import urllib.request
import os.path
import winreg

from PySide2.QtWidgets import QMessageBox, QDialog


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
    a = str()
    try:
        with urllib.request.urlopen("https://raw.githubusercontent.com/SiniKraft/SiniKraft-Store/master/update.json") \
                as url:
            a = json.loads(url.read().decode())
    except Exception as _e:
        e = _e
    return a, e


def perform():
    result = check_update_main()
    if result[1] is not None:
        msg = QMessageBox(QMessageBox.Critical)
        msg.setText("An error occured while checking for updates : " + str(result[1]))
        msg.exec_()
        sys.exit(1)
    json = result[0]
    app_list = find_apps()
    for x in range(0, len(app_list)):
        if json[app_list[x][0]][0] != app_list[x][2]:
            print(json[app_list[x][0]][0], app_list[x][2])


if __name__ == "__main__":
    perform()
