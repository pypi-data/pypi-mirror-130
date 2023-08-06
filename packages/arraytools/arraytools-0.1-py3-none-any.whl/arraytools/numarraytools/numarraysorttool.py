"""
Number array sorting tool

@Author: Ling Xiang Zou
@Date: Nov 25, 2021
"""
import random
from arraytools.numarraytools.numarraytools import NumArrayTools
class NumArraySortTool(NumArrayTools):
    def __init__(self, arr):
        NumArrayTools.__init__(self,arr)
        if (self.isnumerial() != True) or (self.isnull() != False):
            print("please enter a valid array")
    

    def AscendingSort(self):
        self.arr.sort()


    
    def DescendingSort(self):
        self.arr.sort(reverse=True)

    def Unsort(self):
        self.arr = random.sample(self.arr,len(self.arr))
