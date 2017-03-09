from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import drawingMethods

'''
   Class for creating a QGraphicsView.  Here we detect any user input on the canvas etc.
   scene    the QGraphicsScene defined in graphicalUI, needed to create the view
   gui      the GUI object from graphicalUI
'''
class Canvas(QGraphicsView):
    def __init__(self, scene, gui):
        super().__init__(scene)
        self.GUI = gui
        
        self.objects = []
        self.penSet = []
        self.workLog = []
              
        __startX = 0
        __startY = 0
        __oX = 0
        __oY = 0
        self.draw = False
        self.move = False

        __item = ""

    '''
       Method for adding information about the objects added to the QGraphicsScene 'self.GUI.scene'
       obj    a lits of information, called from self.mouseReleaseEvent
       pen    the current pen settings for saving
       Adds information that is needed when saving pictures
    '''
    def addObject(self, obj, pen):
        self.objects.append(obj)
        self.penSet.append(pen)

    '''
       Method for deleting items from the two information lists
    '''
    def deleteObject(self):
        if (self.objects):
            self.objects.pop()
            self.penSet.pop()

    def getObjects(self):
        return self.objects

    def getPen(self):
        return self.penSet

    def getWorkLog(self):
        return self.workLog

    '''
       Adds the latest change into work log that is used when user clicks undo
       obj    consist of the name of the action (addition/movement) and coordinates if needed
    '''
    def addWork(self, obj):
        self.workLog.append(obj)

    '''
       Removes the lates action from the worklog. Is called when user want to undo
    '''
    def removeWork(self):
        self.workLog.pop()

    '''
       Creates the picture that has been saved earlier and is loaded by calling appropriate drawing functions.
       name    the name of the object type
       sX      top left x coorinate
       sY      top left y coordinate
       x       width/end coordinate
       y       height/end coordinate
       col     the color used when drawing the object
       solid   a string telling if the shape should be filled
    '''
    def createPic(self, name, sX, sY, x, y, col, solid):
        self.GUI.color.setNamedColor(col)
        self.GUI.square.setStyleSheet("QFrame {background-color: %s }" % self.GUI.color.name())
        if(name == "ellipse"):
            drawingMethods.drawCircles(int(sX), int(sY), int(x), int(y), self.GUI, solid)
        elif(name == "rect"):
            drawingMethods.drawRectangles(int(sX), int(sY), int(x), int(y), self.GUI, solid)
        elif(name == "line"):
            drawingMethods.drawLines(int(sX), int(sY), int(x), int(y), self.GUI)
        self.GUI.items += 1
        self.addWork("addition")
        self.addObject([sX, sY, x, y, col, solid],[str(self.GUI.combo.currentText()), str(self.GUI.penWidth.currentText())])

    '''
       Creates the text in earlier saved and 'now' loaded picture. Calls the drawText funtion from drawingMethods
       text    the text string
       sX      top left x coordinate
       sY      top left y
       col     the color with which the text was written
    '''
    def createText(self, text, sX, sY, col):
        self.GUI.color.setNamedColor(col)
        self.GUI.square.setStyleSheet("QFrame {background-color: %s }" % self.GUI.color.name())
        self.GUI.texthere.setPos(int(sX), int(sY))
        drawingMethods.drawText(int(sX), int(sY), text, self.GUI)
        
        self.GUI.items += 1
        self.addWork("addition")
        self.addObject([sX, sY, sX, sY, col, False],[str(self.GUI.combo.currentText()), str(self.GUI.penWidth.currentText())])

    '''
       Override for when mouse movement (with mouse pressed) is detected over the canvas
       event    the current event
       Calls drawing functions from drawingMethods when coordinates change the object's size must be updated
    '''
    def mouseMoveEvent(self, event):
        s = self.GUI.solid.isChecked()
        if(self.GUI.shape == "circle" and self.draw):
            drawingMethods.drawCircles(self.startX, self.startY, event.x(), event.y(), self.GUI, s)
        elif(self.GUI.shape == "square" and self.draw):
            drawingMethods.drawRectangles(self.startX, self.startY, event.x(), event.y(), self.GUI, s)
        elif(self.GUI.shape == "line" and self.draw):
            drawingMethods.drawLines(self.startX, self.startY, event.x(), event.y(), self.GUI)
        elif self.GUI.shape == "select" and self.move == True:
            try:
                self.item.setPos(float((self.oX-self.startX)+event.x()), float((self.oY-self.startY)+event.y()))
                
            except Exception as e:
                print(e)
    '''
       Override method for when mouse press is detected
    '''
    def mousePressEvent(self, event):
        self.startX = event.x()
        self.startY = event.y()
        self.GUI.teksti = ""
        
        if self.GUI.shape != "None" and self.GUI.shape != "select":
            # for text writing
            if self.GUI.shape == "text":
                self.GUI.texthere = QGraphicsTextItem()
                self.GUI.texthere.setPos(self.startX, self.startY)
                self.GUI.scene.addItem(self.GUI.texthere)
            self.draw = True
        # try to selct and move object crashes when only canvas has been clicked so it's in a try-except
        if self.GUI.shape == "select" and len(self.GUI.canvas.items()) > 0:
            self.draw = False
            try:
                self.oX = self.GUI.scene.itemAt(float(event.x()), float(event.y()), QTransform()).scenePos().x()
                self.oY = self.GUI.scene.itemAt(float(event.x()), float(event.y()), QTransform()).scenePos().y()
                self.item = self.GUI.scene.itemAt(float(event.x()), float(event.y()), QTransform())
                self.move = True
            except Exception as e:
                self.GUI.setInfoText("Nothing to move here :/")
            
    '''
       Override method for mouse releasing event
       Adds information about new objects to the information lists
       addObject takes a list of: [x1, y1, x2, y2, color, sloidOrNot], [pen style, pen width]
       add work takes ["addition"] or ["movement", (original position), (new position)]
    '''
    def mouseReleaseEvent(self, event):
        if self.draw:
            self.GUI.items += 1
            self.addWork("addition")
            self.addObject([str(self.startX), str(self.startY), str(event.x()), str(event.y()),
                        str(self.GUI.color.name()), str(self.GUI.solid.isChecked())],
                       [str(self.GUI.combo.currentText()), str(self.GUI.penWidth.currentText())])
        elif self.move:
            self.addWork(("movement", (self.oX, self.oY),
                          ((self.oX-self.startX)+event.x(), (self.oY-self.startY)+event.y())))
            lista = self.GUI.scene.items()
            lista.reverse()
            for i in range(len(lista)):
                if lista[i] == self.item:
                    self.objects[i][0] = str(int(float(self.objects[i][0])+(event.x()-self.startX)))
                    self.objects[i][1] = str(int(float(self.objects[i][1])+(event.y()-self.startY)))
                    self.objects[i][2] = str(int(float(self.objects[i][2])+(event.x()-self.startX)))
                    self.objects[i][3] = str(int(float(self.objects[i][3])+(event.y()-self.startY)))

        self.draw = False
        self.move = False

    '''
       Override mwthod for when key presses are detected.Turns the key presses into text to be added to the canvas
    '''
    def keyPressEvent(self, event):
        if self.GUI.shape == "text":
            if event.key() == QKeySequence("Backspace"):# would also work: 16777219
                self.GUI.teksti = self.GUI.teksti[:-1]
            else:
                self.GUI.teksti += event.text()
            
            drawingMethods.drawText(self.startX, self.startY, self.GUI.teksti, self.GUI)

    '''
       Override for when the mouse 'hovers' over the canvas
       Changes the cursor according to what the user has selected
    '''
    def enterEvent(self, event):
        if self.GUI.shape != "None" and self.GUI.shape != "select":
            QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        elif self.GUI.shape == "select":
            QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))
    '''
       Override for when the hoverin mouse leaves the canvas
       Changes the cursor back so the user won't be confused
    '''
    def leaveEvent(self, event):
        QApplication.restoreOverrideCursor()

