from PySide import QtGui, QtCore
from real_machine import RealMachine
import sys, os

class RMWindow(QtGui.QMainWindow):
    def __init__(self):
        super(RMWindow, self).__init__()
        
        self.rm = RealMachine()
        self.row = self.rm.MAX_VMS * 16 
        self.column = 16
        self.vmWindow = None
        self.fileName = None
        #self.window_list = []
        
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Windows'))
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
        
        self.setGeometry(0, 0, 870, 340)
        self.move(self.frameGeometry().topLeft())
        self.setWindowTitle('Real Machine')
        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setEnabled(True)
        self.setCentralWidget(self.centralWidget)
        
        #self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        
        #---------------------------------------------------------------------
        self.init_table(self.row)
        self.init_load_btn()
        self.init_reset_btn()
        #---------------------------------------------------------------------
        
    def load_btn_handler(self):
        self.show_file_dialog()
        if os.path.exists(self.fileName):
            self.rm.start_vm(self.fileName)
            self.fill_rm()
            #if not self.vmWindow:
            self.vmWindow = VMWindow(self)
            self.connect(self.vmWindow, QtCore.SIGNAL("vm_win_close( QWidget * )"), self.vm_close_sig_handler)
            self.vmWindow.show()
            #self.window_list.append(self.vmWindow)
    
    def reset_btn_handler(self):
        self.rm.clear_mem()
        self.fill_rm()
    
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
      
    def show_file_dialog(self):
        directory = QtCore.QDir.currentPath()
        fDialog = QtGui.QFileDialog()
        self.fileName, _ = fDialog.getOpenFileName(self, 'Open file', directory, "*.pr")
        
    def vm_close_sig_handler(self):
        self.rm.remove_vm()
        
    def init_load_btn(self):
        self.loadButton = QtGui.QPushButton(self.centralWidget)
        self.loadButton.setGeometry(QtCore.QRect(800, 20, 50, 25))
        self.loadButton.setText("Load")
        self.loadButton.clicked.connect(self.load_btn_handler)
        
    def init_reset_btn(self):
        self.resetButton = QtGui.QPushButton(self.centralWidget)
        self.resetButton.setGeometry(QtCore.QRect(800, 45, 50, 25))
        self.resetButton.setText("Reset")
        self.resetButton.clicked.connect(self.reset_btn_handler)
                
class VMWindow(QtGui.QFrame, RMWindow):
    def __init__(self, parent = None):
        super(VMWindow, self).__init__(parent)
        
        self.row = self.column = 16
        self.rm = parent.rm
        self.screen = QtGui.QApplication.desktop()
        self.parent = parent
        self.center = 0x0004
        
        self.setGeometry(0, self.parent.height()+200, 1020, 340)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle('Virtual Machine')
        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setEnabled(True)
        
        self.init_table(self.row)
        
        self.fill_vm()
        
        self.execCommands = QtGui.QPushButton(self.centralWidget)
        self.execCommands.setGeometry(QtCore.QRect(800, 20, 99, 40))
        self.execCommands.setText("Run")
        self.execCommands.clicked.connect(self.run_btn_handler)
        
        self.execCommand = QtGui.QPushButton(self.centralWidget)
        self.execCommand.setGeometry(QtCore.QRect(900, 20, 99, 40))
        self.execCommand.setText("Run by step")
        self.execCommand.clicked.connect(self.run_by_step_btn_handler)
        
        self.init_tree_widget()
        self.fill_tree_widget()
        
        self.output = QtGui.QLabel(self)
        self.output.setText("Output:")
        self.output.setGeometry(QtCore.QRect(800, 195, 100, 20))
        
        self.outputBox = QtGui.QTextEdit(self)
        self.outputBox.setGeometry(QtCore.QRect(800, 217, 198, 100))
        self.outputBox.setReadOnly(True)
        
    def fill_vm(self):
        for i in range(self.row):
            for j in range(self.column):
                item = QtGui.QTableWidgetItem(str(self.rm.memory[16 * i + j + self.rm.vm.PAGE]))
                self.tableWidget.setItem(i, j, item)
                
    def init_tree_widget(self):
        self.treeWidget = QtGui.QTreeWidget(self.centralWidget)
        self.treeWidget.setGeometry(QtCore.QRect(800, 62, 198, 132))
        #self.treeWidget.setFrameShape(QtGui.QFrame.WinPanel)
        #self.treeWidget.setFrameShadow(QtGui.QFrame.Plain)
        self.treeWidget.setRootIsDecorated(False)
        self.treeWidget.header().setDefaultSectionSize(99)
        self.treeWidget.header().setMinimumSectionSize(20)
        self.treeWidget.header().setStretchLastSection(False)
        self.treeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.treeWidget.setColumnCount(2)
        self.treeWidget.headerItem().setText(0, "REGISTER")
        self.treeWidget.headerItem().setTextAlignment(0, self.center)
        self.treeWidget.headerItem().setText(1, "VALUE")
        self.treeWidget.headerItem().setTextAlignment(1, self.center)
        for i in range(5):
            self.item = QtGui.QTreeWidgetItem(self.treeWidget)
            self.item.setTextAlignment(0, self.center)
            self.item.setTextAlignment(1, self.center) 
        self.select_cell(self.rm.vm.IP)
            
    def run_btn_handler(self):
        self.rm.vm.exec_commands(self.outputBox, self)
        self.select_cell(self.rm.vm.IP)
        self.fill_tree_widget()
        self.fill_vm()
        self.parent.fill_rm()
        
    def run_by_step_btn_handler(self):
        self.rm.vm.exec_command(self.outputBox, self)
        self.select_cell(self.rm.vm.IP)
        self.fill_tree_widget()
        self.fill_vm()
        self.parent.fill_rm()
        
    def fill_tree_widget(self):
        self.registers = ['DS', 'CS', 'SS', 'IP', 'SP']
        self.reg_values = [self.rm.vm.DS, self.rm.vm.CS, self.rm.vm.SS, self.rm.vm.IP, self.rm.vm.SP]
        for i in range(5):
            self.treeWidget.topLevelItem(i).setText(0, self.registers[i])
            self.treeWidget.topLevelItem(i).setText(1, str(hex(self.reg_values[i])).upper()[2:])
            
    def select_cell(self, IP):
        self.IP = hex(IP)[2:]
        row = self.IP[:1]
        column = self.IP[-1:]
        self.tableWidget.setCurrentCell(int(row, 16), int(column, 16))
    
    def read_msg_box(self):
        text, ok = QtGui.QInputDialog.getText(self, "Read", "Enter number or string:", QtGui.QLineEdit.Normal)
        if ok:
            self.rm.vm.SP += 1
            self.rm.vm.memory[self.rm.vm.SP] = text
            
    def closeEvent(self, evt):
        self.emit(QtCore.SIGNAL("vm_win_close( QWidget * )"), self)
        return super(VMWindow, self).closeEvent(evt)
        
        
        
myApp = QtGui.QApplication(sys.argv)
gui = RMWindow()
gui.show()
sys.exit(myApp.exec_())