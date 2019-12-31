"""
authors: @climatebrad, @dougjohnsonmd
"""

from nhanes_loader import NHANES

class HouseholdYouthFile(NHANES):
    """Loads Household Youth File"""
    def __init__(self):
        super().__init__()
        self.params = {
            'formatfile' : 'data/household_youth_file_format.csv',
            'datafile' : 'data/household_youth_file.csv.gz',
            'url' : 'https://wwwn.cdc.gov/nchs/data/nhanes3/1a/youth.dat',
        }
        self.load_cols()
        self.load_file()
