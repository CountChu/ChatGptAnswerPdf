#
# Question Set Package
#

import sys
import pdb

br = pdb.set_trace

def parse_context(lines):

    chat = None 
    date = None

    while True:
        if lines[0].startswith('from:'):
            _, chat = lines[0].split(':', 1)
            chat = chat.strip() 
            lines.pop(0)

        elif lines[0].startswith('d:'):
            _, date = lines[0].split(':', 1)
            date = date.strip() 
            lines.pop(0)            

        elif lines[0].strip() == '':
            lines.pop(0)

        else:
            break 

    sections = lines 

    return chat, date, sections

def build_question(qs_name):
    question = {'hide': False, 'error': False, 'qs': qs_name}
    return question

#
# section_ls = [section]
# section = {'sec_title', 'question_ls'}
# question_ls = [question]
# question = {
#       'q1', 'q2', 'q1-prefix', 'q2-prefix', 'a-prefix', 
#       'from', 'hide', 'date', 'qs', 'error', 
#       'sec_title', 'q_title',
#       'q_date', 'q_time'}
#   qs: question set
#    

# q1 = https://en.wikipedia.org/wiki/Trusted_execution_environment
# q2 = https://en.wikipedia.org/wiki/Trusted\_execution\_environment
#

def read_sections(lines, qs_name, default_chat, default_date):
    section_ls = []

    section = None
    question = None
    s = None                            # s: sec_title, q, a-prefix
    for line in lines:
        line = line.strip()
        if line == '':
            continue

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
            s = 'sec_title'

        if s == 'q':
            _, line = line.split(':', 1)
            line = line.strip()
            q1 = line 
            q2 = line.replace('_', '\\_')
            
            question = build_question(qs_name)
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

            question = build_question(qs_name)
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

        elif s == 'sec_title':
            if line.find(':') >= 0:
                print('Error! line = %s' % line)
                print('qs_name = %s' % qs_name)
                sys.exit(1) 

            if section != None:
                section['question_ls'] = question_ls
                section_ls.append(section)

            section = {} 
            section['sec_title'] = line 
            question_ls = []

        else:
            assert False, s

    if section != None:
        section['question_ls'] = question_ls
        section_ls.append(section)

    #
    # Remember title in each question and set is_short
    #    

    for section in section_ls:
        for question in section['question_ls']:
            question['sec_title'] = section['sec_title']
            question['is_short'] = False

    return section_ls


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
        print(section['sec_title'])

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

