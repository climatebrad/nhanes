"""
authors: @climatebrad, @dougjohnsonmd
"""

import pandas as pd
from nhanes_loader import NHANES
from nhanes.exam_file import ExamFile
from nhanes.household_adult_file import HouseholdAdultFile

class AdultExam(CombinedExam):
    def __init__(self):
        adult = HouseholdAdultFile()
        params = {'exclusion_file' : 'data/adult_exclusion.csv' }
        super().__init__(adult, params)
        