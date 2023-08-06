import os
import sys
from pathlib import Path
from unittest import TestCase

import enilm


class TestContext(TestCase):
    def setUp(self) -> None:
        self.file_path = Path('log.txt')

    def tearDown(self) -> None:
        os.remove(self.file_path)

    def test_redirect_stdout_file(self):
        with enilm.context.sec(redirect_stdout_file=self.file_path, n_spaces=0):
            print('This should be written to the file')

        self.assertEqual(self.file_path.read_text(), 'This should be written to the file\n')

    # def test_print_with_mem(self):
    #     with enilm.context.sec(mem=True):
    #         print('Something...')


'''
test_print_sec = False
test_print_with_mem = False
test_nested_sections = True


if test_print_sec:
    with sec('Test Section'):
        print('foo')
        print('bar')

    """
    Test Section
      foo
      bar
    """

if test_nested_sections:
    print('foo')
    with sec('first level'):
        print('in first level')
        with sec('second level'):
            print('in second leve')
            print('in second leve')
        print('in first level')
    print('bar')
'''
