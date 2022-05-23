import random

from gradescope_utils.autograder_utils.decorators import weight

from Base_Class import BaseClass


class TestA(BaseClass):

    @weight(1)
    def test_list(self):
        """A1. test function on list from instructions"""
        function_to_test = "bubble_sort"
        # tuple with one element (or more, if more than one argument)
        args = ([5, 2, 1, 3, 4],)
        input_values = ""  # "2\n3\n4\n" <- if there are any input() in function expected
        self.make_check(function_to_test, args, input_values)

    @weight(4)
    def test_random_list(self):
        """A2. test function on random list"""
        function_to_test = "bubble_sort"
        # tuple with one element (or more, if more than one argument)
        args = ([random.randint(1, 100) for _ in range(random.randint(8, 10))],)
        input_values = ""  # "2\n3\n4\n" <- if there are any input() in function expected
        self.make_check(function_to_test, args, input_values)
