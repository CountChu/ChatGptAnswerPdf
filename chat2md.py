import argparse
import sys
import os
import json
import util
import pdb

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

def handle_chat(output, chat): 
    title = chat['title']
    #if title != 'TEE-PP.0414':
    #    return

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

        else: 
            assert False, role

        content = message['content']
        parts = content['parts']

        for part in parts:
            #if role == 'user':
            #    line = part.replace('\n', ' ')
            #    line = line.strip()
            #    #print(line)
            #    f.write(line)
            #else:
            #    f.write(part)

            f.write(part.strip())

        f.write('\n\n')
        f.write('* * *\n\n')
        #print('')

    f.close()

def main():

    #
    # Read arguments.
    #

    args = build_args()
    
    #
    # Check if the input directory exists.
    #

    if not os.path.exists(args.input):
        print('Error. The directory does not exist.')
        print(args.input)
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
        handle_chat(args.output, chat)


if __name__ == '__main__':
    main()