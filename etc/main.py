#!/usr/bin/env python
from PyQt4.QtGui import QApplication
import etc

app = QApplication([])
calculator = etc.ETC()
calculator.run(app)
