import os
import sys

import re
import json

scl_keys = [
    "level", "vacanam",
    "vargaH", "lifgam", "viBakwiH",
    "XAwuH", "prayogaH", "lakAraH", "puruRaH", "paxI", "gaNaH",
    "kqw_XAwu", "kqw_prawyayaH", "waxXiwa_prawyayaH",
    "upasarga", "upapaxa_cp"
]

avy_identifying_key = "vargaH"

sup_identifying_key = "viBakwiH"
wif_identifying_key = "lakAraH"

kqw_identifying_key = "kqw_prawyayaH"
waxXiwa_identifying_key = "waxXiwa_prawyayaH"

#samAsa_identifying_key = "samAsa"
kqw_samAsa_identifying_key = "kqw_prawyayaH"
upapaxa_samAsa_identifying_key = "upapaxa_cp"
waxXiwa_samAsa_identifying_key = "waxXiwa_prawyayaH"
other_samAsa_identifying_key = "sapUpa"

scl_map = {
    "level" : ["0", "1", "2", "3", "4"],
    "vargaH" : ["nA", "sarva", "saMKyeyam", "saMKyA", "pUraNam", "avy", "sapUpa"],
#    "XAwuH" : [ list of XAwus ],
    "lifgam" : ["puM", "swrI", "napuM", "a"],
    "vacanam" : ["eka", "xvi", "bahu"],
    "puruRaH" : ["u", "ma", "pra"],
    "viBakwiH" : ["1", "2", "3", "4", "5", "6", "7", "8"],
    "lakAraH" : ["lat", "lit", "lut", "lqt", "lot", "laf", "viXilif", "ASIrlif", "luf", "lqf"],
    "paxI" : ["AwmanepaxI", "parasmEpaxI"],
    "prayogaH" : ["karwari", "karmaNi", "BAve"],
    "gaNaH" : ["BvAxiH", "axAxiH", "juhowyAxiH", "xivAxiH", "svAxiH", "wuxAxiH", "ruXAxiH", "wanAxiH", "kryAxiH", "curAxiH"],
#    "kqw_XAwu" : [ list of XAwus ],
    "kqw_prawyayaH" : ["wqc", "wumun", "wavyaw", "yak", "Sawq", "SAnac", "GaF", "Namul", "Nvul", "Nyaw", "lyut", "yaw", "kwvA", "lyap", "kwa", "kwavawu", "anIyar"],
    "waxXiwa_prawyayaH" : ["wal", "mawup", "warap", "wamap", "wva", "vaw", "wasil", "karam", "arWam", "pUrvaka", "mayat", "vAram", "kqwvasuc", "xA", "Sas"],
    "sanAxi_prawyayaH": ["Nic", "san", "yaf"]
#    "upasarga" : [ list of upasargas ],
#    "upapaxa_cp" : [ list of upapaxa_cp ],
}
    

