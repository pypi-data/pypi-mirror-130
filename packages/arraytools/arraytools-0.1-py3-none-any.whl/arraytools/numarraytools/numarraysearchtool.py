"""
Number Array searching tool

@Author: Ling Xiang Zou
@Date: Nov 25, 2021
"""
from arraytools.numarraytools.numarraytools import NumArrayTools

class NumArraySearchTool(NumArrayTools):
    def __init__(self, arr):
        NumArrayTools.__init__(self,arr)
        if (self.isnumerial() != True) or (self.isnull() != False):
            print("please enter a valid array")
            
    def searchMin(self):
        return min(self.arr)
    
    def searchMax(self):
        return max(self.arr)
    
    def searchTarget(self,target):
        for i in range(len(self.arr)):
            if target == self.arr[i]:
                return i
        return -1
    