import json
import os
import shutil
import subprocess
import sys
import threading
import datetime
import getpass
import urllib.request

from urllib.parse import urlparse

import win32gui
import win32ui
import win32security
import win32com.client

from PySide2.QtCore import Qt, QUrl, QSize, QBuffer, QIODevice, QTime
from PySide2.QtGui import QDesktopServices, QIcon, QImage, QPixmap
from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PySide2.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QAbstractItemView, QHeaderView, \
    QMessageBox, QDialog, QDialogButtonBox, QSystemTrayIcon, QFileDialog, QStyle

from ui_sinikraft_launcher import Ui_MainWindow as Ui_MainWindow
from ui_settings_dialog import Ui_Dialog as Ui_SettingsDialog
from ui_add_app_dialog import Ui_Dialog as Ui_AddAppDialog

from update_checker import run, check_update_main, find_apps, get_tasks
from constants import *


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


def find_domain(url: QUrl):
    url = url.url()
    return urlparse(url).netloc


def set_automation(num: int, hour: int, minute: int):
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    task_def = scheduler.NewTask(0)

    # Create trigger
    start_time = datetime.datetime.now()
    start_time = start_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
    start_time = start_time.isoformat()

    trigger = task_def.Triggers.Create(TASK_TRIGGER_DAILY)
    trigger.DaysInterval = 1  # 1 day per day
    trigger.StartBoundary = start_time
    trigger.Enabled = False

    trigger_2 = task_def.Triggers.Create(TASK_TRIGGER_WEEKLY)
    trigger_2.DaysOfWeek = DAY_MONDAY
    trigger_2.WeeksInterval = 1
    trigger_2.StartBoundary = start_time
    trigger_2.Enabled = False

    trigger_3 = task_def.Triggers.Create(TASK_TRIGGER_MONTHLY)
    trigger_3.DaysOfMonth = 1
    trigger_3.MonthsOfYear = ALL_MONTHS
    trigger_3.StartBoundary = start_time
    trigger_3.Enabled = False

    trigger_4 = task_def.Triggers.Create(TASK_TRIGGER_LOGON)
    trigger_4.Delay = "PT1M"  # 1 minute
    trigger_4.Enabled = False

    desc = win32security.GetFileSecurity(
        ".", win32security.OWNER_SECURITY_INFORMATION
    )
    sid = desc.GetSecurityDescriptorOwner()

    sid_str = win32security.ConvertSidToStringSid(sid)
    trigger_4.UserId = sid_str
    trigger_4.StartBoundary = start_time

    # Create action
    action = task_def.Actions.Create(TASK_ACTION_EXEC)
    action.ID = 'LAUNCH APP'
    action.Path = '"' + str(os.path.join(os.getcwd(), "Updater.exe")) + '"'
    action.Arguments = ''
    action.WorkingDirectory = str(os.getcwd())

    if num == 0:  # Check each day + on session login
        trigger.Enabled = True
        trigger_4.Enabled = True
    elif num == 1:  # Check each week + on session login
        trigger_2.Enabled = True
        trigger_4.Enabled = True
    elif num == 2:  # Check on session login
        trigger_4.Enabled = True
    elif num == 3:  # Check each day
        trigger.Enabled = True
    elif num == 4:  # Check each week
        trigger_2.Enabled = True
    elif num == 5:  # Check each month
        trigger_3.Enabled = True

    # Set parameters
    task_def.RegistrationInfo.Description = 'SiniKraft STORE Automatic Update Task. Disable it in Update Settings, in' \
                                            ' the Application !'
    task_def.RegistrationInfo.Author = getpass.getuser() + " | SiniKraft STORE"
    task_def.RegistrationInfo.Date = str(datetime.datetime.now().isoformat())
    task_def.RegistrationInfo.Source = "SiniKraft STORE"
    task_def.Settings.Enabled = True
    task_def.Settings.StopIfGoingOnBatteries = False
    task_def.Settings.RunOnlyIfNetworkAvailable = True
    task_def.Settings.DisallowStartIfOnBatteries = False
    task_def.Settings.StartWhenAvailable = True
    task_def.Settings.MultipleInstances = TASK_INSTANCES_IGNORE_NEW  # doesn't create if already running
    task_def.Principal.UserId = sid_str
    task_def.Principal.RunLevel = 0  # Low

    # Register task
    # If task already exists, it will be updated
    root_folder.RegisterTaskDefinition(
        'SiniKraft STORE Background Update Checking',  # Task name
        task_def,
        TASK_CREATE_OR_UPDATE,
        '',  # No user
        '',  # No password
        TASK_LOGON_NONE)


