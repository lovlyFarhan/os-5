from PySide import QtGui, QtCore
from init import Init
from process import Process
from rm import RM
from vata_os import OS
from load import Load
from vm import VM
from output import Output


class Frame(QtGui.QFrame):
    
    def __init__(self, parent=None):
        super(Frame, self).__init__(parent)
        
#        self.setFrameStyle(QtGui.QFrame.StyledPanel)
#        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        QtGui.QApplication.setStyle("Windows")
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
        self.col = QtGui.QColor(159, 182, 205)
        
        mainGrid = QtGui.QGridLayout()
        mainGrid.addWidget(self.createLeftFrame(), 0, 0)
        mainGrid.addWidget(self.createRightFrame(), 0, 1)
        self.setLayout(mainGrid)
        
        self.fillProcessTree()
        
        self.move(self.frameGeometry().topLeft())
        self.setWindowTitle('VATA OS')
        self.show()
        
        
    def createLeftFrame(self):
        
        leftFrame = QtGui.QFrame()
        leftGrid = QtGui.QGridLayout()
        leftGrid.addWidget(self.createMemoryTable(), 0, 0)
        leftGrid.addWidget(self.createVMview(), 0, 1)
        leftFrame.setLayout(leftGrid)
        
        return leftFrame
    
    def createRightFrame(self):
        rightFrame = QtGui.QFrame()
        rightFrame.setStyleSheet("QWidget { background-color: %s }" % 
            self.col.name())
        
        rightGrid = QtGui.QGridLayout()
        rightGrid.addWidget(self.createProcessTree(), 0, 0, 1, 4) 
        rightGrid.addWidget(self.createInteruptBox(), 1, 0, 1, 2) 
        rightGrid.addWidget(self.createLoadBtn(), 1, 2) 
        rightGrid.addWidget(self.createCloseBtn(), 1, 3) 
        rightGrid.addWidget(self.createRunBtn(), 2, 0, 1, 2)
        rightGrid.addWidget(self.createRunCycleBtn(), 2, 2)
        rightGrid.addWidget(self.createRunAllBtn(), 2, 3)
        rightFrame.setLayout(rightGrid)
        rightFrame.setMaximumWidth(400)
        
        return rightFrame
    
    def createVMview(self):
        
        self.scrollBar = QtGui.QScrollBar()
        
        dialog = QtGui.QDialog()
        scrolllayout = QtGui.QVBoxLayout()

        scrollwidget = QtGui.QWidget()
        scrollwidget.setLayout(scrolllayout)

        scroll = QtGui.QScrollArea()
        scroll.setWidgetResizable(True)  
        scroll.setWidget(scrollwidget)
        
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        scroll.setVerticalScrollBar(self.scrollBar)
        

        self.groupboxesList = []  
        for i in range(16):    
            groupbox = QtGui.QGroupBox("VM #" + '%d' % i)
            groupbox.setMinimumHeight(395)
            grouplayout = QtGui.QVBoxLayout()
            grouplayout.addWidget(self.createRegisterTree())
            grouplayout.addWidget(self.createOutputBox())
            grouplayout.addWidget(self.createInputBox())
            groupbox.setLayout(grouplayout)
            scrolllayout.addWidget(groupbox)
            self.groupboxesList.append(groupbox)
        
        groupbox.setMaximumHeight(100)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(scroll)
        dialog.setLayout(layout)
        dialog.setMinimumWidth(250)
        dialog.setMaximumWidth(250)
        
        return dialog
    
    def createMemoryTable(self):
        
        self.arial_10 = QtGui.QFont()
        self.arial_10.setPointSize(9)
#        self.arial_10.setFamily("Arial")
        
        self.tableWidget = QtGui.QTableWidget()
        self.tableWidget.setFont(self.arial_10)
#        tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setMinimumWidth(647)
        self.tableWidget.setMaximumWidth(647)
        self.tableWidget.setColumnCount(16)
        self.tableWidget.setRowCount(256)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        list = []
        for i in range(256):
            list.append(str(hex(i)[2:]).upper())
        self.tableWidget.setHorizontalHeaderLabels(list)
        self.tableWidget.setVerticalHeaderLabels(list)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(40)
        self.tableWidget.verticalHeader().setDefaultSectionSize(18) 
        
        return self.tableWidget
    
    def createRegisterTree(self):
