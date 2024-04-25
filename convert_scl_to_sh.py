import os
import sys

import re
import json

from tqdm import tqdm

import devtrans as dt

import scl_to_sh_map as ssm
import transliteration as tl

keys = [
    "level", "vacanam",
    "vargaH", "lifgam", "viBakwiH",
    "XAwuH", "prayogaH", "lakAraH", "puruRaH", "paxI", "gaNaH",
    "kqw_XAwu", "kqw_prawyayaH", "waxXiwa_prawyayaH",
    "upasarga", "upapaxa_cp"
]

def wx_to_dev(text):
    """ """
    
    return dt.wx2dev(text, False)


def decode_level_0(morph_dict):
    """ """
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    if ssm.upapaxa_samAsa_identifying_key in morph_dict:
        stem, root, inf_morph_str, der_morph_str = ssm.handle_upapaxa_pUrva(morph_dict)
    elif ssm.kqw_samAsa_identifying_key in morph_dict:
        stem, root, inf_morph_str, der_morph_str = ssm.handle_kqw_pUrva(morph_dict)
    elif ssm.waxXiwa_samAsa_identifying_key in morph_dict:
        stem, root, inf_morph_str, der_morph_str = ssm.handle_waxXiwa_pUrva(morph_dict)
    elif ssm.other_samAsa_identifying_key in morph_dict:
        stem, root, inf_morph_str, der_morph_str = ssm.handle_samAsa_pUrva(morph_dict)
    else:
        stem, root, inf_morph_str, der_morph_str = "", "", "", ""
    
    return stem, root, inf_morph_str, der_morph_str
    

def decode_level_1(morph_dict):
    """ """
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    if ssm.avy_condition(morph_dict):
        stem, root, inf_morph_str, der_morph_str = ssm.handle_avy(morph_dict)
    elif ssm.sup_identifying_key in morph_dict:
        stem, root, inf_morph_str, der_morph_str = ssm.handle_sup(morph_dict)
    elif ssm.wif_identifying_key in morph_dict:
        stem, root, inf_morph_str, der_morph_str = ssm.handle_wif(morph_dict)
    else:
        stem, root, inf_morph_str, der_morph_str = "", "", "", ""
    
    return stem, root, inf_morph_str, der_morph_str


def decode_level_2(morph_dict):
    """ """
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    if ssm.kqw_identifying_key in morph_dict:
        stem, root, inf_morph_str, der_morph_str = ssm.handle_kqw(morph_dict)
    else:
        stem, root, inf_morph_str, der_morph_str = "", "", "", ""
    
    return stem, root, inf_morph_str, der_morph_str


def decode_level_3(morph_dict):
    """ """
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    if ssm.waxXiwa_identifying_key in morph_dict:
        stem, root, inf_morph_str, der_morph_str = ssm.handle_waxXiwa(morph_dict)
    else:
        stem, root, inf_morph_str, der_morph_str = "", "", "", ""
    
    return stem, root, inf_morph_str, der_morph_str


def decode_level_4(morph_dict):
    """ """
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    # Considering only upapaxa_cp as only these were available
    # Uncomment others if they are available
    if ssm.upapaxa_samAsa_identifying_key in morph_dict:
        stem, root, inf_morph_str, der_morph_str = ssm.handle_upapaxa_uttara(morph_dict)
#    elif ssm.kqw_samAsa_identifying_key in morph_dict:
#        stem, root, inf_morph_str, der_morph_str = ssm.handle_kqw_uttara(morph_dict)
#    elif ssm.waxXiwa_samAsa_identifying_key in morph_dict:
#        stem, root, inf_morph_str, der_morph_str = ssm.handle_waxXiwa_uttara(morph_dict)
#    elif ssm.other_samAsa_identifying_key in morph_dict:
#        stem, root, inf_morph_str, der_morph_str = ssm.handle_samAsa_uttara(morph_dict)
    else:
        stem, root, inf_morph_str, der_morph_str = "", "", "", ""
    
    return stem, root, inf_morph_str, der_morph_str


