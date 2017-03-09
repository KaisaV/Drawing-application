from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

'''
   Function for defining which button was clicked in the GUI
   gui    the GUI object
   btn    the signal sender (the name of the button clicked in this case)
   Changes the gui.shape and/or calls a function according to the button clicked.
   Handles also saving, loading, clearing the scene/canvas.
'''
def Clicked(gui, btn):
    btnName = btn.text()
    
    if (btnName == "circle"):
        gui.shape = "circle"
        gui.setInfoText("Draw a circle by dragging the cursor on the canvas (white box). You can change the"
                        " color by clicking the color on the top right corner.")
        
    elif (btnName == "square"):
        gui.shape = "square"
        gui.setInfoText("Draw a rectangle by dragging the cursor along the canvas (white box). You can fill the"+
                        " shape by ticking the solid box.")
        
    elif (btnName == "line"):
        gui.shape = "line"
        gui.setInfoText("Draw a line by dragging the cursor along the canvas (white box). You can change the"+
                        " linestyle by selecting from the 'LineStyle'.")
        
    elif (btnName == "undo"): 
        if undo(gui):
            gui.setInfoText("The change is now undone.")
            if gui.shape == "text":
                gui.shape = "None"
        else:
            gui.setInfoText("Nothing to undo.")
        
    elif (btnName == "New"):
        if checkForLoading(gui, "New picture"):
            gui.scene.setSceneRect(QRectF(0, 0, 900.0, 550.0))
            gui.canvas.setMaximumSize(gui.scene.width()+5, gui.scene.height()+5)
            gui.setInfoText("Click on the buttons to choose what you want to draw!")
        
    elif (btnName == "Save"):
        if saveCurrentScene(gui):
            gui.setInfoText("Picture succesfully saved!")
        else:
            gui.setInfo("An error occured in saving the file.")

    elif(btnName == "Export"):
        if exportPicture(gui):
            gui.setInfoText("Your picture has been succesfully exported as 'kuva.png'. Please re(locate/name)"+
                            " it before exporting a new picture.")      

    elif(btnName == "Import"):
        if importPicture(gui):
            gui.setInfoText("The picture you chose has been imported!")
        
    elif(btnName == "Color"):
        try:
            co = QColorDialog().getColor()
            if co.isValid():
                gui.color.setNamedColor(co.name())
        except Exception as e:
            print(e)
        gui.square.setStyleSheet("QFrame {background-color: %s }" % gui.color.name())

    elif(btnName == "Text"):
        gui.shape = "text"
        gui.setInfoText("Click the position on the canvas where you want the text and start typing!"+
                        " You can change the font size from the 'PenWidth'.")

    elif btnName == "Select":
        gui.shape = "select"
        gui.setInfoText("You can move the obects by dragging them around.")

    elif btnName == "height":
        if not setScale(gui, btnName):
            gui.setInfoText("You wrote something that was not a number.")

    elif btnName == "width":
        if not setScale(gui, btnName):
            gui.setInfoText("You wrote something that was not a number.")
                
            

    elif(btnName == "Load"):
        loadPicture(gui)
        
'''
   Function for checking if anything in the scene needs saving before opening a new picture.
   Does not check if the contents of the scene are already saved.
   gui    The GUI passed from the graphicalUI
   Returns True if can proceed to loading, False if the action (here loading) is cancelled.
'''
def checkForLoading(gui, text):
    if(len(gui.scene.items()) > 0):
        reply = QMessageBox.warning(gui, text, "You will lose all unsaved data if you proceed!", QMessageBox.Save | QMessageBox.Ok | QMessageBox.Cancel , QMessageBox.Save)
        if (reply == QMessageBox.Ok):
            gui.scene.clear()
            gui.items = 1
            return True
        elif (reply == QMessageBox.Save):
            if saveCurrentScene(gui):
                gui.scene.clear()
                gui.items = 1
                return True

        return False
    return True

