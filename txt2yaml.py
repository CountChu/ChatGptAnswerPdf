#
# FILENAME.
#       txt2yaml.py - TXT To YAML Python App.
#
# FUNCTIONAL DESCRIPTION.
#       The app converts question set files from TXT to YAML.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2023/5/1
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
    Usage 1: python txt2yaml.py -i questions-txt -o questions 
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
            help='A directory that contains question set TXT files. E.g., questions-txt')     

    parser.add_argument(
            '-o',
            dest='output',
            help='A directory that contains question set YAML filest. E.g., questions')     

    #
    # Check arguments and return.
    #

    args = parser.parse_args()

    return args  

def convert(name, input_dn, output_dn):
    txt_fn = os.path.join(input_dn, f'{name}.txt')
    yaml_fn = os.path.join(output_dn, f'{name}.yaml')

    print(f'Reading {txt_fn}')
    print(f'Writing {yaml_fn}')

    f = open(txt_fn, 'r', encoding='utf-8')
    f_w = open(yaml_fn, 'w', encoding='utf-8')

    for line in f:
        s_line = line.rstrip()

        if s_line == '':
            f_w.write(f'{s_line}\n')

        elif line.strip()[0] == '#':
            f_w.write(line)

        elif s_line[0] != ' ':
            if s_line[:5] == 'from:':
                f_w.write(f'{s_line}\n')
            elif s_line[:2] == 'd:':
                f_w.write(f'{s_line}\n')                
            else:
                assert s_line.find(':') == -1, s_line 
                f_w.write(f'{s_line.rstrip()}:\n')
                f_w.write(f'  questions:\n')

        else:
            assert s_line.find(':') != -1, s_line 
            key, value = s_line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if key == 'q':
                f_w.write(f'    - q: {value}\n')
            elif key == 'q-prefix':
                f_w.write(f'    - q-prefix: {value}\n')                
            else:
                f_w.write(f'      {key}: {value}\n')

    f_w.close()
    f.close()


def main():

    #
    # Read arguments.
    #

    args = build_args()

    util.check_dir_exist(args.input)
    util.check_dir_exist_make(args.output)    

    #
    # Get all TXT files.
    #

    name_bn_fn_ls = []
    for bn in os.listdir(args.input):
        name, ext = os.path.splitext(bn)
        if ext != '.txt':
            continue

        fn = os.path.join(args.input, bn)
        if not os.path.isfile(fn):
            continue 

        name_bn_fn_ls.append((name, bn, fn))

    #
    # Convert each file.
    #

    for name, bn, fn in name_bn_fn_ls:
        convert(name, args.input, args.output)    

if __name__ == '__main__':
    main()