import os      ## To create a path, as a output of data ingestion we have our train file and test file in some specific path called test path,trian path and that path we try to create inside artifacts folder(artifacts main purpose is to store some files preproccessor,pickle files wrt the model  )
import sys      ## It  is required to import logging and exception 
from src.logger import logging         ## Importing logging 
from src.exception import CustomException      ## Importing CustomException so that we can implement custom exception in this particular page wrt the data ingestion
import pandas as pd
from sklearn.model_selection import train_test_split    ## As at the end our output is trian and test dataset
from dataclasses import dataclass


## intialize the data ingestion configuration

## As our output of data ingestion is train and test dataset so initially we have to provide some parameters(train_data_path,test_data_path) to data ingestion 
@dataclass  # placeholder to create a class itself and it works alomost like how we specifically work with classes itself to create init method and all and here we dont have to specifically write init method and all 
class DataIngestionconfig:      # here when we define @dataclass we dont write any init and all
    train_data_path=os.path.join('artifacts','train.csv')
    test_data_path=os.path.join('artifacts','test.csv')
    raw_data_path=os.path.join('artifacts','raw.csv')         ## raw file is created as to reuse the dataset saving the train and test path in the specific path 
# here use of @dataclass is we can directly been create the class variables and we can create init function we want if we dont want above @dataclass method 


# In @dataclass we just considered that we need to create some class variables and not considered any functionalities 
## create a data ingestion class 
class DataIngestion:     # here we give data ingestion config 
    def __init__(self):   #constructor  ## As soon as we create the object of this data ingestion class we need to have all the above files path ready in our object of data ingestion so we create a variable called ingestion_config 
        self.ingestion_config=DataIngestionconfig()   ## Now we can have train,test,raw data path ready 

    def initiate_data_ingestion(self):      ## whatever data ingestion we are planning to do first read dataset, do the train test split and return or create files in the specific path will basically happen inside this particular folder  
        logging.info('Data Ingestion method starts')   ## creatin log which says that Data Ingestion method starts

        try:     ## here we first read dataset and then we do train test split and then we save the particular data in the above specific path wrt train,raw,test files 
            df=pd.read_csv(os.path.join('notebooks/data','gemstone.csv'))  ## specifing the path of file we are reading 
            logging.info('Dataset read as pandas Dataframe')
             
             # whatever folder or directory name we have given above i.e., artifacts, we need to create it as default it is there but when we aer running for the first time that folder will not be there so we can create our ffolder with os.mk=akedirrectory
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)   #here we are giving the default folder location so we create that specific file and we give exist_ok=True as if the folder already exists we are not going to delete that folder 
             ##whatever dataframe we have we are going to save it inside the raw_data_path so we say as below
            df.to_csv(self.ingestion_config.raw_data_path,index=False)   ## index=Flase is added so that it will not take index numbers in out dataset 
            
            logging.info('Raw data is created')

            ## Initaiting train test split 
            
            train_set,test_set=train_test_split(df,test_size=0.30,random_state=42)    ## here when we using this train test split we dont have our independent and dependent feature we are directly giving so that it divide into train and test and later on we can try to split our independent and dependent features 
            #reason we have did above one is to create our training data as one file and our test data as one file 
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)   # saving train data in a particular location and headder is to have all the info of all the columns 
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('Ingestion of data is completed')

            return( ## return two paths after creating files 
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )



        except Exception as e:
            logging.info('Error occured in Data Ingestion config')




## REvise
# Initially we create our variables inside a separate class where we need  to save train,test,raw data
# And next we created another class adding all functionalities 


## Now in order to test this above one we can test it in the same folder location and all 
# we can open our pipelines/training_pipelines as data_ingestion is part of training pipeline and we cna enter our info 

# for runnig the data_ingestion run the command    python src/pipelines/training_pipeline.py
# now we even get some logs folder 