'''
   Function for saving the contents of the QGraphicsScene into a textfile.
   gui    The GUI passed from the graphicalUI
'''
def saveCurrentScene(gui):
    for item in gui.scene.items():
        if str(item)[26:27] == "P":
            QMessageBox.information(gui, "You have imported content",
                                                "You can't save pictures with imported content into .kbv files. If you wish to export the picture as a .png file, you can use the export option (Ctrl+E).",
                                                QMessageBox.Ok,QMessageBox.Ok)
            return False

        
    name = QFileDialog.getSaveFileName(gui, 'Save file')

    if(name[0] != ''):
        if name[0][-4:] == ".kbv":
            f = open(name[0], 'w')
        else:
            f = open(name[0] + ".kbv", 'w')
        size = str(gui.scene.width()) + "," + str(gui.scene.height()) + ";"

        f.write(size)
        text = []
        items = gui.scene.items()
        objects = gui.canvas.getObjects()
        penSet = gui.canvas.getPen()
        objects.reverse()
        penSet.reverse()
        skipped = 0

        for i in range(len(items)):
            lista = ""
            for t in range(6):
                lista += str(objects[i][t]) + ","
            for s in range(2):
                lista += str(penSet[i][s]) + ","    
            if(str(items[i])[26:27] == "L"):
                text.append("line,")
            elif(str(items[i])[26:27] == "R"):
                text.append("rect,")
            elif(str(items[i])[26:27] == "E"):
                text.append("ellipse,")
            elif(str(items[i])[26:27] == "T"):
                if items[i].toPlainText() != "":
                    text.append("text")
                    text[i-skipped] += items[i].toPlainText() + ","
                else:
                    skipped += 1
            
            if len(text) == i-skipped+1 :
                text[i-skipped] += lista
                
        objects.reverse()
        penSet.reverse()
        f.write(str(text))
        f.close()

    return True

'''
   Function for deleting/taking back the latest change to the picture.
   gui    the GUI object from the graphicalUI
   If there has been any changes to the picture and the canvas is not empty, the latest change
   (adding a new object or moving an existing object) is undone.
'''
def undo(gui):
    log = gui.canvas.getWorkLog()
    index = len(log)
    if index != 0:
        delete = log[index-1]
        if delete == "addition":
            if(len(gui.scene.items()) > 0):
                gui.scene.removeItem(gui.scene.items()[0])
                gui.items -= 1
                gui.canvas.deleteObject()
                gui.canvas.removeWork()
        elif delete[0] == "movement":
            for item in gui.scene.items():
                if item.x() == delete[2][0] and item.y() == delete[2][1]:
                    item.setPos(delete[1][0], delete[1][1])
            gui.canvas.removeWork()    
        return True

    return False

'''
   A function for exporting everything that is on the canvas at the moment.
   gui    the GUI object from graphicalUI
   Renders the scene and saves the picture as 'kuva.png'. Occasionally causes C++ Visual run-time error?
'''
def exportPicture(gui):
    # Causes a run-time error sometimes
    size = gui.scene.sceneRect().size().toSize()
    image = QImage(size, QImage.Format_ARGB32)
    paint = QPainter(image)
    gui.scene.render(paint)
    image.save("kuva.png", "PNG")
    return True

    '''
    Works with PyQt4:
    QPixmap.grabWindow(QApplication.desktop().winId()).save('kuvaaaa.jpg', 'jpg')
    Should work with PyQt5 but does not work?
    QScreen.grabWindow(QApplication.desktop().winId()).save('kuvaaaa.jpg', 'jpg')
    return True
    '''

'''
   A function for importing a picture.
   gui    the GUI object from graphicalUI
   Tries to make QPixmap object of the wanted file and adds it to the canvas.
'''
def importPicture(gui):
    pic = QFileDialog.getOpenFileName(gui, 'Open file')
    if pic[0] != '':
        picc = QPixmap(pic[0])
        gui.scene.addItem(QGraphicsPixmapItem(picc))
        gui.items +=1
        return True
    return False

