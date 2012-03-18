from PySide import QtGui, QtCore
from real_machine import RealMachine
import sys

class RMWindow(QtGui.QMainWindow):
    def __init__(self):
        
        self.rm = RealMachine()
        self.row = self.rm.MAX_VMS * 16 
        self.column = 16
        self.vmWindow = None
        self.fileName = None
        
        super(RMWindow, self).__init__()
        self.setGeometry(0, 0, 1366, 320)
        self.move(self.frameGeometry().topLeft())
        self.setWindowTitle('Real Machine')
        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setEnabled(True)
        self.setCentralWidget(self.centralWidget)
        #---------------------------------------------------------------------
        self.init_table(self.row)
        #---------------------------------------------------------------------
        self.loadButton = QtGui.QPushButton(self.centralWidget)
        self.loadButton.setGeometry(QtCore.QRect(800, 20, 500, 300))
        self.loadButton.setText("Load")
        self.loadButton.clicked.connect(self.load_btn_handler)
        
    def load_btn_handler(self):
        self.show_file_dialog()
        self.rm.start_vm(self.fileName)
        self.fill_rm()
        if not self.vmWindow:
            self.vmWindow = VMWindow(self.rm, self)
        self.vmWindow.show()
         
    def fill_rm(self):
        for i in range(self.row):
            for j in range(self.column):
                item = QtGui.QTableWidgetItem(str(self.rm.memory[16 * i + j]))
                self.tableWidget.setItem(i, j, item)
                
    def init_table(self, row):
        self.tableWidget = QtGui.QTableWidget(self.centralWidget)
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
        #self.tableWidget.horizontalHeader().setStretchLastSection(False)
      
        
    def show_file_dialog(self):
        directory = QtCore.QDir.currentPath()
        fDialog = QtGui.QFileDialog()
        self.fileName, _ = fDialog.getOpenFileName(self, 'Open file', directory, "*.pr")
                
class VMWindow(QtGui.QFrame, RMWindow):
    def __init__(self, rm, primary_window):
        self.row = self.column = 16
        self.rm = rm
        self.screen = QtGui.QApplication.desktop()
        self.primary_window = primary_window
        self.center = 0x0004 
        
        
        super(VMWindow, self).__init__()
        self.setGeometry(0, self.primary_window.height() + 75, 1366, 320)
        
        self.setWindowTitle('Virtual Machine')
        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setEnabled(True)
        
        self.init_table(self.row)
        
        self.fill_vm()
        self.execCommands = QtGui.QPushButton(self.centralWidget)
        self.execCommands.setGeometry(QtCore.QRect(800, 20, 99, 80))
        self.execCommands.setText("Run")
        self.execCommands.clicked.connect(self.run_btn_handler)
        
        self.execCommand = QtGui.QPushButton(self.centralWidget)
        self.execCommand.setGeometry(QtCore.QRect(899, 20, 99, 80))
        self.execCommand.setText("Run by step")
        self.execCommand.clicked.connect(self.run_by_step_btn_handler)
        
        self.init_tree_widget()
        self.fill_tree_widget()
        
        
        self.input = QtGui.QLineEdit(self)
        self.input.move(1050, 20)
        self.input.setPlaceholderText('input')
        
        
        
    def fill_vm(self):
        for i in range(self.row):
            for j in range(self.column):
                item = QtGui.QTableWidgetItem(str(self.rm.memory[16 * i + j]))
                self.tableWidget.setItem(i, j, item)
                
    def init_tree_widget(self):
        self.treeWidget = QtGui.QTreeWidget(self.centralWidget)
        self.treeWidget.setGeometry(QtCore.QRect(800, 110, 198, 192))
        self.treeWidget.setFrameShape(QtGui.QFrame.WinPanel)
        self.treeWidget.setFrameShadow(QtGui.QFrame.Plain)
        #self.treeWidget.setRootIsDecorated(False)
        self.treeWidget.header().setDefaultSectionSize(97)
        self.treeWidget.header().setMinimumSectionSize(20)
        self.treeWidget.header().setStretchLastSection(False)
        self.treeWidget.setColumnCount(2)
        self.treeWidget.headerItem().setText(0, "REGISTER")
        self.treeWidget.headerItem().setTextAlignment(0, self.center)
        self.treeWidget.headerItem().setText(1, "VALUE")
        self.treeWidget.headerItem().setTextAlignment(1, self.center)
        for i in range(6):
            self.item = QtGui.QTreeWidgetItem(self.treeWidget)
            self.item.setTextAlignment(0, self.center)
            self.item.setTextAlignment(1, self.center) 
        self.select_cell(self.rm.vm.IP)
            
    def run_btn_handler(self):
        self.rm.vm.exec_commands()
        self.select_cell(self.rm.vm.IP)
        self.fill_tree_widget()
        self.fill_vm()
        
    def run_by_step_btn_handler(self):
        self.rm.vm.exec_command()
        self.select_cell(self.rm.vm.IP)
        self.fill_tree_widget()
        self.fill_vm()
        
        
    def fill_tree_widget(self):
        self.registers = ['DS', 'CS', 'SS', 'IP', 'SP', 'DR']
        self.reg_values = [self.rm.vm.DS, self.rm.vm.CS, self.rm.vm.SS, self.rm.vm.IP, self.rm.vm.SP, self.rm.vm.DR]
        for i in range(6):
            self.treeWidget.topLevelItem(i).setText(0, self.registers[i])
            if type(self.reg_values[i]) is str:
                self.treeWidget.topLevelItem(i).setText(1, self.reg_values[i])
            else:
                self.treeWidget.topLevelItem(i).setText(1, str(hex(self.reg_values[i])).upper()[2:])
        #self.treeWidget.topLevelItem(5).setText(0, self.registers[5])
        
            
    def select_cell(self, IP):
        self.IP = hex(IP)[2:]
        row = self.IP[:1]
        column = self.IP[-1:]
        self.tableWidget.setCurrentCell(int(row, 16), int(column, 16))
        
          
        
        
myApp = QtGui.QApplication(sys.argv)
gui = RMWindow()
gui.show()
sys.exit(myApp.exec_())