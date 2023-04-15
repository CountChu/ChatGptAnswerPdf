import argparse
import sys
import os
import subprocess
import util

import pdb
br = pdb.set_trace

def build_args():
    desc = '''
    Usage 1: python chatpdf.py list  
    Usage 2: python chatpdf.py list -q questions-230402   
    Usage 3: python chatpdf.py update
    Usage 4: python chatpdf.py update -q questions-230402 -c chats-manual
    Usage 5: python chatpdf.py build
    Usage 6: python chatpdf.py build -f 230328.TEE.txt
    Usage 7: python chatpdf.py build -q questions-230402 -c chats-manual   
    Usage 8: python chatpdf.py build -q questions-230402 -f 230327.OP-TEE.txt -c chats-manual   
'''
    #
    # Build an ArgumentParser object to parse arguments.
    #

    parser = argparse.ArgumentParser(
                formatter_class=argparse.RawTextHelpFormatter,
                description=desc)

    #
    # Anonymous arguments.
    #

    parser.add_argument(
            'command',
            help='list, build, or update')    

    #
    # Standard arguments.
    #

    parser.add_argument(
            '-c',
            dest='chats',
            default='chats',
            help='E.g., "chats-manual"')      

    parser.add_argument(
            '-q',
            dest='questions',
            default='questions',
            help='E.g., "questions-230402"')    

    parser.add_argument(
            '-f',
            dest='file',
            help='E.g., "230328.TEE.txt"')    

    #
    # Check arguments and return.
    #

    args = parser.parse_args()

    return args  

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


def handle_list(args, ctx):
    print('')
    print('Question Sets in the directory "%s":' % ctx['questions'])

    bn_fn_ls = get_files(ctx['questions'])

    for bn, fn in bn_fn_ls:
        print('    %s' % bn)

    print('')

def run_it(cmd):
    print(cmd)

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    print(res.stdout.decode())
    
    if res.returncode != 0:
        print('Error! ----------------')
        print(res.stderr.decode())
        sys.exit(1)

def build_pdf(ctx, bn):
    name, _ = util.get_name(bn)

    cmd_ls = []

    cmd = 'python answer.py -q "%s/%s" -c "%s" -a "%s" -s'
    cmd = cmd % (ctx['questions'], bn, ctx['chats'], ctx['out'])
    cmd_ls.append(cmd)

    cmd = 'python tohtml.py -f "%s.md" -i output -o output-html -s'
    cmd = cmd % (name)
    cmd_ls.append(cmd)

    cmd = 'python topdf.py -f "%s.html" -i output-html -o output-pdf -s'
    cmd = cmd % (name)
    cmd_ls.append(cmd)

    for cmd in cmd_ls:
        run_it(cmd)  

def handle_build(args, ctx):

    bn_ls = []

    if args.file != None:
        bn_ls.append(args.file)

    else:
        bn_fn_ls = get_files(ctx['questions'])
        for bn, _ in bn_fn_ls:
            bn_ls.append(bn)

    for bn in bn_ls:
        fn = os.path.join(ctx['questions'], bn)

        if not os.path.exists(fn):
            print('Error! The file does not exist.')
            print(fn)
            sys.exit(1)

        build_pdf(ctx, bn)  

def handle_update(args, ctx):
    print('Update output if question set files in the dir [%s] are updated.' % ctx['questions'])
    
    #
    # Get files in the questions directory.
    #

    bn_fn_ls = get_files(ctx['questions'])

    #
    # Check for each files to see if it is necessary to build PDF.
    #

    for bn, fn in bn_fn_ls:
        name, _ = util.get_name(fn)
        fn_pdf = os.path.join(ctx['pdf'], '%s.pdf' % name)
        
        do_update = False
        if not os.path.exists(fn_pdf):
            do_update = True 
        else:
            mt_fn = os.path.getmtime(fn)
            mt_pdf = os.path.getmtime(fn_pdf)

            if mt_fn > mt_pdf: 
                do_update = True

        if do_update:
            print('Handle %s --------------------------------' % bn)
            build_pdf(ctx, bn)

def main():

    #
    # Read arguments.
    #

    args = build_args()

    #
    # Build ctx.
    #

    ctx = {
        'chats': args.chats,
        'questions': args.questions,
        'out': 'output',
        'html': 'output-html',
        'pdf': 'output-pdf',
    }

    #
    # Dispatch the command.
    #

    if args.command == 'list':
        handle_list(args, ctx)

    elif args.command == 'build':
        handle_build(args, ctx)

    elif args.command == 'update':
        handle_update(args, ctx)

    else:
        print('Error command! %s' % args.command)
        sys.exit(1)

if __name__ == '__main__':
    main()