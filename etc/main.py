#!/usr/bin/env python
from PyQt4.QtGui import QApplication
import etc
'''Hello World!'''

app = QApplication([])
calculator = etc.ETC()
print calculator.__version__
calculator.run(app)
