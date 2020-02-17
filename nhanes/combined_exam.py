"""
authors: @climatebrad, @dougjohnsonmd
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from nhanes_loader import NHANES
from nhanes.exam_file import ExamFile

class CombinedExam(NHANES):
    def __init__(self, adult_or_youth, params):
        super().__init__()
        exam = ExamFile()
        self.data = adult_or_youth.data.set_index('SEQN').join(exam.data.set_index('SEQN'),rsuffix='_exam')
        self.cols = pd.concat((adult_or_youth.cols, exam.cols))
        self.params = params
        
    def do_exclusion(self):
        exclusion = pd.read_csv(self.params['exclusion_file'])
        self.data = self.data.query(' & '.join(exclusion.inclusion_formula))
        
    def do_height_regression(self, gender, ethnicity, y_var):
        lr = LinearRegression()