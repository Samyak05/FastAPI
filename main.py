from fastapi import FastAPI, Path, Query, HTTPException
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as file:
        data = json.load(file)
    return data

@app.get('/')
def hello():
    return {'message' : 'Patient Management API'}

@app.get('/view')
def view():
    return load_data()

@app.get('/patient/{patient_id}')
def view_id(patient_id : str = Path(...,description='ID of the patient', example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail='Not found')

@app.get('/sort')
def sort_patients(sort_by : str = Query(..., description='sort on the basis of height/weight/bmi'), order_by:str = Query('asc', description='sort in asc or desc')):

    valid_fields = ['height', 'weight', 'bmi']
    valid_orders = ['asc', 'desc']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Bad Request, select from {valid_fields}')
    
    if order_by not in valid_orders:
        raise HTTPException(status_code=400, detail=f'Invalid order, select from {valid_orders}')

    data = load_data()
    sort_order = True if order_by=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    
    return sorted_data