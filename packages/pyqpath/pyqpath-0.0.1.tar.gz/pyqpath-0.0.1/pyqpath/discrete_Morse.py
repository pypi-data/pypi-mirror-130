# -*- coding:utf-8 -*-

import numpy as np
from pyqpath.weights import *


def logo():
    print(' _____        ____  _____      _   _     ') 
    print('|  __ \      / __ \|  __ \    | | | |    ')
    print('| |__) |   _| |  | | |__) |_ _| |_| |__  ')
    print('|  ___/ | | | |  | |  ___/ _  | __|  _ \ ')
    print('| |   | |_| | |__| | |  | (_| | |_| | | |')
    print('|_|    \__, |\___\_\_|   \__,_|\__|_| |_|')
    print('        __/ |                            ')
    print('       |___/                             ')
    


#===============================

#Discrete Morse function:
def discMorsefunc_node(M, path, v):
    f = local_node_weights(M, path)[v]*local_node_weights(M, path)[v+1]
    return f


#F(e) = sum_{i} f(i):
def discMorsefunc_path(M, k, path):
    F = 0
    if path[0] != path[len(path)-1]:
        for i in range(k-2):
            F += discMorsefunc_node(M, path[0:k], i)
    else:
        for i in range(k-2):
             F += discMorsefunc_node(M, path[0:k+1], i)
    return F


#Critical paths:
def critical_path(M, k, path):
     if discMorsefunc_path(M, k, path) == discMorsefunc_path(M, k-1, path) or \
        discMorsefunc_path(M, k, path[0:k]) == discMorsefunc_path(M, k, path[0:k+1]):
          print("%s is not critical." % path)
     else:
          print("%s is critical." % path)

          

 #===============================         
          