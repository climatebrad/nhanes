"""
authors: @climatebrad, @dougjohnsonmd
"""

from nhanes_loader import NHANES

class ExamFile(NHANES):
    """Loads Household Adult File"""
    def __init__(self):
        super().__init__()
        self.params = {
            'formatfile' : 'data/exam_file_format.csv',
            'datafile' : 'data/exam_file.csv.gz',
            'url' : 'https://wwwn.cdc.gov/nchs/data/nhanes3/1a/exam.dat',
            'dtypes' : {
                'DEPSTLC2' : 'category',
                'DEPSTLC3' : 'category',
                'DEPSTLC4' : 'category',
                'DEPSTLC5' : 'category',
                'DEPSTLC6' : 'category',
                'DMARACER' : 'category',
             }
        }
        self.load_cols()
        self.load_file()
