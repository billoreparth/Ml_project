import os 
import sys
import pandas as pd 
from src.exception import CustomException
from src.logger import logging 
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.component.data_transformation import Data_transformation
from src.component.model_trainer import Modeltrainerconfig
from src.component.model_trainer import Modeltrainingintialize

@dataclass # this will allow us to difine path variable without using __init__ constuctor 
class Dataconfig:
    train_path:str=os.path.join('artifact','train.csv')
    test_path:str=os.path.join('artifact','test.csv')
    raw_path:str=os.path.join('artifact','raw-data.csv')

# not using decorator and making a class to define function because it is recommended 
class Dataingestion:
    def __init__(self):
        self.ingestion_config = Dataconfig()

    def data_ingestion_initilize(self):
        logging.info('the data ingestion method or component has been called ')
        try:
            df=pd.read_csv("D:/Work/NLP & ML/ML_Project_1/notebook/Data/stud.csv")
            logging.info('the data frame has been read')

            os.makedirs(os.path.dirname(self.ingestion_config.train_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_path,index=False,header=True)

            logging.info('train test split has been initilize')
            train_set,test_set=train_test_split(df,test_size=0.3,random_state=42)

            train_set.to_csv(self.ingestion_config.train_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_path,index=False,header=True)

            logging.info('ingestion of data has been completed')

            return(
                self.ingestion_config.train_path,
                self.ingestion_config.test_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=='__main__':
    obj=Dataingestion()
    train_data,test_data=obj.data_ingestion_initilize()

    transform_obj=Data_transformation()
    train,test,_=Data_transformation().data_transformation_intialize(train_path=train_data,test_path=test_data)

    model_t=Modeltrainingintialize()
    print(model_t.model_training_intilize(train,test))


