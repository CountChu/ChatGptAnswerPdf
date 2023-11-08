#
# FILENAME.
#       topdf.py - To PDF Python App.
#
# FUNCTIONAL DESCRIPTION.
#       The app converts HTML files into pdf files.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2023/4/5
#       Updated on 2023/11/8
#

import argparse
import sys
import os
import pdfkit

from core import util

import pdb
br = pdb.set_trace

def build_args():
    desc = '''
    Usage 1: python topdf.py -i out-ans-html -o out-ans-pdf
    Usage 2: python topdf.py -f 230328.TEE.html -i out-ans-html -o out-ans-pdf    
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
            help='The input directory that contains HTML files. E.g., "output-html"')    

    parser.add_argument(
            '-o',
            dest='output',
            help='The output directory where the generated PDF files. E.g., "output-pdf"')    

    parser.add_argument(
            '-f',
            dest='file',
            help='An HTML file in the input directory. E.g., "230328.TEE.html"')  

    parser.add_argument(
            '-s',
            dest='silence',
            action='store_true',
            help='To display less messages.')    
    
    #
    # Check arguments.
    #

    args = parser.parse_args()

    return args  

def html_to_pdf(fn_html, fn_pdf): 
    print('Generating: %s' % (fn_pdf))
    
    f = open(fn_html, encoding='utf-8')
    html_text = f.read()
    f.close()

    pdfkit.from_string(html_text, fn_pdf)

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
    # Check if the output directory exists. If not, make it.
    #

    if not os.path.exists(args.output):
        print('The directory does not exist. Building it')
        print(args.input)
        os.mkdir(args.output)

    #
    # Collect input HTML files.
    #

    bn_fn_ls = util.collect_input_files(args.file, args.input)        

    #
    # Handle each HTML files.
    #

    for bn, fn in bn_fn_ls:
        name, ext = util.get_name(fn)
        if ext != '.html':
            print('Skip %s' % fn)
            continue 

        print('Handling %s' % name) 

        do_gen = False
        fn_out = os.path.join(args.output, "%s.pdf" % (name))
        if os.path.exists(fn_out):
            print('    The file %s exists.' % (os.path.basename(fn_out)))
            if os.path.getmtime(fn) > os.path.getmtime(fn_out):
                print('    It is old!')
                do_gen = True
        else:
            do_gen = True           

        if do_gen:
            html_to_pdf(fn, fn_out) 

if __name__ == '__main__':
    main()



