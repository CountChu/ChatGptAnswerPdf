import argparse
import sys
import os
import re
import datetime
import util

import pdb
br = pdb.set_trace

def build_args():
    desc = '''
    Usage 1: python answer.py -q "questions/230328 TEE.txt" -c "chats" -a "output"
'''
    #
    # Build an ArgumentParser object to parse arguments.
    #

    parser = argparse.ArgumentParser(
                formatter_class=argparse.RawTextHelpFormatter,
                description=desc)

    parser.add_argument(
            '-q',
            dest='questions',
            required=True,
            help='E.g., "questions/230328 OP-TEE.txt"')    

    parser.add_argument(
            '-c',
            dest='chats',
            help='A directory that contains original MD files from ChatGPT. E.g., "chats"')     

    parser.add_argument(
            '-a',
            dest='answers',
            required=True,
            help='A directory that contains answers in MD format. E.g., "output/230328 OP-TEE.md"')    

    parser.add_argument(
            '-s',
            dest='silence',
            action='store_true',
            help='To display less messages.')    

    #
    # Check arguments and return.
    #

    args = parser.parse_args()

    return args  

def parse_context(lines):

    if not lines[0].startswith('from:'):
        chat = None 
        sections = lines 

    else:
        _, chat = lines[0].split(':', 1)
        chat = chat.strip()

        sections = lines[1:]

    return chat, sections

#
# section_ls = [section]
# section = {'title', 'question_ls'}
# question_ls = [question]
# question = {'q1', 'q2', 'q-prefix', 'a-prefix', 'from'}
#    
# q1 = https://en.wikipedia.org/wiki/Trusted_execution_environment
# q2 = https://en.wikipedia.org/wiki/Trusted\_execution\_environment
#

def read_sections(lines):
    section_ls = []

    section = None
    question = None
    s = None                            # s: title, q, a-prefix
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
        else:
            s = 'title'

        if s == 'q':
            _, line = line.split(':', 1)
            line = line.strip()
            q1 = line 
            q2 = line.replace('_', '\\_')
            question = {'q1': q1, 'q2': q2, 'hide': False}
            question_ls.append(question)

        elif s == 'q-prefix':
            _, line = line.split(':', 1)
            line = line.strip()
            question = {'q-prefix': line}
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

        elif s == 'title':
            if section != None:
                section['question_ls'] = question_ls
                section_ls.append(section)

            section = {} 
            section['title'] = line 
            question_ls = []

        else:
            assert False, s

    if section != None:
        section['question_ls'] = question_ls
        section_ls.append(section)
    
    return section_ls

def dump_sections(section_ls):
    for section in section_ls:
        print(section['title'])

        for question in section['question_ls']:
            if 'q1' in question:
                print('    q: %s' % question['q1'])
            elif 'q-prefix' in question:
                print('    q-prefix: %s' % question['q-prefix'])

            if 'a-prefix' in question:
                print('    a-prefix: %s' % question['a-prefix'])

            if 'from' in question:
                print('    from: %s' % question['from'])

        print('')

def read_qa_ls(fn):
    f = open(fn, encoding='utf-8')
    s = 'init'   # s: init, q, a

    q = []
    a = []
    qa_ls = []
    for line in f:
        line = line.rstrip()

        if s == 'init':
            if line == '**You:**':
                s = 'q'
            elif line == '**ChatGPT:**':
                print('Error. s = %s', s)
                sys.exit(1)

        elif s == 'q':
            if line == '**ChatGPT:**':
                s = 'a'
            elif line == '**You:**':
                print('Error. s = %s', s)
                sys.exit(1)

        elif s == 'a':
            if line == '**You:**':
                s = 'q'
            elif line == '**ChatGPT:**':
                print('Error. s = %s', s)
                sys.exit(1)             

        else:
            print('Error. s = %s', s)
            sys.exit(1)

        #print('%10s | %s' % (s, line))  

        if s == 'q':
            if line == '* * *':
                pass
            else:
                q.append(line)
        elif s == 'a':
            if line == '* * *':
                qa_ls.append((q, a))
                q = []
                a = []
            else:
                a.append(line)

    if len(q) != 0:
        assert len(a) != 0 
        qa_ls.append((q, a))

    return qa_ls

def remove_empty_lines_from_head_and_tail(lines):    
    while True:
        if lines[0].strip() == '':
            lines.pop(0)
        else:
            break

    while True: 
        if lines[-1].strip() == '':
            lines.pop(-1)
        else:
            break

#
#   Fix the problem:
#
#   1.  TEE Management APIs:
#    
#       *   Enclave or secure world creation and destruction
#       *   Resource management, such as memory allocation and deallocation
#       *   Context switching between the secure and non-secure worlds
#   2.  Cryptographic APIs:
#

def refine_md_1(lines):
    new_lines = []
    for i in range(len(lines)):
        line = lines[i]
        new_lines.append(line)
        if line.startswith('    * '):
            if i <= len(lines) - 2:
                next_line = lines[i+1]
                match = re.match(r"\d\.\s", next_line)
                if match:
                    new_lines.append('')

    return new_lines

def build_qa(q, a):

    for i in range(len(q)):
        if q[i] == '**You:**':
            q[i] = ''
    remove_empty_lines_from_head_and_tail(q)
    assert len(q) == 1, q
    q2 = q[0]


    for i in range(len(a)):
        if a[i] == '**ChatGPT:**':
            a[i] = ''
    remove_empty_lines_from_head_and_tail(a)

    a = refine_md_1(a)

    qa = {'q2': q2, 'a': a}
    return qa

