"""
Character array sorting tool

@Author: Nelson Tang
@Date: Nov 25, 2021
"""
import random


from arraytools.chararraytools.chararraytools import CharArrayTools


class CharArraySortTool(CharArrayTools):
    def __init__(self, arr, sorted=False):
        CharArrayTools.__init__(self, arr)
        self.sorted = sorted

    def sort_asc(self):
        """
        Sort the character array in ascending alphabetical order by implementing a bubble sort.
        :return:
        """
        n = len(self.arr)
        for i in range(n):
            for j in range(n-i-1):
                if self.arr[j] > self.arr[j+1]:
                    self.arr[j], self.arr[j+1] = self.arr[j+1], self.arr[j]
        self.sorted = True
        # print("Sorted Array is: ", str(self))

    def sort_desc(self):
        """
        Sort the character array in descending alphabetical order.
        :return:
        """
        self.sort_asc()
        self.arr = self.arr[len(self.arr)::-1]
        self.sorted = True
        # print("Sorted Array is: ", str(self))

    def unsort(self):
        """
        Make a sorted array to unsorted.
        :return:
        """
        if self.sorted:
            random.shuffle(self.arr)
            self.sorted = False
        # print("Unsorted Array is: ", str(self))







