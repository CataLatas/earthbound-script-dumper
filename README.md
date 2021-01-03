# earthbound-script-dumper
An Earthbound/Mother 2 text script dumper that aims for a human readable format


## Running
This program requires Python 3.

To run, simply use the following command on the command line:  
`python3 script_dumper.py earthbound_rom output_file [symbols_file]`

Where:
- `earthbound_rom` is the filepath to an Earthbound or Mother 2 ROM
- `output_file` is the filepath where the output text dump file will be created
- `symbols_file` is an optional filepath to a file containing symbol definitions (see below)

## Symbol files
Symbol files allow for an even more readable text dump by defining labels and comments. The general syntax for those files is the following:

`LABEL = ADDRESS_IN_HEXADECIMAL[, OPTIONAL COMMENT]`  
(*e.g.* `TEXT_PMemberPoliteUpper = C7E6C5, "Sir/Ma'am" depending on party member`)  
A label name may only contain numbers, letters and underscores (`_`)

A semicolon (`;`) can also be used to start a comment in the symbols file. Everything after it will be ignored.

Invalid lines are ignored, but are also shown as a warning when read.


This repository contains a symbols file to be used with the US version of Earthbound at `symbols/symbols_US.txt`

## Features
- Translates control codes to a human-readable format (*e.g.* `[04 69 00]` becomes `[SET_FLAG PATH_TO_TWOSON_OPEN]`)
- Symbol files, allowing for custom labels and comments at a certain addresses (described above)
- Dumps the **entire** text script, including unused lines
- Works with Mother 2, Earthbound and the Earthbound localization prototype
