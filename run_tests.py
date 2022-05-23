import unittest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner
import os

if __name__ == '__main__':
    unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: y < x
    suite = unittest.defaultTestLoader.discover('tests')
    if "CS8_DEBUG" in os.environ:
        path = r'/results.json'
        unittest.main()
    else:
        path = r'/autograder/results/results.json'

        with open(path, 'w') as f:
            JSONTestRunner(visibility='visible', stream=f).run(suite)