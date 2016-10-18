#!/usr/bin/env python
from PyQt4.QtGui import QApplication, QWidget
import sys

class ETC(QWidget):
    def __init__(self):
        super(ETC, self).__init__()
        self.setup()
        
    def setup(self):
        self.setWindowTitle('Gratama Exposure Time Calculator')
        
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    calculator = ETC()
    
    sys.exit(app.exec_())
    