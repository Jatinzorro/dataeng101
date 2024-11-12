import json
import boto3
import pandas as pd
import pymysql
from io import StringIO
# remember to make a layer of required library that you will upload to s3 and use in AWS lambda. because AWS lambda doesnt provide all libraries
# Configuration  -- Its better if you provide these configuration in LAMBDA environment variable and if its something like password, u should use AWS Secret manager
RDS_HOST = 'YOUR_HOST'
RDS_PORT = 3306  # Change if necessary
RDS_USER = 'admin'
RDS_PASSWORD = 'YPUR_PASSWORD'
RDS_DB_NAME = 'YOURDB NAME'
S3_BUCKET = 'YOURBUCKET NAME'
S3_KEY = 'output-data.csv'

def lambda_handler(event, context):
    # Connect to RDS
    connection = pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DB_NAME,
        port=RDS_PORT
    )
    
    # Query data from RDS
    query = "SELECT * FROM ORDERS;"
    df = pd.read_sql(query, connection)
    connection.close()
    
    # Convert DataFrame to CSV
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    
    # Write CSV to S3
    s3_client = boto3.client('s3')
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=S3_KEY,
        Body=csv_buffer.getvalue(),
        ContentType='text/csv'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data successfully written to S3')
    }
