"""
authors: @climatebrad, @dougjohnsonmd
"""

from nhanes_loader import NHANES

class HouseholdAdultFile(NHANES):
    """Loads Household Adult File"""
    def __init__(self):
        super().__init__()
        self.params = {
            'formatfile' : 'data/household_adult_file_format.csv',
            'datafile' : 'data/household_adult_file.csv.gz',
            'url' : 'https://wwwn.cdc.gov/nchs/data/nhanes3/1a/adult.dat',
            'dtypes' : {'HAZA1CC' : str}
        }
        self.load_cols()
        self.load_file()
