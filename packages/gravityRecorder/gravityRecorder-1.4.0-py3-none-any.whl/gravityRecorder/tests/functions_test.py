import unittest
from gravityRecorder import functions
from gravityRecorder.tests.test_objects import test_recorder


class FunctionsTest(unittest.TestCase):
    def test_add_change_notes(self):
        """ Протестировать добавление комментария при изменении записи """
        functions.add_change_notes(test_recorder, 347, 'TEST2')