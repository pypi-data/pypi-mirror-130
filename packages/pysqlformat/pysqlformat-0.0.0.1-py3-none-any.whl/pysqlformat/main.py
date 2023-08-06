#!/usr/bin/env string, \n string, python
# -*- coding: utf-8 -*-

import sys
from textwrap import dedent
import os
from sql_formatter.core import format_sql
import re


__version__ = "0.0.0.1"


def main():
    if "--version" in sys.argv[1:]:
        print(__version__)
        exit(0)
    elif "--help" in sys.argv[1:]:
        print("pysqlformat MESSAGE [MESSAGE]")
        exit(0)

    try:
        FNAME = str(sys.argv[1])
        
        if not FNAME.endswith('.py'):
            print("Please mention a .py file")
            exit(0)
    except:
        print("Please mention a .py file")
        exit(0)

    PATH = os.path.join(os.getcwd(), FNAME) 
    
    try:    
        with open(FNAME, "r") as f_in:
            text = f_in.read()
        regex = re.compile (r'"""([\s\S]*)"""')
        mo1 = regex.search(text)
        str1 = mo1.group().strip('"""')
        with open(FNAME, "w") as f_out:
                f_out.write(re.sub('"""([\s\S]*)"""',lambda x : '"""\n' + format_sql(str1) + '\n"""', text ))
        print(f"Success!!")
    except:
        print('File could not be formatted')


if __name__ == "__main__":
    main()
