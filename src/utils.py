import os 
import sys
import pandas as pd 
import numpy as np 
import dill
import pickle
from src.exception import CustomException
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV


def save_object(file_path,obj):
    try:    
        dir_name=os.path.dirname(file_path)

        os.makedirs(dir_name,exist_ok=True)

        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)
    
    except Exception as e:
        raise CustomException(e,sys)

def evaluate_models(x_tr,y_tr,x_te,y_te,models):
        
    try:    
        report = {}
        for i in range(len(list(models))):

            model = list(models.values())[i]
            model.fit(x_tr,y_tr)

            y_tr_pred= model.predict(x_tr)
            y_te_pred= model.predict(x_te)
            
            train_model_score = r2_score(y_tr,y_tr_pred)
            test_model_score = r2_score(y_te,y_te_pred)

            report[list(models.keys())[i]] = test_model_score

            return report
    

    except Exception as e :
        raise CustomException(e,sys)   
    
def load_object(file_path:str):
    try:
        with open(file_path,'rb') as file:
            return pickle.load(file)
    
    except Exception as e :
        raise CustomException(e,sys)