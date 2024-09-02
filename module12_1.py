import unittest
from runner import *


class RunnerTest(unittest.TestCase):
    def runTest(self):
        self.test_walk()
        self.test_run()
        self.test_challenge()

    def test_walk(self):
        walker = Runner('Johnnie Walker')
        for i in range(10):
            walker.walk()
        self.assertEqual(walker.distance, 50)

    def test_run(self):
        runner = Runner('Forrest')
        for i in range(10):
            runner.run()
        self.assertEqual(runner.distance, 100)

    def test_challenge(self):
        runner1 = Runner('Beavis')
        runner2 = Runner('Butthead')
        for i in range(10):
            runner1.run()
            runner2.walk()
        self.assertNotEqual(runner1.distance, runner2.distance)


if __name__ == "__main__":
    unittest.main()
