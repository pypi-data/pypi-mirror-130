# -*- coding:utf-8 -*-

import numpy as np


def logo():
    print(' _____        ____  _____      _   _     ') 
    print('|  __ \      / __ \|  __ \    | | | |    ')
    print('| |__) |   _| |  | | |__) |_ _| |_| |__  ')
    print('|  ___/ | | | |  | |  ___/ _| | __|  _ \ ')
    print('| |   | |_| | |__| | |  | (_| | |_| | | |')
    print('|_|    \__, |\___\_\_|   \__,_|\__|_| |_|')
    print('        __/ |                            ')
    print('       |___/                             ')
    


#==========================================

#------------ Global Weights --------------


#Computing global node weights:
def global_node_weights(M):
    W = []
    for i in range(len(M)):
        sw1 = sw2 = 0
        for j in range(len(M)):
            if i != j:
                sw1 += M[j,i] 
                sw2 += M[i,j]
                w = [abs(sw1-sw2), 1]
            else:
                pass
        W.append(round(max(w), 1))
    return W

#Computing global path weight:
def global_path_weight(M, p):
    w = 1
    path = sorted(p)
    for i in range(len(path)):
        w *= global_node_weights(M)[path[i]]
    return round(w, 2)


#------------ Local Weights --------------

#Computing local node weights:
def local_node_weights(M, path):
    W = []
    for i in path:
        sw1 = sw2 = 0
        for j in path:
            if i != j:
                sw1 += M[j,i] 
                sw2 += M[i,j]
                w = [abs(sw1-sw2), 1]
            else:
                pass
        W.append(round(max(w), 1))
    return W

#Computing local path weight:
def local_path_weight(M, path):
    w = 1
    for i in range(len(path)):
        w *= local_node_weights(M, path)[i]
    return round(w, 2)


#------------ Bidirected Edges --------------

#Bidirected edges:
def bidir_edges(M):
    W=[]
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i,j] != 0  and M[j,i] != 0:
               W.append([i, j])
            else:
                pass
    return W
          

          
  #==========================================