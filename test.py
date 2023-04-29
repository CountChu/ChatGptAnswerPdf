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

    def test_parse(self):
        fn_qs = os.path.join('user-Alice', 'questions', '230327.OP-TEE.txt')

        lines = qs.read_lines(fn_qs)
        
        from_chat, date, sections = qs.parse(lines)

        self.assertEqual(from_chat, 'OP-TEE.0327.md')
        self.assertEqual(date, '2023/4/1')
        self.assertEqual(len(sections), 15)
        self.assertEqual(sections[0]['title'], 'Basic Concepts')
        self.assertEqual(sections[-1]['title'], 'PKCS#11')

        qs_name = os.path.basename(fn_qs)
        section_ls = qs.read_sections(sections, qs_name, from_chat, date)   
        self.assertEqual(len(section_ls), 15)

        section = section_ls[0]
        self.assertEqual(section['title'], 'Basic Concepts')
        self.assertEqual(len(section['question_ls']), 10)

        question = section['question_ls'][9]
        self.assertEqual(question['q_title'], 'What is OP-TEE Dispatcher?')
        self.assertEqual(question['date'], '2023/4/13')

        qs.check_sections(section_ls)

if __name__ == '__main__':
    unittest.main()