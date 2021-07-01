"""
authors: @climatebrad, @dougjohnsonmd
Load NHANES adult, youth, exam files, perform Hankinson exclusions, create additional features
"""

import pandas as pd
import nhanes_loader
from nhanes.household_adult_file import HouseholdAdultFile
from nhanes.household_youth_file import HouseholdYouthFile
from nhanes.exam_file import ExamFile

def ratio_feature(df, feature, numerator, denominator, multiplication_factor=1):
    '''generate new dataframe feature as a ratio between numerator and denominator'''
    if pd.isnull(multiplication_factor):
        multiplication_factor = 1
        
    if pd.isnull(denominator):
        df[feature] = df[numerator] * multiplication_factor
    else:
        df[feature] = df[numerator] / df[denominator] * multiplication_factor
    
def create_features(df, features_csv='data/features.csv'):
    """Load feature information from csv for use by ratio_feature"""
    variable_list = pd.read_csv(features_csv)
    for index, row in variable_list.iterrows():
        ratio_feature(adult_final, row.feature, row.numerator, row.denominator, row.multiplication_factor)

nh = HouseholdAdultFile()
youth = HouseholdYouthFile()
exam = ExamFile()

# Combine with exam file data
adult_exam = nh.data.set_index('SEQN').join(exam.data.set_index('SEQN'),rsuffix='_exam')
youth_exam = youth.data.set_index('SEQN').join(exam.data.set_index('SEQN'),rsuffix='_exam')

# Perform exclusions on adult exam file

adult_final = (adult_exam.query('(SPPMANEU > 1 & SPPMANEU < 88) & (SPPREPRO == 4 | SPPREPRO == 1)')
 .query('MXPAXTMR < 1080').query('DMARETHN < 4').query('not HAR1 ==1')
 .query('not HAR23 == 1').query('not HAR26 == 1' )
 .query('not (0 < HXPG1 < 888 | 0 < HXPG2A < 88 | 0 < HXPG2B < 88)')
 .query('not HAR26 == 1'). query('not HAC1E == 1')
 .query('not HAC1F == 1')
 .query('not HAC1G == 1')
 .query('not HAL6 == 1')
 .query('not HAL10 == 1')
 .query('not HAL1 == 1')
 .query('not HAL3 == 1')
 .query('not HAL5 == 1')
 .query('not SPPFEV3 == 88888')
 .query('not MXPAXTMR == 9999'))

# Set null values on adult 

adult_final = adult_final.replace({'HSAITMOR' : 9999}, {'HSAITMOR' : np.nan})

# Perform exclusions on youth exam file

youth_final = (youth_exam.query('MXPAXTMR > 95')
.query('(SPPMANEU > 1 & SPPMANEU < 88) & (SPPREPRO == 4 | SPPREPRO == 1)')
.query('DMARETHN < 4')
.query('not MYPB3 == 1')
.query('not MYPB11 >0').query('not MYPB27A >0')
.query('not HYE1G == 1')
.query('not HYE1H == 1')
.query('not HYG8 == 1')
.query('not HYG12 == 1')
.query('not HYG2 == 1')
.query('not HYG4 == 1') 
.query('not HYG7 == 555')
.query('BMPHT > 114')
.query('not SPPFEV3 == 88888')
.query('not MXPAXTMR == 9999'))

create_features(adult_final)
create_features(youth_final)

adult_final.to_pickle('data/adult_final.pkl.gz')
youth_final.to_pickle('data/youth_final.pkl.gz')