import boto3
import pandas as pd
import logging
from botocore.exceptions import ClientError
import io

bucket_name = "webpresence-geocore-geojson-to-parquet-dev"
file_name = "records.parquet"

pd.set_option('max_columns', None)

def open_S3_file_as_df(bucket_name, file_name):
    """Open a S3 parquet file from bucket and filename and return the parquet as pandas dataframe
    :param bucket_name: Bucket name
    :param file_name: Specific file name to open
    :return: body of the file as a string
    """
    try: 
        s3 = boto3.resource('s3')
        object = s3.Object(bucket_name, file_name)
        body = object.get()['Body'].read()
        df = pd.read_parquet(io.BytesIO(body))
        print(f'Loading {file_name} from {bucket_name} to pandas dataframe')
        # print(df['error'].to_string(index=False))
        # print all of the column names
        print(df.columns.tolist())
        last_column = df.iloc[:, -1]
        print(last_column) 
        return df
    
    except ClientError as e:
        logging.error(e)
        return e
    
open_S3_file_as_df(bucket_name, file_name)

'''
# Add a new column to log the process, and loop through the pandas rows to assign values  
df['process_log'] = 'error'

## Loop through the DataFrame and update the new column based on processing condition 'Fail' or 'Success'
for index, row in df.iterrows():
    if Transformed == True:
        df.at[index, 'process_log'] = 'Success' # or 1 
    else:
        df.at[index, 'process_log'] = 'Fail' # or 0
'''