def find_current_task(__win):
    _msg = "Background Update is performing. If you don't see a SiniKraft STORE icon in the tray apps area (near Noti" \
           "fications) after you closed the SiniKraft STORE window, Click on Check for Updates on this window."
    msg2 = ""
    _tsk = get_tasks()
    if _tsk["current_task"] is not None:
        if _tsk["current_task"] == 1:
            msg2 = "Current task : Downloading"
        elif _tsk["current_task"] == 2:
            msg2 = "Current task : Uninstalling"
        elif _tsk["current_task"] == 3:
            msg2 = "Current task : Installing"
    msg = QMessageBox(__win)
    msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
    msg.setWindowTitle("An Update is running ...")
    msg.setIcon(QMessageBox.Information)
    msg.setText(_msg + "\n" + msg2)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


class WebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url, _type, is_main_frame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            if not find_domain(url) == find_domain(self.url()):
                if str(url.url())[-4:] == ".exe" or str(url.url())[-4:] == ".msi":
                    msgbox = QMessageBox(parent=self.parent())
                    msgbox.setIcon(QMessageBox.Question)
                    msgbox.setWindowTitle("SiniKraft STORE")
                    msgbox.setText("An app is about to be installed."
                                   "\nDo you want to let SiniKraft STORE install it,\n"
                                   "Or open the download in your browser ?")
                    msgbox.setStandardButtons(
                        QMessageBox.Cancel | QMessageBox.Yes | QMessageBox.Discard | QMessageBox.Ignore)
                    install_btn = msgbox.button(QMessageBox.Yes)
                    install_btn.setText("Install")
                    copy_btn = msgbox.button(QMessageBox.Ignore)
                    copy_btn.setText("Copy Link")
                    open_btn = msgbox.button(QMessageBox.Discard)
                    open_btn.setText("Open in browser")

                    msgbox.exec_()
                    if msgbox.clickedButton() == open_btn:
                        QDesktopServices.openUrl(url)
                    if msgbox.clickedButton() == copy_btn:
                        clipboard = QApplication.clipboard()
                        clipboard.setText(url.url())
                    if msgbox.clickedButton() == install_btn:
                        path_to_save = os.path.expandvars("%TEMP%") + "\\" + "tmp_installer" + url.url()[-4:]
                        a = QMessageBox.information(self.parent(), "SiniKraft STORE",
                                                    "The download will start after you press ok"
                                                    "\nThis can take a while, so please do not close the app"
                                                    "\nEven if it's not responding. When the download finish,\n"
                                                    "The installer will launch normally.", QMessageBox.Ok,
                                                    QMessageBox.Cancel)
                        if a == QMessageBox.Ok:
                            urllib.request.urlretrieve(url.url(), path_to_save)
                            if path_to_save[-4:] == ".msi":
                                path_to_save = "MsiExec.exe /I " + path_to_save
                            subprocess.Popen(path_to_save)
                else:
                    QDesktopServices.openUrl(url)
                return False
        return True


