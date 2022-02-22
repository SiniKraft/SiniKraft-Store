# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerLYAiUo.ui'
##
## Created by: Qt User Interface Compiler version 5.15.5
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

import ui_sinikraft_launcher_rc  # type: ignore


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(566, 214)
        Dialog.setMaximumSize(QSize(566, 214))
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.gridLayout_5 = QGridLayout(Dialog)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(269, 139))
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBox_5 = QCheckBox(self.groupBox)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setEnabled(False)
        self.checkBox_5.setCheckable(True)
        self.checkBox_5.setChecked(True)

        self.gridLayout.addWidget(self.checkBox_5, 1, 0, 1, 1)

        self.checkBox_7 = QCheckBox(self.groupBox)
        self.checkBox_7.setObjectName(u"checkBox_7")
        self.checkBox_7.setChecked(True)

        self.gridLayout.addWidget(self.checkBox_7, 3, 0, 1, 1)

        self.checkBox_6 = QCheckBox(self.groupBox)
        self.checkBox_6.setObjectName(u"checkBox_6")
        self.checkBox_6.setChecked(True)

        self.gridLayout.addWidget(self.checkBox_6, 2, 0, 1, 1)

        self.checkBox_4 = QCheckBox(self.groupBox)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setChecked(True)

        self.gridLayout.addWidget(self.checkBox_4, 0, 0, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_4 = QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkBox = QCheckBox(self.groupBox_2)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setChecked(True)

        self.verticalLayout.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.groupBox_2)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setChecked(True)

        self.verticalLayout.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.groupBox_2)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setChecked(True)

        self.verticalLayout.addWidget(self.checkBox_3)

        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.gridLayout_3.addWidget(self.groupBox_2, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.comboBox = QComboBox(Dialog)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_3.addWidget(self.comboBox, 1, 1, 1, 1)

        self.gridLayout_5.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults | QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(False)

        self.gridLayout_5.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.checkBox_3.toggled.connect(self.checkBox_5.setDisabled)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Notifications", None))
        self.checkBox_5.setText(QCoreApplication.translate("Dialog", u"Notifies when download finished", None))
        self.checkBox_7.setText(QCoreApplication.translate("Dialog", u"Notifies when finished installing", None))
        self.checkBox_6.setText(QCoreApplication.translate("Dialog", u"Notifies when installing", None))
        self.checkBox_4.setText(QCoreApplication.translate("Dialog", u"Notifies when start downloading", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Automatisation", None))
        self.checkBox.setText(
            QCoreApplication.translate("Dialog", u"Enable Automatic Background Update Checking", None))
        self.checkBox_2.setText(QCoreApplication.translate("Dialog", u"Download Updates Once Avaible", None))
        self.checkBox_3.setText(QCoreApplication.translate("Dialog", u"Install Updates Once Downloaded", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Update check frequency", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"Check each day + on session login", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Check each hour + on session login", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"Check on session login", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Dialog", u"Check each day", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Dialog", u"Check each hour", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Dialog", u"Check each months", None))

    # retranslateUi
