"""
authors: @climatebrad, @dougjohnsonmd
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# DMARETHN – 1 non-Hispanic white, 2 non-hispanic black, 3 Mexican American, 4 other

ATTRIBUTES = {
    'ethnicity' : {'var' : 'DMARETHN', 'values' : {'black' : 2, 'white' : 1,'mexican': 3}},
    'sex' : {'var' : 'HSSEX', 'values' : {'male' : 1, 'female' : 2}},
    'age' : {'var' : 'MXPAXTMR', 'factor': 12 }
}

AGE_CUT_OFF = {'male' : 20, 'female' : 18 }

def query_from_attributes(ethnicity, sex, max_age=None, min_age=None):
    """Generate query language for dataframes based on demographic attributes"""
    vars = []
    values = { 'ethnicity': ethnicity, 'sex' : sex }
    for key, value in values.items():
        if type(value) is list:
            subvars = []
            for i in value:
                subvars.append(f"{ATTRIBUTES[key]['var']} == {ATTRIBUTES[key]['values'][i]}")
            vars.append("(" + " | ".join(subvars) + ")")
        else:
            vars.append(f"{ATTRIBUTES[key]['var']} == {ATTRIBUTES[key]['values'][value]}")
            
    if max_age is not None:
        vars.append(f"{ATTRIBUTES['age']['var']} < {max_age * ATTRIBUTES['age']['factor']}")
        
    if min_age is not None:
        vars.append(f"{ATTRIBUTES['age']['var']} >= {min_age * ATTRIBUTES['age']['factor']}")
        
    return " & ".join(vars)

def generate_demo_group_internal(adult_final, youth_final, ethnicity, sex, max_age=None, min_age=None):
    """Return dataframe based on demographic variables"""
    if min_age is not None and min_age > 17:  # too old for youth_final
        return adult_final.query(query_from_attributes(ethnicity, sex, max_age, min_age))
    else:
        return pd.concat([
            adult_final.query(query_from_attributes(ethnicity, sex, max_age, min_age)),
            youth_final.query(query_from_attributes(ethnicity, sex))
        ])

    
def generate_demo_group(adult, youth, ethnicity, sex, age_range='all'):
    """Wrapper for generate_demo_group_internal to accept simpler inputs. 
    age_range can be 'all', 'under', 'over' """
    min_age = None
    max_age = None
    if age_range == 'under':
        max_age = AGE_CUT_OFF[sex]
    elif age_range == 'over':
        min_age = AGE_CUT_OFF[sex]
    ethnicity_value = ethnicity
    if ethnicity == 'non-black':
        ethnicity_value = ['white', 'mexican']
    return generate_demo_group_internal(adult, youth, ethnicity_value, sex, max_age, min_age)

def do_age_regression(data, y_var, verbose=None):
    """Return the results of a linear regression against age for the given variable"""
    X = data['MXPAXTMR'] / 12  # convert to years from age in months at exam (MXPAXTMR)
    X = np.array(X).reshape(-1, 1)
    y = data[y_var]
    lr = LinearRegression().fit(X, y)
        # do linear regression fit on X, y
    if verbose is not None:
        print("R^2 = ",lr.score(X, y))
        print("Intercept: ",  lr.intercept_)
        print("Coefficients: ", lr.coef_)
    return lr.intercept_, lr.coef_, lr.score(X, y)

def do_height_age_regression(data, y_var, verbose=None):
    """Return the results of a linear regression against height, age, and age^2"""
# convert agemonths to years
    X_age = data['MXPAXTMR']/12 # convert to years from age in months at exam (MXPAXTMR)
    X_age = np.array(X_age).reshape(-1, 1)
    X_age = np.hstack((X_age, X_age**2)) 
    X_height = data['BMPHT']**2   # height in centimeters
    X_height = np.array(X_height).reshape(-1, 1)
    X = np.concatenate((X_age, X_height), axis=1)
    y = data[y_var]
    lr = LinearRegression().fit(X, y)
    if verbose is not None:
        print("R^2 = ",lr.score(X, y))
        print("Intercept: ",  lr.intercept_)
        print("Coefficients: ", lr.coef_)
    return lr.intercept_, lr.coef_, lr.score(X, y)

def do_regression(regression_type, data, y_var, verbose=None):
    """regression_type can be 'age' or 'height_age'
      'age' returns the results of a linear regression against age for the given variable
      'height_age' returns the results of a linear regression against height, age, and age^2"""
    X_age = data['MXPAXTMR']/12 # convert to years from age in months at exam (MXPAXTMR)
    X_age = np.array(X_age).reshape(-1, 1)
    if regression_type == 'height_age':
        X_age = np.hstack((X_age, X_age**2)) 
        X_height = data['BMPHT']**2   # height in centimeters
        X_height = np.array(X_height).reshape(-1, 1)
        X = np.concatenate((X_age, X_height), axis=1)
    else:
        X = X_age
    y = data[y_var]
    lr = LinearRegression().fit(X, y)
    if verbose is not None:
        print("R^2 = ",lr.score(X, y))
        print("Intercept: ",  lr.intercept_)
        print("Coefficients: ", lr.coef_)
    return lr.intercept_, lr.coef_, lr.score(X, y)

def get_regression_results(adult_final, youth_final, regression_type, variables):
    """Generate array of regression results for various demographic combinations.
       regression_type can be 'age' or 'height_age'"""
    
    regression_results = []

    for sex in ('male', 'female'):
        for ethnicity in ('black', 'non-black', 'white', 'mexican'):
            for age_range in ('all', 'under', 'over'):
                 # generate demographic group dataframe
                demo_group = generate_demo_group(adult_final, youth_final, ethnicity, sex, age_range)

                # do linear regression for variables
                for var in variables:
                    intercept, slope, r_squared = do_regression(regression_type, demo_group, var) 
                    slope = slope[0]
                    std = demo_group.loc[:, var].std()
                    count = demo_group.loc[:, var].count()
                    regression_results.append({
                        'sex' : sex,
                        'ethnicity' : ethnicity,
                        'age_range' : age_range,
                        'var' : var,
                        'intercept' : intercept,
                        'slope' : slope,
                        'r_squared' : r_squared,
                        'std' : std,
                        'count' : count
                    })  
    return regression_results