class HtmlView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        QWebEngineView.__init__(self, *args, **kwargs)
        self.setPage(WebEnginePage(self))

    def createWindow(self, _type):
        print(_type)
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
        self.urlChanged.connect(self.open_url)

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
        self.webEngineView.setUrl(QUrl(u"https://sinikraft.github.io/website/api/SiniKraft-STORE/news-channel/main_test"
                                       u".html"))
        self.webEngineView.setZoomFactor(1.0)
        self.gridLayout.addWidget(self.webEngineView, 0, 0, 1, 1)
        self.currentlySelected = None
        self.t1 = threading.Thread(target=get_targets, args=(self,))
        self.t1.start()

        self.toolButton_2.clicked.connect(lambda: uninstall_app_from_gui(self))
        self.tableWidget.currentItemChanged.connect(self.update_selection)
        self.toolButton_3.clicked.connect(lambda: self.handle_save_data(1))
        self.toolButton_4.clicked.connect(lambda: self.handle_save_data(0))
        self.toolButton_5.clicked.connect(self.check_update)
        self.toolButton_6.clicked.connect(lambda: SettingsDialog(self).exec_())
        self.toolButton.clicked.connect(self.open_app_dialog)

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
                    _icon = icons[0][0]
                    width = height = 32

                    # Create DC and bitmap and make them compatible.
                    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
                    hbmp = win32ui.CreateBitmap()
                    hbmp.CreateCompatibleBitmap(hdc, width, height)
                    hdc = hdc.CreateCompatibleDC()
                    hdc.SelectObject(hbmp)

                    # Draw the icon.
                    win32gui.DrawIconEx(hdc.GetHandleOutput(), 0, 0, _icon, width, height, 0, None, 0x0003)

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
                        for __icon in iconList:
                            win32gui.DestroyIcon(__icon)
                    icn = QIcon(pixmap)
                except:
                    pass
            self.tableWidget.setVerticalHeaderItem(apps, QTableWidgetItem())
            self.tableWidget.setItem(apps, 0, QTableWidgetItem(icn, self.app_list[apps][0]))
            self.tableWidget.setItem(apps, 1, QTableWidgetItem(self.app_list[apps][2]))
            self.tableWidget.setItem(apps, 2, QTableWidgetItem(self.app_list[apps][3]))
            self.tableWidget.setItem(apps, 3, QTableWidgetItem(self.app_list[apps][6]))
            self.tableWidget.setItem(apps, 4, QTableWidgetItem("Checking ..."))
        try:
            if not os.path.isfile("config.json"):
                SettingsDialog(self).exec_()
        except:
            pass

    def update_selection(self, __arg_1: QTableWidgetItem, __arg_2: QTableWidgetItem):
        self.currentlySelected = __arg_1.row()

    def check_update(self):
        if not os.path.isfile("Updater.exe"):
            p = threading.Thread(target=run, args=(self, True,))
            p.start()
            self.close()
            app.exit(0)
        else:
            subprocess.Popen(os.path.join(os.getcwd(), "Updater.exe") + " -launched-from-store")

    def show(self):
        super(MainWindow, self).show()
        if os.path.isfile("checking"):
            find_current_task(self)
            os.remove("checking")

    def handle_save_data(self, _type: int):
        # Type 0 : Export Save
        # Type 1 : Import Save
        game_title = self.app_list[self.currentlySelected][0]
        if game_title == "NoMoskito!" or game_title == "Gob Fish" or game_title == "Snake" or game_title == "GobFish":
            if self.app_list[self.currentlySelected][4][-23:] == "Uninstall\\unins000.exe\"":
                game_unins = self.app_list[self.currentlySelected][4][:-23][1:] + 'save.dat'
                if game_title == "Snake":
                    game_unins = self.app_list[self.currentlySelected][4][:-23][1:] + 'sauvegarde.dat'
            else:
                game_unins = self.app_list[self.currentlySelected][4][:-13][1:] + 'save\\save.dat'
            if _type == 0:
                state = "exported"
                dlg = QFileDialog.getSaveFileName(self, "Export Save data of %s" % game_title, "save.dat",
                                                  "%s Save data file (*.dat)" % game_title)[0]
                if dlg != "":
                    try:
                        shutil.copyfile(game_unins, dlg)
                    except Exception as e:
                        showerror("Failed to export data : " + str(e), self)
            else:
                state = "imported"
                dlg = QFileDialog.getOpenFileName(self, "Import Save data of %s" % game_title, "save.dat",
                                                  "%s Save data file (*.dat)" % game_title)[0]
                if dlg != "":
                    try:
                        shutil.copyfile(dlg, game_unins)
                    except Exception as e:
                        showerror("Failed to import data : " + str(e), self)
            if dlg != "":
                msg = QMessageBox(self)
                msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
                msg.setWindowTitle("Successfully %s Save Data !" % state)
                msg.setIcon(QMessageBox.Information)
                msg.setText("The save data of %s was successfully %s" % (game_title, state))
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
        else:
            msg = QMessageBox(self)
            msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
            msg.setWindowTitle("Invalid Title Selected !")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("The save data of this app can't be imported/exported !")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def open_app_dialog(self):
        dlg = AddAppDialog(self)
        dlg.exec_()


