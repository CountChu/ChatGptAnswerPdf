import datetime
import pdb
from core import util

br = pdb.set_trace

def get_q(question, dis_date, dis_q_date, dis_q_time, full=False):    
    if 'q1' in question:
        q_one_line = question['q1']
    elif 'q1-prefix' in question:
        q_one_line = question['q1-prefix']
    else:
        assert False, question

    if question['is_short']:
        q_one_line = '%s ... ...' % q_one_line

    if 'q_title' in question:
        q_one_line = '%s <span style="color:blue">`[title]`</span>' % question['q_title']

    if question['error']:
        q_one_line = '%s <span style="color:red">`[error]`</span>' % q_one_line   

    if question['del']:
        q_one_line = '`[del]` %s' % q_one_line         

    display_q = False 
    if dis_date:
        if 'date' not in question:
            display_q = True 
    else:
        display_q = True 

    if display_q:
        if dis_q_date and dis_q_time:
            q_one_line = '%s `(%s %s)`' % (q_one_line, question['q_date'], question['q_time'][:5])
        elif dis_q_date and not dis_q_time:
            if 'q_date' in question:
                q_one_line = '%s `(%s)`' % (q_one_line, question['q_date'])
        elif not dis_q_date and dis_q_time:
            q_one_line = '`[%s]` %s' % (question['q_time'][:5], q_one_line)
    else:
            q_one_line = '%s `(%s)`' % (q_one_line, question['date'])

    if 'my' in question.keys():
        q_one_line = '%s `(my answer)`' % (q_one_line)
    else:
        q_one_line = '%s `(%s)`' % (q_one_line, question['from'])


    if question['del']:
        #q = '<span style="color:red">`[del]`</span> <span style="color:lightgray"> %s </span>' % q             
        q_one_line = ' <span style="color:lightgray"> %s </span>' % q_one_line  
        out = [q_one_line]

    else:
        if full and 'q_full' in question:
            out = question['q_full']
        else:
            out = [q_one_line]

    return out

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

    if question['del']:
        q = '[del] %s' % q          

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
            q = '%s | %s' % (question['q_time'][:5], q)
    else:
            q = '%s (%s)' % (q, question['date'])

    if 'my' in question.keys():
        q = '%s (my answer)' % (q)
    else:
        q = '%s (%s)' % (q, question['from'])            

    return q    

def build_md_content(q_section_ls, c_section_ls, fn, dis_date, dis_q_date, dis_q_time):

    #
    # Check options.
    #

    if dis_date == True and dis_q_time == True:
        print('Error.')
        sys.exit(1)

    #
    # Build contents
    #

    lines = []

    name, _ = util.get_name(fn)
    lines.append('# %s\n' % name)

    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    lines.append('Created: %s\n' % (now_str))

    for title, section_ls in zip(['Questions', 'Chats'], [q_section_ls, c_section_ls]):
        
        if len(section_ls) >= 1:
            lines.append('# %s\n' % title)

        for section in section_ls:
            lines.append('* %s\n' % section['title'])

            for question in section['question_ls']:
                #if question['hide']:
                #    continue

                q = get_q(question, dis_date, dis_q_date, dis_q_time)
                lines.append('    * %s\n' % q[0])

        if len(section_ls) >= 1:
            lines.append('\n')
            lines.append('---\n')
            lines.append('\n')

    lines.append('# Q & A\n')
    for section_ls in [q_section_ls, c_section_ls]:
        for section in section_ls:
            lines.append('## %s\n' % section['title'])

            for question in section['question_ls']:
                
                q = get_q(question, dis_date, dis_q_date, dis_q_time, True)
                a = question['a']

                if len(q) == 1:
                    lines.append('**Question:** %s\n' % q[0])
                    lines.append('\n')

                else:
                    lines.append('**Question:**\n')
                    lines.append('\n')

                    #lines.append('```bash\n')
                    for line in q:  
                        lines.append('    '+line+'\n')
                    #lines.append('```\n')


                if question['hide']:
                    lines.append('**Answer:** ... ...\n')
                    lines.append('\n')

                elif question['del']:
                    lines.append('**Answer:** <span style="color:lightgray">[del]</span>\n')
                    lines.append('\n')

                else:
                    lines.append('**Answer:**\n')
                    lines.append('\n')

                    for line in a:                          
                        lines.append(line+'\n')

                lines.append('\n')
                lines.append('---\n')
                lines.append('\n')

    return lines


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
            f.write('%s\n' % section['title'].replace('```', ''))

            for question in section['question_ls']:
                #if question['hide']:
                #    continue

                q = get_q_in_text(question, dis_date, dis_q_date, dis_q_time)
                f.write('%s\n' % q)

            f.write('\n')

    f.close()

