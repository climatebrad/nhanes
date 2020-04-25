"""
authors: @climatebrad, @dougjohnsonmd
"""

from nhanes_loader import NHANES

class HouseholdYouthFile(NHANES):
    """Loads Household Youth File"""
    def __init__(self, **params):
        super().__init__()
        self.params = {
            'formatfile' : 'data/household_youth_file_format.csv',
            'datafile' : 'data/household_youth_file.csv.gz',
            'url' : 'https://wwwn.cdc.gov/nchs/data/nhanes3/1a/youth.dat',
            'usecols' : [
                'SEQN',
              #  'MYPB11',     # youth only
              #  'MYPB27A',    # youth only
               # 'MYPB27B',    # youth only
                'HYE1G',
                'HYE1H',
                'HSSEX',
                'HSAGEIR',
                'HSAGEU',
                'DMARACER',
                'DMARETHN',
                'DMAETHNR',
                'HXPAXTMR',
                'HXPSESSR',
                'HYG2',
                'HYG4',
                'HYG7',
                'HYG8',
                'HYG12',
              #  'HXPEJ6A2',
            ]
        }
        self.params['usecols'] = params.get('usecols', self.params['usecols'])
        self.load_cols()
        self.load_file()