def decode_morph_analysis(input_, morph_str, output_enc):
    """ """
    
    lemma = re.search('^(.*?)<', morph_str).group(1)
    der_lemma = morph_str
    der_lemma = re.sub(r'(^.*?(<.*?>))+|(<.*?>)', '', der_lemma)
    morph_matches = re.findall('<(.*?)>', morph_str)
    
    scl_morph_dict = {}
    scl_morph_dict["lemma"] = lemma
    scl_morph_dict["der_lemma"] = der_lemma
    for match in morph_matches:
        key, value = tuple(match.split(":"))
        scl_morph_dict[key] = value
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    if scl_morph_dict["level"] == "0":
        # Check what is zero
        stem, root, inf_morph_str, der_morph_str = decode_level_0(scl_morph_dict)
    elif scl_morph_dict["level"] == "1":
        # inf analysis
        stem, root, inf_morph_str, der_morph_str = decode_level_1(scl_morph_dict)
    elif scl_morph_dict["level"] == "2":
        # kqw
        stem, root, inf_morph_str, der_morph_str = decode_level_2(scl_morph_dict)
    elif scl_morph_dict["level"] == "3":
        # waxXiwa
        stem, root, inf_morph_str, der_morph_str = decode_level_3(scl_morph_dict)
    elif scl_morph_dict["level"] == "4":
        # samAsa
        stem, root, inf_morph_str, der_morph_str = decode_level_4(scl_morph_dict)
    else:
        # unknown
        pass
    
    sh_morph_dict = {}
    
    # Modify this word based on how it is handled in SH
    
    sh_morph_dict["word"] = input_
    sh_morph_dict["stem"] = tl.output_transliteration(stem, output_enc)[0]
    sh_morph_dict["root"] = tl.output_transliteration(root, output_enc)[0]
    sh_morph_dict["derivational_morph"] = der_morph_str
    sh_morph_dict["inflectional_morphs"] = [ inf_morph_str ]
    
    return scl_morph_dict, sh_morph_dict
    

def convert(item, output_enc):
    
    item = item.replace("^", "")
    item = item.replace("$", "")
    
    new_dict = {}
    status_val = ()
    
    morph_possibilites = item.split("/")
    input_ = morph_possibilites[0]
    trans_input, trans_enc = tl.output_transliteration(input_, output_enc)
    new_dict["input"] = trans_input
    
    if "*" in "/".join(morph_possibilites[1:]):
        new_dict["status"] = "unrecognized"
        status_val = (trans_input, "unrecognized")
        
        return new_dict, status_val
    else:
        new_dict["status"] = "success"
        
        new_dict["segmentation"] = [ trans_input ]
        status_val = (trans_input, "success")
    
    scl_morphs_lst = []
    sh_morphs_lst = []
    
    for j in range(len(morph_possibilites)):
        if j == 0:
            continue
        
        scl_morph, sh_morph = decode_morph_analysis(
            trans_input, morph_possibilites[j], output_enc
        )
        scl_morphs_lst.append(scl_morph)
        sh_morphs_lst.append(sh_morph)
    
    new_dict["morph"] = sh_morphs_lst
    new_dict["source"] = "SCL"
    
    return new_dict, status_val


def convert_all(scl_morph_str, output_enc):
    """ """
    
    if " " in scl_morph_str:
        terms = scl_morph_str.split(" ")
    else:
        terms = [ scl_morph_str ]
    
    analysis_dict = {}
    new_term = ""
    status = ""
    
    for trm_analysis in terms:
        new_dict, status_val = convert(trm_analysis, output_enc)
        
        if status_val[1] == "unrecognized":
            analysis_dict = new_dict
            new_term = status_val[0]
            status = status_val[1]
            break
            
        if not analysis_dict:
            analysis_dict = new_dict
            new_term = status_val[0]
            status = status_val[1]
        else:
            new_mrph_lst = analysis_dict["morph"] + new_dict["morph"]
            analysis_dict["morph"] = new_mrph_lst
            new_term = new_term + " " + status_val[0]
            status = "success" if (status == "success" and status == status_val[1]) else "unrecognized"
    
    return analysis_dict, (new_term, status)
    