scl_sh_map = {
    # lifgam
    "puM" : "m.", "swrI" : "f.", "napuM" : "n.", "a" : "*",
    # vacanam
    "eka" : "sg.", "xvi" : "du.", "bahu" : "pl.",
    # puruRaH
    "pra" : "3", "ma" : "2", "u" : "1",
    # viBakwiH
    "1" : "nom.", "2" : "acc.", "3" : "i.", "4" : "dat.",
    "5" : "abl.", "6" : "g.", "7" : "loc.", "8" : "voc.",
    # lakAraH
    "lat" : "pr.", "lit" : "pft.", "lut" : "per. fut.", "lqt" : "fut.", "lot" : "imp.",
    "laf" : "impft.", "viXilif" : "opt.", "ASIrlif" : "ben.", "luf" : "aor.", "lqf" : "cond.",
    # paxI-prayogaH - handled by function map_padi_prayoga, hence commented here
#    "AwmanepaxI" : "ac.", "parasmEpaxI" : "md.",
#    "karwari" : "", "karmaNi" : "ps.", "BAve" : "ps.",
    # gaNaH
    "BvAxiH" : "[1]", "axAxiH" : "[2]", "juhowyAxiH" : "[3]", "xivAxiH" : "[4]", "svAxiH" : "[5]",
    "wuxAxiH" : "[6]", "ruXAxiH" : "[7]", "wanAxiH" : "[8]","kryAxiH" : "[9]", "curAxiH" : "[10]",
    # sanAxi_prawyayaH
    "Nic" : "ca.", "san" : "des.", "yaf" : "int.",
    # kqw_prawyayaH
    # handled by function map_kqw_prawyaya
    # waxXiwa_prawyayaH
    "wasil" : "tasil", "mawup" : "matup", "vaw" : "vat", "wva" : "tva", "wal" : "tal",
    "mayat" : "mayaṭ", "warap" : "tarap", "wamap" : "tamap", "karam" : "karam", "arWam" : "artham",
    "pUrvaka" : "pūrvaka", "vAram" : "vāram", "kqwvasuc" : "kṛtvasuc", "xA" : "dā", "Sas" : "śas",
    # samAsa
    "sapUpa" : "iic."
}
    

def map_padi_prayoga(morph_dict):
    """ """
    
    sh_padi_prayoga = ""
    
    if morph_dict.get("paxI", "") == "parasmEpaxI" and morph_dict.get("prayogaH", "") == "karwari":
        sh_padi_prayoga = "ac."
    elif morph_dict.get("paxI", "") == "AwmanepaxI" and morph_dict.get("prayogaH", "") == "karwari":
        sh_padi_prayoga = "md."
    elif morph_dict.get("paxI", "") == "AwmanepaxI" and morph_dict.get("prayogaH", "") == "karmaNi":
        sh_padi_prayoga = "ps."
    elif morph_dict.get("paxI", "") == "AwmanepaxI" and morph_dict.get("prayogaH", "") == "BAve":
        sh_padi_prayoga = "ps."
    else:
        pass
        
    return sh_padi_prayoga
    

def handle_wif(morph_dict):
    """ """
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    conj = ""
    tense_mood = ""
    class_ = ""
    upasarga = ""
    voice = ""
    base = ""
    number = ""
    person = ""
    extra = ""
    for key in morph_dict.keys():
        if key == "puruRaH":
            person = scl_sh_map[morph_dict[key]]
        elif key == "lakAraH":
            tense_mood = scl_sh_map[morph_dict[key]]
        elif key == "paxI" or key == "prayogaH":
            voice = map_padi_prayoga(morph_dict) if voice == "" else voice
        elif key == "gaNaH":
            class_ = scl_sh_map[morph_dict[key]]
        elif key == "vacanam":
            number = scl_sh_map[morph_dict[key]]
        elif key == "sanAxi_prawyayaH":
            conj = scl_sh_map[morph_dict[key]]
        elif key == "upasarga":
            upasarga = morph_dict[key]
        elif key == "lemma":
            base = morph_dict[key]
        elif key in ["vargaH", "XAwuH", "level", "der_lemma"]:
            pass
        else:
            extra = scl_sh_map[morph_dict[key]]
    
    inf_morph_str = " ".join(list((conj, tense_mood, class_, voice, number, person, extra)))
    
    root = upasarga + "-" + base if upasarga else base
    
    return stem, root, inf_morph_str.strip(), der_morph_str.strip()


def handle_sup(morph_dict):
    """ """
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    gender = ""
    case = ""
    number = ""
    extra = ""
    for key in morph_dict.keys():
        if key == "lifgam":
            gender = scl_sh_map[morph_dict[key]]
        elif key == "vacanam":
            number = scl_sh_map[morph_dict[key]]
        elif key == "viBakwiH":
            case = scl_sh_map[morph_dict[key]]
        elif key == "lemma":
            stem = morph_dict[key]
        elif key in ["der_lemma", "vargaH", "level"]:
            pass
        else:
            extra = scl_sh_map[morph_dict[key]]
    
    inf_morph_str = " ".join(list((gender, number, case, extra)))
    
    return stem, root, inf_morph_str.strip(), der_morph_str.strip()
    
    
