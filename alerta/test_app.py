
import unittest

from alerta.app import app, db


class AlertaTestCase(unittest.TestCase):

    def setUp(self):

        app.config['TESTING'] = True

    def tearDown(self):

        pass


if __name__ == '__main__':

    unittest.main()