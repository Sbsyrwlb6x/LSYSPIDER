# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
import sys
import os
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QDialog, QApplication

from Ui_UI import Ui_Dialog


class UI(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
    
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        os.system('redis-server.exe')
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
        

    @pyqtSignature("")
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        os.system('redis-cli shutdown')
        # TODO: not implemented yet
        raise NotImplementedError
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = UI()
    dlg.show()
    sys.exit(app.exec_())
