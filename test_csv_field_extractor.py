import unittest
import pandas as pd
import tempfile
import os
from io import StringIO
from unittest.mock import patch
from csv_field_extractor import extract_field_from_csv, main


class TestCSVFieldExtractor(unittest.TestCase):

    def setUp(self):
        """Create a temporary CSV file for testing"""
        self.test_data = {
            'Symbol': ['ARKK', 'ARKF', 'ARKG', '', 'ARKQ'],
            'Description': ['Innovation ETF', 'Fintech ETF', 'Genomics ETF',
                            'Empty Row', 'Robotics ETF'],
            'Net Expense Ratio': ['0.75%', '0.75%', '0.75%', '', '0.75%']
        }

        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv',
                                                     delete=False)
        df = pd.DataFrame(self.test_data)
        df.to_csv(self.temp_file.name, index=False)
        self.temp_file.close()

    def tearDown(self):
        """Clean up temporary file"""
        os.unlink(self.temp_file.name)

    def test_extract_basic_field(self):
        """Test basic field extraction"""
        symbols = extract_field_from_csv(self.temp_file.name, 'Symbol')
        expected = ['ARKK', 'ARKF', 'ARKG', 'ARKQ']
        self.assertEqual(symbols, expected)

    def test_extract_with_sorting(self):
        """Test field extraction with alphabetical sorting"""
        symbols = extract_field_from_csv(self.temp_file.name, 'Symbol',
                                         sort_alphabetically=True)
        expected = ['ARKF', 'ARKG', 'ARKK', 'ARKQ']
        self.assertEqual(symbols, expected)

    def test_extract_nonexistent_field(self):
        """Test that ValueError is raised for nonexistent field"""
        with self.assertRaises(ValueError) as context:
            extract_field_from_csv(self.temp_file.name, 'NonExistentField')

        self.assertIn('NonExistentField', str(context.exception))
        self.assertIn('Available fields', str(context.exception))

    def test_extract_different_field_types(self):
        """Test extracting different types of fields"""
        descriptions = extract_field_from_csv(self.temp_file.name,
                                              'Description')
        expected = ['Innovation ETF', 'Fintech ETF', 'Genomics ETF',
                    'Empty Row', 'Robotics ETF']
        self.assertEqual(descriptions, expected)

    def test_nonexistent_file(self):
        """Test that appropriate error is raised for nonexistent file"""
        with self.assertRaises(FileNotFoundError):
            extract_field_from_csv('nonexistent_file.csv', 'Symbol')


class TestCLI(unittest.TestCase):

    def setUp(self):
        """Create a temporary CSV file for CLI testing"""
        self.test_data = {
            'Symbol': ['ARKK', 'ARKF', 'ARKG', 'ARKQ'],
            'Description': ['Innovation ETF', 'Fintech ETF', 'Genomics ETF',
                            'Robotics ETF']
        }

        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv',
                                                     delete=False)
        df = pd.DataFrame(self.test_data)
        df.to_csv(self.temp_file.name, index=False)
        self.temp_file.close()

    def tearDown(self):
        """Clean up temporary file"""
        os.unlink(self.temp_file.name)

    def test_cli_basic_output(self):
        """Test basic CLI functionality"""
        test_args = ['csv_field_extractor.py', self.temp_file.name,
                     'Symbol']
        with patch('sys.argv', test_args):
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                result = main()
                output = fake_stdout.getvalue().strip().split('\n')

        self.assertEqual(result, 0)
        self.assertEqual(output, ['ARKK', 'ARKF', 'ARKG', 'ARKQ'])

    def test_cli_sorted_output(self):
        """Test CLI with sorting"""
        test_args = ['csv_field_extractor.py', self.temp_file.name, 'Symbol',
                     '--sort']
        with patch('sys.argv', test_args):
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                result = main()
                output = fake_stdout.getvalue().strip().split('\n')

        self.assertEqual(result, 0)
        self.assertEqual(output, ['ARKF', 'ARKG', 'ARKK', 'ARKQ'])

    def test_cli_comma_output(self):
        """Test CLI with comma-separated output"""
        test_args = ['csv_field_extractor.py', self.temp_file.name, 'Symbol',
                     '--output', 'comma']
        with patch('sys.argv', test_args):
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                result = main()
                output = fake_stdout.getvalue().strip()

        self.assertEqual(result, 0)
        self.assertEqual(output, 'ARKK,ARKF,ARKG,ARKQ')

    def test_cli_space_output(self):
        """Test CLI with space-separated output"""
        test_args = ['csv_field_extractor.py', self.temp_file.name, 'Symbol',
                     '--output', 'space']
        with patch('sys.argv', test_args):
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                result = main()
                output = fake_stdout.getvalue().strip()

        self.assertEqual(result, 0)
        self.assertEqual(output, 'ARKK ARKF ARKG ARKQ')

    def test_cli_nonexistent_file(self):
        """Test CLI error handling for nonexistent file"""
        test_args = ['csv_field_extractor.py', 'nonexistent.csv', 'Symbol']
        with patch('sys.argv', test_args):
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                result = main()
                output = fake_stdout.getvalue().strip()

        self.assertEqual(result, 1)
        self.assertIn('File \'nonexistent.csv\' not found', output)

    def test_cli_invalid_field(self):
        """Test CLI error handling for invalid field name"""
        test_args = ['csv_field_extractor.py', self.temp_file.name,
                     'InvalidField']
        with patch('sys.argv', test_args):
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                result = main()
                output = fake_stdout.getvalue().strip()

        self.assertEqual(result, 1)
        self.assertIn('InvalidField', output)
        self.assertIn('Available fields', output)


if __name__ == '__main__':
    unittest.main()
