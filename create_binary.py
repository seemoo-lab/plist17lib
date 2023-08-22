from plist17lib import _BinaryPlist17Writer
import sys, getopt
import os
import json

from io import BytesIO

def create_from_json(json_in_path, plist_file_path, with_type_info):
    with open(json_in_path, 'r') as json_file:
        data = json.load(json_file)
        f = open(plist_file_path, 'wb') # will overwrite file
        p = _BinaryPlist17Writer(f)
        p.write(data, with_type_info=with_type_info)
        f.close()

def printHelp(isError=False):
    if isError:
        out = sys.stderr
    else:
        out = sys.stdout
    print('Usage:', file=out)
    print('  ' + os.path.basename(__file__) + ' [-t] -i <input> -o <output>', file=out)
    print('  ' + os.path.basename(__file__) + ' [--typed] --input <input> --output <output>', file=out)
    print('Input and output can either both be file paths, or both be directories.', file=out)
    print('The output contains additional type information if the option --typed or -t is used.', file=out)

def main(argv):
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

    if not outputpath:
        print('No output specified.')
        printHelp(isError=True)
        sys.exit(1)

    if os.path.isfile(inputpath):
        if not os.path.basename(outputpath) or os.path.isdir(outputpath):
            print('The specified input is not a directory, so the output path must also not be a directory.')
            printHelp(isError=True)
            sys.exit(1)
        else:
            create_from_json(inputpath, outputpath, typed)
    else:
        if os.path.isfile(outputpath):
            print('The specified input is a directory, so the output path must be also a directory.')
            printHelp(isError=True)
            sys.exit(1)
        if not os.path.exists(outputpath):
            # Create new output directory since it does not exist
            os.makedirs(outputpath)

        # create *.bplist17 files for all *.json files in directory
        for file in sorted(os.listdir(inputpath)): 
            if file.endswith(".json"):
                in_filepath = os.path.join(inputpath, file)
                # use file name without 'bplist17' at the end, i.e. file[:-4], and append 'bplist17' instead
                out_filepath = os.path.join(outputpath, file[:-4] + 'bplist17')
                # print('Input file path is:  ', in_filepath)
                # print('Output file path is: ', out_filepath)
                create_from_json(in_filepath, out_filepath, typed)

    print('Done.')


if __name__ == "__main__":
    main(sys.argv[1:])
