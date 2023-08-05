import sys

PYSIDE2_LOADED = False
PYQT5_LOADED = False

if not PYSIDE2_LOADED:
    try:
        from PyQt5 import QtGui, QtWidgets, QtCore, QtMultimedia
        from PyQt5.QtCore import pyqtSignal, pyqtSlot

        PYQT5_LOADED = True
        print("Use PyQt5")
    except:
        pass

if not PYQT5_LOADED:
    try:
        from PySide2 import QtGui, QtWidgets, QtCore, QtMultimedia
        from PySide2.QtCore import Signal as pyqtSignal, Slot as pyqtSlot

        PYSIDE2_LOADED = True
        print("Use PySide2")
    except:
        pass

x = 50

if not PYQT5_LOADED and not PYSIDE2_LOADED:
    sys.exit(
        "Missing application dependancies, try:\n\tpip install pose-classification-kit[app]"
    )
