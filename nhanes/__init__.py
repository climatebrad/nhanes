"""
authors: @climatebrad, @dougjohnsonmd
"""

import os.path
import matplotlib.pyplot as plt
import pandas as pd

class NHANES():
    def __init__(self):
        self.data = None
        self.load_household_adult_file()
        self.cols = None
        self.load_cols()

    @staticmethod
    def get_length(start, end):
        """calculate length given start and end (end is na if length is 1)"""
        if pd.isna(end):
            end = start
        return end - start + 1

    def load_cols(self, formatfile='data/nhanes_questionnaire_format.csv'):
        """read in cols from format csv"""
        cols = pd.read_csv(formatfile, sep='\t')
        cols['length'] = cols.apply(lambda x: get_length(x.position, x['end position']), axis=1)
        cols.length = cols.length.astype(int)
        self.cols = cols


    def save_df(self, outfile='data/household_adult_file.csv.gz'):
        """save to csv"""
        self.data.to_csv(outfile, index=False)

    def load_household_adult_file(self, infile='data/household_adult_file.csv.gz', url='https://wwwn.cdc.gov/nchs/data/nhanes3/1a/adult.dat'):
        """load household_adult_file either from infile, or if it does not exist, from URL"""
        if not os.path.exists(infile):
            self.data = pd.read_fwf(url,
                                    widths=self.cols.length.to_list(),
                                    names=self.cols.variable.to_list())
            self.save_df()
        self.data = pd.read_csv(infile, dtype={'HAZA1CC' : str})

    def hist_amount(self, variable, outliers=100):
        """plot variable values to hist"""
        ax = self.data[self.data[variable] < outliers][variable].hist(bins=20)
        plt.title(self.cols[self.cols.variable == variable].description.to_string(index=False))
        plt.ylabel('# of patients')
        return ax
