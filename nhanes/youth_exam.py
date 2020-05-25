"""
authors: @climatebrad, @dougjohnsonmd
"""

import pandas as pd
from nhanes_loader import NHANES
from nhanes.exam_file import ExamFile
from nhanes.household_youth_file import HouseholdYouthFile

class YouthExam(CombinedExam):
    def __init__(self):
        youth = HouseholdYouthFile()
        params = {'exclusion_file' : 'data/youth_exclusion.csv' }
        super().__init__(youth, params)
        