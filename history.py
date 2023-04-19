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
    Usage 1: python history.py -q questions -c chats -o out-qst
    Usage 2: python history.py -c chats -o out-cht
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
            help='A directory that contains question set files. E.g., "questions"')

    parser.add_argument(
            '-c',
            dest='chats',
            help='A directory that contains original MD files from ChatGPT. E.g., "chats"')

    parser.add_argument(
            '-o',
            dest='output',
            required=True,
            help='A directory that contains answers in MD files by date. E.g., "output-hist"')

    #
    # Check arguments and return.
    #

    args = parser.parse_args()

    return args

def transform_to_question(qa, title):
    question = {}
    question['q1'] = qa['q']
    question['q2'] = qa['q']
    question['is_short'] = qa['is_short']
    question['from'] = title
    question['hide'] = False
    question['q_date'] = qa['create_time'][:10]
    question['q_time'] = qa['create_time'][11:]
    question['qs'] = None
    question['title'] = None
    question['a'] = qa['a']

    return question

def get_title(question):
    if question['title'] == None:
        title = '%s' % (question['from'])
    else:
        title = '%s @ %s' % (question['title'], question['from'])

    return title

def build_sections_by_title(question_ls):
    sorted_title_ls = []
    for question in question_ls:
        title = get_title(question)
        if title not in sorted_title_ls:
            sorted_title_ls.append(title)

    title_question_ls_d = {}
    for question in question_ls:
        title = get_title(question)
        if title not in title_question_ls_d:
            title_question_ls_d[title] = []

        title_question_ls_d[title].append(question)

    section_ls = []
    for title in sorted_title_ls:
        section = {'title': title, 'question_ls': title_question_ls_d[title]}
        section_ls.append(section)

    for section in section_ls:
        question_ls = section

    return section_ls

def main():

    #
    # Read arguments.
    #

    args = build_args()

    #
    # If use -q, check if the questions directory exists.
    #

    if args.questions != None:
        if not os.path.exists(args.questions):
            print('Error! The directory does not exist.')
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
    # Check if the output directory exists.
    # If not, make it.
    #

    if not os.path.exists(args.output):
        print('The directory does not exist.')
        print('Making it.')
        print(args.output)
        os.mkdir(args.output)

    #
    # If use -q
    #

    if args.questions:

        #
        # Get all question set files to build question_ls
        #

        question_ls = []
        bn_fn_ls = util.get_files(args.questions)
        for bn, fn in bn_fn_ls:
            print(fn)

            lines = util.read_lines(fn)
            chat, date, sections = util.parse_context(lines)

            #
            # Read sections to build section_ls.
            #       section_ls = [section]
            #       section = {'title', 'question_ls'}
            #       question_ls = [question]
            #       question = {'q1', ...'date', ...}
            #

            section_ls = util.read_sections(sections, bn, chat, date)

            #
            # Check section_ls
            #

            util.check_sections(section_ls)

            #
            # Build question_ls
            #

            for section in section_ls:
                question_ls += section['question_ls']

        #
        # Build fn_qa_ls_d
        # fn_qa_ls_d[fn] = qa_ls
        #

        fn_qa_ls_d = {}
        for question in question_ls:
            fn = os.path.join(args.chats, question['from'])

            if not os.path.exists(fn):
                print('Error! The file does not exist.')
                print(fn)
                sys.exit(1)

            if fn not in fn_qa_ls_d:
                qa_ls = util.parse_chat(fn)
                fn_qa_ls_d[fn] = qa_ls

        #
        # Find aswer for each question in question_ls
        #

        for question in question_ls:
            util.find_answer(args.chats, fn_qa_ls_d, question)

    else:

        #
        # For each chat file, get qa_ls and transform it into questions
        #

        question_ls = []
        bn_fn_ls = util.get_files(args.chats)
        for bn, fn in bn_fn_ls:
            qa_ls = util.parse_chat(fn)
            for qa in qa_ls:
                title, _ = util.get_name(bn)
                question = transform_to_question(qa, title)
                question_ls.append(question)

    #
    # Build date_question_ls_d[date] = question_ls
    #

    date_question_ls_d = {}
    for question in question_ls:
        date = question['q_date']
        if date not in date_question_ls_d:
            date_question_ls_d[date] = [] 

        date_question_ls_d[date].append(question)

    #
    # Build history
    #

    for date in sorted(date_question_ls_d.keys()):
        print(date)

        #
        # Get question_ls by date and sort it by time.
        #

        question_ls = date_question_ls_d[date]
        question_ls = sorted(question_ls, key=lambda x: x['q_time'])

        section_ls = build_sections_by_title(question_ls)
        fn_history = os.path.join(args.output, '%s.md' % date)
        util.write_sections(section_ls, fn_history, dis_date = False, dis_q_date=False, dis_q_time=True)

if __name__ == '__main__':
    main()
