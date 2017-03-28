import unittest

import rstr
from builtins import print

from raspyrfm_client import RaspyRFMClient


class TestStringMethods(unittest.TestCase):
    def test_random_config(self):
        """
        Tests all devices with random configurations.
        """

        rfm_client = RaspyRFMClient()

        from raspyrfm_client.device.base import Device

        def test_device(device: Device):
            """
            Tests random device configurations for the specified device
            
            :param device: the device to test 
            """

            self.assertIsNotNone(device.get_manufacturer())
            self.assertIsNotNone(device.get_model())
            self.assertIsNotNone(device.get_supported_actions())

            channel_config_args = device.get_channel_config_args()

            # tests 50 randomly chosen configurations
            for i in range(50):
                channel_config = {}

                for arg in channel_config_args:
                    channel_config[arg] = rstr.xeger(channel_config_args[arg])

                device.set_channel_config(**channel_config)

                for action in device.get_supported_actions():
                    generated_code = device.generate_code(action)
                    self.assertIsNotNone(generated_code)

        def test_models(manufacturer_name: str):
            """
            Tests all models of the specified manufacturer
            
            :param manufacturer_name:  name of the manufacturer to test all available models
            """
            for model in rfm_client.get_supported_models(manufacturer_name):
                print("Testing " + model)
                device = rfm_client.get_device(manufacturer_name, model)
                test_device(device)

        for manufacturer in rfm_client.get_supported_manufacturers():
            test_models(manufacturer)

        print("All random config device tests passed!")


if __name__ == '__main__':
    unittest.main()
