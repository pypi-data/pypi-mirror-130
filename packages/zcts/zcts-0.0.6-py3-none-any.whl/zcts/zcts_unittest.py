# -----------------------------------------------------------------------------
# - File              converter2000_sdk_unittest.py
# - Owner             Zhengkun Li
# - Version           1.0
# - Date              21.06.2021
# - Classification    converter2000_sdk_unittest
# ----------------------------------------------------------------------------- 
import unittest
from zcts import *
comport = "COM41"
class TestTemplate(unittest.TestCase):
    def test_detect_comports(self):
        detect_comports()
    def test_get_sw_version(self):
        get_sw_version(comport)
    def test_reboot_sys(self):
        reboot_sys(comport)
    def test_save_config(self):
        a = save_config(comport)
        self.assertEqual(True,a)
    def test_clear_config(self):
        a = clear_config(comport)
        self.assertEqual(True,a)
    def test_disp_config(self):
        a = disp_config(comport)
        self.assertEqual(True,a)
    def test_disp_port_status(self):
        a = disp_port_status(comport)
        self.assertEqual(True,a)
    def test_disp_port_statistics(self):##### VERBINDUNG benotigen
        a = disp_port_statistics(comport)
        self.assertEqual(True,a)


    def test_set_op_mode(self): #####no return value
        for i in range(0,4):
            a = set_op_mode(comport,i)
            self.assertEqual(True,a)
    def test_get_op_mode(self):
        a = get_op_mode(comport)
        for i in range(0,3):
            self.assertNotEqual(-1,a[i])
    

    def test_set_eth_speed(self):
        for i in [1,2]:
            for j in [100,1000]:
                a = set_eth_speed(comport,i,j)
                self.assertEqual(True,a)
        a = set_eth_speed(comport,1,200)
        self.assertEqual(False,a)
        a = set_eth_speed(comport,3,100)
        self.assertEqual(False,a)
    def test_get_eth_speed(self):
        for i in [1,2]:
            for j in [100,1000]:
                set_eth_speed(comport,i,j)
                a = get_eth_speed(comport,i)
                self.assertEqual(str(j),a[1])
    
    
    def test_set_eth_down(self):
        for i in [1,2]:
            for j in [0,1]:
                a = set_eth_down(comport,i,j)
                self.assertEqual(True,a)
    def test_get_eth_down(self):
        for i in [1,2]:
            a = get_eth_down(comport,i)
            self.assertEqual(str(i),a[0])
    
    
    def test_set_brr_speed(self):
        for i in [1,2]:
            for j in [100,1000]:
                a = set_brr_speed(comport,i,j)
                self.assertEqual(True,a)
        a = set_brr_speed(comport,1,200)
        self.assertEqual(False,a)
        a = set_brr_speed(comport,3,100)
        self.assertEqual(False,a)
    


    def test_get_brr_speed(self):
        for i in [1,2]:
            for j in [100,1000]:
                set_brr_speed(comport,i,j)
                a = get_brr_speed(comport,i)
                self.assertEqual(str(j),a[1])


    def test_set_brr_down(self):
        for i in [1,2]:
            for j in [0,1]:
                a = set_brr_down(comport,i,j)
                self.assertEqual(True,a)
    def test_get_brr_down(self):
        for i in [1,2]:
            a = get_brr_down(comport,i)
            self.assertEqual(str(i),a[0])



    def test_set_brr_role(self):
        for i in [1,2]:
            for j in [0,1]:
                a = set_brr_role(comport,i,j)
                self.assertEqual(True,a)
    def test_get_brr_role(self):
        for i in [1,2]:
            a = get_brr_role(comport,i)
            self.assertEqual(str(i),a[0])

    def test_set_brr_mode(self):
        for i in [1,2]:
            for j in [0,1]:
                a = set_brr_mode(comport,i,j)
                self.assertEqual(True,a)

    def test_get_brr_mode(self):
        for i in [1,2]:
            for j in [0,1]:
                set_brr_mode(comport,i,j)
                save_config(comport)
                # time.sleep(3)
                reboot_sys(comport)
                # time.sleep(5)
                a = get_brr_mode(comport,i) 
                print(a)
                print(j)
                self.assertEqual(j,int(a[1]))
    
if __name__ == '__main__':
    unittest.main()