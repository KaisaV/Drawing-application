import sys
from PyQt5.QtWidgets import *
from graphicalUI import GUI

ex=None
# starts running the application
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
