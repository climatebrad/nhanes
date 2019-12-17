"""
authors: @climatebrad, @dougjohnsonmd
"""

import os.path
import pandas as pd

def get_length(start, end):
    """calculate length given start and end (end is na if length is 1)"""
    if pd.isna(end):
        end = start
    return end - start + 1

def load_cols(formatfile='nhanes_questionnaire_format.csv'):
    """read in cols from format csv"""
    cols = pd.read_csv(formatfile, sep='\t')
    cols['length'] = cols.apply(lambda x: get_length(x.position, x['end position']), axis=1)
    cols.length = cols.length.astype(int)
    return cols

def save_df(data, outfile='household_adult_file.csv.gz'):
    """save to csv"""
    data.to_csv(outfile, index=False)

def load_household_adult_file(infile='household_adult_file.csv.gz', url='https://wwwn.cdc.gov/nchs/data/nhanes3/1a/adult.dat'):
    """load household_adult_file either from infile, or if it does not exist, from URL"""
    if not os.path.exists(infile):
        cols = load_cols()
        data = pd.read_fwf(url, widths=cols.length.to_list(), names=cols.variable.to_list())
        save_df(data)
        return data
    return pd.read_csv(infile, dtype={'HAZA1CC' : str})
