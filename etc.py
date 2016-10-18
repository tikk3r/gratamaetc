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
        # Telescope properties.
        self.all_filters = ['U', 'V', 'B', 'R', 'Ha', 'Hb', 'OIII', 'SII']
        self.src_types = ['Point source', 'Extended']
        
        # Logger.
        self.loghandler = TextLogger(self)
        logging.getLogger().addHandler(self.loghandler)
        logging.getLogger().setLevel(logging.INFO)
        self.setup()
    
    def go_calculate(self):
        logging.info('Calculating...')
        
    def go_reset(self):
        logging.info('Gratama ETC reset to default values.')
    
    def select_filter(self, filter):
        logging.info('Changed filter to {:s}'.format(self.all_filters[filter]))
        
    def select_source(self, src):
        logging.info('Changed source type to {:s}'.format(self.src_types[src]))
        
    def setup(self):
        ''' Setup the inital state of the calculator.
        
        '''
        self.setWindowTitle('Gratama Exposure Time Calculator')

        # Telescope section.
        title_tel = QLabel('Telescope Parameters')
        label_exptime = QLabel('Exposure Time [s]: ')
        label_sovern = QLabel('Signal to Noise: ')
        label_filters = QLabel('Filter: ')
        
        filters = QComboBox()
        filters.addItems(self.all_filters)
        filters.currentIndexChanged.connect(self.select_filter)
        
        exptime = QLineEdit()
        sovern = QLineEdit()
        
        # Source section.
        title_src = QLabel('Source Parameters')
        label_type = QLabel('Source type: ')
        label_mag = QLabel('Apparent Magnitude: ')
        
        srctype = QComboBox()
        srctype.addItems(self.src_types)
        srctype.currentIndexChanged.connect(self.select_source)
        
        mag = QLineEdit()
        
        # Other components.
        button_reset = QPushButton('Reset')
        button_reset.clicked.connect(self.go_reset)
        button_calculate = QPushButton('Calculate')
        button_calculate.clicked.connect(self.go_calculate)
        
        
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
        
        grid.addWidget(button_reset, 9, 0); grid.addWidget(button_calculate, 9, 1)
        
        # Logger window.
        grid.addWidget(QLabel('Logs'), 1, 3)
        grid.addWidget(self.loghandler.widget, 2, 3, 8, 1)

        self.setLayout(grid)
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = ETC()
    app.exec_()
    