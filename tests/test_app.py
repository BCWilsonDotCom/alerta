import unittest


from alerta.app import app


class AppTestCase(unittest.TestCase):

    def setUp(self):

        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):

        pass

    def test_get_alerts(self):

        rv = self.app.get('/_')
        assert 'No entries so far' in rv.data