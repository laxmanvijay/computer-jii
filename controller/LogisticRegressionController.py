def LogisticRegressionController(request=None):
    if request==None:
        return 'linear'
    value = request.form['value']
    return value