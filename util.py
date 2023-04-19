import os
import sys
import datetime
import pdb

br = pdb.set_trace

def get_name(fn):
    name = os.path.basename(fn)
    name, ext = os.path.splitext(name)
    return name, ext

def collect_input_files(file, dn):
    bn_fn_ls = []

    if file != None:
        bn = file 
        fn = os.path.join(dn, bn)

        if not os.path.exists(fn):
            print('Error! The file does not exist.')
            print(fn)
            sys.exit(1)

        if not os.path.isfile(fn):
            print('Error! It is directory.')
            print(fn)
            sys.exit(1)

        bn_fn_ls.append((bn, fn))

    else:
        for bn in os.listdir(dn):
            fn = os.path.join(dn, bn)
            if not os.path.isfile(fn):
                print('Skip %s' % bn)
                continue 

            bn_fn_ls.append((bn, fn))

    return bn_fn_ls

def get_q(question, dis_date, dis_q_date, dis_q_time):
    if 'q1' in question:
        q = question['q1']
    elif 'q1-prefix' in question:
        q = question['q1-prefix']
    else:
        assert False, question

    if question['is_short']:
        q = '%s ... ...' % q

    display_q = False 
    if dis_date:
        if 'date' not in question:
            display_q = True 
    else:
        display_q = True 

    if display_q:
        if dis_q_date and dis_q_time:
            q = '%s `(%s %s)`' % (q, question['q_date'], question['q_time'][:5])
        elif dis_q_date and not dis_q_time:
            q = '%s `(%s)`' % (q, question['q_date'])
        elif not dis_q_date and dis_q_time:
            q = '`[%s]` %s' % (question['q_time'][:5], q)
    else:
            q = '%s `(%s)`' % (q, question['date'])

    return q

def get_date_time(ts):
    date = datetime.datetime.fromtimestamp(ts)
    dt_str = date.strftime("%Y-%m-%d %H:%M:%S")
    return dt_str

def get_files(dn):
    if not os.path.exists(dn):
        print('Error! The directory does not exist.')
        print(dn)
        sys.exit(1)

    bn_ls = []
    for bn in os.listdir(dn):
        bn_ls.append(bn)

    bn_ls.sort()

    bn_fn_ls = []
    for bn in bn_ls:
        fn = os.path.join(dn, bn)
        bn_fn_ls.append((bn, fn))

    return bn_fn_ls

def read_lines(fn):
    lines = []
    f = open(fn)
    for line in f:
        line = line.strip()
        if line == '':
            continue    
        lines.append(line)

    return lines

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


#
# section_ls = [section]
# section = {'title', 'question_ls'}
# question_ls = [question]
# question = {
#       'q1', 'q2', 'q1-prefix', 'q2-prefix', 'a-prefix', 
#       'from', 'hide', 'date', 'qs', 'title',
#       'q_date', 'q_time'}
#   qs: question set
#    

# q1 = https://en.wikipedia.org/wiki/Trusted_execution_environment
# q2 = https://en.wikipedia.org/wiki/Trusted\_execution\_environment
#

def read_sections(lines, qs, default_chat, default_date):
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
        elif line.startswith('d:'):
            s = 'date'            
        else:
            s = 'title'

        if s == 'q':
            _, line = line.split(':', 1)
            line = line.strip()
            q1 = line 
            q2 = line.replace('_', '\\_')
            
            question = {'q1': q1, 'q2': q2, 'hide': False, 'qs': qs}

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

            question = {'q1-prefix': q1_prefix, 'q2-prefix': q2_prefix, 'hide': False, 'qs': qs}
            
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

        elif s == 'date':
            _, line = line.split(':', 1)
            line = line.strip()
            question['date'] = line

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

    #
    # Remember title in each question and set is_short
    #    

    for section in section_ls:
        for question in section['question_ls']:
            question['title'] = section['title']
            question['is_short'] = False

    return section_ls

def check_sections(section_ls):
    for section in section_ls:
        for question in section['question_ls']:
            assert not ('q1' in question and 'q1-prefix' in question)
            assert 'from' in question
            assert question['from'] != None
            assert 'qs' in question
            assert 'title' in question

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

#
# q, q1, a, a1, q, q1, a, a1, q, q1, q, q1, a, a1, a, a1
#

def read_qa_ls(fn):
    f = open(fn, encoding='utf-8', errors='ignore')
    s = 'init'   # s: init, q, q1, a, a1

    q = []
    a = []
    qa_ls = []
    for line in f:
        line = line.rstrip()

        if s == 'init':
            if line == '**You:**':
                s = 'q'
            elif line == '**ChatGPT:**':
                print('1: Error! s = %s @ %s' % (s, fn))
                sys.exit(1)

        elif s == 'q':
            if line == '**ChatGPT:**':
                s = 'a'
            elif line == '**You:**':
                s = 'q'
            else:
                s = 'q1'

        elif s == 'q1':
            if line == '**ChatGPT:**':
                s = 'a'
            elif line == '**You:**':
                s = 'q'
            else:
                s = 'q1'

        elif s == 'a':
            if line == '**You:**':
                s = 'q'
            elif line == '**ChatGPT:**':
                print('2: Error! s = %s @ %s' % (s, fn))
                sys.exit(1)             
            else: 
                s = 'a1'

        elif s == 'a1':
            if line == '**You:**':
                s = 'q'
            elif line == '**ChatGPT:**':
                s = 'a'         
            else: 
                s = 'a1'

        else:
            print('4: Error! s = %s @ %s' % (s, fn))
            sys.exit(1)

        #print('%10s | %s' % (s, line))  

        if s == 'q1':
            if line == '* * *':
                pass
            else:
                q.append(line)

        elif s == 'a1':
            if line == '* * *':
                pass
            else:
                a.append(line)

        elif s == 'q':
            if q != []:                
                if a != []:
                    qa_ls.append((q, a))
                a = []
                q = [] 

        elif s == 'a':
            a = []


    if q != []:
        if a != []:
            qa_ls.append((q, a))

    return qa_ls

