import argparse
import sys
import os
import re
import datetime
import my_pkg.util as util
import my_pkg.qs as qs
import my_pkg.report as report

import pdb
br = pdb.set_trace

def build_args():
    desc = '''
    Usage 1: python history.py -q questions -c chats -o out-hist-qst
    Usage 2: python history.py -q questions -c chats -o out-hist-mrg --merge    
    Usage 3: python history.py -q questions -c chats -o out-hist-mrg -t out-hist-mrg-txt --merge        
    Usage 4: python history.py -c chats -o out-hist-cht
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
            help='A directory that contains answers in MD files by date. E.g., "out-hist-mrg"')

    parser.add_argument(
            '-t',
            dest='output_text',
            help='A directory that contains only questions in TXT files by date. E.g., "out-hist-mrg-txt"')

    parser.add_argument(
            '--merge',
            dest='merge',
            action='store_true',
            help='Enable to merge questions and chats')

    #
    # Check arguments and return.
    #

    args = parser.parse_args()

    return args

def get_questions(questions_dn, chats_dn):

    #
    # Get all question set files to build question_ls
    #

    question_ls = []
    bn_fn_ls = util.get_files(questions_dn)
    for bn, fn in bn_fn_ls:
        print(fn)

        lines = util.read_lines(fn)
        chat, date, sections = qs.parse_context(lines)

        #
        # Read sections to build section_ls.
        #       section_ls = [section]
        #       section = {'sec_title', 'question_ls'}
        #       question_ls = [question]
        #       question = {'q1', ...'date', ...}
        #

        section_ls = qs.read_sections(sections, bn, chat, date)

        #
        # Check section_ls
        #

        qs.check_sections(section_ls)

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
        fn = os.path.join(chats_dn, question['from'])

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
        util.find_answer(chats_dn, fn_qa_ls_d, question)

    return question_ls

def transform_to_question(qa, title):
    question = qs.build_question(None)
    question['q1'] = qa['q']
    question['q2'] = qa['q']
    question['is_short'] = qa['is_short']
    question['from'] = title
    question['q_date'] = qa['create_time'][:10]
    question['q_time'] = qa['create_time'][11:]
    question['sec_title'] = None
    question['a'] = qa['a']
    question['guid'] = qa['guid']

    return question

def build_chats(chats_dn):

    #
    # For each chat file, get qa_ls and transform it into questions
    #

    out = []
    bn_fn_ls = util.get_files(chats_dn)
    for bn, fn in bn_fn_ls:
        qa_ls = util.parse_chat(fn)
        for qa in qa_ls:
            #title, _ = util.get_name(bn)
            title = bn
            question = transform_to_question(qa, title)
            out.append(question)

    return out

def get_solo_chats(question_ls, chats_dn):
    print('Number of questions  : %d' % len(question_ls))

    out = []

    dup_count = 0
    guid_set = set()                     # The guid may be duplicated.
    for question in question_ls:
        guid = question['guid']
        if guid in guid_set:
            print('Duplicated question: %s' % question['q1'])
            dup_count += 1

        guid_set.add(guid)
    print('Number of duplicated : %d' % dup_count)

    chat_ls = build_chats(chats_dn)
    print('Number of chats      : %d' % len(chat_ls))

    for chat in chat_ls:
        if chat['guid'] not in guid_set:
            out.append(chat)

    print('Number of solo chats : %d' % len(out))

    assert len(question_ls) - dup_count + len(out) == len(chat_ls)

    return out 

def build_group_by_date(question_ls):
    out = {}
    for question in question_ls:
        date = question['q_date']
        if date not in out:
            out[date] = [] 

        out[date].append(question)

    return out

def get_title(question):
    if question['sec_title'] == None:
        title = '%s' % (question['from'])
    else:
        title = '%s ```(%s)```' % (question['sec_title'], question['qs'])

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
        section = {'sec_title': title, 'question_ls': title_question_ls_d[title]}
        section_ls.append(section)

    for section in section_ls:
        question_ls = section

    return section_ls

def get_section_ls_order_by_time(question_ls):
    question_ls = sorted(question_ls, key=lambda x: x['q_time'])
    section_ls = build_sections_by_title(question_ls)    
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
    # If use -t, check if the output_text directory exists.
    # If not, make it.
    #

    if args.output_text != None:
        if not os.path.exists(args.output_text):
            print('The directory does not exist.')
            print('Making it.')
            print(args.output_text)
            os.mkdir(args.output_text)

    #
    # If use -q, build question_ls from questions with answers from chats.
    #

    question_ls = []
    chat_ls = []

    if args.questions:
        question_ls = get_questions(args.questions, args.chats)

        if args.merge:
            chat_ls = get_solo_chats(question_ls, args.chats)

    #
    # Else, build question_ls form chats.
    #

    else:
        chat_ls = build_chats(args.chats)

    #
    # Build date_question_ls_d[date] = question_ls
    # build date_chat_ls_d[date] = chat_ls
    #

    date_question_ls_d = build_group_by_date(question_ls)
    date_chat_ls_d = build_group_by_date(chat_ls)

    #
    # Build date_set.
    # 

    date_ls = list(date_question_ls_d.keys()) + list(date_chat_ls_d.keys())
    date_set = set(date_ls)

    #
    # Build history
    #

    for date in sorted(date_set):
        print(date)

        q_section_ls = []
        if date in date_question_ls_d:
            q_section_ls = get_section_ls_order_by_time(date_question_ls_d[date])

        c_section_ls = []
        if date in date_chat_ls_d:
            c_section_ls = get_section_ls_order_by_time(date_chat_ls_d[date])


        fn_history = os.path.join(args.output, '%s.md' % date)

        fn_history_txt = None 
        if args.output_text:
             fn_history_txt = os.path.join(args.output_text, '%s.txt' % date)

        report.write_sections(q_section_ls, c_section_ls, fn_history, dis_date = False, dis_q_date=False, dis_q_time=True)
        if args.output_text:
            report.write_sections_in_text(q_section_ls, c_section_ls, fn_history_txt, dis_date = False, dis_q_date=False, dis_q_time=True)


if __name__ == '__main__':
    main()
