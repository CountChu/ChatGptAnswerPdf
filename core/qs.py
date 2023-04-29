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
import pdb

br = pdb.set_trace

#
# Private functions.
#

def _build_question(qs_name):
    question = {'hide': False, 'error': False, 'qs': qs_name}
    return question

def read_section(section, qs_name, default_chat, default_date):
    
    out = {} 
    out['title'] = section['title'] 

    question_ls = []    
    s = None
    for line in section['lines']:
        line = line.strip()

        if line.startswith('q:'):
            s = 'q'
        elif line.startswith('q-prefix:'):
            s = 'q-prefix'
        elif line.startswith('a-prefix:'):
            s = 'a-prefix'
        elif line.startswith('from:'):
            s = 'from'
        elif line.startswith('hide:'):
            s = 'hide'
        elif line.startswith('d:'):
            s = 'date'            
        elif line.startswith('title:'):
            s = 'q_title'  
        elif line.startswith('error:'):
            s = 'error'  
        else:
            assert False, f'{s} | {line}'

        print('%10s | %s' % (s, line))

        if s == 'q':
            _, line = line.split(':', 1)
            line = line.strip()
            q1 = line 
            q2 = line.replace('_', '\\_')
            
            question = _build_question(qs_name)
            question['q1'] = q1
            question['q2'] = q2 

            if default_date != None:
                question['date'] = default_date

            if 'from' not in question:
                question['from'] = default_chat

            question_ls.append(question)

        elif s == 'q-prefix':
            _, line = line.split(':', 1)
            line = line.strip()
            q1_prefix = line
            q2_prefix = line.replace('_', '\\_')

            question = _build_question(qs_name)
            question['q1-prefix'] = q1_prefix
            question['q2-prefix'] = q2_prefix
            
            if default_date != None:
                question['date'] = default_date

            if 'from' not in question:
                question['from'] = default_chat                

            question_ls.append(question)

        elif s == 'a-prefix':
            _, line = line.split(':', 1)
            line = line.strip()
            question['a-prefix'] = line

        elif s == 'from':
            _, line = line.split(':', 1)
            line = line.strip()
            question['from'] = line

        elif s == 'hide':
            question['hide'] = True  

        elif s == 'error':
            question['error'] = True                  

        elif s == 'date':
            _, line = line.split(':', 1)
            line = line.strip()
            question['date'] = line

        elif s == 'q_title':
            _, line = line.split(':', 1)
            line = line.strip()
            question['q_title'] = line            

        else:
            assert False, s

    #
    # Assign sec_title.
    #

    for question in question_ls:
        question['sec_title'] = section['title']

    out['question_ls'] = question_ls

    return out

#
# Public functions.
#

def parse(lines):
    out_from = None 
    out_date = None    
    out_sec_ls = []                     # out_sec_ls = [{title, lines}] 

    s = 'init'                          # init, head, sec-title, sec-content

    sec = None
    for line in lines:
        s_line = line.strip()
        if s_line == '':
            continue 

        if s_line[0] == '#':
            continue 

        if s == 'init':
            if line[0] != ' ':
                if line.find(':') == -1:
                    s = 'sec-title'
                else:
                    s = 'head'

            else:
                assert False, f'{s} | {line}'

        elif s == 'head':
            if line[0] != ' ':
                if line.find(':') != -1:
                    s = 'head'
                else:
                    s = 'sec-title'
            else:
                assert False, f'{s} | {line}'

        elif s in ['sec-title', 'sec-content']:
            if line[0] != ' ':
                s = 'sec-title'
            else:
                s = 'sec-content'

        else:
            assert False, f'{s} | {line}'

        print('%20s | %s' % (s, line))

        if s == 'init':
            pass

        elif s == 'head':
            if line.startswith('from:'):
                _, out_from = line.split(':', 1)
                out_from = out_from.strip()

            elif line.startswith('d:'):
                _, out_date = line.split(':', 1)
                out_date = out_date.strip()

            else:
                assert False, f'{s} | {line}'

        elif s == 'sec-title':
            if sec != None:
                 out_sec_ls.append(sec)

            sec = {'title': line.strip(), 'lines': []}

        elif s == 'sec-content':
            sec['lines'].append(line.strip())

        else:
            assert False, f'{s} | {line}'

    if sec != None:
        out_sec_ls.append(sec)

    return out_from, out_date, out_sec_ls

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

def read_sections(sections, qs_name, default_chat, default_date):

    sec_ls = []
    for section in sections:
        sec = read_section(section, qs_name, default_chat, default_date)
        sec_ls.append(sec)

    return sec_ls

def check_sections(section_ls):
    for section in section_ls:
        for question in section['question_ls']:
            assert not ('q1' in question and 'q1-prefix' in question)
            assert 'from' in question
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

