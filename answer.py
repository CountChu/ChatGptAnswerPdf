import argparse
import sys
import os
import re
import datetime
from core import util, qs, report

import pdb
br = pdb.set_trace

def build_args():
    desc = '''
    Usage 1: python answer.py -q "questions/230328 TEE.txt" -c "chats" -a "out-ans"
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
            help='A directory that contains answers in MD format. E.g., "out-ans"')    

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

    lines = util.read_lines(args.questions)

    #
    # Parse lines.
    #

    chat, date, sections = qs.parse(lines)

    #
    # Read sections
    #

    qs_name = os.path.basename(args.questions)
    section_ls = qs.read_sections(sections, qs_name, chat, date)

    #
    # Check section_ls
    #

    qs.check_sections(section_ls)

    #
    # Dump section_ls to check.
    #

    if not args.silence:
        qs.dump_sections(section_ls)

    #
    # Build fn_qa_ls_d
    # fn_qa_ls_d[fn] = qa_ls
    #

    fn_qa_ls_d = {}

    for section in section_ls:
        for question in section['question_ls']:
            fn = os.path.join(args.chats, question['from'])
            
            if not os.path.exists(fn):
                print('Error! The file does not exist.')
                print(fn)
                sys.exit(1)

            if fn not in fn_qa_ls_d:
                qa_ls = util.parse_chat(fn)
                fn_qa_ls_d[fn] = qa_ls

    #
    # Find answers.
    #

    for section in section_ls:
        for question in section['question_ls']:
            util.find_answer(args.chats, fn_qa_ls_d, question)

    #
    # Write new_chat_ls
    #

    print('Write: %s' % fn_answer)
    report.write_sections(section_ls, [], fn_answer, dis_date=True, dis_q_date=False, dis_q_time=False)

if __name__ == '__main__':
    main()
