from sklearn.impute import SimpleImputer ## HAndling Missing Values
from sklearn.preprocessing import StandardScaler # HAndling Feature Scaling
from sklearn.preprocessing import OrdinalEncoder # Ordinal Encoding
## pipelines
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

import sys,os
from dataclasses import dataclass
import pandas as pd
import numpy as np

from src.exception import CustomException    ## using exception handling 
from src.logger import logging

from src.utils import save_object


## Data Transformation config

## wkt after data transformation we are probably going to get a Feature Engineering preprocessing pickle file bcz for FE also we create a pipeline and that entire FE is also need to be automated and it can be automated when we follow pipeline process for that we cerate @dataclass 
@dataclass
class DataTransformationconfig:      ## This is to give the path of the pickle file where its need to get saved and again we give that artifacts folder path only and the pickle should save in what file name that path we need to give over here 
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

    
    # Any input or output info that needs to be given ususally we create a configuration class

## Data Ingestionconfig class

class DataTransformation:
    def __init__(self):          ## here we initialise the data transformation config as we require the preprocessror picle file name  
        self.data_transformation_config=DataTransformationconfig()  ## now we will have preprocessor_obj_file_path value in data_transformation_config

    def get_data_transformation_object(self):       ##  we call this when we have our entire data and get our preprocessor file back i.e, we are getting FE preprocessor model over here 
         
          # now here we write about our entire data transformation i.e, we are going to take our ordinal categorical varaible separately, our numerical variable separetely and then we are going to apply pipeline for making sure to handle the missing values and to handle the categorical varaibles, after this we combine the particular pipeline and we probably create that in the form pickle file  
         # refer notebooks/Model_Training file as we are going to copy the same code over here  

         try:
            logging.info('Data Transformation initiated')
            # Define which columns should be ordinal-encoded and which should be scaleD
            ## Categorical and numerical columns 
            categorical_cols = ['cut', 'color','clarity']
            numerical_cols = ['carat', 'depth','table', 'x', 'y', 'z']
            
            # Define the custom ranking for each ordinal variable(this is where we are going to use pipeline )
            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']
            
            logging.info('Data Transformation Pipeline Initiated')

            ## Numerical Pipeline
            num_pipeline=Pipeline(           ## pipeline for handling any missing value if we have
                steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())               ## performing standard scalar so that we scale our dataset
 
                ]

            )

            # Categorigal Pipeline
            cat_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),              ## handling missing values with most frequent values 
                ('ordinalencoder',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                ('scaler',StandardScaler())             ## applying StandardScaler
                ]

            )

            preprocessor=ColumnTransformer([               ## Combining Numerical pipeline and categorical pipeline usinf ColumnTransformer 
            ('num_pipeline',num_pipeline,numerical_cols),
            ('cat_pipeline',cat_pipeline,categorical_cols)
            ])
            # in this preprocessor we will be getting our pickle file 

            return preprocessor      ## returning the preprocessor 

            logging.info('Pipeline Completed')

         except Exception as e:
            
            logging.info("Error in Data Trnasformation")
            raise CustomException(e,sys)
    
    ## here we initialy started categorising the categorical and numerical cols separately 
    # ANd then we give our ordinal ranking based on domain expert website we have 
    # And then we created numerical pipeline and then we created our categorical pipeline where initialy we handle the missing values by using median .....
    ## Combining numerical and categorical pipelines 
    ## And at the end we are going to get the entire FE preprocessor 


# As the train_path,test_path are been returned from data ingestion and further we calling data transformation 
    def initiate_data_transformation(self,train_data_path,test_data_path):   ## Taking our train and test data and perform all our FE and give preprocessor pickle file   
         
         
        try:
            # Reading train and test data 
            train_df = pd.read_csv(train_data_path)
            test_df = pd.read_csv(test_data_path)

            logging.info('Read train and test data completed')
            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head  : \n{test_df.head().to_string()}')

            logging.info('Obtaining preprocessing object')
             
            # getting our FE preprocessor file by calling get_data_transformation_object() func we will get our preprocessor file through which we will be doing fit_transform(done for traini data) and transform(done for test data)
            preprocessing_obj = self.get_data_transformation_object()    ## our preprocessor get saved in this particular variable

            target_column_name = 'price'
            drop_columns = [target_column_name,'id']

            ## features into independent and dependent features
            # For Train Data 
            input_feature_train_df = train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]

            # For Test Data 
            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name]

            ## apply the data transformation

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            logging.info("Applying preprocessing object on training and testing datasets.")
            
            ## After transformation we combine with our target_feature_train_df,target_feature_test_df on this particular arrays 
            # For combining an array with dataframe and to convert that entirely into an array we use np.c_ and c_ is an concatenation operation 
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            

            ## For Saving the preprocessor object in the form of pickle file(as when it is in production we can use the specific pickle file  i.e, where we use our utils.py )and we create a function and this func will not be created over here 
            # In utils.py we create all our generic functionality 
            # file path is initialy created as data_transformation_config and which is saved in data_transformation_config.preprocessor_obj_file_path and 
            # and we need to create the object pickle file i.e, our FE object 
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            logging.info('Processsor pickle in created and saved')

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        
        except Exception as e:
            logging.info("Exception occured in the initiate_datatransformation")

            raise CustomException(e,sys)


    

## To run this we first to go our src/pipelines/training_pipeline
# we intialise the data transformation and firstly we have to import our data transformation 
# and when we call data_transformation.initiate_data_transformation we provide train_data_path and test_data_path and which is returning train_arr,test_arr,obj_path

# for runnig the data_ingestion run the command    python src/pipelines/training_pipeline.py
# now we even get some logs folder 