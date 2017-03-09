from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from penSettings import Pencil
'''
    Module for drawing/adding objects to the QGraphicsScene.
    The functions are called from the Canvas class.
'''

'''
   Function for drawing circles according to the given coordinates.
   startX    the left top corner coordinate for the circle, redefined when the mouse is clicked on the canvas
   startY    the top left y coordinate for the circle, - | | -
   x         the width of the circle, redefined when mouse is moved on the canvas
   y         the height of the circle, - | | -
   gui       the GUI object from graphicalUI
   s         boolean or string (after loading) that tells the function wheter the shape should be filled
'''
def drawCircles(startX, startY, x, y, gui, s):
    if(s == "True" or s == True):
        gui.scene.addEllipse(startX, startY, (x-startX), (y-startY), Pencil(gui), QBrush(gui.color))
    else:
        gui.scene.addEllipse(startX, startY, (x-startX), (y-startY), Pencil(gui), QBrush())

    if(len(gui.scene.items()) > gui.items):
        gui.scene.removeItem(gui.scene.items()[len(gui.scene.items())-gui.items])
    
'''
   Function for drawing rectangles according to the given coordinates.
   startX    the left top corner coordinate for the rectangle, redefined when the mouse is clicked on the canvas
   startY    the top left y coordinate for the rectangle, - | | -
   x         the width of the rectangle, redefined when mouse is moved on the canvas
   y         the height of the rectangle, - | | -
   gui       the GUI object from graphicalUI
   s         boolean or string (after loading) that tells the function wheter the shape should be filled
'''
def drawRectangles(startX, startY, x, y, gui, s):

    # For some reason the negative width and height cause problems with drawing rectangles
    if(x-startX >= 0 and y-startY >= 0):
        leftX = startX
        topY = startY
        w = x-startX
        h = y-startY
    elif(x-startX < 0 and y-startY < 0):
        leftX = x
        topY = y
        w = startX-x
        h = startY-y
    elif(y-startY < 0 and x-startX >=0):
        leftX = startX
        topY = y
        w = x-startX
        h = startY-y
    else:
        leftX = x
        topY = startY
        w = startX-x
        h = y-startY

    if(s == "True" or s == True):
        gui.scene.addRect(leftX, topY, w, h, Pencil(gui), QBrush(gui.color))
    else:
        gui.scene.addRect(leftX, topY, w, h, Pencil(gui), QBrush())

    
    if(len(gui.scene.items()) > gui.items):
        gui.scene.removeItem(gui.scene.items()[len(gui.scene.items())-gui.items])

'''
   Function for drawing lines
   startX    start x coordinate for the line
   startY    start y coordinate for the line
   x         end x for the line
   y         end y for the line
   gui       the GUI object from graphicalUI
'''
def drawLines(startX, startY, x, y, gui):

    gui.scene.addLine(startX, startY, x, y, Pencil(gui))

    if(len(gui.scene.items()) > gui.items):
        gui.scene.removeItem(gui.scene.items()[len(gui.scene.items())-gui.items])

'''
   Function for writing text
   sX    the left top x of the text's rectangle
   sY    the left top y of the text's rectangle
   text  text that will be added to the scene
   gui   the GUI object from graphicalUI
'''
def drawText(sX, sY, text, gui):
    if (gui.penWidth.currentText() != "PenWidth"):
        gui.texthere.setFont(QFont("Comic Sans MS", int(gui.penWidth.currentText()), QFont.Bold))
    gui.texthere.setDefaultTextColor(gui.color)
    gui.texthere.setPlainText(text)

    gui.scene.addItem(gui.texthere)