def map_kqw_prawyaya(conj, class_, voice, kqw_prawyayaH):
    """ """
    
    der_morph_str = ""
    
    if kqw_prawyayaH == "kwavawu":
        der_morph_str = " ".join(list((conj, "ppa.")))
    elif kqw_prawyayaH == "kwa":
        der_morph_str = " ".join(list((conj, "pp.")))
    elif kqw_prawyayaH == "Sawq_lat":
        der_morph_str = " ".join(list((conj, "ppr.", class_, voice)))
    elif kqw_prawyayaH == "SAnac_lat":
        if voice == "ps.":
            der_morph_str = " ".join(list((conj, "ppr.", voice)))
        elif voice == "ac." or voice == "md.":
            der_morph_str = " ".join(list((conj, "ppr.", class_, voice)))
        else:
            # here class information needs to be extracted from XAwu
            der_morph_str = " ".join(list((conj, "ppr.", voice)))
    elif kqw_prawyayaH == "yaw":
        der_morph_str = " ".join(list((conj, "pfp. [1]")))
    elif kqw_prawyayaH == "anIyar":
        der_morph_str = " ".join(list((conj, "pfp. [2]")))
    elif kqw_prawyayaH == "wavyaw":
        der_morph_str = " ".join(list((conj, "pfp. [3]")))
    elif kqw_prawyayaH == "wumun":
        der_morph_str = " ".join(list((conj, "inf.")))
    elif kqw_prawyayaH in ["kwvA", "lyap", "Namul"]:
        der_morph_str = " ".join(list((conj, "abs.")))
    elif kqw_prawyayaH in ["wqc", "yak", "GaF", "Nvul", "Nyaw", "lyut"]:
        # Need to give a proper analysis for SH, but SH does not analyse these
        der_morph_str = ""
    else:
        der_morph_str = ""
    
    return der_morph_str


def handle_kqw(morph_dict):
    """ """
    
    stem = ""
    root = ""
    base = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    conj = ""
    class_ = ""
    voice = ""
    upasarga = ""
    kqw_XAwu = ""
    kqw_prawyayaH = ""
    gender = ""
    case = ""
    number = ""
    extra = ""
    for key in morph_dict.keys():
        if key == "lifgam":
            gender = scl_sh_map[morph_dict[key]]
        elif key == "vacanam":
            number = scl_sh_map[morph_dict[key]]
        elif key == "viBakwiH":
            case = scl_sh_map[morph_dict[key]]
        elif key == "paxI" or key == "prayogaH":
            voice = map_padi_prayoga(morph_dict) if voice == "" else voice
        elif key == "gaNaH":
            class_ = scl_sh_map[morph_dict[key]]
        elif key == "sanAxi_prawyayaH":
            conj = scl_sh_map[morph_dict[key]]
        elif key == "kqw_XAwu":
            kqw_XAwu = morph_dict[key]
        elif key == "kqw_prawyayaH":
            kqw_prawyayaH = morph_dict[key]
        elif key == "upasarga":
            upasarga = morph_dict[key]
        elif key == "lemma":
            base = morph_dict[key]
        elif key == "der_lemma":
            stem = morph_dict[key]
        elif key in ["vargaH", "XAwuH", "level"]:
            pass
        else:
            extra = scl_sh_map[morph_dict[key]]
    
    inf_morph_str = " ".join(list((gender, number, case, extra)))
    der_morph_str = map_kqw_prawyaya(conj, class_, voice, kqw_prawyayaH)
    
    # For abs and inf
    if inf_morph_str.strip() == "":
        inf_morph_str = der_morph_str
        der_morph_str = ""
    
    if kqw_XAwu:
        root = upasarga + "-" + kqw_XAwu if upasarga else kqw_XAwu
    elif base:
        root = upasarga + "-" + base if upasarga else base
    
    return stem, root, inf_morph_str.strip(), der_morph_str.strip()
    
    
