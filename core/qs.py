#
# FILENAME.
#       qs.py - Question Set Python Module.
#
# FUNCTIONAL DESCRIPTION.
#       The package parses the question set TXT file.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2023/4/22
#       Updated on 2023/4/29
#

import sys
import yaml
import os
import pdb

br = pdb.set_trace

#
# Private functions.
#

def build_question(default_chat, default_date, sec_chat, qst):
    question = {'hide': False, 'error': False}

    if default_chat != None:
        question['from'] = default_chat

    if default_date != None:
        question['date'] = default_date

    if sec_chat != None:
        question['from'] = sec_chat

    if 'q' in qst:
        q1 = qst['q']
        q2 = q1.replace('_', '\\_')

        question['q1'] = q1 
        question['q2'] = q2 

    if 'q-prefix' in qst:
        q1_prefix = qst['q-prefix']
        q2_prefix = q1_prefix.replace('_', '\\_')

        question['q1-prefix'] = q1_prefix 
        question['q2-prefix'] = q2_prefix 

    if 'a-prefix' in qst:
        question['a-prefix'] = qst['a-prefix']

    if 'from' in qst:
        question['from'] = qst['from']

    if 'd' in qst:
        question['date'] = qst['d']        

    if 'hide' in qst:
        question['hide'] = True

    if 'error' in qst:
        question['error'] = True

    if 'title' in qst:
        question['q_title'] = qst['title']

    return question

#
# Public functions.
#

#
# section_ls = [section]
# section = {'title', 'question_ls'}
# question_ls = [question]
# question = {
#       'q1', 'q2', 'q1-prefix', 'q2-prefix', 'a-prefix', 
#       'from', 'hide', 'date', 'qs', 'error', 
#       'sec_title', 'q_title',
#       'q_date', 'q_time'}
#   qs: question set
#    
#
# q1 = https://en.wikipedia.org/wiki/Trusted_execution_environment
# q2 = https://en.wikipedia.org/wiki/Trusted\_execution\_environment
#    

def parse(fn):
    f = open(fn)
    y = yaml.load(f, Loader=yaml.loader.SafeLoader)
    f.close()

    qs_name = os.path.basename(fn)

    default_chat = None 
    default_date = None 

    if 'from' in y:
        default_chat = y['from']
        del y['from']

    if 'd' in y:
        default_date = y['d']
        del y['d']

    section_ls = []
    for sec_title, sec in y.items():
        section = {}
        section['title'] = sec_title
        
        sec_chat = None 
        if 'from' in sec:
            sec_chat = sec['from']
        
        question_ls = []
        for qst in sec['questions']:
            question = build_question(default_chat, default_date, sec_chat, qst)
            question['qs'] = qs_name
            question['sec_title'] = sec_title
            question['is_short'] = False

            question_ls.append(question)
        
        section['question_ls'] = question_ls

        section_ls.append(section)

    return section_ls

def check_sections(section_ls):
    for section in section_ls:
        for question in section['question_ls']:
            assert not ('q1' in question and 'q1-prefix' in question)
            assert 'from' in question, question
            assert question['from'] != None
            assert 'qs' in question
            assert 'sec_title' in question

def dump_sections(section_ls):
    for section in section_ls:
        print(section['title'])

        for question in section['question_ls']:
            if 'q1' in question:
                print('    q: %s' % question['q1'])
            elif 'q1-prefix' in question:
                print('    q1-prefix: %s' % question['q1-prefix'])

            if 'a-prefix' in question:
                print('    a-prefix: %s' % question['a-prefix'])

            if 'from' in question:
                print('    from: %s' % question['from'])

        print('')

