from functools import partial

from PyQt4.QtGui import QApplication, QComboBox, QGridLayout, QLabel, QLineEdit, QPainter, QPlainTextEdit, QPushButton, QRadioButton, QWidget
from PyQt4 import QtCore

import astrotools

import logging
import sys

# Also have logging output to the console.
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

class TextLogger(logging.Handler):
    ''' A logger to record the users actions and write them to a QPlainTextEdit widget.
    '''
    def __init__(self, parent):
        super(TextLogger, self).__init__()
        
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
    
    def emit(self, record):
        ''' Log a message.
        Args:
            record (str) : the message to log.
        '''
        message = self.format(record)
        self.widget.appendPlainText(message)

    
class ETC(QWidget):
    ''' The exposure time calculator for the Gratama telescope.
    '''
    def __init__(self):
        super(ETC, self).__init__()
        self.widgets = {}
        # Telescope properties.
        self.all_filters = ['U', 'V', 'B', 'R', 'Ha', 'Hb', 'OIII', 'SII']
        self.src_types = ['Point source', 'Extended']
        self.quantities = ['Signal to Noise', 'Exposure Time', 'Limiting Magnitude']
        
        # Logger.
        self.loghandler = TextLogger(self)
        logging.getLogger().addHandler(self.loghandler)
        logging.getLogger().setLevel(logging.INFO)
        self.setup()
    
    def add_action(self, widget, event, action):
        'self.{0:s}.{1:s}.connect({2:s})'.format(self.widgets[widget], event, action)
    
    def go_clearlog(self):
        self.loghandler.widget.setPlainText('')
    
    def go_calculate(self, mode):
        logging.info('Calculating ' + self.widgets['quantity'].currentText())
        logging.info(mode)
        if mode == 0:
            astrotools.signal_to_noise()
        elif mode == 1:
            pass
        elif mode == 2:
            pass
        logging.info('Finished')
        
    def go_reset(self):
        ''' Reset all fields to their default values.
        '''
        # Reset filter selection.
        self.widgets['filters'].setCurrentIndex(0)
        # Reset source type.
        self.widgets['source'].setCurrentIndex(0)
        # Reset exposure time.
        self.widgets['exptime'].setText('10')
        # Reset signal to noise.
        self.widgets['sovern'].setText('')
        # Reset object apparent magnitude.
        self.widgets['mag'].setText('20')
        # Write to the log.
        logging.info('Gratama ETC reset to default values.')
    
    def reconnect(self, signal, newhandler=None, oldhandler=None):
        while True:
            try:
                if oldhandler is not None:
                    signal.disconnect(oldhandler)
                else:
                    signal.disconnect()
            except TypeError:
                break
        if newhandler is not None:
            signal.connect(newhandler)
    
    def select_filter(self, filter):
        logging.info('Changed filter to {:s}'.format(self.all_filters[filter]))
        
    def select_source(self, src):
        logging.info('Changed source type to {:s}'.format(self.src_types[src]))
    
    def select_quantity(self, q):
        logging.info('Changed calculation to {:s}'.format(self.quantities[q]))
        if q == 0:
            # Signal to noise selected.
            handler = partial(self.go_calculate, 0)
        elif q == 1:
            # Exposure time selected.
            handler = partial(self.go_calculate, 1)
        elif q == 2:
            # Limiting magnitude selected.
            handler = partial(self.go_calculate, 2)
        # Update the event handler.
        self.reconnect(self.widgets['calc'].clicked, newhandler=handler)
    
    def run(self, app):
        app.exec_()
    
    def setup(self):
        ''' Setup the inital state of the calculator.
        
        '''
        self.setWindowTitle('Gratama Exposure Time Calculator')

        # Telescope section.
        title_tel = QLabel('Telescope Parameters')
        label_exptime = QLabel('Exposure Time [s]: ')
        label_sovern = QLabel('Signal to Noise: ')
        label_filters = QLabel('Filter: ')
        
        filters = QComboBox(); self.widgets['filters'] = filters
        filters.addItems(self.all_filters)
        filters.currentIndexChanged.connect(self.select_filter)
        
        exptime = QLineEdit(); self.widgets['exptime'] = exptime
        sovern = QLineEdit(); self.widgets['sovern'] = sovern
        
        # Source section.
        title_src = QLabel('Source Parameters')
        label_type = QLabel('Source type: ')
        label_mag = QLabel('Apparent Magnitude: ')
        
        srctype = QComboBox(); self.widgets['source'] = srctype
        srctype.addItems(self.src_types)
        srctype.currentIndexChanged.connect(self.select_source)
        
        mag = QLineEdit(); self.widgets['mag'] = mag
        
        # Other components.
        button_reset = QPushButton('Reset')
        button_reset.clicked.connect(self.go_reset)
        
        button_calculate = QPushButton('Calculate'); self.widgets['calc'] = button_calculate
        button_calculate.clicked.connect(self.go_calculate)
        
        button_clearlog = QPushButton('Clear Log')
        button_clearlog.clicked.connect(self.go_clearlog)
        
        label_quantity = QLabel('Quantity to Calculate: ')
        quantity = QComboBox(); self.widgets['quantity'] = quantity
        quantity.addItems(self.quantities)
        quantity.currentIndexChanged.connect(self.select_quantity)
        self.select_quantity(0)
        
        # Layout the components.
        ########################
        grid = QGridLayout()
        grid.setSpacing(10)
        
        # Telecope widgets.
        grid.addWidget(title_tel, 1, 0)
        grid.addWidget(label_filters, 2, 0); grid.addWidget(filters, 2, 1)
        grid.addWidget(label_exptime, 3, 0); grid.addWidget(exptime, 3, 1)
        grid.addWidget(label_sovern, 4, 0); grid.addWidget(sovern, 4, 1)
        
        grid.addWidget(label_quantity, 0, 0); grid.addWidget(quantity, 0, 1)

        # Source widgets.
        grid.addWidget(title_src, 6, 0)
        grid.addWidget(label_type, 7, 0); grid.addWidget(srctype, 7, 1)
        grid.addWidget(label_mag, 8, 0); grid.addWidget(mag, 8, 1)
        
        # Other widgets
        grid.addWidget(button_reset, 9, 0); grid.addWidget(button_calculate, 9, 1)
        # Logger window.
        grid.addWidget(QLabel('Logs'), 0, 3)
        grid.addWidget(self.loghandler.widget, 1, 3, 8, 2)
        grid.addWidget(button_clearlog, 9, 3, 1, 2)

        self.go_reset()
        self.go_clearlog()
        self.setLayout(grid)
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = ETC()
    app.exec_()
    