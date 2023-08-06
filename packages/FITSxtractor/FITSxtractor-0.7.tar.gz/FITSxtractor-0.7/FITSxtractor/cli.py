#!/usr/bin/env python3
"""
This script crawls over a directory, that contains xml files form a FITS output. It extracts
the metadata and saves it accordingly in a excel file / table.
FITS documentation link: https://projects.iq.harvard.edu/fits/fits-xml

Usage:
- The directory path is handed to the program via CLI
- The outputfile name is handed via CLI (the name can contain the file extension)

@Author: ovanov
@Date: 23.06.21
@LastChanged: 28.07.21
"""

import os
import sys
import argparse
import time
from dataclasses import asdict
from typing import Dict, List
import xml.etree.cElementTree as ET

import pandas as pd
from pandas.core.frame import DataFrame
from tqdm import trange


from ExtractorClass import Extraction
from FITSClass import FITS_obj

def argument_parser() -> Dict:
    """
    The Argument parser specifies positional and optional arguments. The directory path is expected
    and therefore registered as a positional argument. The optional argument is the outputfile name.
    """
    parser = argparse.ArgumentParser('Metadata Extractor', description='Command line tool for specific data extraction from xml files')
    parser.add_argument('infile',
    help='The first argument should be a directory path, containing xml files',
    type=str,
    nargs='*',
    default=[sys.stdin])

    parser.add_argument('--output', '-o',
    help='Give the path and the name of the output file. The name of the output file should be specified (use .csv or .xlsx) If no extension was specified, it defaults to .xlsx',
    nargs='?',
    type=str,
    default=False)

    # future TODO: adding more flags, if more "explicit" XML information is needed

    return parser

def crawler(p: str) -> List[Dict]:
    """
    This function takes the path variable 'p' and iterates over the files.
    it passes each file to the extractor function. Each returend object is appended as a DICT to a LIST.
    """
    for root, dirs, files in os.walk(p):
        # os.walk yields a 3-tuple of strings, which can be concatenated
        if len(files) != 0:
            # maybe the directory is empty or yields no files (empty list). making sure, there is no error
            table_list = []
            
            for num in trange(len(files)): # trange from tqdm module is used to create the progressbar
                file = os.path.join(root, files[num])
                table_list.append(extractor(file))

            return table_list

        else:
            raise KeyError("directory is empty. Please give a directory with at least one file.")


def extractor(file_path: str) -> FITS_obj:
    """
    This function Calls the ExtractorFITS class which uses specific methods to extract the needed metadata from the 
    subtrees of each xml file. This class is expandable as well as the FITSClass and this function.
    """
    metadata = Extraction(file_path) 

    ## One can extend or add more methods in the ExtractorClass.py file in order to call them here :)
    metadata = metadata.extract_fileinfo()
    metadata = metadata.extract_identification()
    metadata = metadata.extract_filestatus()
    
    return asdict(metadata.fits_obj) # retruning as asdict in order to represent the dataclass-obj as a hash (pandas can use this as a df structure)
    

def table_writer(l: List[Dict], filename: str) -> DataFrame:
    """
    This function creates a table with the FITS dataclass attributes
    as columns. Pandas takes the FITS_OBJ attribute's values to fill the DataFrame and write to file
    """
    df = pd.DataFrame(l)

    ## respect the extensnions in the --output flag
    if 'csv' in filename:
        return df.to_csv(filename, sep='\t')
    elif 'xlsx' in filename:
        return df.to_excel(filename)
    else:
        return df.to_excel(f'{filename}.xlsx')


def main():

    # get parser together
    parser = argument_parser()
    args = parser.parse_args()
    args_dict = {
        arg: value for arg, value in vars(args).items()
        if value is not None
    }

    if len(args_dict['infile']) < 1: # this conditional is met, if no directory containing XML files was given
        raise KeyError('Please specify a directory path')

    if args_dict['output'] == False: # this conditional is met, if not output filename was given
        raise KeyError('Please give a output filename')

    return table_writer(crawler(args_dict['infile'][0]),args_dict['output'])


if __name__ == "__main__":

    start_time = time.time()
    main()
    print(f'--- {time.time() - start_time:.3f} seconds ---')