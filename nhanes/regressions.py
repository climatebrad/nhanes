def do_height_regression(data, gender=None, ethnicity, y_var):
    if gender == 'male':
        data = data.query('HSSEX == 1')
    elif gender == 'female':
        data = data.query('HSSEX == 2')
    lr = LinearRegression()
    
def do_age_regression(data, y_var):
    X = data['HSAITMOR'] / 12
    X = np.array(X).reshape(-1, 1)
    y = data[y_var]
    lr = LinearRegression().fit(X, y)
        # do linear regression fit on X, y
    print("R^2 = ",lr.score(X, y))
    print("Intercept: ",  lr.intercept_)
    print("Coefficients: ", lr.coef_)
    return lr