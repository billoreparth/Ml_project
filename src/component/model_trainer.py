import os 
import sys 
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.metrics import r2_score
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging 
from src.utils import save_object,evaluate_models

@dataclass
class Modeltrainerconfig:
    Model_trainer_file_path=os.path.join('artifact','model.pkl')

class Modeltrainingintialize:
    def __init__(self):
        self.model_path=Modeltrainerconfig()

    def model_training_intilize(self,train_set,test_set):

        try:
            logging.info('training split has initialize')
            x_train,y_train,x_test,y_test=(
                train_set[:,:-1],train_set[:,-1],
                test_set[:,:-1],test_set[:,-1]
            )

            models={'linearmodel':LinearRegression(),
                    'adaboost':AdaBoostRegressor(),
                    'gradientboost':GradientBoostingRegressor(),
                    'randomforrestsearch':RandomForestRegressor(),
                    'knearestneighbout':KNeighborsRegressor(),
                    'decisiontreeregressor':DecisionTreeRegressor(),
                    'xgboostregressor':XGBRegressor(),
                    'catboostregressor':CatBoostRegressor()
                    }
            
            # params={
                
                
                
            # }

            report:dict=evaluate_models(x_tr=x_train,y_tr=y_train,x_te=x_test,y_te=y_test,models=models)

            # getting best score and model name 

            best_model_score = max(sorted(report.values()))

            best_model_name = list(report.keys())[list(report.values()).index(best_model_score)]
            
            best_model = models[best_model_name]

            if best_model_score < 0.6 :
                raise CustomException('no best model found for this data',sys)

            save_object(
                file_path=self.model_path.Model_trainer_file_path,obj=best_model
            )

            predicted=best_model.predict(x_test)
            r2_=r2_score(y_test,predicted)

            return r2_
        
        except Exception as e :
            raise CustomException(e,sys)
    