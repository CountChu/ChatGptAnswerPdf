import argparse
import sys
import os
import markdown

import util

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

def markdown_to_html(fn_md, name, extensions, css, fn_html): 
    print('Generating: %s' % (fn_html))

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
    <style>
    {css}
    </style>
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
    ]    

    #
    # Get CSS content.
    #

    fn_css = 'github.css'
    f = open(fn_css)
    css = f.read()
    f.close()

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

        fn_out = os.path.join(args.output, "%s.html" % (name))
        markdown_to_html(fn, name, extensions, css, fn_out) 

if __name__ == '__main__':
    main()



