# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './lib/devices/Scanner/DeviceTemplate.ui'
#
# Created: Fri Nov 25 10:03:53 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(587, 333)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.calibrationList = QtGui.QTreeWidget(self.layoutWidget)
        self.calibrationList.setRootIsDecorated(False)
        self.calibrationList.setItemsExpandable(False)
        self.calibrationList.setObjectName(_fromUtf8("calibrationList"))
        self.calibrationList.header().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.calibrationList)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.calibrateBtn = QtGui.QPushButton(self.layoutWidget)
        self.calibrateBtn.setObjectName(_fromUtf8("calibrateBtn"))
        self.horizontalLayout_2.addWidget(self.calibrateBtn)
        self.deleteBtn = QtGui.QPushButton(self.layoutWidget)
        self.deleteBtn.setObjectName(_fromUtf8("deleteBtn"))
        self.horizontalLayout_2.addWidget(self.deleteBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.groupBox = QtGui.QGroupBox(self.layoutWidget)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 5, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 4, 2, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 5, 2, 1, 1)
        self.yMaxSpin = QtGui.QDoubleSpinBox(self.groupBox)
        self.yMaxSpin.setMinimum(-10.0)
        self.yMaxSpin.setMaximum(10.0)
        self.yMaxSpin.setSingleStep(0.1)
        self.yMaxSpin.setProperty(_fromUtf8("value"), 2.0)
        self.yMaxSpin.setObjectName(_fromUtf8("yMaxSpin"))
        self.gridLayout_2.addWidget(self.yMaxSpin, 5, 3, 1, 1)
        self.scanDurationSpin = QtGui.QDoubleSpinBox(self.groupBox)
        self.scanDurationSpin.setMinimum(0.01)
        self.scanDurationSpin.setMaximum(100.0)
        self.scanDurationSpin.setProperty(_fromUtf8("value"), 5.0)
        self.scanDurationSpin.setObjectName(_fromUtf8("scanDurationSpin"))
        self.gridLayout_2.addWidget(self.scanDurationSpin, 2, 3, 1, 1)
        self.xMinSpin = QtGui.QDoubleSpinBox(self.groupBox)
        self.xMinSpin.setMinimum(-10.0)
        self.xMinSpin.setMaximum(10.0)
        self.xMinSpin.setSingleStep(0.1)
        self.xMinSpin.setProperty(_fromUtf8("value"), -2.0)
        self.xMinSpin.setObjectName(_fromUtf8("xMinSpin"))
        self.gridLayout_2.addWidget(self.xMinSpin, 4, 1, 1, 1)
        self.scanLabel = QtGui.QLabel(self.groupBox)
        self.scanLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.scanLabel.setObjectName(_fromUtf8("scanLabel"))
        self.gridLayout_2.addWidget(self.scanLabel, 2, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.cameraCombo = QtGui.QComboBox(self.groupBox)
        self.cameraCombo.setObjectName(_fromUtf8("cameraCombo"))
        self.gridLayout_2.addWidget(self.cameraCombo, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.laserCombo = QtGui.QComboBox(self.groupBox)
        self.laserCombo.setObjectName(_fromUtf8("laserCombo"))
        self.gridLayout_2.addWidget(self.laserCombo, 2, 1, 1, 1)
        self.storeCamConfBtn = QtGui.QPushButton(self.groupBox)
        self.storeCamConfBtn.setObjectName(_fromUtf8("storeCamConfBtn"))
        self.gridLayout_2.addWidget(self.storeCamConfBtn, 1, 2, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.gridLayout_2.addItem(spacerItem, 3, 1, 1, 1)
        self.yMinSpin = QtGui.QDoubleSpinBox(self.groupBox)
        self.yMinSpin.setMinimum(-10.0)
        self.yMinSpin.setMaximum(10.0)
        self.yMinSpin.setSingleStep(0.1)
        self.yMinSpin.setProperty(_fromUtf8("value"), -2.0)
        self.yMinSpin.setObjectName(_fromUtf8("yMinSpin"))
        self.gridLayout_2.addWidget(self.yMinSpin, 4, 3, 1, 1)
        self.xMaxSpin = QtGui.QDoubleSpinBox(self.groupBox)
        self.xMaxSpin.setMinimum(-10.0)
        self.xMaxSpin.setMaximum(10.0)
        self.xMaxSpin.setSingleStep(0.1)
        self.xMaxSpin.setProperty(_fromUtf8("value"), 2.0)
        self.xMaxSpin.setObjectName(_fromUtf8("xMaxSpin"))
        self.gridLayout_2.addWidget(self.xMaxSpin, 5, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.shutterGroup = QtGui.QGroupBox(self.layoutWidget)
        self.shutterGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.shutterGroup.setObjectName(_fromUtf8("shutterGroup"))
        self.gridLayout_4 = QtGui.QGridLayout(self.shutterGroup)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setHorizontalSpacing(5)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.shutterBtn = QtGui.QPushButton(self.shutterGroup)
        self.shutterBtn.setObjectName(_fromUtf8("shutterBtn"))
        self.gridLayout_4.addWidget(self.shutterBtn, 0, 5, 1, 1)
        self.label_7 = QtGui.QLabel(self.shutterGroup)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_4.addWidget(self.label_7, 0, 0, 1, 1)
        self.shutterXSpin = QtGui.QDoubleSpinBox(self.shutterGroup)
        self.shutterXSpin.setEnabled(False)
        self.shutterXSpin.setDecimals(3)
        self.shutterXSpin.setMinimum(-10.0)
        self.shutterXSpin.setMaximum(10.0)
        self.shutterXSpin.setObjectName(_fromUtf8("shutterXSpin"))
        self.gridLayout_4.addWidget(self.shutterXSpin, 0, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.shutterGroup)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_4.addWidget(self.label_8, 0, 2, 1, 1)
        self.shutterYSpin = QtGui.QDoubleSpinBox(self.shutterGroup)
        self.shutterYSpin.setEnabled(False)
        self.shutterYSpin.setDecimals(3)
        self.shutterYSpin.setMinimum(-10.0)
        self.shutterYSpin.setMaximum(10.0)
        self.shutterYSpin.setObjectName(_fromUtf8("shutterYSpin"))
        self.gridLayout_4.addWidget(self.shutterYSpin, 0, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 4, 1, 1)
        self.verticalLayout.addWidget(self.shutterGroup)
        self.view = ImageView(self.splitter)
        self.view.setObjectName(_fromUtf8("view"))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.calibrationList.headerItem().setText(0, QtGui.QApplication.translate("Form", "Camera", None, QtGui.QApplication.UnicodeUTF8))
        self.calibrationList.headerItem().setText(1, QtGui.QApplication.translate("Form", "Objective", None, QtGui.QApplication.UnicodeUTF8))
        self.calibrationList.headerItem().setText(2, QtGui.QApplication.translate("Form", "Laser", None, QtGui.QApplication.UnicodeUTF8))
        self.calibrationList.headerItem().setText(3, QtGui.QApplication.translate("Form", "Spot", None, QtGui.QApplication.UnicodeUTF8))
        self.calibrationList.headerItem().setText(4, QtGui.QApplication.translate("Form", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.calibrateBtn.setText(QtGui.QApplication.translate("Form", "Calibrate", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteBtn.setText(QtGui.QApplication.translate("Form", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "Calibration Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "X min", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "X max", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Y min", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Form", "Y max", None, QtGui.QApplication.UnicodeUTF8))
        self.yMaxSpin.setSuffix(QtGui.QApplication.translate("Form", " V", None, QtGui.QApplication.UnicodeUTF8))
        self.scanDurationSpin.setSuffix(QtGui.QApplication.translate("Form", " s", None, QtGui.QApplication.UnicodeUTF8))
        self.xMinSpin.setSuffix(QtGui.QApplication.translate("Form", " V", None, QtGui.QApplication.UnicodeUTF8))
        self.scanLabel.setText(QtGui.QApplication.translate("Form", "Scan duration:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Camera:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Laser:", None, QtGui.QApplication.UnicodeUTF8))
        self.storeCamConfBtn.setToolTip(QtGui.QApplication.translate("Form", "Remember the current camera configuration (including exposure time, ROI, etc) to use whenever calibrating against this camera.", None, QtGui.QApplication.UnicodeUTF8))
        self.storeCamConfBtn.setText(QtGui.QApplication.translate("Form", "Store Camera Config", None, QtGui.QApplication.UnicodeUTF8))
        self.yMinSpin.setSuffix(QtGui.QApplication.translate("Form", " V", None, QtGui.QApplication.UnicodeUTF8))
        self.xMaxSpin.setSuffix(QtGui.QApplication.translate("Form", " V", None, QtGui.QApplication.UnicodeUTF8))
        self.shutterGroup.setTitle(QtGui.QApplication.translate("Form", "Virtual Shutter", None, QtGui.QApplication.UnicodeUTF8))
        self.shutterBtn.setText(QtGui.QApplication.translate("Form", "Close Shutter", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Form", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Form", "Y", None, QtGui.QApplication.UnicodeUTF8))

from pyqtgraph.ImageView import ImageView
