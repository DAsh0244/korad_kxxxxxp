import unittest
from korad_api import *


TEST_KORAD_INFO = {
    'addr':'COM4',
    'id':'RND 320-KD3005P V2.0',
    'channels':1,
    'max_voltage':30,
    'max_current':5,
}

TEST_KORAD_CONFIG = {
    'ocp':False,
    'output':True,
    'voltage':[{'ch':1,'voltage':3.29}],
    'current':[{'ch':1,'current':0.01}],
}

# todo: implement methods for testing settign and measuring 
class KoradObjectTests(unittest.TestCase):
    def setUp(self):
        self.psu = Korad(TEST_KORAD_INFO['addr'])
        self.psu.configure(TEST_KORAD_CONFIG)

    def tearDown(self):
        self.psu.close()

    def test_information(self):
        korad_info = {
            'addr':self.psu.addr,
            'id':self.psu.id,
            'channels':self.psu.channels,
            'max_voltage':self.psu.max_voltage,
            'max_current':self.psu.max_current,
        }
        self.assertEqual(korad_info, TEST_KORAD_INFO, 'ID Mismatch.')

    def test_configured_voltage(self):
        for channel in range(1,self.psu.channels+1):
            configured_voltage = [x['voltage'] for x in TEST_KORAD_CONFIG['voltage'] if x['ch'] == channel][0]
            self.assertAlmostEqual(self.psu.configured_voltage(channel), configured_voltage, delta=0.001, msg='Set voltage mismatch')
    
    def test_configured_current(self):
        for channel in range(1,self.psu.channels+1):
            configured_current = [x['current'] for x in TEST_KORAD_CONFIG['current'] if x['ch'] == channel][0]
            self.assertAlmostEqual(self.psu.configured_current(channel), configured_current, delta=0.0005, msg='Set current mismatch')

    def test_ocp(self):
        enable = True
        self.psu.set_ocp(enable)
        self.assertEqual(self.psu.status['ocp'],enable,'OCP status not recognized correctly')

    def test_output(self):
        self.psu.set_output(False)
        status = self.psu.status
        self.assertEqual(status['output'],False,'output status not recognized correctly')
        self.assertEqual(status['v_out'],0,'ouput may not be disabled')
        self.assertEqual(status['i_out'],0,'ouput may not be disabled')
        self.psu.set_output(True)

# todo: implement tests for functional interface

if __name__ == "__main__":
    unittest.main()
