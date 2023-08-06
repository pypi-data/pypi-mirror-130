"""
Number Array Tools

@Author: Ling Xiang Zou
@Date: Nov 25, 2021
"""

class NumArrayTools:
    def __init__(self, arr):
        self.arr = arr


    def isnumerial(self):
        for i in self.arr:
            try:
                if not isinstance(i, int):
                    raise ValueError("Invalid array")

            except ValueError as ex:
                print("Error:", ex)
                raise ValueError
            else:
                return True

    def isnull(self):
        try:
            if len(self.arr) == 0:
                raise ValueError("Empty array is not allowed")
        except ValueError as ex:
            print("Error:", ex)
            raise ValueError
        else:
            return False
    
    def append(self, x):
        try:
            if not isinstance(x, int):
                raise ValueError("Only integers are allowed")
        except ValueError as ex:
            print("Error:", ex)
        else:
            self.arr.append(x)