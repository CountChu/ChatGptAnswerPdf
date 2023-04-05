import os
import sys

def get_name(fn):
    name = os.path.basename(fn)
    name, ext = os.path.splitext(name)
    return name, ext

def collect_input_files(file, dn):
    bn_fn_ls = []

    if file != None:
        bn = file 
        fn = os.path.join(dn, bn)

        if not os.path.exists(fn):
            print('Error! The file does not exist.')
            print(fn)
            sys.exit(1)

        if not os.path.isfile(fn):
            print('Error! It is directory.')
            print(fn)
            sys.exit(1)

        bn_fn_ls.append((bn, fn))

    else:
        for bn in os.listdir(dn):
            fn = os.path.join(dn, bn)
            if not os.path.isfile(fn):
                print('Skip %s' % bn)
                continue 

            bn_fn_ls.append((bn, fn))

    return bn_fn_ls