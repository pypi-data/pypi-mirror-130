"""
Character Array searching tool

@Author: Nelson Tang
@Date: Nov 25, 2021
"""
from arraytools.chararraytools.chararraytools import CharArrayTools


class CharArraySearchTool(CharArrayTools):
    def __init__(self, arr):
        CharArrayTools.__init__(self, arr)

    def search_min(self):
        try:
            return min(self.arr)
        except ValueError as ve:
            print("Error: Invalid array!")
            raise ValueError

    def search_max(self):
        try:
            return max(self.arr)
        except ValueError as ve:
            print("Error: Invalid array!")
            raise ValueError

    def search_key(self, target):
        """
        Search a character in the array by implementing a linear search
        :param target: a character
        :return:  The index of the target, if not found return -1.
        """
        if not isinstance(target, str):
            try:
                raise NotCharError(target)  # user define error
            except NotCharError as ne:
                print("Error: Target(", str(ne), ") is not a character!", ne.value)
                raise NotCharError(target)
        else:
            for i in range(0, len(self.arr)):
                if self.arr[i] == target:
                    return i
            return -1


class NotCharError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
