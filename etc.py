#!/usr/bin/env python
from PyQt4.QtGui import QApplication, QComboBox, QGridLayout, QLabel, QLineEdit, QPainter, QPlainTextEdit, QPushButton, QWidget
from PyQt4 import QtCore
import logging
import sys
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')
class TextLogger(logging.Handler):
    ''' A logger to record the users actions.
    '''
    def __init__(self, parent):
        super(TextLogger, self).__init__()
        
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
    
    def emit(self, record):
        message = self.format(record)
        self.widget.appendPlainText(message)

    
class ETC(QWidget):
    ''' The exposure time calculator for the Gratama telescope.
    '''
    def __init__(self):
        super(ETC, self).__init__()
        self.loghandler = TextLogger(self)
        logging.getLogger().addHandler(self.loghandler)
        logging.getLogger().setLevel(logging.INFO)
        self.setup()
        
    def setup(self):
        ''' Setup the inital state of the calculator.
        
        '''
        self.setWindowTitle('Gratama Exposure Time Calculator')

        # Telescope section.
        title_tel = QLabel('Telescope Parameters')
        label_exptime = QLabel('Exposure Time [s]: ')
        label_sovern = QLabel('Signal to Noise: ')
        label_filters = QLabel('Filter: ')
        
        all_filters = ['U', 'V', 'B', 'R', 'Ha', 'Hb', 'OII', 'SIII']
        filters = QComboBox()
        filters.addItems(all_filters)
        
        exptime = QLineEdit()
        sovern = QLineEdit()
        
        # Source section.
        title_src = QLabel('Source Parameters')
        label_type = QLabel('Source type: ')
        label_mag = QLabel('Apparent Magnitude: ')
        
        types = ['Point source', 'Extended']
        srctype = QComboBox()
        srctype.addItems(types)
        
        mag = QLineEdit()

        # Layout the components.
        ########################
        grid = QGridLayout()
        grid.setSpacing(10)
        
        # Telecope widgets.
        grid.addWidget(title_tel, 1, 0)
        grid.addWidget(label_filters, 2, 0); grid.addWidget(filters, 2, 1)
        grid.addWidget(label_exptime, 3, 0); grid.addWidget(exptime, 3, 1)
        grid.addWidget(label_sovern, 4, 0); grid.addWidget(sovern, 4, 1)
        

        # Source widgets.
        grid.addWidget(QLabel(''), 5, 0)
        grid.addWidget(title_src, 6, 0)
        grid.addWidget(label_type, 7, 0); grid.addWidget(srctype, 7, 1)
        grid.addWidget(label_mag, 8, 0); grid.addWidget(mag, 8, 1)
        
        # Logger window.
        grid.addWidget(QLabel('Logs'), 9, 0)
        grid.addWidget(self.loghandler.widget, 10, 0, 1, 2)

        self.setLayout(grid)
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = ETC()
    app.exec_()
    