class AddAppDialog(QDialog, Ui_AddAppDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.setWindowTitle("Add Application")
        self.pushButton.setIcon(self.style().standardIcon(getattr(QStyle, "SP_CommandLink")))
        self.pushButton.setIconSize(QSize(32, 32))
        self.webEngineView = HtmlView(self.groupBox)
        self.webEngineView.setObjectName(u"webEngineView")
        self.gridLayout.addWidget(self.webEngineView, 1, 0, 1, 1)
        self.webEngineView.setUrl(QUrl("https://sinikraft.github.io/website/api/SiniKraft-STORE/add-app-dialog/list_mai"
                                       "n.html"))
        self.webEngineView.loadFinished.connect(self.on_loaded)

    def on_loaded(self):
        javascript_text = "var list = [];"
        for element in self.parent().app_list:
            javascript_text = javascript_text + '\nlist.push("%s");' % element[0]
        javascript_text = javascript_text.replace('GobFish', 'Gob Fish')  # fix name change
        javascript_text = javascript_text + "\nfor(var i = 0, size = list.length; i < size ; i++){\n    var item = li" \
                                            "st[i];\n    if (document.getElementById(item) != null) {\n        docume" \
                                            "nt.getElementById(item).firstElementChild.textContent = \"Installed\"\n " \
                                            "   }\n}"
        self.webEngineView.page().runJavaScript(javascript_text)


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
                time = QTime().currentTime()
                time.setHMS(int(_dict["time"]["hour"]), int(_dict["time"]["minute"]), 0, 0)
                self.timeEdit.setTime(time)
        except Exception as e:
            msg = QMessageBox(self)
            msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
            msg.setWindowTitle("Failed to load Settings !")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("An error occured while loading Settings : " + str(e))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def save(self):
        time = self.timeEdit.time()
        with open("config.json", "w") as file:
            _dict = {"notifications": {"start_download": self.checkBox_4.isChecked(),
                                       "finish_download": self.checkBox_5.isChecked(),
                                       "start_install": self.checkBox_6.isChecked(),
                                       "finish_install": self.checkBox_7.isChecked()},
                     "automating": {"enable_automating": self.checkBox.isChecked(),
                                    "download_when_available": self.checkBox_2.isChecked(),
                                    "install_when_downloaded": self.checkBox_3.isChecked()},
                     "frequency": self.comboBox.currentIndex(),
                     "time": {'hour': time.hour(), "minute": time.minute()}}
            json.dump(_dict, file, indent=4)
            set_automation(self.comboBox.currentIndex(), time.hour(), time.minute())

    def restore_defaults(self):
        time = QTime().currentTime()
        # time.setHMS(0, 0, 0, 0)
        self.timeEdit.setTime(time)
        self.checkBox_4.setChecked(True)
        self.checkBox_5.setChecked(True)
        self.checkBox_6.setChecked(True)
        self.checkBox_7.setChecked(True)
        self.checkBox_5.setDisabled(True)
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)
        self.checkBox_3.setChecked(True)
        self.comboBox.setCurrentIndex(0)


def showerror(_msg, _win=None, title="SiniKraft STORE - An error occurred"):
    msg = QMessageBox(win)
    msg.setWindowIcon(QIcon(QPixmap(":/images/SiniKraft-STORE-icon.png")))
    msg.setWindowTitle(title)
    msg.setIcon(QMessageBox.Critical)
    msg.setText(_msg)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


if __name__ == "__main__":
    args = sys.argv
    args.append("--enable-smooth-scrolling")
    app = QApplication(args)
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    win = MainWindow()
    icon = QIcon(":/images/SiniKraft-STORE-icon.png")
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    tray.setToolTip("SiniKraft STORE")
    win.show()
    sys.exit(app.exec_())
