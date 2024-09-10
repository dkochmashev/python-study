import unittest

from module12_1 import *
from module12_2 import *

test_suite = unittest.TestSuite()
test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(RunnerTest))
test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TournamentTest))

test_tournament = unittest.TextTestRunner(verbosity=2)
test_tournament.run(test_suite)
