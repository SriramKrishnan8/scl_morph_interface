import devtrans as dt


def input_transliteration(input_text, input_enc):
    """ Converts input in any given notation to WX  
    """
    
    trans_input = ""
    trans_enc = ""
    
    if input_enc == "DN":
        trans_input = dt.dev2wx(input_text)
        trans_enc = "WX"
    elif input_enc == "RN":
        trans_input = dt.iast2wx(input_text)
        trans_enc = "WX"
    else:
        trans_input = input_text
        trans_enc = input_enc
    
    # The following condition makes sure that the chandrabindu
    # which comes on top of other characters is replaced with m
    if "z" in trans_input:
        if trans_input[-1] == "z":
            trans_input = trans_input.replace("z", "m")
        else:
            trans_input = trans_input.replace("z", "M")
    
    return (trans_input, trans_enc)


def output_transliteration(output_text, output_enc):
    """ Converts the output which is always in WX to 
        deva or roma
    """
    
    trans_output = ""
    trans_enc = ""
    
    if output_enc == "deva":
        trans_out = dt.wx2dev(output_text)
        num_map = str.maketrans('०१२३४५६७८९', '0123456789')
        trans_output = trans_out.translate(num_map)
        trans_enc = "deva"
    elif output_enc == "roma":
        trans_output = dt.wx2iast(output_text)
        trans_enc = "roma"
    else:
        trans_output = output_text
        trans_enc = output_enc
    
    return (trans_output, trans_enc)
    

