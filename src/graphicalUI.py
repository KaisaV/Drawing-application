# -*- coding: utf-8 -*-
import Buttons
from canvas import Canvas

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class GUI(QWidget):
    lab = None
    def __init__(self):
        super().__init__()

        
        
        self.initUI()
        
        
    def initUI(self):
        self.teksti = ""
        # Create the QGraphicsScene and the Canvas objects
        self.scene = QGraphicsScene(0, 0, 900, 550, self)
        self.canvas = Canvas(self.scene, self)
        self.canvas.setMaximumSize(self.scene.width()+5, self.scene.height()+5)
        # no scroll bars because they break the coordinates
        self.canvas.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.canvas.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.canvas.show()

        # Variables that are needed when drawing
        self.shape = "None"
        self.items = 1
        self.color = QColor(0, 0, 0)
        
        # The info text on the bottom of the screen
        self.info = QLabel("Click on the buttons to choose what you want to draw! Ctrl+Z is undo and" +
                           " from Ctrl+S you can save. Find other shortcuts from the menubar (File, Edit).")
        
        
        ''' Items to the row above the canvas '''
        # Add buttons and their clicked-functions
        self.lab = QLabel("DRAW")
        self.circleBtn = QPushButton('circle', self)
        self.circleBtn.clicked.connect(self.buttonWrapper)
        self.squareBtn = QPushButton('square', self)
        self.squareBtn.clicked.connect(self.buttonWrapper)
        self.lineBtn = QPushButton('line', self)
        self.lineBtn.clicked.connect(self.buttonWrapper)
        self.textBtn = QPushButton('Text', self)
        self.textBtn.clicked.connect(self.buttonWrapper)
        
        # The rectangle for choosing color, located on the top right corner
        self.square = Colour(self)
        self.square.setStyleSheet("QWidget {background-color: %s }" % self.color.name())

        self.solid = QCheckBox("Draw solid shapes")

        # A combobox for choosing the line style of the pen
        self.combo = QComboBox()
        self.combo.setFont(QFont('Times New Roman', 10))
        self.combo.addItem("SolidLine")
        self.combo.addItem("DashLine")
        self.combo.addItem("DotLine")
        self.combo.addItem("DashDotLine")
        self.combo.addItem("DashDotDotLine")
        # A combobox for choosing the pen width
        self.penWidth = QComboBox()
        self.penWidth.addItem("PenWidth")
        for i in range(20):
            self.penWidth.addItem(str(i*3))        
        
        # Add all visible elements to the grid 
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.combo, 3, 7)
        grid.addWidget(self.penWidth, 3, 8)
        grid.addWidget(self.circleBtn, 3, 2)
        grid.addWidget(self.squareBtn, 3, 3)
        grid.addWidget(self.lineBtn, 3, 4)
        grid.addWidget(self.textBtn, 3, 5)
        grid.addWidget(self.solid, 3, 6)
        grid.addWidget(self.canvas, 4, 0, 10, 10)
        grid.addWidget(self.square, 3, 9)
        wid = QWidget()
        wid.setLayout(grid)

        ''' menuBar items '''
        # Create a menubar and actions for it
        menu = QMenuBar(self)
        # 'File' menu
        fileMenu = menu.addMenu('File')
        newAction = QAction('New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.triggered.connect(self.buttonWrapper)
        loadAction = QAction('Load', self)
        loadAction.setShortcut('Ctrl+L')
        loadAction.triggered.connect(self.buttonWrapper)
        saveAction = QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.buttonWrapper)
        exportAction = QAction('Export', self)
        exportAction.setShortcut('Ctrl+E')
        exportAction.triggered.connect(self.buttonWrapper)
        importAction = QAction('Import', self)
        importAction.setShortcut('Ctrl+I')
        importAction.triggered.connect(self.buttonWrapper)
        # Add actions to the menubar
        fileMenu.addAction(newAction)
        fileMenu.addAction(loadAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exportAction)
        fileMenu.addAction(importAction)

        # 'Edit' menu
        editMenu = menu.addMenu('Edit')
        undoAction = QAction('undo', self)
        undoAction.setShortcut('Ctrl+Z')
        undoAction.triggered.connect(self.buttonWrapper)
        scaleMenu = QMenu('scale', self)
        wAction = QAction('width', scaleMenu)
        wAction.triggered.connect(self.buttonWrapper)
        hAction = QAction('height', scaleMenu)
        hAction.triggered.connect(self.buttonWrapper)
        scaleMenu.addAction(wAction)
        scaleMenu.addAction(hAction)
        editMenu.addAction(undoAction)
        editMenu.addMenu(scaleMenu)
        selectA = QAction('Select', self)
        selectA.triggered.connect(self.buttonWrapper)
        editMenu.addAction(selectA)
        
        
        ''' Setting the layout '''
        splitter = QSplitter(Qt.Horizontal)
        splitter = QVBoxLayout(self)
        splitter.addWidget(wid)
        splitter.addWidget(self.info)
        self.setLayout(splitter)
        
        # set the main window
        self.setGeometry(300, 300, 1000, 650)
        self.setWindowTitle('Piirustusohjelma')    
        self.show()    


    '''
       Method for calling the Clicked method from Buttons.py.
       sends arguments self (the GUI object) and source (the source of the signal that called the method)
    '''
    def buttonWrapper(self):
        source = self.sender()
        Buttons.Clicked(self, source)


    '''
       A message box before closing the window
    ''' 
    def closeEvent(self, event):
        close = Buttons.checkForLoading(self, "Close program")
        if close :
            event.accept()
        else:
            event.ignore()


    def setInfoText(self, text):
        self.info.setText(text)
        

'''
   Class for the rectangle for color so it can be clickable
'''
class Colour(QFrame):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        
    def mousePressEvent(self, event):
        Buttons.Clicked(self.gui, QPushButton("Color"))

    def enterEvent(self, event):
        QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))

    def leaveEvent(self, event):
        QApplication.restoreOverrideCursor()
        