def remove_empty_lines_from_head_and_tail(lines):    
    if lines == []:
        return

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
    #print('q = %s' % q)
    #print('a = %s' % a)

    remove_empty_lines_from_head_and_tail(q)

    guid = None
    create_time = None 
    while True:
        if q[0].startswith('guid:'):
            _, guid = q[0].split(':', 1)
            guid = guid.strip()
            q.pop(0)

        elif q[0].startswith('create_time:'):
            _, create_time = q[0].split(':', 1)
            create_time = create_time.strip()
            q.pop(0)
        
        else:
            break

    assert guid != None

    assert len(q) >= 1, q
    one_q = q[0]

    is_short = len(q) > 1

    remove_empty_lines_from_head_and_tail(a)
    a = refine_md_1(a)

    qa = {'guid': guid, 'q': one_q, 'is_short': is_short, 'create_time': create_time, 'a': a}
    return qa

#
# Parse the chat file to build qa_ls
# qa_ls = [qa]
# qa = {'q', 'guid', 'create_time', 'a'}
#

def parse_chat(fn):

    org_qa_ls = read_qa_ls(fn)
    qa_ls = []
    for q, a in org_qa_ls:
        qa = build_qa(q, a)
        qa_ls.append(qa)

    return qa_ls

def find_qa(qa_ls, question, chat):

    out = None

    if 'a-prefix' in question:
        for qa in qa_ls:
            if qa['a'][0].startswith(question['a-prefix']):
                out = qa
                return out

        if out == None:
            print('Error. The answer of the question is not found.')
            print('chat = %s' % chat)
            print('q1 = %s' % question['q1'])
            print('q2 = %s' % question['q2'])
            print('a-prefix: %s' % question['a-prefix'])
            sys.exit(1)

    else:
        for qa in qa_ls:
            if 'q2-prefix' in question:
                if qa['q'].startswith(question['q2-prefix']):
                    out = qa
                    break

            if 'q2' in question:
                if qa['q'] == question['q2']:
                    out = qa
                    break

            if 'q2-prefix' in question:
                if qa['q'].startswith(question['q1-prefix']):
                    out = qa
                    break

            if 'q2' in question:
                if qa['q'] == question['q1']:
                    out = qa
                    break                    

        if out == None:
            print('Error. The answer of the question is not found.')
            print('chat = %s' % chat)

            if 'q1' in question:
                print('q1 = %s' % question['q1'])
                print('q2 = %s' % question['q2'])
            elif 'q1-prefix' in question:
                print('q1-prefix = %s' % question['q1-prefix'])

            sys.exit(1)

    return out    

def find_answer(chats, fn_qa_ls_d, question):
    fn = os.path.join(chats, question['from'])
    qa_ls = fn_qa_ls_d[fn]
    qa = find_qa(qa_ls, question, question['from'])

    question['guid'] = qa['guid']    
    question['a'] = qa['a']


    if qa['create_time'] != None:
        question['q_date'] = qa['create_time'][:10]
        question['q_time'] = qa['create_time'][11:]

def write_sections(q_section_ls, c_section_ls, fn, dis_date, dis_q_date, dis_q_time):

    #
    # Check options.
    #

    if dis_date == True and dis_q_time == True:
        print('Error.')
        sys.exit(1)

    #
    # Create a file to write.
    #


    name, _ = get_name(fn)

    f = open(fn, 'w', encoding='utf-8')

    f.write('# %s\n' % name)

    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    f.write('Created: %s\n' % (now_str))

    for title, section_ls in zip(['Questions', 'Chats'], [q_section_ls, c_section_ls]):
        
        if len(section_ls) >= 1:
            f.write('# %s\n' % title)

        for section in section_ls:
            f.write('* %s\n' % section['title'])

            for question in section['question_ls']:
                #if question['hide']:
                #    continue

                q = get_q(question, dis_date, dis_q_date, dis_q_time)
                f.write('    * %s\n' % q)

        if len(section_ls) >= 1:
            f.write('\n')
            f.write('---\n')
            f.write('\n')

    f.write('# Q & A\n')
    for section_ls in [q_section_ls, c_section_ls]:
        for section in section_ls:
            f.write('## %s\n' % section['title'])

            for question in section['question_ls']:
                
                q = get_q(question, dis_date, dis_q_date, dis_q_time)
                a = question['a']

                f.write('**Question:** %s\n' % q)
                f.write('\n')


                if question['hide']:
                    f.write('**Answer:** (Hide)\n')
                    f.write('\n')

                else:
                    f.write('**Answer:**\n')
                    f.write('\n')
                    for line in a:
                        f.write(line+'\n')

                f.write('\n')
                f.write('---\n')
                f.write('\n')

    f.close()

