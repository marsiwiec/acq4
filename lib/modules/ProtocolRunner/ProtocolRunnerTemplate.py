# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProtocolRunnerTemplate.ui'
#
# Created: Mon Aug 24 19:45:56 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1118, 593)
        MainWindow.setStyleSheet("""QDockWidget::title { background-color: #446;}
QSplitter::handle {background-color: #666}
QMainWindow::separator {background-color: #666}""")
        MainWindow.setDockNestingEnabled(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.LoaderDock = QtGui.QDockWidget(MainWindow)
        self.LoaderDock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable|QtGui.QDockWidget.DockWidgetVerticalTitleBar)
        self.LoaderDock.setObjectName("LoaderDock")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridlayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridlayout.setObjectName("gridlayout")
        self.newProtocolBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.newProtocolBtn.setObjectName("newProtocolBtn")
        self.gridlayout.addWidget(self.newProtocolBtn, 1, 1, 1, 1)
        self.loadProtocolBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.loadProtocolBtn.setObjectName("loadProtocolBtn")
        self.gridlayout.addWidget(self.loadProtocolBtn, 2, 1, 1, 1)
        self.saveProtocolBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.saveProtocolBtn.setEnabled(False)
        self.saveProtocolBtn.setObjectName("saveProtocolBtn")
        self.gridlayout.addWidget(self.saveProtocolBtn, 5, 1, 1, 1)
        self.saveAsProtocolBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.saveAsProtocolBtn.setEnabled(True)
        self.saveAsProtocolBtn.setObjectName("saveAsProtocolBtn")
        self.gridlayout.addWidget(self.saveAsProtocolBtn, 6, 1, 1, 1)
        self.deleteProtocolBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.deleteProtocolBtn.setEnabled(False)
        self.deleteProtocolBtn.setObjectName("deleteProtocolBtn")
        self.gridlayout.addWidget(self.deleteProtocolBtn, 8, 1, 1, 1)
        self.protocolList = QtGui.QTreeView(self.dockWidgetContents)
        self.protocolList.setAcceptDrops(True)
        self.protocolList.setEditTriggers(QtGui.QAbstractItemView.SelectedClicked)
        self.protocolList.setDragEnabled(True)
        self.protocolList.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.protocolList.setObjectName("protocolList")
        self.gridlayout.addWidget(self.protocolList, 2, 0, 8, 1)
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.currentProtocolLabel = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.currentProtocolLabel.sizePolicy().hasHeightForWidth())
        self.currentProtocolLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.currentProtocolLabel.setFont(font)
        self.currentProtocolLabel.setObjectName("currentProtocolLabel")
        self.horizontalLayout.addWidget(self.currentProtocolLabel)
        self.gridlayout.addLayout(self.horizontalLayout, 10, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 77, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 7, 1, 1, 1)
        self.LoaderDock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.LoaderDock)
        self.ProtocolDock = QtGui.QDockWidget(MainWindow)
        self.ProtocolDock.setEnabled(True)
        self.ProtocolDock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable|QtGui.QDockWidget.DockWidgetVerticalTitleBar)
        self.ProtocolDock.setObjectName("ProtocolDock")
        self.dockWidgetContents_5 = QtGui.QWidget()
        self.dockWidgetContents_5.setObjectName("dockWidgetContents_5")
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents_5)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.dockWidgetContents_5)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.protoContinuousCheck = QtGui.QCheckBox(self.dockWidgetContents_5)
        self.protoContinuousCheck.setEnabled(False)
        self.protoContinuousCheck.setObjectName("protoContinuousCheck")
        self.gridLayout.addWidget(self.protoContinuousCheck, 0, 1, 1, 2)
        self.deviceList = QtGui.QListWidget(self.dockWidgetContents_5)
        self.deviceList.setObjectName("deviceList")
        self.gridLayout.addWidget(self.deviceList, 1, 0, 5, 1)
        self.label_8 = QtGui.QLabel(self.dockWidgetContents_5)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 1, 1, 2)
        self.label_6 = QtGui.QLabel(self.dockWidgetContents_5)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 1, 1, 2)
        self.protoLoopCheck = QtGui.QCheckBox(self.dockWidgetContents_5)
        self.protoLoopCheck.setObjectName("protoLoopCheck")
        self.gridLayout.addWidget(self.protoLoopCheck, 3, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.dockWidgetContents_5)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 4, 1, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(20, 91, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 2, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.testSingleBtn = QtGui.QPushButton(self.dockWidgetContents_5)
        self.testSingleBtn.setEnabled(True)
        self.testSingleBtn.setObjectName("testSingleBtn")
        self.horizontalLayout_2.addWidget(self.testSingleBtn)
        spacerItem3 = QtGui.QSpacerItem(13, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.runProtocolBtn = QtGui.QPushButton(self.dockWidgetContents_5)
        self.runProtocolBtn.setEnabled(True)
        self.runProtocolBtn.setObjectName("runProtocolBtn")
        self.horizontalLayout_2.addWidget(self.runProtocolBtn)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.stopSingleBtn = QtGui.QPushButton(self.dockWidgetContents_5)
        self.stopSingleBtn.setObjectName("stopSingleBtn")
        self.horizontalLayout_2.addWidget(self.stopSingleBtn)
        self.gridLayout.addLayout(self.horizontalLayout_2, 6, 0, 1, 4)
        self.protoDurationSpin = QtGui.QSpinBox(self.dockWidgetContents_5)
        self.protoDurationSpin.setMaximum(10000000)
        self.protoDurationSpin.setSingleStep(10)
        self.protoDurationSpin.setProperty("value", QtCore.QVariant(100))
        self.protoDurationSpin.setObjectName("protoDurationSpin")
        self.gridLayout.addWidget(self.protoDurationSpin, 1, 3, 1, 1)
        self.protoLeadTimeSpin = QtGui.QSpinBox(self.dockWidgetContents_5)
        self.protoLeadTimeSpin.setMaximum(10000000)
        self.protoLeadTimeSpin.setSingleStep(10)
        self.protoLeadTimeSpin.setProperty("value", QtCore.QVariant(10))
        self.protoLeadTimeSpin.setObjectName("protoLeadTimeSpin")
        self.gridLayout.addWidget(self.protoLeadTimeSpin, 2, 3, 1, 1)
        self.protoCycleTimeSpin = QtGui.QSpinBox(self.dockWidgetContents_5)
        self.protoCycleTimeSpin.setMaximum(10000000)
        self.protoCycleTimeSpin.setSingleStep(10)
        self.protoCycleTimeSpin.setProperty("value", QtCore.QVariant(250))
        self.protoCycleTimeSpin.setObjectName("protoCycleTimeSpin")
        self.gridLayout.addWidget(self.protoCycleTimeSpin, 4, 3, 1, 1)
        self.ProtocolDock.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.ProtocolDock)
        self.SequenceDock = QtGui.QDockWidget(MainWindow)
        self.SequenceDock.setEnabled(True)
        self.SequenceDock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable|QtGui.QDockWidget.DockWidgetVerticalTitleBar)
        self.SequenceDock.setObjectName("SequenceDock")
        self.dockWidgetContents_7 = QtGui.QWidget()
        self.dockWidgetContents_7.setObjectName("dockWidgetContents_7")
        self.gridLayout_2 = QtGui.QGridLayout(self.dockWidgetContents_7)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_10 = QtGui.QLabel(self.dockWidgetContents_7)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_9 = QtGui.QLabel(self.dockWidgetContents_7)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.seqCycleTimeSpin = QtGui.QSpinBox(self.dockWidgetContents_7)
        self.seqCycleTimeSpin.setMaximum(10000000)
        self.seqCycleTimeSpin.setSingleStep(10)
        self.seqCycleTimeSpin.setProperty("value", QtCore.QVariant(250))
        self.seqCycleTimeSpin.setObjectName("seqCycleTimeSpin")
        self.verticalLayout.addWidget(self.seqCycleTimeSpin)
        self.label_11 = QtGui.QLabel(self.dockWidgetContents_7)
        self.label_11.setObjectName("label_11")
        self.verticalLayout.addWidget(self.label_11)
        self.seqRepetitionSpin = QtGui.QSpinBox(self.dockWidgetContents_7)
        self.seqRepetitionSpin.setMinimum(0)
        self.seqRepetitionSpin.setMaximum(1000000)
        self.seqRepetitionSpin.setObjectName("seqRepetitionSpin")
        self.verticalLayout.addWidget(self.seqRepetitionSpin)
        spacerItem5 = QtGui.QSpacerItem(17, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents_7)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.paramSpaceLabel = QtGui.QLabel(self.dockWidgetContents_7)
        self.paramSpaceLabel.setObjectName("paramSpaceLabel")
        self.verticalLayout.addWidget(self.paramSpaceLabel)
        self.label_4 = QtGui.QLabel(self.dockWidgetContents_7)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.seqTimeLabel = QtGui.QLabel(self.dockWidgetContents_7)
        self.seqTimeLabel.setObjectName("seqTimeLabel")
        self.verticalLayout.addWidget(self.seqTimeLabel)
        spacerItem6 = QtGui.QSpacerItem(13, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 1, 2, 1)
        self.sequenceParamList = ParamList(self.dockWidgetContents_7)
        self.sequenceParamList.setDragEnabled(True)
        self.sequenceParamList.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.sequenceParamList.setRootIsDecorated(True)
        self.sequenceParamList.setAnimated(True)
        self.sequenceParamList.setObjectName("sequenceParamList")
        self.gridLayout_2.addWidget(self.sequenceParamList, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.testSequenceBtn = QtGui.QPushButton(self.dockWidgetContents_7)
        self.testSequenceBtn.setObjectName("testSequenceBtn")
        self.horizontalLayout_3.addWidget(self.testSequenceBtn)
        spacerItem7 = QtGui.QSpacerItem(38, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.runSequenceBtn = QtGui.QPushButton(self.dockWidgetContents_7)
        self.runSequenceBtn.setObjectName("runSequenceBtn")
        self.horizontalLayout_3.addWidget(self.runSequenceBtn)
        spacerItem8 = QtGui.QSpacerItem(58, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.stopSequenceBtn = QtGui.QPushButton(self.dockWidgetContents_7)
        self.stopSequenceBtn.setObjectName("stopSequenceBtn")
        self.horizontalLayout_3.addWidget(self.stopSequenceBtn)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 2, 0, 1, 2)
        self.SequenceDock.setWidget(self.dockWidgetContents_7)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.SequenceDock)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Protocol Runner", None, QtGui.QApplication.UnicodeUTF8))
        self.LoaderDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Loader", None, QtGui.QApplication.UnicodeUTF8))
        self.newProtocolBtn.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.loadProtocolBtn.setText(QtGui.QApplication.translate("MainWindow", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.saveProtocolBtn.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.saveAsProtocolBtn.setText(QtGui.QApplication.translate("MainWindow", "Save As..", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteProtocolBtn.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Protocols", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Current Protocol:", None, QtGui.QApplication.UnicodeUTF8))
        self.ProtocolDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Protocol", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Devices", None, QtGui.QApplication.UnicodeUTF8))
        self.protoContinuousCheck.setToolTip(QtGui.QApplication.translate("MainWindow", "Protocol runs continuously without \n"
"gaps until stopped (not yet implemented).", None, QtGui.QApplication.UnicodeUTF8))
        self.protoContinuousCheck.setText(QtGui.QApplication.translate("MainWindow", "Continuous", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Duration (ms)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Lead Time (ms)", None, QtGui.QApplication.UnicodeUTF8))
        self.protoLoopCheck.setToolTip(QtGui.QApplication.translate("MainWindow", "Protocol will run repeatedly until stopped and \n"
"waits a minimum of Cycle Time between episodes.\n"
"Not the same as continuous acquisition (there \n"
"will be a time gap between each recording).", None, QtGui.QApplication.UnicodeUTF8))
        self.protoLoopCheck.setText(QtGui.QApplication.translate("MainWindow", "Loop", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Cycle Time (ms)", None, QtGui.QApplication.UnicodeUTF8))
        self.testSingleBtn.setText(QtGui.QApplication.translate("MainWindow", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.runProtocolBtn.setText(QtGui.QApplication.translate("MainWindow", "Record Single", None, QtGui.QApplication.UnicodeUTF8))
        self.stopSingleBtn.setText(QtGui.QApplication.translate("MainWindow", "Stop Single", None, QtGui.QApplication.UnicodeUTF8))
        self.protoDurationSpin.setToolTip(QtGui.QApplication.translate("MainWindow", "Duration of stimulus/acquisition in the protocol.", None, QtGui.QApplication.UnicodeUTF8))
        self.protoLeadTimeSpin.setToolTip(QtGui.QApplication.translate("MainWindow", "Duration of time to wait before acquisition starts \n"
"(the hardware is reserved so nothing else can \n"
"run during this time).", None, QtGui.QApplication.UnicodeUTF8))
        self.protoCycleTimeSpin.setToolTip(QtGui.QApplication.translate("MainWindow", "The minimum time to wait between recordings \n"
"in loop mode.", None, QtGui.QApplication.UnicodeUTF8))
        self.SequenceDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Sequence", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "Sequence Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Cycle Time (ms)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Repetitions", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Parameter Space: ", None, QtGui.QApplication.UnicodeUTF8))
        self.paramSpaceLabel.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Total time:", None, QtGui.QApplication.UnicodeUTF8))
        self.seqTimeLabel.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.sequenceParamList.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "dev", None, QtGui.QApplication.UnicodeUTF8))
        self.sequenceParamList.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "param", None, QtGui.QApplication.UnicodeUTF8))
        self.sequenceParamList.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "len", None, QtGui.QApplication.UnicodeUTF8))
        self.testSequenceBtn.setText(QtGui.QApplication.translate("MainWindow", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.runSequenceBtn.setText(QtGui.QApplication.translate("MainWindow", "Record Sequence", None, QtGui.QApplication.UnicodeUTF8))
        self.stopSequenceBtn.setText(QtGui.QApplication.translate("MainWindow", "Stop Sequence", None, QtGui.QApplication.UnicodeUTF8))

from ParamList import ParamList
