from plist17lib import _BinaryPlist17Parser
import plistlib
import json
import sys, getopt
import os
from . import prog_name
from io import BytesIO

def parse_file(plist_file_path, json_out_path, with_type_info):
    with open(plist_file_path, 'rb') as file:
        p = _BinaryPlist17Parser(dict_type=dict)
        result = p.parse(file, with_type_info=with_type_info)
        jsonString = json.dumps(result, indent=4)
        # write to output if specified, else write to stdout
        if json_out_path:
             f = open(json_out_path, "w") # will overwrite file
             f.write(jsonString)
             f.close()
        else:
            print("================================================================================")
            print("Parsing: ", plist_file_path)
            print("--------------------------------------------------------------------------------")
            print(jsonString)
            print("================================================================================\n\n")

def printHelp(isError=False):
    if isError:
        out = sys.stderr
    else:
        out = sys.stdout
    print('Usage:', file=out)
    print('  %s [-t] -i <input> [-o <output>]' % prog_name, file=out)
    print('  %s [--typed] --input <input> [--output <output>]' % prog_name, file=out)
    print('Input and output can either both be file paths, or both be directories.', file=out)
    print('The output contains additional type information if the option --typed or -t is used.', file=out)

def main(argv = None):
    if argv == None:
        argv = sys.argv[1:]
    inputpath = ''
    outputpath = ''
    typed = False
    opts, args = getopt.getopt(argv,"hti:o:",["help","typed","input=","output="])
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printHelp()
            sys.exit(0)
        elif opt in ("-t", "--typed"):
            typed = True
        elif opt in ("-i", "--input"):
            inputpath = arg
            # print('Input is:  ', inputpath)
        elif opt in ("-o", "--output"):
            outputpath = arg
            # print('Output is: ', outputpath)

    if not inputpath: 
        print('No input specified.')
        printHelp(isError=True)
        sys.exit(1)

    if os.path.isfile(inputpath):
        if outputpath and (not os.path.basename(outputpath) or os.path.isdir(outputpath)):
            print('The specified input is not a directory, so the output path must also not be a directory.')
            printHelp(isError=True)
            sys.exit(1)
        else:
            parse_file(inputpath, outputpath, typed)
    else:
        if outputpath: # if an output path was specified, check it
            if os.path.isfile(outputpath):
                print('The specified input is a directory, so the output path must be also a directory.')
                printHelp(isError=True)
                sys.exit(1)
            if not os.path.exists(outputpath):
                # Create new output directory since it does not exist
                os.makedirs(outputpath)

        # parse all *.bplist17 files in directory
        for file in sorted(os.listdir(inputpath)): 
            if file.endswith(".bplist17"):
                in_filepath = os.path.join(inputpath, file)
                if outputpath:
                    # use file name without 'bplist17' at the end, i.e. file[:-8], and append 'json' instead
                    out_filepath = os.path.join(outputpath, file[:-8] + 'json')
                else:
                    out_filepath = ''
                # print('Input file path is:  ', in_filepath)
                # print('Output file path is: ', out_filepath)
                parse_file(in_filepath, out_filepath, typed)

    print('Done.')


if __name__ == "__main__":
    main(sys.argv[1:])
