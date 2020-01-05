"""
authors: @climatebrad, @dougjohnsonmd
"""

import os.path
import matplotlib.pyplot as plt
import pandas as pd

class NHANES():
    """Base NHANES loader class"""
    def __init__(self):
        self.data = None
        self.cols = None
        self.params = {}

    @staticmethod
    def get_length(start, end):
        """calculate length given start and end (end is na if length is 1)"""
        if pd.isna(end):
            end = start
        return end - start + 1

    def load_cols(self):
        """read in cols from format csv"""
        formatfile = self.params.get('formatfile')
        cols = pd.read_csv(formatfile, sep='\t')
        cols['length'] = cols.apply(lambda x: self.get_length(x.position, x['end position']), axis=1)
        cols.length = cols.length.astype(int)
        self.cols = cols


    def save_df(self):
        """save to csv"""
        outfile = self.params.get('datafile')
        self.data.to_csv(outfile, index=False)

    def load_file(self, all_cols=False):
        """load file either from infile, or if it does not exist, from URL"""
        infile = self.params.get('datafile')
        url = self.params.get('url')
        dtypes = self.params.get('dtypes',{})
        if not os.path.exists(infile):
            self.data = pd.read_fwf(url,
                                    widths=self.cols.length.to_list(),
                                    names=self.cols.variable.to_list())
            self.save_df()
        self.data = pd.read_csv(infile, dtype=dtypes)
        if not all_cols and self.params.get('usecols'):
            self.data = self.data[self.params['usecols']]

    def hist_amount(self, variable, outliers=100):
        """plot variable values to hist"""
        ax = self.data[self.data[variable] < outliers][variable].hist(bins=20)
        plt.title(self.cols[self.cols.variable == variable].description.to_string(index=False))
        plt.ylabel('# of patients')
        return ax
