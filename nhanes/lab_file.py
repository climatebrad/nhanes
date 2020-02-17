"""
authors: @climatebrad, @dougjohnsonmd
"""

from nhanes_loader import NHANES

class LabFile(NHANES):
    """Loads Laboratory File"""
    def __init__(self):
        super().__init__()
        self.params = {
            'formatfile' : 'data/lab_file_format.csv',
            'datafile' : 'data/lab_file.csv.gz',
            'url' : 'https://wwwn.cdc.gov/nchs/data/nhanes3/1a/lab.dat',
        }
        self.load_cols()
        self.load_file()
