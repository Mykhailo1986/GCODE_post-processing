import unittest
import extrusion_width_hight

class ExtrusionWidthHightTestCase(unittest.TestCase):
    def test_number_from_string_int(self):
        '''test for Extracts the int from the string'''
        string:str = "Give 5 apples"
        expected:int = 5
        answer:int = extrusion_width_hight.number_from_string(string)
        self.assertEqual(answer, expected)

    def test_number_from_string_float(self):
        '''test for Extracts the int from the string'''
        string:str = "Width 1.86 m"
        expected:float = 1.86
        answer:float = extrusion_width_hight.number_from_string(string)
        self.assertEqual(answer, expected)


    def test_line_width_prusa_slicer(self):
        '''test for correct reading width from PrusaSlicer gcode '''
        file_path = "Cyl.gcode"
        expected_width = 0.66
        width = extrusion_width_hight.line_width(file_path)
        self.assertEqual(width, expected_width)
    def test_layer_higth_prusa_slicer(self):
        '''test for correct reading width from PrusaSlicer gcode '''
        file_path = "Cyl.gcode"
        expected_higth = .16
        higth = extrusion_width_hight.layer_higth(file_path)
        self.assertEqual(higth, expected_higth)



if __name__ == '__main__':
    unittest.main()