#        groupBox = QtGui.QGroupBox()
#        groupBox.setMaximumWidth(220)    
#        groupBox.setMaximumHeight(153)
        self.center = 0x0004
        registerTree = QtGui.QTreeWidget()
        registerTree.setMinimumWidth(172)
        registerTree.setMaximumWidth(172)
        registerTree.setMinimumHeight(120)
        registerTree.setMaximumHeight(120)
        
        registerTree.setRootIsDecorated(False)
        registerTree.header().setDefaultSectionSize(85)
        registerTree.header().setMinimumSectionSize(20)
        registerTree.header().setStretchLastSection(False)
        registerTree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        registerTree.setColumnCount(2)
        registerTree.headerItem().setText(0, "REGISTER")
        registerTree.headerItem().setTextAlignment(0, self.center)
        registerTree.headerItem().setText(1, "VALUE")
        registerTree.headerItem().setTextAlignment(1, self.center)
#        for i in range(6):
#            item = QtGui.QTreeWidgetItem(registerTree)
#            item.setTextAlignment(0, center)
#            item.setTextAlignment(1, center) 
#        select_cell(self.rm.vm.IP)
#        vbox = QtGui.QVBoxLayout()
#        vbox.addWidget(registerTree)
#        groupBox.setLayout(vbox)
        return registerTree
            
    def createOutputBox(self):
        groupBox = QtGui.QGroupBox("Output")
        groupBox.setMaximumWidth(169)    
        groupBox.setMaximumHeight(120)
        output = QtGui.QTextEdit(self)
#        output.setMaximumWidth(198)    
#        output.setMaximumHeight(100)
        output.setReadOnly(True)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(output)
        groupBox.setLayout(vbox)
        
        return groupBox
    
    def createInputBox(self):
        groupBox = QtGui.QGroupBox("Input")
        output = QtGui.QTextEdit(self)
#        output.setMaximumWidth(198)    
#        output.setMaximumHeight(50)
        output.setReadOnly(True)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(output)
        groupBox.setMaximumWidth(169)    
        groupBox.setMaximumHeight(70)
        groupBox.setLayout(vbox)
        
        return groupBox
    
    def createInteruptBox(self):
        
        SI = QtGui.QLabel('SI')
        PI = QtGui.QLabel('PI')
        TI = QtGui.QLabel('TI')
        
        groupBox = QtGui.QGroupBox("Interupt Registers")
        self.SIoutput = QtGui.QTextEdit(self)
        self.PIoutput = QtGui.QTextEdit(self)
        self.TIoutput = QtGui.QTextEdit(self)
        self.SIoutput.setReadOnly(True)
        self.PIoutput.setReadOnly(True)
        self.TIoutput.setReadOnly(True)
        grid = QtGui.QGridLayout()
        grid.addWidget(SI, 0, 0)
        grid.addWidget(self.SIoutput, 0, 1)
        grid.addWidget(PI, 0, 2)
        grid.addWidget(self.PIoutput, 0, 3)
        grid.addWidget(TI, 0, 4)
        grid.addWidget(self.TIoutput, 0, 5)
        groupBox.setMaximumWidth(198)    
        groupBox.setMaximumHeight(70)
        groupBox.setLayout(grid)
        return groupBox
    
    def updateInteruptBox(self):
        self.SIoutput.setText(str(RM.SI))
        self.PIoutput.setText(str(RM.PI))
        self.TIoutput.setText(str(RM.TI))
        
    def createProcessTree(self):
        groupBox = QtGui.QGroupBox("Processes")
#        groupBox.setMaximumWidth(220)    
        self.processTree = QtGui.QTreeWidget()
        self.processTree.setMinimumWidth(356)
        self.processTree.setMaximumWidth(356)
#        registerTree.setMinimumHeight(132)
        self.processTree.setRootIsDecorated(False)
        self.processTree.header().setDefaultSectionSize(89)
        self.processTree.header().setMinimumSectionSize(20)
        self.processTree.header().setStretchLastSection(False)
        self.processTree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.processTree.setColumnCount(4)
        self.processTree.headerItem().setText(0, "NAME")
        self.processTree.headerItem().setTextAlignment(0, self.center)
        self.processTree.headerItem().setText(1, "ID")
        self.processTree.headerItem().setTextAlignment(1, self.center)
        self.processTree.headerItem().setText(2, "STATE")
        self.processTree.headerItem().setTextAlignment(2, self.center)
        self.processTree.headerItem().setText(3, "PRIORITY")
        self.processTree.headerItem().setTextAlignment(3, self.center)
#        for i in range(6):
#            item = QtGui.QTreeWidgetItem(registerTree)
#            item.setTextAlignment(0, center)
#            item.setTextAlignment(1, center) 
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.processTree)
        groupBox.setLayout(vbox)
