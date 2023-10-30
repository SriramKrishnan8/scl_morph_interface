# Pada-Vishleshika - Sanskrit Morphological Analyser (Powered by Samsaadhanii)

[Samsaadhanii](www.sanskrit.uohyd.ac.in/scl) hosts various tools like morphological analyser, sandhi joiner, noun-forms generator, verb-forms generator, parser, translator, etc. An interface for its morphological analyser is built here and the results are converted to the format identical to [Sanskrit Heritage Segmenter's analysis](www.sanskrit.inria.fr/DICO/reader.fr.html). The following are the constituents:

1. all_morf.bin &rarr; binary file from Samsaadhanii that is built using lttoolbox and used to analyse a given word, invoked from samsaadhanii\_morph\_analysis.py
2. samsaadhanii\_morph\_analysis.py &rarr; a python interface / wrapper for morphological analysis of Samsaadhanii
2. convert\_scl\_to\_sh.py &rarr; contains conversion program of Samsaadhanii's results into the SH format
3. scl\_to\_sh\_map.py &rarr; contains mapping of Samsaadhanii terminology to SH terminology, used by convert\_scl\_to\_sh.py
4. transliteration.py  &rarr; contains transliteration methods
5. run\_scl.sh &rarr; sample input file is invoked for testing

## Pre-Requisites

1. lttoolbox (from Apertium)
```
sudo apt install lttoolbox
```
2. python3
3. devtrans (used for transliteration to and fro various notations, installed via pip)
```
pip3 install devtrans
```

## Instructions

To run samsaadhanii\_morph\_analysis.py:

```
python3 samsaadhanii_morph_analysis.py <input_encoding> <output_encoding> [-t text] [-i input_file] [-o output_file]
```

Options for:
* input\_encoding &rarr; WX, DN, RN, SL, KH, VH
* output\_encoding &rarr; deva, roma

Examples are provided in run.sh

## Output format

* input 
* status &rarr; ["success", "failed", "error", "unrecognized"]
* segmentation
* morph
    * word &rarr; pada
    * derived\_stem &rarr; stem / prātipadika
    * base &rarr; root / dhātu
    * derivational\_morph 
    * inflectional\_morphs &rarr; list of analyses
