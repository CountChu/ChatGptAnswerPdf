#
# FILENAME.
#       tohtml.py - To HTML Python App.
#
# FUNCTIONAL DESCRIPTION.
#       The app converts MD files into HTML files. 
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2023/4/5
#       Updated on 2023/7/22
#

import argparse
import sys
import os
import markdown
import shutil

from core import util

import pdb
br = pdb.set_trace

def build_args():
    desc = '''
    Usage 1: python tohtml.py -i out-ans -o out-ans-html
    Usage 2: python tohtml.py -f 230328.TEE.md -i out-ans -o out-ans-html

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
            help='The input directory that contains Markdown files. E.g., "out-ans"')    

    parser.add_argument(
            '-o',
            dest='output',
            required=True,            
            help='The output directory where the generated HTML files. E.g., "out-ans-html"')    

    parser.add_argument(
            '-f',
            dest='file',
            help='A Markdown file in the input directory. E.g., "230328.TEE.md"')  

    parser.add_argument(
            '-s',
            dest='silence',
            action='store_true',
            help='To display less messages.')    
    
    #
    # Check arguments and return.
    #

    args = parser.parse_args()

    return args  

def markdown_to_html(fn_md, name, extensions, fn_html): 

    f = open(fn_md, encoding='utf-8')
    md = f.read()
    f.close()

    md_html = markdown.markdown(md, extensions=extensions)

    html = f'''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="github.css" type="text/css">
    <title>{name}</title>    
  </head>
  <body>
    <article class="markdown-body">
        <!-- Markdown-generated HTML content here -->
        {md_html}
    </article>
  </body>
</html>
'''

    #html = html % (css, name, md_html)

    f = open(fn_html, 'w', encoding='utf-8')
    f.write(html)
    f.close()

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
    # Copy github.css
    #

    fn_css = os.path.join(home, 'github.css')
    print('fn_css: %s' % fn_css)
    fn_css_dst = os.path.join(args.output, 'github.css')
    print('fn_css_dst: %s' % fn_css_dst)    
    shutil.copy2(fn_css, fn_css_dst)

    #
    # Build extensions.
    #

    extensions = [
        #"markdown.extensions.smart_strong",
        "markdown.extensions.footnotes",
        "markdown.extensions.attr_list",
        "markdown.extensions.def_list",
        "markdown.extensions.tables",
        "markdown.extensions.abbr",
        #"pymdownx.extrarawhtml",
        "markdown.extensions.meta",
        "markdown.extensions.sane_lists",
        "markdown.extensions.smarty",
        "markdown.extensions.wikilinks",
        "markdown.extensions.admonition",

        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',

        'pymdownx.magiclink',
    ]    

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
            markdown_to_html(fn, name, extensions, fn_out) 

if __name__ == '__main__':
    main()



