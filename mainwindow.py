# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1178, 667)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.JobPoolLabel = QtWidgets.QLabel(self.centralwidget)
        self.JobPoolLabel.setGeometry(QtCore.QRect(20, 20, 60, 16))
        self.JobPoolLabel.setObjectName("JobPoolLabel")
        self.JobPoolTable = QtWidgets.QTableWidget(self.centralwidget)
        self.JobPoolTable.setGeometry(QtCore.QRect(10, 40, 831, 181))
        self.JobPoolTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.JobPoolTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.JobPoolTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.JobPoolTable.setObjectName("JobPoolTable")
        self.JobPoolTable.setColumnCount(6)
        self.JobPoolTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.JobPoolTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.JobPoolTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.JobPoolTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.JobPoolTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.JobPoolTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.JobPoolTable.setHorizontalHeaderItem(5, item)
        self.JobPoolTable.horizontalHeader().setVisible(True)
        self.JobPoolTable.horizontalHeader().setHighlightSections(True)
        self.JobPoolTable.verticalHeader().setVisible(False)
        self.ReadyTable = QtWidgets.QTableWidget(self.centralwidget)
        self.ReadyTable.setGeometry(QtCore.QRect(10, 250, 831, 181))
        self.ReadyTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.ReadyTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ReadyTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ReadyTable.setObjectName("ReadyTable")
        self.ReadyTable.setColumnCount(8)
        self.ReadyTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.ReadyTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ReadyTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ReadyTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.ReadyTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.ReadyTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.ReadyTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.ReadyTable.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.ReadyTable.setHorizontalHeaderItem(7, item)
        self.ReadyTable.verticalHeader().setVisible(False)
        self.RunningLabel = QtWidgets.QLabel(self.centralwidget)
        self.RunningLabel.setGeometry(QtCore.QRect(20, 230, 60, 16))
        self.RunningLabel.setObjectName("RunningLabel")
        self.SuspendTable = QtWidgets.QTableWidget(self.centralwidget)
        self.SuspendTable.setGeometry(QtCore.QRect(10, 460, 831, 121))
        self.SuspendTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.SuspendTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.SuspendTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.SuspendTable.setObjectName("SuspendTable")
        self.SuspendTable.setColumnCount(8)
        self.SuspendTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.SuspendTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.SuspendTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.SuspendTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.SuspendTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.SuspendTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.SuspendTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.SuspendTable.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.SuspendTable.setHorizontalHeaderItem(7, item)
        self.SuspendTable.verticalHeader().setVisible(False)
        self.SuspendLabel = QtWidgets.QLabel(self.centralwidget)
        self.SuspendLabel.setGeometry(QtCore.QRect(20, 440, 141, 16))
        self.SuspendLabel.setObjectName("SuspendLabel")
        self.AddJobGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.AddJobGroupBox.setGeometry(QtCore.QRect(850, 10, 241, 161))
        self.AddJobGroupBox.setObjectName("AddJobGroupBox")
        self.AddJobButton = QtWidgets.QPushButton(self.AddJobGroupBox)
        self.AddJobButton.setGeometry(QtCore.QRect(120, 120, 113, 32))
        self.AddJobButton.setObjectName("AddJobButton")
        self.layoutWidget = QtWidgets.QWidget(self.AddJobGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 221, 23))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.AddJobNameLabel = QtWidgets.QLabel(self.layoutWidget)
        self.AddJobNameLabel.setObjectName("AddJobNameLabel")
        self.horizontalLayout_2.addWidget(self.AddJobNameLabel)
        self.AddJobNameEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.AddJobNameEdit.setObjectName("AddJobNameEdit")
        self.horizontalLayout_2.addWidget(self.AddJobNameEdit)
        self.layoutWidget1 = QtWidgets.QWidget(self.AddJobGroupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 60, 221, 23))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.AddJobPriorityLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.AddJobPriorityLabel.setObjectName("AddJobPriorityLabel")
        self.horizontalLayout_3.addWidget(self.AddJobPriorityLabel)
        self.AddJobPriorityEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.AddJobPriorityEdit.setObjectName("AddJobPriorityEdit")
        self.horizontalLayout_3.addWidget(self.AddJobPriorityEdit)
        self.layoutWidget2 = QtWidgets.QWidget(self.AddJobGroupBox)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 90, 221, 23))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.AddJobTimeLabel = QtWidgets.QLabel(self.layoutWidget2)
        self.AddJobTimeLabel.setObjectName("AddJobTimeLabel")
        self.horizontalLayout_4.addWidget(self.AddJobTimeLabel)
        self.AddJobTimeEdit = QtWidgets.QLineEdit(self.layoutWidget2)
        self.AddJobTimeEdit.setObjectName("AddJobTimeEdit")
        self.horizontalLayout_4.addWidget(self.AddJobTimeEdit)
        self.FinishedGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.FinishedGroupBox.setGeometry(QtCore.QRect(850, 180, 241, 441))
        self.FinishedGroupBox.setObjectName("FinishedGroupBox")
        self.TerminatedTable = QtWidgets.QTableWidget(self.FinishedGroupBox)
        self.TerminatedTable.setGeometry(QtCore.QRect(10, 30, 221, 401))
        self.TerminatedTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.TerminatedTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.TerminatedTable.setObjectName("TerminatedTable")
        self.TerminatedTable.setColumnCount(2)
        self.TerminatedTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.TerminatedTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TerminatedTable.setHorizontalHeaderItem(1, item)
        self.TerminatedTable.verticalHeader().setVisible(False)
        self.layoutWidget3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(480, 590, 361, 36))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.BottomLayout = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.BottomLayout.setContentsMargins(0, 0, 0, 0)
        self.BottomLayout.setObjectName("BottomLayout")
        self.PriorityRadio = QtWidgets.QRadioButton(self.layoutWidget3)
        self.PriorityRadio.setChecked(True)
        self.PriorityRadio.setObjectName("PriorityRadio")
        self.BottomLayout.addWidget(self.PriorityRadio)
        self.DaoshuLabel = QtWidgets.QLabel(self.layoutWidget3)
        self.DaoshuLabel.setObjectName("DaoshuLabel")
        self.BottomLayout.addWidget(self.DaoshuLabel)
        self.DaoshuBox = QtWidgets.QSpinBox(self.layoutWidget3)
        self.DaoshuBox.setMinimum(1)
        self.DaoshuBox.setMaximum(10)
        self.DaoshuBox.setObjectName("DaoshuBox")
        self.BottomLayout.addWidget(self.DaoshuBox)
        self.StartButton = QtWidgets.QPushButton(self.layoutWidget3)
        self.StartButton.setAutoDefault(False)
        self.StartButton.setDefault(True)
        self.StartButton.setObjectName("StartButton")
        self.BottomLayout.addWidget(self.StartButton)
        self.layoutWidget4 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget4.setGeometry(QtCore.QRect(650, 10, 191, 36))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.RandomCountBox = QtWidgets.QSpinBox(self.layoutWidget4)
        self.RandomCountBox.setMinimum(1)
        self.RandomCountBox.setMaximum(1000)
        self.RandomCountBox.setObjectName("RandomCountBox")
        self.horizontalLayout.addWidget(self.RandomCountBox)
        self.GenerateJobButton = QtWidgets.QPushButton(self.layoutWidget4)
        self.GenerateJobButton.setObjectName("GenerateJobButton")
        self.horizontalLayout.addWidget(self.GenerateJobButton)
        self.NowRunningLabel = QtWidgets.QLabel(self.centralwidget)
        self.NowRunningLabel.setGeometry(QtCore.QRect(10, 600, 141, 16))
        self.NowRunningLabel.setText("")
        self.NowRunningLabel.setObjectName("NowRunningLabel")
        self.rightBarWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.rightBarWidget.setGeometry(QtCore.QRect(1100, 10, 71, 611))
        self.rightBarWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rightBarWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rightBarWidget.setObjectName("rightBarWidget")
        self.rightBarWidget.setColumnCount(1)
        self.rightBarWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.rightBarWidget.setHorizontalHeaderItem(0, item)
        self.rightBarWidget.horizontalHeader().setVisible(False)
        self.rightBarWidget.verticalHeader().setVisible(False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1178, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "调度演示 by Frederic"))
        self.JobPoolLabel.setText(_translate("MainWindow", "Job Pool"))
        item = self.JobPoolTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "PID"))
        item = self.JobPoolTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "作业名称"))
        item = self.JobPoolTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "状态"))
        item = self.JobPoolTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "优先权"))
        item = self.JobPoolTable.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "要求运行时间"))
        item = self.JobPoolTable.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "所需内存"))
        item = self.ReadyTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "PID"))
        item = self.ReadyTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "作业名称"))
        item = self.ReadyTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "状态"))
        item = self.ReadyTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "优先权"))
        item = self.ReadyTable.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "要求运行时间"))
        item = self.ReadyTable.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "PCB指针"))
        item = self.ReadyTable.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "所需内存"))
        item = self.ReadyTable.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "内存首地址"))
        self.RunningLabel.setText(_translate("MainWindow", "Ready"))
        item = self.SuspendTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "PID"))
        item = self.SuspendTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "作业名称"))
        item = self.SuspendTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "状态"))
        item = self.SuspendTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "优先权"))
        item = self.SuspendTable.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "要求运行时间"))
        item = self.SuspendTable.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "PCB指针"))
        item = self.SuspendTable.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "所需内存"))
        item = self.SuspendTable.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "内存首地址"))
        self.SuspendLabel.setText(_translate("MainWindow", "Suspended"))
        self.AddJobGroupBox.setTitle(_translate("MainWindow", "添加任务"))
        self.AddJobButton.setText(_translate("MainWindow", "添加任务"))
        self.AddJobNameLabel.setText(_translate("MainWindow", "作业名称"))
        self.AddJobPriorityLabel.setText(_translate("MainWindow", "优先权值"))
        self.AddJobTimeLabel.setText(_translate("MainWindow", "运行时间"))
        self.FinishedGroupBox.setTitle(_translate("MainWindow", "已完成"))
        item = self.TerminatedTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "PID"))
        item = self.TerminatedTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "作业名称"))
        self.PriorityRadio.setText(_translate("MainWindow", "动态优先级+时间片调度"))
        self.DaoshuLabel.setText(_translate("MainWindow", "道数"))
        self.StartButton.setText(_translate("MainWindow", "开始运行"))
        self.GenerateJobButton.setText(_translate("MainWindow", "随机生成任务"))
        item = self.rightBarWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "column1"))

