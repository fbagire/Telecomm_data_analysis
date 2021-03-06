import unittest
import pandas as pd
import sys, os

sys.path.append(os.path.abspath(os.path.join('../')))

from clean_df import CleanDataframe

df = pd.read_excel('Week1_challenge_data_source.xlsx',
                   dtype={'Bearer Id': str, 'IMSI': str, 'MSISDN/Number': str, 'IMEI': str,
                          'Handset Manufacturer': str, 'Handset Type': str}, engine='openpyxl', nrows=50)


class TestDFCleaner(unittest.TestCase):
    """
    A class for unit-testing function in the clean_df.py file

    Args:
        -----
        unittest.TestCase this allows the new class to inherit
        from the unittest module

    """

    def __init__(self):
        self.df = CleanDataframe(df)

    def test_drop_unwanted_columns(self):
        self.assertEqual(len(self.df.drop_unwanted_columns().columns), 44)

    def test_fix_datatypes(self):
        self.assertEqual(self.df.fix_data_types()['Handset Manufacturer'][:7],
                         ['Samsung', 'Samsung', 'Samsung', 'Undefined', 'Samsung', 'Undefined', 'Huawei'])


if __name__ == '__main__':
    unittest.main()
