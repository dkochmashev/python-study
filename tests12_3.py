import unittest
from runner_and_tournament import *


class RunnerTest(unittest.TestCase):
    is_frozen = False

    def runTest(self):
        self.test_walk()
        self.test_run()
        self.test_challenge()

    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_walk(self):
        walker = Runner('Johnnie Walker')
        for i in range(10):
            walker.walk()
        self.assertEqual(walker.distance, 50)

    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_run(self):
        runner = Runner('Forrest')
        for i in range(10):
            runner.run()
        self.assertEqual(runner.distance, 100)

    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_challenge(self):
        runner1 = Runner('Beavis')
        runner2 = Runner('Butthead')
        for i in range(10):
            runner1.run()
            runner2.walk()
        self.assertNotEqual(runner1.distance, runner2.distance)


class FairTournament(Tournament):
    def start(self):
        finishers = {}
        place = 1
        by_speed = sorted(self.participants, key=lambda i: i.speed, reverse=True)
        while by_speed:
            for participant in by_speed:
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    by_speed.remove(participant)
                    break

        return finishers


class TournamentTest(unittest.TestCase):
    is_frozen = True
    all_results = list()

    def runTest(self):
        self.test_1()
        self.test_2()
        self.test_3()
        self.test_4()

    @classmethod
    def setUpClass(cls):
        TournamentTest.all_results = list()

    def setUp(self):
        self.runners = {
            'Усэйн': Runner('Усэйн', 10),
            'Андрей': Runner('Андрей', 9),
            'Ник': Runner('Ник', 3)
        }

    @classmethod
    def tearDownClass(cls):
        for result in TournamentTest.all_results:
            print(result)

    def __add_results__(self, results):
        TournamentTest.all_results.append({place: results[place].name for place in results})

    # Усэйн и Ник
    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_1(self):
        tournament = Tournament(90, self.runners['Усэйн'], self.runners['Ник'])
        self.assertIsNotNone(results := tournament.start())
        self.assertEqual(len(results), 2)
        self.assertNotEqual(results[1], results[2])
        self.assertEqual(results[1].name, 'Усэйн')
        self.assertEqual(results[2].name, 'Ник')
        self.__add_results__(results)

    # Андрей и Ник
    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_2(self):
        tournament = Tournament(90, self.runners['Андрей'], self.runners['Ник'])
        self.assertIsNotNone(results := tournament.start())
        self.assertEqual(len(results), 2)
        self.assertNotEqual(results[1], results[2])
        self.assertEqual(results[1].name, 'Андрей')
        self.assertEqual(results[2].name, 'Ник')
        self.__add_results__(results)

    # Усэйн, Андрей и Ник.
    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_3(self):
        tournament = Tournament(90, self.runners['Усэйн'], self.runners['Андрей'], self.runners['Ник'])
        self.assertIsNotNone(results := tournament.start())
        self.assertEqual(len(results), 3)
        self.assertNotEqual(results[1], results[2])
        self.assertNotEqual(results[1], results[3])
        self.assertNotEqual(results[2], results[3])
        self.assertEqual(results[1].name, 'Усэйн')
        self.assertEqual(results[2].name, 'Андрей')
        self.assertEqual(results[3].name, 'Ник')
        self.__add_results__(results)

    # Ошибка в алгоритме:
    # ---
    # Если значение скорости бегуна (Runner.speed) совпадает с дистанцией (Tournament.full_distance)
    # и бегун стоит первым в списке participants при конструировании Tournament, он будет на первом
    # месте в результатах забега, не смотря на то, что его скорость может быть ниже, чем у остальных
    # бегунов.
    #
    # Для выявления ошибки создан производный класс FairTournament с переопределением метода start,
    # и сравниваются результаты работы методов start() в вышеописанных условиях.

    @unittest.skipIf(is_frozen, 'Тесты в этом кейсе заморожены')
    def test_4(self):
        tournament = Tournament(3, self.runners['Ник'], self.runners['Усэйн'], self.runners['Андрей'])
        fair_tournament = FairTournament(3, self.runners['Ник'], self.runners['Усэйн'], self.runners['Андрей'])
        self.assertIsNotNone(results := tournament.start())
        fair_results = fair_tournament.start()
        self.assertDictEqual(results, fair_results, 'Неверный подсчет результатов в Tournament.start()')


test_suite = unittest.TestSuite()
test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(RunnerTest))
test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TournamentTest))

test_runner = unittest.TextTestRunner(verbosity=2)
test_runner.run(test_suite)
