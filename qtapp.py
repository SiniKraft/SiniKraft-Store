import json
import os
import subprocess
import sys
import threading
import winreg

from urllib.parse import urlparse

import win32gui
import win32ui

from PySide2.QtCore import Qt, QUrl, QSize, QBuffer, QIODevice
from PySide2.QtGui import QDesktopServices, QIcon, QImage, QPixmap
from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PySide2.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QAbstractItemView, QHeaderView, \
    QMessageBox, QDialog, QDialogButtonBox

from ui_sinikraft_launcher import Ui_MainWindow as Ui_MainWindow
from ui_settings_dialog import Ui_Dialog as Ui_SettingsDialog

from update_checker import perform, check_update_main


def get_targets(main_window: "MainWindow"):
    result = check_update_main()
    if result[1] is not None:
        for x in range(main_window.tableWidget.rowCount()):
            main_window.tableWidget.setItem(x, 4, QTableWidgetItem("Error"))
    else:
        json = result[0]
        for x in range(main_window.tableWidget.rowCount()):
            try:
                main_window.tableWidget.setItem(x, 4, QTableWidgetItem(json[main_window.tableWidget.item(x, 0).text()]
                                                                       [0]))
            except KeyError:
                main_window.tableWidget.setItem(x, 4, QTableWidgetItem("Unknown"))


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
                                                 get_value("UninstallString"), get_value("QuietUninstallString"),
                                                 (str(round(get_value("EstimatedSize") / 1024, 2)) + " Mo")
                                                 .replace(".", ",")))

                except (WindowsError, KeyError, ValueError):
                    continue

    return app_list


def find_domain(url: QUrl):
    url = url.url()
    return urlparse(url).netloc


class WebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url, _type, is_main_frame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            if not find_domain(url) == find_domain(self.url()):
                QDesktopServices.openUrl(url)
                return False
        return True


class HtmlView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        QWebEngineView.__init__(self, *args, **kwargs)
        self.setPage(WebEnginePage(self))

    def createWindow(self, _type):
        super(HtmlView, self).createWindow(_type)
        if _type == QWebEnginePage.WebBrowserTab:
            self.parent().webEngineView2 = HtmlView2()
            self.parent().webEngineView2.setObjectName(u"webEngineView2")
            self.parent().webEngineView2.setEnabled(True)
            self.parent().webEngineView2.setMinimumSize(QSize(0, 0))
            self.parent().webEngineView2.setMaximumSize(QSize(0, 0))
            return self.parent().webEngineView2


class HtmlView2(QWebEngineView):
    def __init__(self, *args, **kwargs):
        QWebEngineView.__init__(self, *args, **kwargs)
        self.urlChanged.connect(lambda: self.open_url)

    def open_url(self):
        QDesktopServices.openUrl(self.url())


