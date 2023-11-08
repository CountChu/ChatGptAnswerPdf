#
# FILENAME.
#       subl_markdownPreview_save.py - Sublime MarkdownPreview Save App.
#
# FUNCTIONAL DESCRIPTION.
#       The app converts MD files into HTML files with MarkdownPreview 
#       of Sublime plug-in.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2023/9/2
#       Updated on 2023/9/2
#

import argparse
import sys
import os
import shutil
import subprocess
import time

from core import util

import pdb
br = pdb.set_trace

def build_args():
    desc = '''
    Usage 1: python subl_markdownPreview_save.py -i out-hist-mrg -o out-hist-mrg-html
    Usage 2: python subl_markdownPreview_save.py -i out-hist-mrg -o out-hist-mrg-html -f 2023-08-24.md

'''
    #
    # Build an ArgumentParser object to parse arguments.
    #

    parser = argparse.ArgumentParser(
                formatter_class=argparse.RawTextHelpFormatter,
                description=desc)

    parser.add_argument(
            '-i',
            dest='input',
            required=True,
            help='The input directory that contains Markdown files. E.g., "out-hist-mrg"')    

    parser.add_argument(
            '-o',
            dest='output',
            required=True,            
            help='The output directory where the generated HTML files. E.g., " out-hist-mrg-html"')    

    parser.add_argument(
            '-f',
            dest='file',
            help='A Markdown file in the input directory. E.g., "2023-08-24.md"')  

    parser.add_argument(
            '-s',
            dest='silence',
            action='store_true',
            help='To display less messages.')    

    # Always disable quiet otherwise AssertError occurs.
    '''
    parser.add_argument(
            '-q',
            dest='quiet',
            action='store_true',
            help='No prompt.')  
    '''

    parser.add_argument(
            '--force',
            dest='force',
            action='store_true',
            help='Force to update')        
    
    #
    # Check arguments and return.
    #

    args = parser.parse_args()

    return args  

def contain_code(fn_md):
    f = open(fn_md)
    out = False 

    for line in f:
        if line.find('```') != -1:
            out = True 
            break
    f.close()

    return out  

def markdown_to_html(args, fn_md, name, fn_html): 

    #
    # Replace with the actual path to your Sublime Text executable
    #

    subl = "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl"

    #
    # Open the Markdown file in Sublime Text
    #

    subprocess.run([subl, fn_md])    

    #
    # Delay to ensure the file is opened before previewing
    #

    ''' Always disable quiet.
    if args.quiet:
        time.sleep(1)
    else:
        input("Press Enter to continue...")    
    '''
    time.sleep(1)

    #
    # Check if the Markdown file contain code ```
    # Run the MarkdownPreview command to save the MD in HTML.
    #

    if contain_code(fn_md):             # The github parser is friendly for code block 
                                        # [BUGBUG] github parser does not support color text.
        print('    parser: github')
        subprocess.run([subl, "--command", 'markdown_preview {"target":"save", "parser":"github"}'])

    else:                               # The markdown is friendly for LaTex
        print('    parser: markdown')
        subprocess.run([subl, "--command", 'markdown_preview {"target":"save", "parser":"markdown"}'])

    #
    # Move the HTML file.
    #

    time.sleep(0.5)
    fn_html_src, _ = os.path.splitext(fn_md)
    fn_html_src = '%s.html' % fn_html_src 
    assert os.path.exists(fn_html_src)
    shutil.move(fn_html_src, fn_html)

def main():

    #
    # Read home of the app.
    #

    home = os.path.dirname(sys.argv[0])    

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
    # Check if the output directory exists. If not, make it.
    #

    if not os.path.exists(args.output):
        print('The directory does not exist. Building it')
        print(args.input)
        os.mkdir(args.output)  

    #
    # Collect input Markdown files.
    #

    bn_fn_ls = util.collect_input_files(args.file, args.input)

    #
    # Handle each Markdown files.
    #

    for bn, fn in bn_fn_ls:
        name, ext = util.get_name(fn)
        if ext != '.md':
            print('Skip %s' % fn)
            continue 

        print('Handling %s' % name)    

        do_gen = False
        fn_out = os.path.join(args.output, "%s.html" % (name))

        if args.force:
            do_gen = True

        else:
            if os.path.exists(fn_out):
                print('    The file %s exists.' % (os.path.basename(fn_out)))

                #
                # Compare the modified time between *.md and *.html.
                #

                if os.path.getmtime(fn) > os.path.getmtime(fn_out):
                    print('    It is old!')
                    do_gen = True
            else:
                do_gen = True

        if do_gen:
            print('    Generating: %s' % (fn_out))
            markdown_to_html(args, fn, name, fn_out) 

if __name__ == '__main__':
    main()



