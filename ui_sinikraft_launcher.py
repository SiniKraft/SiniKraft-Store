# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sinikraft_launcherfQiUer.ui'
##
## Created by: Qt User Interface Compiler version 5.15.5
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from PySide2.QtWebEngineWidgets import QWebEngineView

import ui_sinikraft_launcher_rc  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(970, 823)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QGridLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableWidget = QTableWidget(self.groupBox)
        if (self.tableWidget.columnCount() < 5):
            self.tableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setAcceptDrops(True)
        self.tableWidget.setStyleSheet(u"")
        self.tableWidget.setFrameShape(QFrame.StyledPanel)
        self.tableWidget.setFrameShadow(QFrame.Sunken)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setProperty("showDropIndicator", True)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setIconSize(QSize(32, 32))
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setGridStyle(Qt.DashLine)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)

        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout_2.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(410, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.webEngineView = QWebEngineView(self.groupBox_2)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setEnabled(True)
        self.webEngineView.setMinimumSize(QSize(0, 150))
        self.webEngineView.setMaximumSize(QSize(400, 16777215))
        self.webEngineView.setUrl(QUrl(u"https://sinikraft.github.io/website/fr/"))
        self.webEngineView.setZoomFactor(1.000000000000000)

        self.gridLayout.addWidget(self.webEngineView, 0, 0, 1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout)

        self.horizontalLayout_2.addWidget(self.groupBox_2)

        self.horizontalLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMaximumSize(QSize(16777215, 130))
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.toolButton = QToolButton(self.groupBox_3)
        self.toolButton.setObjectName(u"toolButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
        self.toolButton.setSizePolicy(sizePolicy1)
        self.toolButton.setCursor(QCursor(Qt.ArrowCursor))
        self.toolButton.setFocusPolicy(Qt.StrongFocus)
        icon = QIcon()
        icon.addFile(u":/images/plus_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QSize(64, 64))
        self.toolButton.setCheckable(False)
        self.toolButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.horizontalLayout_5.addWidget(self.toolButton)

        self.horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.toolButton_2 = QToolButton(self.groupBox_3)
        self.toolButton_2.setObjectName(u"toolButton_2")
        sizePolicy1.setHeightForWidth(self.toolButton_2.sizePolicy().hasHeightForWidth())
        self.toolButton_2.setSizePolicy(sizePolicy1)
        self.toolButton_2.setFocusPolicy(Qt.StrongFocus)
        self.toolButton_2.setAutoFillBackground(False)
        icon1 = QIcon()
        icon1.addFile(u":/images/unins_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_2.setIcon(icon1)
        self.toolButton_2.setIconSize(QSize(64, 64))
        self.toolButton_2.setPopupMode(QToolButton.DelayedPopup)
        self.toolButton_2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.horizontalLayout_5.addWidget(self.toolButton_2)

        self.horizontalSpacer_2 = QSpacerItem(100, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.toolButton_3 = QToolButton(self.groupBox_3)
        self.toolButton_3.setObjectName(u"toolButton_3")
        sizePolicy1.setHeightForWidth(self.toolButton_3.sizePolicy().hasHeightForWidth())
        self.toolButton_3.setSizePolicy(sizePolicy1)
        icon2 = QIcon()
        icon2.addFile(u":/images/load_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_3.setIcon(icon2)
        self.toolButton_3.setIconSize(QSize(64, 64))
        self.toolButton_3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.horizontalLayout_5.addWidget(self.toolButton_3)

        self.horizontalSpacer_3 = QSpacerItem(100, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.toolButton_4 = QToolButton(self.groupBox_3)
        self.toolButton_4.setObjectName(u"toolButton_4")
        sizePolicy1.setHeightForWidth(self.toolButton_4.sizePolicy().hasHeightForWidth())
        self.toolButton_4.setSizePolicy(sizePolicy1)
        icon3 = QIcon()
        icon3.addFile(u":/images/save_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_4.setIcon(icon3)
        self.toolButton_4.setIconSize(QSize(64, 64))
        self.toolButton_4.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.horizontalLayout_5.addWidget(self.toolButton_4)

        self.horizontalSpacer_4 = QSpacerItem(100, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.toolButton_5 = QToolButton(self.groupBox_3)
        self.toolButton_5.setObjectName(u"toolButton_5")
        sizePolicy1.setHeightForWidth(self.toolButton_5.sizePolicy().hasHeightForWidth())
        self.toolButton_5.setSizePolicy(sizePolicy1)
        icon4 = QIcon()
        icon4.addFile(u":/images/update_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_5.setIcon(icon4)
        self.toolButton_5.setIconSize(QSize(64, 64))
        self.toolButton_5.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.horizontalLayout_5.addWidget(self.toolButton_5)

        self.horizontalSpacer_7 = QSpacerItem(100, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)

        self.toolButton_6 = QToolButton(self.groupBox_3)
        self.toolButton_6.setObjectName(u"toolButton_6")
        sizePolicy1.setHeightForWidth(self.toolButton_6.sizePolicy().hasHeightForWidth())
        self.toolButton_6.setSizePolicy(sizePolicy1)
        icon5 = QIcon()
        icon5.addFile(u":/images/settings_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_6.setIcon(icon5)
        self.toolButton_6.setIconSize(QSize(64, 64))
        self.toolButton_6.setPopupMode(QToolButton.DelayedPopup)
        self.toolButton_6.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolButton_6.setAutoRaise(False)
        self.toolButton_6.setArrowType(Qt.NoArrow)

        self.horizontalLayout_5.addWidget(self.toolButton_6)

        self.horizontalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3.addWidget(self.groupBox_3)

        self.horizontalLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(1117, 150))
        self.label.setPixmap(QPixmap(u":/images/SiniKraft-STORE-logo.png"))
        self.label.setScaledContents(True)

        self.horizontalLayout_6.addWidget(self.label)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)

        self.horizontalLayout.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 970, 21))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Installed Apps", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Version", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Installation Date", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Size", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Latest Version", None));
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"News", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Actions", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.toolButton_2.setText(QCoreApplication.translate("MainWindow", u"Uninstall", None))
        self.toolButton_3.setText(QCoreApplication.translate("MainWindow", u"Import Save Data", None))
        self.toolButton_4.setText(QCoreApplication.translate("MainWindow", u"Export Save Data", None))
        self.toolButton_5.setText(QCoreApplication.translate("MainWindow", u"Check For Updates", None))
        self.toolButton_6.setText(QCoreApplication.translate("MainWindow", u"Update Setings", None))
        self.label.setText("")
    # retranslateUi
