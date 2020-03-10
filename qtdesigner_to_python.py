# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 10:32:35 2020

@author: Ethan
"""

from PyQt5 import uic 
fin = open('hh_designer.ui','r')
fout = open('hh_designer.py','w')
uic.compileUi(fin,fout,execute=False)
fin.close()
fout.close()