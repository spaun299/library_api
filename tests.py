import unittest
import app as application
import json


class TestCase(unittest.TestCase):
    def setUp(self):
        app = application.app
        app.testing = True
        self.app = app.test_client()
        self.helloworld_uri = '/api/get/helloworld'

    def test_endpoint(self):
        resp = self.app.get(self.helloworld_uri)
        data = resp.data
        assert resp.status_code == 200, 'Status code %s ' % resp.status_code
        assert b'Hello World' in data, 'Endpoint returned %s ' % data

    def test_helloworld_json(self):
        resp = self.app.get(self.helloworld_uri)
        data = resp.data
        data_dict = json.loads(str(data, 'utf-8'))
        assert len(data_dict) == 2, "Endpoint should returns " \
                                    "json with two keys"
        assert 'error' in data_dict
        assert 'message' in data_dict
        assert data_dict.get('error') is False, \
            'Endpoint returned an error %s' % data_dict.get('message')

if __name__ == '__main__':
    unittest.main()