def uninstall_app_from_gui(main_window: "MainWindow"):
    if main_window.currentlySelected is not None:
        try:
            subprocess.Popen(main_window.app_list[main_window.currentlySelected][4])
        except Exception as e:
            msg = QMessageBox(main_window)
            msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
            msg.setWindowTitle("Failed to Uninstall App !")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("An error occurred while uninstalling app : " + str(e))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.app_list = find_apps()
        self.setWindowTitle("SiniKraft STORE")
        self.setWindowIcon(QIcon(QPixmap(u":/images/SiniKraft-STORE-icon.png")))
        self.webEngineView = None
        self.webEngineView = HtmlView(self.groupBox_2)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setEnabled(True)
        self.webEngineView.setMinimumSize(QSize(0, 150))
        self.webEngineView.setMaximumSize(QSize(400, 16777215))
        self.webEngineView.setUrl(QUrl(u"https://sinikraft.github.io/website/fr/"))
        self.webEngineView.setZoomFactor(1.000000000000000)
        self.gridLayout.addWidget(self.webEngineView, 0, 0, 1, 1)
        self.currentlySelected = None
        self.t1 = threading.Thread(target=get_targets, args=(self,))
        self.t1.start()

        self.toolButton_2.clicked.connect(lambda: uninstall_app_from_gui(self))
        self.tableWidget.currentItemChanged.connect(self.update_selection)
        self.toolButton_5.clicked.connect(lambda: perform(self, True))
        self.toolButton_6.clicked.connect(lambda: SettingsDialog(self).exec_())

        self.tableWidget.setRowCount(len(self.app_list))
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        for apps in range(0, len(self.app_list)):
            icn = QIcon(QPixmap(u":/images/no_photo.png"))
            path = self.app_list[apps][1]
            if self.app_list[apps][0] == 'Discord Spammer':
                path = 'C:\\Windows\\System32\\msiexec.exe'
            if path != "":
                try:
                    icons = win32gui.ExtractIconEx(path, 0)
                    icon = icons[0][0]
                    width = height = 32

                    # Create DC and bitmap and make them compatible.
                    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
                    hbmp = win32ui.CreateBitmap()
                    hbmp.CreateCompatibleBitmap(hdc, width, height)
                    hdc = hdc.CreateCompatibleDC()
                    hdc.SelectObject(hbmp)

                    # Draw the icon.
                    win32gui.DrawIconEx(hdc.GetHandleOutput(), 0, 0, icon, width, height, 0, None, 0x0003)

                    # Get the icon's bits and convert to a QtGui.QImage.
                    bitmapbits = hbmp.GetBitmapBits(True)
                    image = QImage(bitmapbits, width, height, QImage.Format_ARGB32_Premultiplied)

                    # Write to and then load from a buffer to convert to PNG.
                    # This step is only necessary if you are displaying the image.
                    # QtWidgets.QLabel and similar have trouble displaying the current format.
                    buffer = QBuffer()
                    buffer.setOpenMode(QIODevice.ReadWrite)
                    image.save(buffer, "PNG")
                    image.loadFromData(buffer.data(), "PNG")

                    # Create a QtGui.QPixmap from the QtGui.QImage.
                    pixmap = QPixmap.fromImage(image)

                    # Destroy the icons.
                    for iconList in icons:
                        for icon in iconList:
                            win32gui.DestroyIcon(icon)
                    icn = QIcon(pixmap)
                except:
                    pass
            self.tableWidget.setVerticalHeaderItem(apps, QTableWidgetItem())
            self.tableWidget.setItem(apps, 0, QTableWidgetItem(icn, self.app_list[apps][0]))
            self.tableWidget.setItem(apps, 1, QTableWidgetItem(self.app_list[apps][2]))
            self.tableWidget.setItem(apps, 2, QTableWidgetItem(self.app_list[apps][3]))
            self.tableWidget.setItem(apps, 3, QTableWidgetItem(self.app_list[apps][6]))
            self.tableWidget.setItem(apps, 4, QTableWidgetItem("Checking ..."))

    def update_selection(self, __arg_1: QTableWidgetItem, __arg_2: QTableWidgetItem):
        self.currentlySelected = __arg_1.row()


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.setWindowTitle("Automatic Update Settings")
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore_defaults)
        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.save)
        self.load()

    def load(self):
        if not os.path.isfile("config.json"):
            self.save()
        try:
            with open("config.json", "r") as file:
                _dict = json.load(file)
                self.checkBox.setChecked(bool(_dict["automating"]["enable_automating"]))
                self.checkBox_2.setChecked(bool(_dict["automating"]["download_when_available"]))
                self.checkBox_3.setChecked(bool(_dict["automating"]["install_when_downloaded"]))
                self.checkBox_4.setChecked(bool(_dict["notifications"]["start_download"]))
                self.checkBox_5.setChecked(bool(_dict["notifications"]["finish_download"]))
                self.checkBox_6.setChecked(bool(_dict["notifications"]["start_install"]))
                self.checkBox_7.setChecked(bool(_dict["notifications"]["finish_install"]))
                self.comboBox.setCurrentIndex(int(_dict["frequency"]))
        except Exception as e:
            msg = QMessageBox(self)
            msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
            msg.setWindowTitle("Failed to load Settings !")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("An error occured while loading Settings : " + str(e))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def save(self):
        with open("config.json", "w") as file:
            _dict = {"notifications": {"start_download": self.checkBox_4.isChecked(),
                                       "finish_download": self.checkBox_5.isChecked(),
                                       "start_install": self.checkBox_6.isChecked(),
                                       "finish_install": self.checkBox_7.isChecked()},
                     "automating": {"enable_automating": self.checkBox.isChecked(),
                                    "download_when_available": self.checkBox_2.isChecked(),
                                    "install_when_downloaded": self.checkBox_3.isChecked()},
                     "frequency": self.comboBox.currentIndex()}
            json.dump(_dict, file, indent=4)

    def restore_defaults(self):
        self.checkBox_4.setChecked(True)
        self.checkBox_5.setChecked(True)
        self.checkBox_6.setChecked(True)
        self.checkBox_7.setChecked(True)
        self.checkBox_5.setDisabled(True)
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)
        self.checkBox_3.setChecked(True)
        self.comboBox.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