def map_waxXiwa_prawyaya(waxXiwa_prawyayaH):
    """ """
    
    # Discuss with Amba Madam and Gerard Sir regarding the 
    # representation of waxXiwa_prawyayaH as a derived 
    # analysis with respect to SH terminologies
    
    # Temporarily returning the same waxXiwa_prawyayaH
    return waxXiwa_prawyayaH


def handle_waxXiwa(morph_dict):
    """ """
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    gender = ""
    case = ""
    number = ""
    waxXiwa_prawyayaH = ""
    extra = ""
    for key in morph_dict.keys():
        if key == "lifgam":
            gender = scl_sh_map[morph_dict[key]]
        elif key == "vacanam":
            number = scl_sh_map[morph_dict[key]]
        elif key == "viBakwiH":
            case = scl_sh_map[morph_dict[key]]
        elif key == "lemma":
            stem = morph_dict[key]
        elif key == "waxXiwa_prawyayaH":
            waxXiwa_prawyayaH = scl_sh_map[morph_dict[key]]
        elif key in ["vargaH", "level", "der_lemma"]:
            pass
        else:
            extra = scl_sh_map[morph_dict[key]]
        
    inf_morph_str = " ".join(list((gender, number, case, extra)))
    der_morph_str = map_waxXiwa_prawyaya(waxXiwa_prawyayaH)
    
    return stem, root, inf_morph_str.strip(), der_morph_str.strip()
    

def avy_condition(morph_dict):
    """ """
    
    return morph_dict.get("vargaH", "") == "avy"


def handle_avy(morph_dict):
    """ """
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    extra = ""
    avy = ""
    waxXiwa_prawyayaH = ""
    for key in morph_dict.keys():
        if key == "lemma":
            stem = morph_dict[key]
        elif key == "vargaH" and morph_dict[key] == "avy":
            avy = "ind."
        elif key == "waxXiwa_prawyayaH":
            # Currently this is not included as SH does not handle this
            # Should check with Amba madam and Gerard sir
            waxXiwa_prawyayaH = scl_sh_map[morph_dict[key]]
        elif key in ["vargaH", "der_lemma", "level"]:
            pass
        else:
            extra = scl_sh_map[morph_dict[key]]
    
    inf_morph_str = " ".join(list((avy, extra)))
    
    return stem, root, inf_morph_str.strip(), der_morph_str.strip()

    
def handle_upapaxa_pUrva(morph_dict):
    """ """
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    stem = ""
    root = ""
    base = ""
    gender = ""
    upapaxa_cp = ""
    kqw_XAwu = ""
    upasarga = ""
    extra = ""
    for key in morph_dict.keys():
        if key == "lifgam":
            gender = scl_sh_map[morph_dict[key]]
        elif key == "upapaxa_cp":
            upapaxa_cp = morph_dict[key]
        elif key == "lemma":
            base = morph_dict["lemma"]
        elif key == "der_lemma":
            stem == morph_dict["der_lemma"]
        elif key in ["level", "vargaH", "XAwuH"]:
            pass
        else:
            extra = scl_sh_map[morph_dict[key]]
    
    # Since SH does not differentiate the upapaxa_cp separately, these
    # are marked simply as "iic."
    inf_morph_str = "iic."
#    der_morph_str = "agt."
    
    root = base if base else root
    
    return stem, root, inf_morph_str.strip(), der_morph_str.strip()


