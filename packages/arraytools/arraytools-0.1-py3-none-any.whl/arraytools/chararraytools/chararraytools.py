"""
Character Array Tools

@Author: Nelson Tang
@Date: Nov 25, 2021
"""


class CharArrayTools(object):

    def __init__(self, arr):
        self.arr = arr

    def __str__(self):
        return str(self.arr)

    def __instancecheck__(self):
        """
        Check each elements in this array is character

            Returns:
                True:  all elements are character
                False: there at least one element is not character
        """
        for e in self.arr:
            if not isinstance(e, str):
                return False
        return True

    def check_empty(self):
        """
        Check whether the array is empty

        :return: True: It is empty, False: It is not empty
        """
        if len(self.arr) == 0:
            return True
        return False

    def append(self, element):
        """
        Insert an element into the array

        :param element: a character
        """
        if isinstance(element, int):
            try:
                raise AppendIntegerError(element)
            except AppendIntegerError as ae:
                print("Error: Can not append integer", str(ae), " to CharArrayTools!", ae.value)
                raise AppendIntegerError(element)
        else:
            self.arr.append(element)


class AppendIntegerError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)