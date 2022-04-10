# -*- coding: utf-8 -*-
# uvicorn main:app --reload
# http://127.0.0.1:8000/docs#/
import json
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from fastapi import Depends, FastAPI, Response, HTTPException
from fastapi.security import HTTPBasic,HTTPBasicCredentials
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
app = FastAPI(title='API_MLOps_PROJECT',
              description='Projet API powered by Fast_API',
              version='1.0',
              openapi_tags=[
                    {
                        'name': 'API_Utilisateurs',
                        'description': '🦄'
                    },
					])

security=HTTPBasic()
users = {
    'alice': 'wonderland',
    'bob': 'builder',
	'clementine':'mandarine'
}
docs_tags=[
	{
        'name': 'ML',
        'description': 'machine learning modèles'
    },
    {
        'name': 'USER',
        'description': 'droits d\'acces'
    },
    {
        'name': 'SYSTEM & SECURITY',
        'description': 'Fonctions système pour l\'API'
    }
	]

data=pd.DataFrame(np.array([['SGD','SGD', 'SGD_model.pkl'],
       ['LOGITC','RegLogistic','LOGIT_model.pkl'], ['NBC','NBC','GAUSSIANNB_modelbis.pkl']]),# ['DTC','DTC','DTC_model_2.pkl']]),
	   	   columns=['title','name', 'model'])

def authenticate_user(username, password):
    authenticated_user = False
    if username in users.keys():
        if users[username] == password:
            authenticated_user = True
    return authenticated_user

def ETL_data():
	myChurn=pd.read_csv("churn.csv")
	myChurn['TotalCharges'] = pd.to_numeric(myChurn.TotalCharges, errors='coerce')
	myChurn.dropna(subset = ["TotalCharges"], inplace=True)
	myChurn = pd.get_dummies(myChurn,columns=['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'InternetService',
       'DeviceProtection', 'StreamingTV', 'Contract', 'PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
	   'TechSupport', 'StreamingMovies', 'PaymentMethod','PaperlessBilling'],drop_first=True)
	myData=myChurn.drop(columns=['customerID'])
	X = myData.drop(columns = ['Churn'])
	y = myData['Churn'].values
	return X,y

@app.get("/",tags=['System_Security'])
async def root():
    return {"message": "Welcome to churn FAST API"}

@app.get("/users/me",tags=['USER'])
def Listing_current_user(credentials: HTTPBasicCredentials= Depends(security)):
	authorization =authenticate_user(credentials.username,credentials.password)
	if authorization==False:
		HTTPException(status_code=403, detail="Forbidden")
	return {"username":credentials.username,"password":credentials.password,"authorization":authorization }

@app.get('/status',tags=['System_Security'])
async def return_status(credentials: HTTPBasicCredentials= Depends(security)):
    '''
    returns 1 if this FAST API application is working well
    '''
    return 1

@app.get('/model/list',tags=['ML'])
async def list_models(credentials: HTTPBasicCredentials= Depends(security)):
	"""
	Return the list of available models
	---
    In addition to current list, you can easily find more performant models by implementing hyperparameters fine tuning
	"""
	authorization = authenticate_user(credentials.username,credentials.password)
	if authorization==False:
		raise HTTPException(status_code=403, detail="Forbidden")		
		
	df=data.to_json(orient="split")
	df2=df[1:]
	df3= '{'+df2+'}'
	result=json.dumps(df3)
	return Response(content=df, media_type="application/json")

@app.get('/model/{nom_model}',tags=['ML'])
async def get_model_info(nom_model,credentials: HTTPBasicCredentials= Depends(security)):
	"""
	Return informations about models
	---
    Option to display generic informations about models 
	"""
	authorization = authenticate_user(credentials.username,credentials.password)
	if authorization == False:
		raise HTTPException(status_code=403, detail="Forbidden")
	for index, row in data.iterrows():
		if row['title']==nom_model:
			return {'model name':row['name'],'title':row['title'],'fichier de modele':row['model']}
	return None

@app.get('/model/{nom_model}/score',tags=['ML'])
async def get_model_score(nom_model,credentials: HTTPBasicCredentials= Depends(security)):
	"""
	Return models scoring
	---
    Please choose one or several models for performances assessment
	"""
	authorization = authenticate_user(credentials.username,credentials.password)
	if authorization == False:
		raise HTTPException(status_code=403, detail="Forbidden")
	result=""

	#X,y = [ETL_data() for index, row in data.iterrows() if row['title']==nom_model]
	for index, row in data.iterrows():
		if row['title']==nom_model:
			
			X,y=ETL_data()
			
			X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.4, random_state = 1 , stratify=y)
			filename = row['model']
			loaded_model = pickle.load(open(filename, 'rb'))
			result = loaded_model.score(X_test, y_test)
			
	return {'modele':nom_model,'score':result}

  

