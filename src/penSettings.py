from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

'''
    Class for a new pencil that has its properties defined according to the user's choices
'''
class Pencil(QPen):
    def __init__(self, gui):
        super().__init__()
        self.GUI = gui
        self.setPenStyle(self.GUI)
        self.setPenWidth(self.GUI)
        self.setPenColor(self.GUI)
        self.setPenCap()
        
    '''
       Method for setting pen style
       gui    the GUI object from graphicalUI
       pen    the Qpen that has been created before calling this function
       The pen changes the pen's style according to what the user has chosen from the combobox 'combo'
    '''
    def setPenStyle(self, gui):
        if(str(gui.combo.currentText()) == "SolidLine"):
            self.setStyle(Qt.SolidLine)
        elif(str(gui.combo.currentText()) == "DashLine"):
            self.setStyle(Qt.DashLine)
        elif(str(gui.combo.currentText()) == "DotLine"):
            self.setStyle(Qt.DotLine)
        elif(str(gui.combo.currentText()) == "DashDotLine"):
            self.setStyle(Qt.DashDotLine)
        elif(str(gui.combo.currentText()) == "DashDotDotLine"):
            self.setStyle(Qt.DashDotDotLine)

    '''
       Function for setting the pen's width. Also used when writing text.
       gui    the GUI object from graphicalUI
       pen    the Qpen that has been created before calling this function
       Sets the width of the pen according to what the user has chosen from the combobox 'penWidth'
    '''
    def setPenWidth(self, gui):
        if(str(gui.penWidth.currentText()) != "PenWidth"):
            self.setWidth(int(gui.penWidth.currentText()))

    def setPenColor(self, gui):
        self.setBrush(gui.color)

    def setPenCap(self):
        self.setCapStyle(Qt.RoundCap)
