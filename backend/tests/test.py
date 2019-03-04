import unittest
from werkzeug.datastructures import ImmutableMultiDict
from app import create_app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_generate(self):
        data = ImmutableMultiDict({'length': 64})
        response = self.app.post('/api/generate', data=data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
