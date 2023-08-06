'''
Unit Test
'''

import unittest
import numpy as np
from pyqpath.path_weights import global_node_weights, local_node_weights


A = np.matrix([[0, 8, 4], [0, 0, 0], [0, 7, 0]])

class WeightTest(unittest.TestCase):
   
    def test_global_weights(self):
        self.assertEqual(global_node_weights(A), [12, 15, 3])
        
    
    def test_local_weights(self):
        self.assertEqual(local_node_weights(A, [0,1,2]), [12, 15, 3])



if __name__ == '__main__':
    unittest.main()