def handle_kqw_pUrva(morph_dict):
    """ """
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    conj = ""
    class_ = ""
    voice = ""
    upasarga = ""
    kqw_XAwu = ""
    kqw_prawyayaH = ""
    gender = ""
    case = ""
    number = ""
    extra = ""
    for key in morph_dict.keys():
        if key == "lifgam":
            gender = scl_sh_map[morph_dict[key]]
        elif key == "paxI" or key == "prayogaH":
            voice = map_padi_prayoga(morph_dict) if voice == "" else voice
        elif key == "gaNaH":
            class_ = scl_sh_map[morph_dict[key]]
        elif key == "sanAxi_prawyayaH":
            conj = scl_sh_map[morph_dict[key]]
        elif key == "kqw_XAwu":
            kqw_XAwu = morph_dict[key]
        elif key == "kqw_prawyayaH":
            kqw_prawyayaH = morph_dict[key]
        elif key == "upasarga":
            upasarga = morph_dict[key]
        elif key == "lemma":
            base = morph_dict[key]
        elif key == "der_lemma":
            stem = morph_dict[key]
        elif key in ["vargaH", "XAwuH", "level"]:
            pass
        else:
            extra = scl_sh_map[morph_dict[key]]
    
    inf_morph_str = "iic."
    der_morph_str = map_kqw_prawyaya(conj, class_, voice, kqw_prawyayaH)
    
    if kqw_XAwu:
        root = upasarga + "-" + kqw_XAwu if upasarga else kqw_XAwu
    elif base:
        root = upasarga + "-" + base if upasarga else base
    
    return stem, root, inf_morph_str.strip(), der_morph_str.strip()
    

def handle_waxXiwa_pUrva(morph_dict):
    """ """
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    gender = ""
    case = ""
    number = ""
    waxXiwa_prawyayaH = ""
    extra = ""
    for key in morph_dict.keys():
        if key == "lifgam":
            gender = scl_sh_map[morph_dict[key]]
        elif key == "lemma":
            stem = morph_dict[key]
        elif key == "waxXiwa_prawyayaH":
            waxXiwa_prawyayaH = scl_sh_map[morph_dict[key]]
        elif key in ["vargaH", "level", "der_lemma"]:
            pass
        else:
            extra = scl_sh_map[morph_dict[key]]
        
    inf_morph_str = "iic."
    der_morph_str = map_waxXiwa_prawyaya(waxXiwa_prawyayaH)
    
    return stem, root, inf_morph_str.strip(), der_morph_str.strip()
    

def handle_samAsa_pUrva(morph_dict):
    """ """
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    for key in morph_dict.keys():
        if key == "vargaH" and morph_dict.get("vargaH", "") == "sapUpa":
            inf_morph_str = "iic."
        elif key == "lifgam":
            gender = scl_sh_map[morph_dict[key]]
        elif key == "lemma":
            root = morph_dict[key]
        elif key == "der_lemma":
            stem = morph_dict[key]
        else:
            pass
    
    return stem, root, inf_morph_str.strip(), der_morph_str.strip()


def handle_upapaxa_uttara(morph_dict):
    """ """
    
    stem = ""
    root = ""
    inf_morph_str = ""
    der_morph_str = ""
    
    stem = ""
    root = ""
    base = ""
    gender = ""
    upapaxa_cp = ""
    number = ""
    case = ""
    extra = ""
    for key in morph_dict.keys():
        if key == "lifgam":
            gender = scl_sh_map[morph_dict[key]]
        elif key == "vacanam":
            number = scl_sh_map[morph_dict[key]]
        elif key == "viBakwiH":
            case = scl_sh_map[morph_dict[key]]
        elif key == "upapaxa_cp":
            upapaxa_cp = morph_dict[key]
        elif key == "lemma":
            base = morph_dict[key]
        elif key == "der_lemma":
            stem = morph_dict[key]
        elif key in ["vargaH", "level"]:
            pass
        else:
            extra = scl_sh_map[morph_dict[key]]
    
    inf_morph_str = "iic."
#    der_morph_str = "agt."
    
    root = base if base else root
    
    return stem, root, inf_morph_str.strip(), der_morph_str.strip()
    

