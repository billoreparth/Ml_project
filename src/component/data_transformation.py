import os 
import sys 
from dataclasses import dataclass 
import numpy as np 
import pandas as pd 
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.exception import CustomException
from src.logger import logging 
from src.utils import save_object

@dataclass
class Data_transformation_config:
    pre_processor_obj_file_path=os.path.join('artifact','preprocessor.pkl')

class Data_transformation:
    def __init__(self):
        self.data_transformation_config = Data_transformation_config()

    def get_data_transform(self):
        try:
            num_feature= ['reading_score', 'writing_score']
            cat_feature=['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            num_pipeline=Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='median')),('standardscaler',StandardScaler())
            ])

            cat_pipeline = Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),('onehotencoder',OneHotEncoder()),('standardscaler',StandardScaler(with_mean=False))
            ])

            logging.info("standard scaling completed")
            logging.info('encoding categorical columns completed')

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline,num_feature),('cat_pipeline',cat_pipeline,cat_feature) 
                ]
            )

            return preprocessor

        except Exception as e :
            raise CustomException(e,sys)
        
    def data_transformation_intialize(self,train_path,test_path):

        try:    
            train_set = pd.read_csv(train_path)
            test_set = pd.read_csv(test_path)

            logging.info("reading train and test data completed ")
            logging.info("preprocessing started")

            preprossing_obj = self.get_data_transform()

            target_col='math_score'
            num_col=['writing_score','reading_score']

            input_feature_train=train_set.drop(columns=[target_col],axis=1)
            target_feature_train=train_set[target_col]
            
            input_feature_test=test_set.drop(columns=[target_col],axis=1)
            target_feature_test=test_set[target_col]

            logging.info("applying column transformer on both train and test data")

            input_feature_train_arr=preprossing_obj.fit_transform(input_feature_train)
            input_feature_test_arr=preprossing_obj.transform(input_feature_test)

            train_arr=np.c_[
                input_feature_train_arr,np.array(target_feature_train)
            ]

            test_arr=np.c_[
                input_feature_test_arr,np.array(target_feature_test)
            ]

            logging.info("saving preprocessing info")
            
            save_object(
                file_path=self.data_transformation_config.pre_processor_obj_file_path,
                obj=preprossing_obj
            )

            return(
                train_arr,test_arr,self.data_transformation_config.pre_processor_obj_file_path
            )

        except Exception as e :
            raise CustomException(e,sys)

