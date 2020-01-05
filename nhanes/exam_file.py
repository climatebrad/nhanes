"""
authors: @climatebrad, @dougjohnsonmd
"""

from nhanes_loader import NHANES

class ExamFile(NHANES):
    """Loads Exam File"""
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
             },
            'usecols' : [
                'SPPQ5',
                'SPPMANEU',
                'DMARETHN',
                'DMAETHNR',
                'DMARACER',
                'MYPB11',
                'MYPB27A',
                'MYPB27B',
                'HSAGEIR',
                'HXPEJ6A2',
                'SPPTECH1',
                'SPPTRIAL',
                'SPPPEAK',
                'SPPFEV05',
                'SPPFEV1',
                'SPPFEV3',
                'SPPFEV6',
                'SPPFVC',
                'SPPMMEF',
                'SPPFEF75',
                'SPPTYPE',
                'SPPREPRO',
                'SPPTIME',
                'SPPEXPIR',
                'SPPTEMP',
                'SEQN',
                'HSSEX',
                'WTPFHX6',
                'MXPAXTMR',
                'BMPHT',
                'BMPSITHT',
                'BMPWT',
            ]
        }
        self.load_cols()
        self.load_file()
