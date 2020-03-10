# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 09:28:37 2020

@author: Ethan
"""
import pyqtgraph as pg
    
from PyQt5 import QtWidgets, uic
import test_stimulation
import sys
#from stg.api import STG4000
from os import chdir
from pathlib import Path
from functools import partial
import reiz
from reiz.marker import push
from matplotlib import pyplot as plt
import time
from scipy import stats
import numpy as np
import liesl
import configparser

# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')


class Ui(QtWidgets.QMainWindow, test_stimulation.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Ui, self).__init__(parent)
        self.setupUi(self)
        self.show()
        

        
        self.on_button.clicked.connect()
        self.off_button.clicked.connect()
        




app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()