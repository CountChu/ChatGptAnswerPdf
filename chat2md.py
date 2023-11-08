#
# FILENAME.
#       chat2md.py - Chat To Markdown Python App.
#
# FUNCTIONAL DESCRIPTION.
#       The app converts conversations.json into Markdown files which are compatible 
#       to the Chrome plugin, [ChatGPT to Markdown]
#       (https://chatopenai.pro/chatgpt-to-markdown/).
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2023/4/15
#       Updated on 2023/4/29
#

import argparse
import sys
import os
import json
import pdb

from core import util 

br = pdb.set_trace

def build_args():
    desc = '''
    Usage 1: chat2md.py -i download-230414 -o chats 
'''
    #
    # Build an ArgumentParser object to parse arguments.
    #

    parser = argparse.ArgumentParser(
                formatter_class=argparse.RawTextHelpFormatter,
                description=desc)

    #
    # Standard arguments.
    #

    parser.add_argument(
            '-i',
            dest='input',
            help='A directory that contains original json files from ChatGPT. E.g., chats-230414')     

    parser.add_argument(
            '-o',
            dest='output',
            help='A directory that contains MD files as output. E.g., chats')     

    #
    # Check arguments and return.
    #

    args = parser.parse_args()

    return args  

def refine_md(part):
    out = ''
    lines = part.split('\n')
    for line in lines:
        if line.find('```') != -1:
            line = line.strip()

        out += f"{line}\n"

    return out.strip()

def handle_chat(output, output_json, chat): 
    title = chat['title']
    #if title != 'Work.0723':
    #    return

    #
    # Write chat in a JSON file.
    #

    text = json.dumps(chat, indent=4)
    fn = os.path.join(output_json, "%s.json" % title)
    print('Write %s' % fn)
    f = open(fn, 'w', encoding='utf-8')
    f.write(text)
    f.close()

    #
    # Write chat in a MD file.
    #

    fn = os.path.join(output, "%s.md" % title)
    print('Write %s' % fn)
    f = open(fn, 'w', encoding='utf-8')

    #s = 'init'

    for guid, msg in chat['mapping'].items():
        message = msg['message']
        if message == None:
            continue

        author = message['author']
        role = author['role']
        if role == 'system':
            continue

        #print('role = %s' % (role))
        #print('id = %s' % (msg['id']))
        #print('children = %s' % (msg['children']))

        metadata = message['metadata']
        #print('metadata = %s' % metadata)

        if role == 'user':
            f.write('**You:**\n\n')

            create_time = util.get_date_time(message['create_time'])
            f.write('guid: %s\n' % guid)
            f.write('create_time: %s\n' % create_time)

        elif role == 'assistant':
            if 'finish_details' in metadata:
                if metadata['finish_details']['type'] == 'interrupted':
                    continue 

            f.write('**ChatGPT:**\n\n')
            #assert s == 'user'
            #s = 'assistant'

        elif role == 'tool':
            f.write('**ChatGPT:**\n\n')

        else: 
            assert False, role

        content = message['content']

        if 'parts' not in content:
            continue
            
        parts = content['parts']

        if parts[0].strip() == '':
            parts[0] = 'N/A\n'

        for part in parts:

            #if role == 'user':
            #    line = part.replace('\n', ' ')
            #    line = line.strip()
            #    #print(line)
            #    f.write(line)
            #else:
            #    f.write(part)

            part = refine_md(part)
            f.write(part)

        f.write('\n\n')
        f.write('* * *\n\n')
        #print('')

    f.close()

def main():

    #
    # Read arguments.
    #

    args = build_args()
    
    util.check_dir_exist(args.input)
    util.check_dir_exist_make(args.output)

    output_json = args.output + '-json'
    util.check_dir_exist_make(output_json)

    #
    # Read conversations.json
    #

    fn = os.path.join(args.input, 'conversations.json')
    if not os.path.exists(fn):
        print('Error. The file does not exist.')
        print(fn)
        sys.exit(1)    

    f = open(fn, encoding='utf-8')
    content = f.read()
    f.close()

    #
    # Parse content as JSON.
    #

    chats = json.loads(content)
    for chat in chats:
        handle_chat(args.output, output_json, chat)


if __name__ == '__main__':
    main()

