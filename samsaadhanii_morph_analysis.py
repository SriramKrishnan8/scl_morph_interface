#!/usr/bin/env python3

import os
import sys
import subprocess as sp

import argparse

import re
import json

from tqdm import tqdm

import devtrans as dt

import convert_scl_to_sh as css
import transliteration as tl


morph_binary_file = "all_morf.bin"


def handle_result(result, output_enc, issue):
    """ """
    
    res_lst = list(filter(None, result.split("\n")))

    morph_all_dict = []

    for i in range(len(res_lst)):
        item = res_lst[i]
        
        new_dict, status_val = css.convert_all(item, output_enc)
        
        morph_all_dict.append(new_dict)
    
    return morph_all_dict


def run_sm_command(command):
    """ """
    
    p = sp.Popen(command, stdout=sp.PIPE, shell=True)
    try:
        outs, errs = p.communicate()
        result = outs.decode('utf-8')
        st = "Success"
    except sp.TimeoutExpired:
        os.kill(p.pid)
        result = ""
        st = "Timeout"
    except Exception as e:
        result = ""
        st = "Error"

    return result, st
        

def run_sm(morph_binary_file, input_, input_enc, output_enc, input_type_text):
    """ """
    
    issue = ""
    trans_input, trans_enc = tl.input_transliteration(input_.strip(), input_enc)
    
    if input_type_text:
        command = "echo " + trans_input + " | " + "lt-proc " + morph_binary_file
    else:
        command = "echo \"" + trans_input + "\" | lt-proc " + morph_binary_file + " /dev/stdin"
    
    try:
        result, issue = run_sm_command(command)
    except Exception as e:
        result = ""
        issue = "input"
    
    morph_all_dict = handle_result(result, output_enc, issue)
    
    return morph_all_dict


def run_sm_text(morph_binary_file, input_, input_enc, output_enc):
    """ """
    
    morph_all_dict = run_sm(
        morph_binary_file, input_, input_enc, output_enc, input_type_text=True
    )

    morph_str_lst = [ json.dumps(item, ensure_ascii=False) for item in morph_all_dict ]
    
    return "".join(morph_str_lst)


def run_sm_file(morph_binary_file, i_file, o_file, input_enc, output_enc):
    """ """
    
    i_f = open(i_file, "r", encoding="utf-8")
    input_contents = i_f.read()
    input_ = list(filter(None, input_contents.strip().split("\n")))
    i_f.close()
    
    morph_all_dict = []
    for in_ in tqdm(input_):
        m_dict = run_sm_text(
            morph_binary_file, in_, input_enc, output_enc
        )
        morph_all_dict.append(m_dict)
#    morph_all_dict = run_sm(
#        morph_binary_file, input_, input_enc, output_enc, input_type_text=False
#    )

    with open(o_file, 'w', encoding="utf-8") as f:
        write_str_lst = [ json.dumps(item, ensure_ascii=False) for item in morph_all_dict]
        write_str_lst = [ str(item) for item in morph_all_dict]
        f.write("\n".join(write_str_lst))


def run_sm_file_old(morph_binary_file, i_file, o_file, input_enc, output_enc):
    """ """
    
    i_f = open(i_file, "r", encoding="utf-8")
    input_contents = i_f.read()
    input_ = input_contents.strip()
    i_f.close()
    
    morph_all_dict = run_sm(
        morph_binary_file, input_, input_enc, output_enc, input_type_text=False
    )

    with open(o_file, 'w', encoding="utf-8") as f:
        write_str_lst = [ json.dumps(item, ensure_ascii=False) for item in morph_all_dict]
        f.write("\n".join(write_str_lst))


def main():
    """ """
    
    # Parsing Arguments
    parser = argparse.ArgumentParser()
    
    # Mandatory Arguments
    parser.add_argument(
        "input_enc", default="WX",
        choices=["DN", "KH", "RN", "SL", "VH", "WX"],
        help="input encoding"
    )
    parser.add_argument(
        "output_enc", default="roma",
        choices=["deva", "roma", "WX"],
        help="output encoding"
    )
    
    # Options (one of -t or -i, -o is mandatory)
    parser.add_argument(
        "-t", "--input_text", type=str,
        help="input string"
    )
    parser.add_argument(
        "-i", "--input_file", type=argparse.FileType('r', encoding='UTF-8'),
        help="reads from file if specified"
    )
    parser.add_argument(
        "-o", "--output_file", type=argparse.FileType('w', encoding='UTF-8'),
        help="for writing to file"
    )
    
    args = parser.parse_args()
    
    if args.input_file and args.input_text:
        print("Please specify either input text ('-t') or input file ('-i, -o')")
        sys.exit()
    
    input_enc = args.input_enc
    output_enc = args.output_enc
    
    if args.input_file:
        i_file = args.input_file.name
        o_file = args.output_file.name if args.output_file else "output.tsv"
        run_sm_file(
            morph_binary_file, i_file, o_file, input_enc, output_enc
        )
    elif args.input_text:
        res = run_sm_text(
            morph_binary_file, args.input_text, input_enc, output_enc
        )
        if args.output_file:
            with open(args.output_file.name, 'w', encoding='utf-8') as o_file:
                o_file.write(res)
        else:
            print(res)
    else:
        print("Please specify one of text ('-t') or file ('-i & -o')")
        sys.exit()
    

if __name__ == "__main__":
    main()
