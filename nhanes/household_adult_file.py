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
            'dtypes' : {'HAZA1CC' : str},
            'usecols' : [
                'HAR1',
                'HAR23',
                'HAR26',
                'HAC1E',
                'HAC1F',
                'HAC1G',
                'HAC1O',
                'HAL6',
                'HAL10',
                'HAL1',
                'HAL3',
                'HAL5',
                'SEQN',
                'DMARACER',
                'DMARETHN',
                'DMAETHNR',
                'HSSEX',
                'HSAGEIR',
                'HSAGEU',
                'HXPAXTMR',
                'HXPSESSR',
                'HXPEJ6A2',

            ]
        }
        self.load_cols()
        self.load_file()
