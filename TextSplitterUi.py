#----------------------------------------------
# Blice Text Splitter v1.0.0
# from 2019.10.23 / Fidelis.lee
#-----------------------------------------------

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 520)
        MainWindow.setMinimumSize(QtCore.QSize(480, 520))
        MainWindow.setMaximumSize(QtCore.QSize(480, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.delimeter = QtWidgets.QTextEdit(self.centralwidget)
        self.delimeter.setEnabled(False)
        self.delimeter.setGeometry(QtCore.QRect(85, 43, 115, 25))
        self.delimeter.setObjectName("delimeter")
        self.textLog = QtWidgets.QTextBrowser(self.centralwidget)
        self.textLog.setGeometry(QtCore.QRect(10, 73, 455, 330))
        self.textLog.setObjectName("textLog")
        self.btnStop = QtWidgets.QPushButton(self.centralwidget)
        self.btnStop.setEnabled(False)
        self.btnStop.setGeometry(QtCore.QRect(320, 430, 120, 30))
        self.btnStop.setObjectName("btnStop")
        self.chkAutoRename = QtWidgets.QCheckBox(self.centralwidget)
        self.chkAutoRename.setEnabled(False)
        self.chkAutoRename.setGeometry(QtCore.QRect(350, 47, 115, 16))
        self.chkAutoRename.setObjectName("chkAutoRename")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(210, 50, 81, 12))
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(15, 17, 60, 16))
        self.label.setObjectName("label")
        self.startIndex = QtWidgets.QTextEdit(self.centralwidget)
        self.startIndex.setEnabled(False)
        self.startIndex.setGeometry(QtCore.QRect(300, 43, 30, 25))
        self.startIndex.setObjectName("startIndex")
        self.startIndex.setText("1")
        self.btnStart = QtWidgets.QPushButton(self.centralwidget)
        self.btnStart.setEnabled(False)
        self.btnStart.setGeometry(QtCore.QRect(180, 430, 120, 30))
        self.btnStart.setObjectName("btnStart")
        self.btnOpen = QtWidgets.QPushButton(self.centralwidget)
        self.btnOpen.setGeometry(QtCore.QRect(40, 430, 120, 30))
        self.btnOpen.setObjectName("btnOpen")
        self.textFile = QtWidgets.QTextBrowser(self.centralwidget)
        self.textFile.setGeometry(QtCore.QRect(85, 13, 382, 25))
        self.textFile.setObjectName("textFile")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 50, 12))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 480, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuAbout = QtWidgets.QAction(MainWindow)
        self.menuAbout.setObjectName("menuAbout")
        self.menuHelp.addAction(self.menuAbout)
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "블라이스 회차분할기"))
        self.btnStop.setText(_translate("MainWindow", "변환중지"))
        self.chkAutoRename.setText(_translate("MainWindow", "첫 줄 파일명으로"))
        self.label_4.setText(_translate("MainWindow", "회차시작번호 :"))
        self.label.setText(_translate("MainWindow", "대상 파일 :"))
        self.btnStart.setText(_translate("MainWindow", "변환시작"))
        self.btnOpen.setText(_translate("MainWindow", "파일열기"))
        self.label_2.setText(_translate("MainWindow", "구분자 :"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuAbout.setText(_translate("MainWindow", "About"))

class AboutDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("About")
        label1 = QtWidgets.QLabel(
            "Release v1.0.0\n"
            "   - 2021.2.15\n"
            "\n"
            "-----------------------------\n"
            "Contacts: Fidelis.Lee\n"
            "-----------------------------"
        )
        self.btnClose = QtWidgets.QPushButton("OK")
        self.btnClose.clicked.connect(self.dialogClose)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.btnClose, 1, 0)
        self.setLayout(layout)

    def dialogClose(self):
        self.close()