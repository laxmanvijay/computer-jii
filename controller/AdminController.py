def AddTrainableModelController(request,db,session):
    model_type = request.form['model_type']
    model_desc = request.form['model_desc']
    input_format = request.form['input_format']
    output_format = request.form['output_format']
    route_url  =request.form['route_url']
    return db.addTrainableModel(model_type,model_desc,input_format,output_format,route_url)

def AddNonTrainableModelController(request,db,session):
    model_type = request.form['model_type']
    model_desc = request.form['model_desc']
    input_format = request.form['input_format']
    output_format = request.form['output_format']
    route_url  =request.form['route_url']
    return db.addNonTrainableModel(model_type,model_desc,input_format,output_format,route_url)