import unittest

from raspyrfm_client import RaspyRFMClient


class TestStringMethods(unittest.TestCase):
    def test_generate_code(self):

        rfm_client = RaspyRFMClient()

        for manufacturer in rfm_client.get_supported_manufacturers():
            for model in rfm_client.get_supported_models(manufacturer):
                device = rfm_client.get_device(manufacturer, model)
                for action in device.get_supported_actions():
                    # TODO: allow programmatic channel configuration

                    code = device.generate_code(action)
                    self.assertIsNotNone(code)


if __name__ == '__main__':
    unittest.main()
