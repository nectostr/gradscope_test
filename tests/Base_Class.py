import copy
import importlib
import sys
import time
import unittest
from io import StringIO
from multiprocessing import Manager, Process

import config
import correct


class BaseClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        This method is for work ones before all tests
        """

        try:
            cls.student = importlib.import_module(config.filename)

        except ModuleNotFoundError:
            cls.student = f"Cannot find your file {config.filename}. Was it named correctly?"

        except (TypeError, ValueError, IndexError) as e:
            cls.student = f"Syntax error in your code, see \n{e}"

        except Exception as e:
            cls.student = f"Unexpected error in your code, see \n{e}"

    def setUp(self) -> None:
        if type(self.student) == str:
            self.fail(f"Unable to test your whole file,"
                      f" the following error occurred\n{self.student}")

    @staticmethod
    def handle(func, args, input_values="", return_dict=None):

        old_stdout = sys.stdout
        # Assign new StringIO object to print area, so we can get the output after student's code
        sys.stdout = student_output_stream = StringIO()
        old_stin = sys.stdin
        # Assign new StringIO object to input area, so we can get the input after student's code
        sys.stdin = StringIO(input_values)
        try:
            result = func(*args)
        except BaseException as e:
            return_dict[func.__name__] = f"In student code {e}"
            return
        finally:
            sys.stdout = old_stdout
            sys.stdin = old_stin
        expected_output = student_output_stream.getvalue()
        result = result, expected_output
        if return_dict is None:
            return result, expected_output
        return_dict[func.__name__] = result

    @staticmethod
    def handle_infinite(func, args, input_values=""):
        manager = Manager()
        return_dict = manager.dict()
        p = Process(target=BaseClass.handle, args=(func, args, input_values, return_dict))
        p.start()
        time.sleep(5)

        if p.is_alive():
            p.terminate()
            return True, "Processes is still running after 5 sec"

        result = return_dict.get(func.__name__, "Wierd inner error")
        if type(result) != tuple:
            return True, result
        else:
            return False, return_dict[func.__name__]

    def make_check(self, function_name, args, input_values):
        try:
            student_function = getattr(self.student, function_name)
        except AttributeError as e:
            self.fail(f"Seems like you did not create {function_name}\n"
                      f"Python says {e}")
        except Exception as e:
            self.fail(f"An error during your function run\n"
                      f"Python says {e}")

        correct_function = getattr(correct, function_name)

        corr_args = copy.deepcopy(args)
        correct_result, correct_output = BaseClass.handle(correct_function, corr_args, input_values)

        infinite, result = BaseClass.handle_infinite(student_function, args, input_values)

        if infinite:
            self.fail("Seems like your code include infinite loop\n"
                      "Make sure you don't have it.\n"
                      f"Additional info {result}")

        student_result, student_output = result

        if args != corr_args:
            self.fail("You should not change the initial arguments!")

        if student_result != correct_result:
            self.fail("Function returned incorrect result")

        if student_output != correct_output:
            self.fail(f"We expected to see \n<{correct_output}>\n but see "
                      f"\n<student_output>\n as print collection from your function")

        print("Well done!")


#####################################################################################################################

if __name__ == '__main__':
    unittest.main()
