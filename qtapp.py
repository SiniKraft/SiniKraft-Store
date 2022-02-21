import os
import sys
import winreg
from urllib.parse import urlparse

import win32gui
import win32ui
from PySide2 import QtGui
from PySide2.QtCore import Qt, QUrl, QSize, QBuffer, QIODevice
from PySide2.QtGui import QDesktopServices, QIcon, QImage, QPixmap
from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PySide2.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QAbstractItemView, QHeaderView

from ui_sinikraft_launcher import Ui_MainWindow


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
                                             str(round(get_value("EstimatedSize") / 1024, 2)) + " Mo"))

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
        print("URLChanged")
        QDesktopServices.openUrl(self.url())


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

        self.tableWidget.setRowCount(len(self.app_list))
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        for apps in range(0, len(self.app_list)):
            icn = QIcon(QPixmap(u":/images/no_photo.png"))
            if self.app_list[apps][1] != "":
                icons = win32gui.ExtractIconEx(self.app_list[apps][1], 0)
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
            self.tableWidget.setVerticalHeaderItem(apps, QTableWidgetItem())
            self.tableWidget.setItem(apps, 0, QTableWidgetItem(icn, self.app_list[apps][0]))
            self.tableWidget.setItem(apps, 1, QTableWidgetItem(self.app_list[apps][2]))
            self.tableWidget.setItem(apps, 2, QTableWidgetItem(self.app_list[apps][3]))
            self.tableWidget.setItem(apps, 3, QTableWidgetItem(self.app_list[apps][6]))
            self.tableWidget.setItem(apps, 4, QTableWidgetItem("Checking ..."))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
