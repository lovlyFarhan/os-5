from PySide import QtGui, QtCore
from real_machine import RealMachine
import sys

class RMWindow(QtGui.QMainWindow):
    def __init__(self):
        
        self.rm = RealMachine()
        self.row = 64 
        self.column = 16
        self.vm_window = None
        
        super(RMWindow, self).__init__()
        self.resize(1366,320)
        self.move(self.frameGeometry().topLeft())
        self.setWindowTitle(self.tr('Real Machine'))
        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setEnabled(True)
        self.setCentralWidget(self.centralWidget)
        #---------------------------------------------------------------------
        self.init_table(self.row)
        #---------------------------------------------------------------------
        self.pushButton = QtGui.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(800, 20, 97, 27))
        self.pushButton.setText("Load")
        self.pushButton.clicked.connect(self.run)
        
    def run(self):
        self.rm.start_vm('first.pr')
        self.fill_rm()
        if not self.vm_window:
            self.vm_window = VMWindow(self.rm.vm.memory)
        self.vm_window.show()
         
    def fill_rm(self):
        for i in range(self.row):
            for j in range(self.column):
                item = QtGui.QTableWidgetItem(str(self.rm.memory[16 * i + j]))
                self.tableWidget.setItem(i, j, item)
                
    def init_table(self, row):
        self.tableWidget = QtGui.QTableWidget(self.centralWidget)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 766, 297))
        self.tableWidget.setColumnCount(self.column)
        self.tableWidget.setRowCount(self.row)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        for i in range(row):
            item = QtGui.QTableWidgetItem(hex(i).upper()[2:])
            self.tableWidget.setVerticalHeaderItem(i, item)
            self.tableWidget.setHorizontalHeaderItem(i, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(45)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18)  
                
class VMWindow(QtGui.QFrame, RMWindow):
    def __init__(self, memory):
        self.row = self.column = 16
        self.memory = memory
        
        super(VMWindow, self).__init__()
        self.resize(1366,320)
        self.move(self.frameGeometry().bottomLeft())
        self.setWindowTitle(self.tr('Virtual Machine'))
        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setEnabled(True)
        self.init_table(self.row)
        
        self.fill_vm()
        
    def fill_vm(self):
        for i in range(self.row):
            for j in range(self.column):
                item = QtGui.QTableWidgetItem(str(self.memory[16 * i + j]))
                self.tableWidget.setItem(i, j, item)
        
myApp = QtGui.QApplication(sys.argv)
gui = RMWindow()
gui.show()
sys.exit(myApp.exec_())