#
# Parse the chat file to build qa_ls
# qa_ls = [qa]
# qa = {'q2', 'a'}
#

def parse_chat(fn):

    org_qa_ls = read_qa_ls(fn)
    qa_ls = []
    for q, a in org_qa_ls:
        qa = build_qa(q, a)
        qa_ls.append(qa)

    return qa_ls

def find_answer(qa_ls, question):

    answer = None

    if 'a-prefix' in question:
        for qa in qa_ls:
            if qa['a'][0].startswith(question['a-prefix']):
                answer = qa['a'] 
                return answer

        if answer == None:
            print('Error. The answer of the question is not found.')
            print('q1 = %s' % question['q1'])
            print('q2 = %s' % question['q2'])
            print('a-prefix: %s' % question['a-prefix'])
            sys.exit(1)

    else:
        for qa in qa_ls:
            if 'q-prefix' in question:
                if qa['q2'].startswith(question['q-prefix']):
                    answer = qa['a']
                    break

            if 'q2' in question:
                if qa['q2'] == question['q2']:
                    answer = qa['a']
                    break

        if answer == None:
            print('Error. The answer of the question is not found.')
            
            if 'q1' in question:
                print('q1 = %s' % question['q1'])
                print('q2 = %s' % question['q2'])
            elif 'q-prefix' in question:
                print('q-prefix = %s' % question['q-prefix'])

            sys.exit(1)

    return answer

def write_sections(section_ls, name, fn):
    f = open(fn, 'w')

    f.write('# %s\n' % name)

    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    f.write('Created: %s\n' % (now_str))

    f.write('# Questions\n')
    for section in section_ls:
        #f.write('## %s\n' % section['title'])
        f.write('* %s\n' % section['title'])

        for question in section['question_ls']:
            if question['hide']:
                continue

            q = util.get_q(question)
            f.write('    * %s\n' % q)


    f.write('\n')
    f.write('---\n')
    f.write('\n')

    f.write('# Q & A\n')
    for section in section_ls:
        f.write('## %s\n' % section['title'])

        for question in section['question_ls']:
            if question['hide']:
                continue
            
            q = util.get_q(question)
            a = question['a']

            f.write('**Question:** %s\n' % q)
            f.write('\n')
            f.write('**Answer:**\n')
            f.write('\n')
            for line in a:
                f.write(line+'\n')
            f.write('\n')
            f.write('---\n')
            f.write('\n')

    f.close()


def main():

    #
    # Read arguments.
    #

    args = build_args()

    #
    # Check if the file of questions exists.
    #

    if not os.path.exists(args.questions):
        print('Error. The file does not exist.')
        print(args.questions)
        sys.exit(1)

    #
    # Check if the chats directory exists.
    #

    if not os.path.exists(args.chats):
        print('Error! The directory does not exist.')
        print(args.chats)
        sys.exit(1)

    #
    # Check if the answers directory exists.
    # If not, make it.
    #

    if not os.path.exists(args.answers):
        print('The directory does not exist.')
        print('Making it.')
        print(args.answers)
        os.mkdir(args.answers)

    #
    # Build fn_answer.
    #

    fn_answer, _ = util.get_name(args.questions)
    fn_answer = fn_answer + '.md'
    fn_answer = os.path.join(args.answers, fn_answer)

    #
    # Read context of the questions.
    #

    lines = []
    f = open(args.questions)
    for line in f:
        line = line.strip()
        if line == '':
            continue    
        lines.append(line)

    #
    # Parse lines.
    #

    chat, sections = parse_context(lines)

    #
    # Build default_qa_ls from the Markdown chat file.
    #

    default_qa_ls = None 

    if chat != None:
        chat_fn = os.path.join(args.chats, chat)
        if not os.path.exists(chat_fn):
            print('Error! The file does not exist.')
            print(chat_fn)
            sys.exit(1)

        default_qa_ls = parse_chat(chat_fn)

    #
    # Read sections
    #

    section_ls = read_sections(sections)

    #
    # Check section_ls
    #

    for section in section_ls:
        for question in section['question_ls']:
            assert not ('q1' in question and 'q-prefix' in question)

    #
    # Dump section_ls to check.
    #

    if not args.silence:
        dump_sections(section_ls)

    #
    # Build fn_qa_ls_d
    # fn_qa_ls_d[fn] = qa_ls
    #

    fn_qa_ls_d = {}

    for section in section_ls:
        for question in section['question_ls']:
            if 'from' not in question:
                continue 

            fn = os.path.join(args.chats, question['from'])
            
            if not os.path.exists(fn):
                print('Error! The file does not exist.')
                print(fn)
                sys.exit(1)

            if fn not in fn_qa_ls_d:
                qa_ls = parse_chat(fn)
                fn_qa_ls_d[fn] = qa_ls

    #
    # Build answers.
    #

    for section in section_ls:
        for question in section['question_ls']:
            if 'from' in question:
                fn = os.path.join(args.chats, question['from'])
                qa_ls = fn_qa_ls_d[fn]
                a = find_answer(qa_ls, question)
            else:
                assert default_qa_ls != None
                a = find_answer(default_qa_ls, question)
            
            question['a'] = a    

    #
    # Write new_chat_ls
    #

    print('Write: %s' % fn_answer)
    name, _ = util.get_name(fn_answer)

    write_sections(section_ls, name, fn_answer)

if __name__ == '__main__':
    main()
