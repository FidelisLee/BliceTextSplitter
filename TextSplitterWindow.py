#----------------------------------------------
# ToolBox  v1.0.0
# from 2020.03.02 / Fidelis.lee
#-----------------------------------------------

import os, sys, chardet
from PyQt5.QtCore import pyqtSignal
from ToolBoxUi import *
from TextSpliter import TextSpliter
from FileRename import FileRename

class FileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args):
        QtWidgets.QFileDialog.__init__(self, *args)
        self.setOption(self.DontUseNativeDialog, True)
        self.setFileMode(self.ExistingFiles)
        btns = self.findChildren(QtWidgets.QPushButton)
        self.openBtn = [x for x in btns if 'open' in str(x.text()).lower()][0]
        self.openBtn.clicked.disconnect()
        self.openBtn.clicked.connect(self.openClicked)
        self.tree = self.findChild(QtWidgets.QTreeView)

    def openClicked(self):
        inds = self.tree.selectionModel().selectedIndexes()
        files = []
        for i in inds:
            if i.column() == 0:
                files.append(os.path.join(str(self.directory().absolutePath()),str(i.data().toString())))
        self.selectedFiles = files
        self.hide()

    def filesSelected(self):
        return self.selectedFiles

class MainApplication(QtWidgets.QMainWindow):
    threadFinished = pyqtSignal()
    threadCanceled = pyqtSignal()
    updateLog = pyqtSignal(str)
    updateRenameLog = pyqtSignal(str)

    def __init__(self):
        super(MainApplication, self).__init__(None)
        self.filePath = ""
        self.log = ""
        self.logRename = ""
        self.spliterThread = None
        self.renameThread = None
        self.delimeter = ""
        self.threadFinished.connect(self.endTask)
        self.threadCanceled.connect(self.cancelTask)
        self.updateLog.connect(self.updateLogMsg)
        self.updateRenameLog.connect(self.updateRenameLogMsg)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnOpen.clicked.connect(self.showFileOpen)
        self.ui.btnStart.clicked.connect(self.textSpliterStart)
        self.ui.btnStop.clicked.connect(self.textSpliterStop)
        self.ui.menuAbout.triggered.connect(self.showDialogAbout)
        self.ui.chkAutoRename.clicked.connect(self.toggleStartIndex)
        self.ui.chkChangeExt.clicked.connect(self.toggleChangeExt)
        self.ui.chkChangeDate.clicked.connect(self.toggleChangeDate)

        self.ui.btnRenOpen.clicked.connect(self.showFileOpen)
        self.ui.btnRenPreview.clicked.connect(self.previewFile)
        self.ui.btnRenStart.clicked.connect(self.renameRun)

    def showDialogAbout(self):
        AboutDialog().exec_()

    def toggleStartIndex(self):
        self.ui.startIndex.setDisabled(self.ui.chkAutoRename.isChecked())

    def textSpliterStart(self):
        self.delimeter = self.ui.delimeter.toPlainText().strip()
        if not self.delimeter:
            self.updateLogMsg("Input Delimeter, plz")
            return
        self.spliterThread = TextSpliter(self, self.filePath, self.delimeter, self.ui.startIndex.toPlainText(), self.ui.chkAutoRename.isChecked())
        self.spliterThread.start()
        self.ui.statusBar.showMessage("Processing...")

    def textSpliterStop(self):
        if self.spliterThread is not None:
            self.spliterThread.thread_stop()

    ####
    # for Rename funtions
    ####
    def toggleChangeExt(self):
        self.ui.extension.setEnabled(self.ui.chkChangeExt.isChecked())

    def toggleChangeDate(self):
        # self.ui.dateFormat.setEnabled(self.ui.chkChangeDate.isChecked())
        return

    def previewFile(self):
        self.renameThread = FileRename(self, self.oriFileLists,
                                       self.ui.prefixText.toPlainText().strip(),
                                       self.ui.suffixText.toPlainText().strip(),
                                       self.ui.extension.toPlainText().strip(),
                                       self.ui.chkChangeDate.isChecked())
        self.renameThread.start()
        self.ui.statusBar.showMessage("Processing...")

    def renameRun(self):
        if self.renameThread is not None:
            self.renameThread.runRename()

    def renameStop(self):
        if self.renameThread is not None:
            self.renameThread.thread_stop()

    # TODO:
    def showFileOpen(self):
        if(self.ui.tabWidget.currentIndex() == 0) :
            fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.getcwd(), "Text files (*.txt)")
            if len(fname[0]) == 0:
                return

            self.clearLogMsg()

            encodingTypes = set()
            with open(fname[0], 'rb') as ori_file:
                self.ui.textFile.setText(fname[0])

                for i in range(100):
                    rst = chardet.detect(ori_file.readline()).get("encoding")
                    encodingTypes.add(rst)

                self.filePath = fname[0]
                self.updateLogMsg("============================")
                self.updateLogMsg("File Info")
                self.updateLogMsg("- Path : " + self.filePath)
                self.updateLogMsg("- Lines : " + str(len(ori_file.readlines())))
                self.updateLogMsg("- Encoding types on Top 100 lines : " + str(encodingTypes))
                self.updateLogMsg("============================")
                ori_file.close()

                self.ui.btnStart.setDisabled(False)
                self.ui.btnStop.setDisabled(False)
                self.ui.delimeter.setDisabled(False)
                self.ui.chkAutoRename.setDisabled(False)
                self.ui.startIndex.setDisabled(False)
                self.ui.statusBar.showMessage("File Open Complete.")
            # else:
            #     self.ui.textLog.setText("Fine Open Failed\n")
        elif(self.ui.tabWidget.currentIndex() == 1) :
            fnames = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open File', os.getcwd())[0]
            if len(fnames) == 0:
                return

            self.clearRenameLogMsg()
            self.oriFileLists = fnames
            self.filePath = self.oriFileLists[0]
            self.ui.renameFilePath.setText(self.filePath)
            self.updateRenameLogMsg("============================")
            self.updateRenameLogMsg("File Info")
            self.updateRenameLogMsg("- Path : " + self.filePath + "\n- File Counts : " + str(len(self.oriFileLists)))
            self.updateRenameLogMsg("============================")

            self.ui.btnRenStart.setDisabled(False)
            self.ui.btnRenPreview.setDisabled(False)
            self.ui.prefixText.setDisabled(False)
            self.ui.suffixText.setDisabled(False)
            self.ui.chkChangeExt.setDisabled(False)
            self.ui.chkChangeDate.setDisabled(False)
            self.ui.statusBar.showMessage("File Open Complete.")

    def windowClose(self):
        if self.spliterThread is not None:
            self.textSpliterStop()
        if self.renameThread is not None:
            self.renameStop()
        sys.exit(app.exec_())

    def updateLogMsg(self, str):
        self.ui.textLog.append(str)

    def clearLogMsg(self):
        self.log = ""
        self.ui.textLog.setText(self.log)

    def updateRenameLogMsg(self, str):
        self.ui.renameLog.append(str)

    def clearRenameLogMsg(self):
        self.logRename = ""
        self.ui.renameLog.setText(self.logRename)

    def endTask(self):
        if(self.ui.tabWidget.currentIndex() == 0) :
            self.spliterThread = None
            self.ui.statusBar.showMessage("Done.")
        elif(self.ui.tabWidget.currentIndex() == 1) :
            self.ui.btnRenStart.setDisabled(False)

    def cancelTask(self):
        self.spliterThread = None
        self.updateLogMsg("====== Spliter Canceled ======")
        self.ui.statusBar.showMessage("Canceled.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("D:\\Python\\workspace_python\\ToolBox\\ui\\icon.ico"))
    mainWindow = MainApplication()
    mainWindow.show()
    sys.exit(app.exec_())

