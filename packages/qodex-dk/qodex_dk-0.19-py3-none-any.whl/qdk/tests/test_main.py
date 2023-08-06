from qdk.main import QDK
import unittest


class MainTets(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.qdk_test = QDK('localhost', 1337, 'testuser', 'testpass')

    def test_get_sdk_methods(self):
        response = self.qdk_test.get_sdk_methods()
        print(response)