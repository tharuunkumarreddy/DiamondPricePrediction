import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd

# Initiating the data ingestion i.e, we have to import the data ingestion that specific class we have 
from src.components.data_ingestion import DataIngestion



if __name__=='__main__':  ## for running the DataIngestion class 
    obj=DataIngestion()    #initiating data ingestion and it is giving out train and test data path 
    train_data_path,test_data_path=obj.initiate_data_ingestion()
    print(train_data_path,test_data_path)

    


## for runnig the data_ingestion run the command    python src/pipelines/training_pipeline.py
# now we even get some logs folder 