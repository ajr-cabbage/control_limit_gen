import os
import sys

from data_parse import data_parse
from md_template import md_template


def main():
    try:
        # parse the arguments
        args = sys.argv
        if len(args) < 3:
            print("Please provide source file and destination file.")
            return 1
        else:
            source_file = args[1]
            dest_file = args[2]
        # get the paths to source/dest
        source_filepath = os.path.abspath(source_file)
        dest_filepath = os.path.abspath(dest_file)
        # read source CSV
        input_csv = ""
        with open(source_filepath) as f:
            input_csv = f.read()
        input_csv = input_csv.lower()
        # send csv to data_handling function
        output_md = data_parse(input_csv, md_template)
        if os.path.isdir(dest_filepath):
            print(f"Cannot write to {dest_file} as it is a directory")
            return 1
        # write formatted data to a file
        with open(dest_filepath, "w") as f:
            f.write(output_md)
            print(f"Sucessfully wrote to {dest_file}")
        return 0
    except Exception as e:
        print(e)
        return 1


if __name__ == "__main__":
    main()
