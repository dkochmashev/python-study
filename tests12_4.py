import logging
import unittest
from rt_with_exceptions import *


logging.basicConfig(
    level=logging.INFO,
    filename='runner_test.log',
    filemode='w',
    encoding='utf-8',
    format='%(asctime)s\t%(levelname)s\t%(message)s'
)


class RunnerTest(unittest.TestCase):
    is_frozen = False

    def runTest(self):
        self.test_walk()
        self.test_run()
        self.test_challenge()

    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_walk(self):
        try:
            walker = Runner('Johnnie Walker', -1)
        except:
            logging.warning('Неверная скорость для Runner', exc_info=True)
        else:
            walker = Runner('Johnnie Walker', 5)
            for i in range(10):
                walker.walk()
            self.assertEqual(walker.distance, 50)
            logging.info('"test_walk" выполнен успешно')

    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_run(self):
        try:
            runner = Runner(False)
        except:
            logging.warning('Неверный тип данных для объекта Runner', exc_info=True)
        else:
            runner = Runner('Forrest')
            for i in range(10):
                runner.run()
            self.assertEqual(runner.distance, 100)
            logging.info('"test_run" выполнен успешно')

    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_challenge(self):
        runner1 = Runner('Beavis')
        runner2 = Runner('Butthead')
        for i in range(10):
            runner1.run()
            runner2.walk()
        self.assertNotEqual(runner1.distance, runner2.distance)


if __name__ == "__main__":
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(RunnerTest))

    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
