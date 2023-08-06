import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir)
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import title_rc

from whatis.whatis_wrap import _Whatis
class _HelpDialog(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super(_HelpDialog, self).__init__(parent)


        loadUi(os.path.join(currentdir,'help.ui'),self)
        self.config()
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self.setWindowFlags(flags)
        
#        self.exec()

    def closeEvent(self,event):
        print("Pop dialog is closing")

    def config(self):
        try:
            
##            style= '.QWidget{background-image: url(:/back_ground/rectangle.png);border:0px;}'
##            self.central.setStyleSheet(style);
##            style= '.QPushButton{background-color: transparent; border:0; color : white;}'
##            self.more.setStyleSheet(style)
##            style= '.QWidget{background-image: url(:/whatis_more/whatis_more.png);border:0px;}'
##            self.whatis_more.setStyleSheet(style);

            



##            style= '.QWidget{background-image: url(:/legal_contact/legal_contact.png);border:0px;}'
##            self.legal_contact.setStyleSheet(style);
            #self.pushButton_5.clicked.connect(self.close)
            self.play_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.play_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.whatis.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.whatis.clicked.connect(self.open_whatis)
            
            self.more.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.faq_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.legal.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.contact.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            QtWidgets.qApp.focusChanged.connect(self.on_focusChanged)

            self.back.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.back.clicked.connect(self.close)

#background-image: url(:/legal_contact/legal_contact.png);
#background-image: url(:/faq/faq.png);
            pass
        except Exception as error:
            print(error)

    def open_whatis(self):

        whatis_window = _Whatis()
        whatis_window.move(self.geometry().x(), self.geometry().y())
        #whatis_window.show_html(os.path.join(currentdir,'test.html'))
        
        whatis_window.exec()
    def on_focusChanged(self):
        print('focus changed')

if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)

    QtWidgets.QMainWindow
##    drtn=_HelpDialog().exec()
##    print('pop dialog end',drtn)
    window=_HelpDialog()
    window.show()
    
    rtn= app.exec_()
    print('main app return', rtn)
    sys.exit(rtn)
