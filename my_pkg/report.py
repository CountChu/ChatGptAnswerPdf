import datetime
import pdb
import my_pkg.util as util

br = pdb.set_trace

def get_q(question, dis_date, dis_q_date, dis_q_time):
    #br()
    
    if 'q1' in question:
        q = question['q1']
    elif 'q1-prefix' in question:
        q = question['q1-prefix']
    else:
        assert False, question

    if question['is_short']:
        q = '%s ... ...' % q

    if 'q_title' in question:
        q = '%s <span style="color:blue">`[title]`</span>' % question['q_title']

    if question['error']:
        q = '%s <span style="color:red">`[error]`</span>' % q

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
            if 'q_date' in question:
                q = '%s `(%s)`' % (q, question['q_date'])
        elif not dis_q_date and dis_q_time:
            q = '`[%s]` %s' % (question['q_time'][:5], q)
    else:
            q = '%s `(%s)`' % (q, question['date'])

    q = '%s `(%s)`' % (q, question['from'])

    return q

def get_q_in_text(question, dis_date, dis_q_date, dis_q_time):
    if 'q1' in question:
        q = question['q1']
    elif 'q1-prefix' in question:
        q = question['q1-prefix']
    else:
        assert False, question

    if question['is_short']:
        q = '%s ... ...' % q

    if 'q_title' in question:
        q = '[title] %s' % question['q_title']

    if question['error']:
        q = '[error] %s' % q

    display_q = False 
    if dis_date:
        if 'date' not in question:
            display_q = True 
    else:
        display_q = True 

    if display_q:
        if dis_q_date and dis_q_time:
            q = '%s (%s %s)' % (q, question['q_date'], question['q_time'][:5])
        elif dis_q_date and not dis_q_time:
            q = '%s (%s)' % (q, question['q_date'])
        elif not dis_q_date and dis_q_time:
            q = '[%s] %s' % (question['q_time'][:5], q)
    else:
            q = '%s (%s)' % (q, question['date'])

    return q    

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


    name, _ = util.get_name(fn)

    f = open(fn, 'w', encoding='utf-8')

    f.write('# %s\n' % name)

    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    f.write('Created: %s\n' % (now_str))

    for title, section_ls in zip(['Questions', 'Chats'], [q_section_ls, c_section_ls]):
        
        if len(section_ls) >= 1:
            f.write('# %s\n' % title)

        for section in section_ls:
            f.write('* %s\n' % section['sec_title'])

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
            f.write('## %s\n' % section['sec_title'])

            for question in section['question_ls']:
                
                q = get_q(question, dis_date, dis_q_date, dis_q_time)
                a = question['a']

                f.write('**Question:** %s\n' % q)
                f.write('\n')


                if question['hide']:
                    f.write('**Answer:** ... ...\n')
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

def write_sections_in_text(q_section_ls, c_section_ls, fn, dis_date, dis_q_date, dis_q_time):

    #
    # Check options.
    #

    if dis_date == True and dis_q_time == True:
        print('Error.')
        sys.exit(1)

    #
    # Create a file to write.
    #


    name, _ = util.get_name(fn)

    f = open(fn, 'w', encoding='utf-8')

    f.write('%s\n\n' % name)

    for title, section_ls in zip(['Questions', 'Chats'], [q_section_ls, c_section_ls]):
        
        if len(section_ls) >= 1:
            f.write('%s\n\n' % title)

        for section in section_ls:
            f.write('%s\n' % section['sec_title'].replace('```', ''))

            for question in section['question_ls']:
                #if question['hide']:
                #    continue

                q = get_q_in_text(question, dis_date, dis_q_date, dis_q_time)
                f.write('%s\n' % q)

            f.write('\n')

    f.close()

