#!/usr/bin/env python
# encoding=utf-8

import os
import sys
import kinortho.kinortho as ko

argv = sys.argv
args = {'-i': '', '-f': '', '-d': '', '-o': './kinortho_out/', '-E': '1e-5', '-t': '1', '-I': '1.5', '-e': '1e-200', '-s': '0', '-S': '6'}

if argv[1] == '-h' or argv[1] == '-help':
    command = 'python ' + ko.__file__ + ' -h' 
    os.system(command)

try:
    proteomes, full_seq, domain_seq, output_folder, e_value, thread, inflat, min_e, start_step, stop_step = list(map(args.get, ['-i', '-f', '-d', '-o', '-E', '-t', '-I', '-e', '-s', '-S']))
except:
    command = 'python ' + ko.__file__ + ' -h'
    os.system(command)

def kinortho():
    command = 'python ' + ko.__file__
    command += ' -i ' + proteomes
    command += ' -f ' + full_seq
    command += ' -d ' + domain_seq
    command += ' -o ' + output_folder
    command += ' -E ' + e_value
    command += ' -t ' + thread
    command += ' -I ' + inflat
    command += ' -e ' + min_e
    command += ' -s ' + start_step
    command += ' -S ' + stop_step
    os.system(command)
