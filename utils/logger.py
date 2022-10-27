#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _authors_: Vozec
# _date_ : 27/10/2022

from datetime import datetime

## LOGGER CLASS

class bcolors:
    WHITE = '\033[0m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

all_context = {
    'progress':bcolors.HEADER,
    'white':bcolors.WHITE,
    'info':bcolors.WARNING,
    'flag':bcolors.OKGREEN,
    'log':bcolors.OKBLUE,
    'error':bcolors.FAIL,
    'warning':bcolors.OKCYAN,
    None:''
    }

def logger(message,context=None,newline=0,tab=0,notime=False):	
    final = ""
    final += '\n'*newline
    now = datetime.now()
    if not notime:
        final += now.strftime("%H:%M:%S")
        final += " | "
    final += all_context[context]
    final += '\t'*tab
    final += ' '
    final += message
    final += bcolors.ENDC
    print(final)