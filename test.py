#
# FILENAME.
#       test.py - Python Unitest Module.
#
# FUNCTIONAL DESCRIPTION.
#       The moudle run unitest.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2023/4/29
#

import unittest
import os
import pdb

from core import qs, util

br = pdb.set_trace

class TestQsModule(unittest.TestCase):

    def test_parse_1(self):
        qs_fn = os.path.join('user-Alice', 'questions', '230327.OP-TEE.yaml')
        
        section_ls = qs.parse(qs_fn)
        qs.check_sections(section_ls)           

        self.assertEqual(len(section_ls), 15)

        section = section_ls[0]
        self.assertEqual(section['title'], 'Basic Concepts')
        self.assertEqual(len(section['question_ls']), 10)     
        
        question = section['question_ls'][9]
        self.assertEqual(question['q_title'], 'What is OP-TEE Dispatcher?')
        self.assertEqual(question['date'], '2023/4/13')


    def test_parse_2(self):
        qs_fn = os.path.join('user-Alice', 'questions', '230330.Questions.yaml')

        section_ls = qs.parse(qs_fn)
        qs.check_sections(section_ls)           

        self.assertEqual(len(section_ls), 4)

        section = section_ls[0]
        self.assertEqual(section['title'], 'Intel KGT & Intel SGX')

        question_ls = section['question_ls']
        self.assertEqual(question_ls[0]['from'], 'OP-TEE.Intel.0330.md')

        section = section_ls[3]
        self.assertEqual(section['title'], 'Development')

        question_ls = section['question_ls']
        self.assertEqual(question_ls[0]['from'], 'TEE.0328.md')
        self.assertEqual(question_ls[1]['from'], 'OP-TEE.0327.md')
        self.assertEqual(question_ls[2]['from'], 'OP-TEE.0327.md')

if __name__ == '__main__':
    unittest.main()