'''
   A function for resizing the scene/canvas.
   gui      the GUI object from graphicalUI
   which    a string that tells if  the wanted size is 'height' or 'width'
   Asks the user the size for the height/width and if the given input is an integer, resizes the scene/canvas.
   Note: If the scene wouldn't fit into the screen, it makes it only as big as it can be while still fitting.
'''
def setScale(gui, which):
    answer = QInputDialog.getText(gui, 'Give ' + which, 'Height:')
    okd = answer[1]
    try:
        answer2 = int(answer[0])
    except Exception as e:
        return False
        
        
    if int(answer2) > gui.height()-60 and which == "height":
        answer2 = gui.height()-60
        reply = QMessageBox.information(gui, "Too big...", "Sorry, the " + which + " you chose does not fit into the window.",
                                        QMessageBox.Ok, QMessageBox.Ok)
    elif int(answer2) > gui.width()-25 and which == "width":
        answer2 = gui.width()-25
        reply = QMessageBox.information(gui, "Too big...", "Sorry, the " + which + " you chose does not fit into the window.",
                                        QMessageBox.Ok, QMessageBox.Ok)
    elif answer2 < 1:
        answer2 = 1
                
    if which == "height":
        gui.scene.setSceneRect(QRectF(0, 0, gui.scene.width(), answer2))
    elif which == "width":
        gui.scene.setSceneRect(QRectF(0, 0, answer2, gui.scene.height()))

    gui.canvas.setMaximumSize(gui.scene.width()+5, gui.scene.height()+5)

    return True

'''
   A function for loading a picture.
   gui    the GUI object from graphicalUI
   Asks the user for the file to be loaded.  Loads only .kbv files that are constructed correctly.
'''
def loadPicture(gui):
    fname = QFileDialog.getOpenFileName(gui, 'Open file')
        
    if(fname[0] != '' and fname[0][-4:] == '.kbv'):        
        try:
            if(checkForLoading(gui, "Load picture")):
                gui.canvas.objects = []
                gui.canvas.penSet = []
                gui.canvas.workLog = []
                f = open(fname[0], 'r')
                data1 = f.read()
                size = data1.split(';')
                scale = size[0]
                data = size[1][1:-2]

                size = scale.split(',')
                gui.scene.setSceneRect(QRectF(0, 0, float(size[0]), float(size[1])))
                gui.canvas.setMaximumSize(gui.scene.width()+5, gui.scene.height()+5)

                objs = data.split('\', ')
                objs.reverse()
                for i in range(len(objs)):
                    obct = objs[i][1:-1]
                    obct = obct.split(',')
                    index = gui.combo.findText(obct[7], Qt.MatchFixedString)
                    if index >= 0:
                        gui.combo.setCurrentIndex(index)
                    index2 = gui.penWidth.findText(obct[8], Qt.MatchFixedString)
                    if index2 >= 0:
                        gui.penWidth.setCurrentIndex(index2)
                    if obct[0][:4] != "text":
                        gui.canvas.createPic(obct[0], obct[1], obct[2], obct[3], obct[4], obct[5], obct[6])
                    else:
                        gui.texthere = QGraphicsTextItem()
                        gui.canvas.createText(obct[0][4:], obct[1], obct[2], obct[5])
                return True

                f.close()
        except Exception as e:
                print(e)
                print("The chosen file was not a valid .kbv file")
                
    elif fname[0] != '' and fname[0][-4:] != '.kbv':
        reply = QMessageBox.information(gui, "Wrong file extension!",
                                            "The file you chose was not a .kbv file or not a valid .kbv file. If you wish to import a .png file, you can use the import option (Ctrl+I).",
                                            QMessageBox.Ok,QMessageBox.Ok)
    return False