#        groupBox.setMaximumHeight(153)
        groupBox.setMaximumWidth(376)
        return groupBox
        
    def createLoadBtn(self):
        self.loadBtn = QtGui.QPushButton()
        self.loadBtn.setText("LOAD")
        self.loadBtn.setEnabled(False)
        self.loadBtn.clicked.connect(self.loadBtnHandler)
        return self.loadBtn
    
    def createCloseBtn(self):
        closeBtn = QtGui.QPushButton()
        closeBtn.setText("CLOSE")
        closeBtn.clicked.connect(self.closeBtnHandler)
        
        return closeBtn
    
    def createRunBtn(self):
        runBtn = QtGui.QPushButton()
        runBtn.setText("RUN")
        runBtn.clicked.connect(self.runBtnHandler)
        
        return runBtn
    
    def createRunCycleBtn(self):
        runCycleBtn = QtGui.QPushButton()
        runCycleBtn.setText("RUN CYCLE")
#        loadBtn.clicked.connect(self.run_btn_handler)
        
        return runCycleBtn
    
    def createRunAllBtn(self):
        runAllBtn = QtGui.QPushButton()
        runAllBtn.setText("RUN ALL")
#        loadBtn.clicked.connect(self.run_btn_handler)
        
        return runAllBtn
    
    def fillProcessTree(self):
        self.processTree.clear()
        processList = []
        processInfo = []
        
        for process in Process.list:
            if process.__class__.__name__ == "VM":
                processInfo = [process.__class__.__name__ + " #" + str(process.PAGE),
                               str(process.id), process.state, process.priority]
            else:    
                processInfo = [process.__class__.__name__, str(process.id), process.state, process.priority]
            processList.append(processInfo)
        
        for item in processList:
            items = QtGui.QTreeWidgetItem(self.processTree, item)
            for count in range(self.processTree.columnCount()):
                items.setTextAlignment(count, self.center)
        
        lp = OS.PP.last_proc
        if lp:
            self.processTree.setCurrentItem(self.processTree.topLevelItem(lp.id))
            
    def createFileDialog(self):
        directory = QtCore.QDir.currentPath() + "/jobs"
        fDialog = QtGui.QFileDialog()
        self.fileName, _ = fDialog.getOpenFileName(self, 'Open file', directory, "*.pr")
        Load.filename = self.fileName
        RM.PI = 5
    
      
    def runBtnHandler(self):
        self.loadBtn.setEnabled(True)
        OS.PP.run_once()
        self.fillProcessTree()
        self.updateInteruptBox()
        if OS.PP.last_proc.__class__.__name__ == "VM":
            self.moveSlider(OS.PP.last_proc)
            self.fillVMTree(OS.PP.last_proc)
            self.fillMemoryTable(OS.PP.last_proc.PAGE)
        if OS.PP.last_proc.__class__.__name__ == "Output":
                self.printOutput()
        
        
    def loadBtnHandler(self):
        self.createFileDialog()
        
    def closeBtnHandler(self):
        sys.exit()
        
    def fillMemoryTable(self, vm_page):
        pptr = vm_page * 256
        for i in range(16):
            for j in range(16):
                if str(RM.memory[pptr + i * 16 + j]) != '':
                    item = QtGui.QTableWidgetItem(str(RM.memory[pptr + i * 16 + j]))
                    item.setFont(self.arial_10)
                    self.tableWidget.setItem(vm_page * 16 + i, j, item)
                
    def fillVMTree(self, proc):
        
        registers = [["DS", str(hex(proc.DS)).upper()[2:]], ["CS", str(hex(proc.CS)).upper()[2:]],
                    ["SS", str(hex(proc.SS)).upper()[2:]],
                    ["IP", str(hex(proc.IP)).upper()[2:]], ["SP", str(hex(proc.SP)).upper()[2:]]]
        
        groupbox = self.groupboxesList[proc.PAGE]
        registerTree = groupbox.children()[1]
        registerTree.clear()
        
        for values in registers:
            items = QtGui.QTreeWidgetItem(registerTree, values)
            for count in range(registerTree.columnCount()):
                items.setTextAlignment(count, self.center)
                
    def printOutput(self):
        
        groupbox = self.groupboxesList[RM.current_vm.PAGE]
        outputbox = groupbox.children()[2].children()[1]
        outputbox.insertPlainText(Output.String)
        
    def moveSlider(self, proc):
        x = proc.PAGE
        self.scrollBar.setSliderPosition(402 * x)
        
if __name__ == '__main__':

    import sys

    myApp = QtGui.QApplication(sys.argv)
    gui = Frame()
    sys.exit(myApp.exec_())
    
