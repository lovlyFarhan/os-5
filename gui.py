from PySide import QtGui, QtCore
from real_machine import RealMachine
import sys

class GUI(QtGui.QMainWindow):
    def __init__(self):
        self.rm = RealMachine()
        self.row = self.column = 15
        QtGui.QMainWindow.__init__(self)
        self.resize(1366,320)
        self.move(self.frameGeometry().topLeft())
        self.setWindowTitle(self.tr('Real Machine'))
        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setEnabled(True)
        #---------------------------------------------------------------------
        self.tableWidget = QtGui.QTableWidget(self.centralWidget)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 697, 297))
        self.tableWidget.setColumnCount(self.column)
        self.tableWidget.setRowCount(self.row)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setCentralWidget(self.centralWidget)
        for i in range(self.row):
            item = QtGui.QTableWidgetItem(hex(i).upper()[2:])
            self.tableWidget.setVerticalHeaderItem(i, item)
            self.tableWidget.setHorizontalHeaderItem(i, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(45)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18)
        #---------------------------------------------------------------------
        self.pushButton = QtGui.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(800, 20, 97, 27))
        self.pushButton.setText("Load")
        self.pushButton.clicked.connect(self.run)
    
    def vm_frame(self):
        window = QtGui.QMainWindow(self)
        window.setWindowTitle(self.tr('Virtual Machine'))
        window.resize(1366,320)
        window.show()
        window.move(self.frameGeometry().bottomLeft())
        #---------------------------------------------------------------------
        window.centralWidget = QtGui.QWidget(self)
        window.centralWidget.setEnabled(True)
        window.tableWidget = QtGui.QTableWidget(window.centralWidget)
        window.tableWidget.setEnabled(True)
        window.tableWidget.setGeometry(QtCore.QRect(20, 20, 697, 297))
        window.tableWidget.setColumnCount(self.column)
        window.tableWidget.setRowCount(self.row)
        window.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        window.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        window.setCentralWidget(window.centralWidget)
        for i in range(self.row):
            item = QtGui.QTableWidgetItem(hex(i).upper()[2:])
            window.tableWidget.setVerticalHeaderItem(i, item)
            window.tableWidget.setHorizontalHeaderItem(i, item)
        window.tableWidget.horizontalHeader().setDefaultSectionSize(45)
        window.tableWidget.verticalHeader().setDefaultSectionSize(18)
        #---------------------------------------------------------------------
    def run(self):
        self.rm.start_vm('first.pr')
        self.fill()
        self.vm_frame()  
    def fill(self):
        for i in range(self.row):
            for j in range(self.column):
                item1 = QtGui.QTableWidgetItem(str(self.rm.vm.memory[16 * i + j]))
                self.tableWidget.setItem(i, j, item1)
           
myApp = QtGui.QApplication(sys.argv)
window = GUI()
window.show()
sys.exit(myApp.exec_())