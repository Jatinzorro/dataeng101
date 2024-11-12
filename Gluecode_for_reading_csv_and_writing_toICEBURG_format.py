#NOTE:::::::::::::PLEASE take care of cost, because this service costs a lottttttttt
import sys
import boto3
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import SparkSession
# # Initialize SparkSession
# spark = SparkSession.builder \
#     .appName("IcebergTableCreation") \
#     .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkCatalog") \
#     .config("spark.sql.catalog.spark_catalog.type", "hadoop") \
#     .config("spark.sql.catalog.spark_catalog.warehouse", "s3://iceburg-oneture-data/") \
#     .getOrCreate()
# # Create an Iceberg table using Spark SQL
# spark.sql("""
# CREATE TABLE spark_catalog.default.ORDERS (
#     ORD_NUM VARCHAR(6), ORD_AMOUNT VARCHAR(12) NOT NULL, ADVANCE_AMOUNT VARCHAR(12) NOT NULL, 
# 	ORD_DATE DATE NOT NULL, 
# 	CUST_CODE VARCHAR(6), 
# 	ORD_DESCRIPTION VARCHAR(60)
# ) USING iceberg
# """)
# Initialize Glue context
#sc = SparkContext()
#glueContext = GlueContext(sc)
#spark = glueContext.spark_session


glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session
# Parameters
#args = getResolvedOptions(sys.argv, ['JOB_NAME', 'jatin-oneture', 'iceburg-oneture-data'])
#source_bucket = args['jatin-oneture']
#dest_bucket = args['iceburg-oneture-data']

# Define source and destination paths
source_path = f"s3://jatin-oneture/output-data.csv"
dest_path = f"s3://iceburg-oneture-data/"



# Read CSV data from S3
df = spark.read.format("csv").option("header", "true").load(source_path)


df.show()
# Convert DataFrame to Glue DynamicFrame
dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")


# Write data in Iceberg format
# dynamic_frame.toDF().write.format("iceberg").mode("overwrite").save(dest_path)
# dynamic_frame.toDF().writeTo("glue_catalog.oneture.orders") \
#     .tableProperty("format-version", "2") \
#     .createOrReplace()

# dynamic_frame.toDF().write.format("iceberg").mode("overwrite").save("glue_catalog.oneture.orders")


glueContext.write_data_frame.from_catalog(
    frame=dynamic_frame.toDF(),
    database="oneture",
    table_name="orders"
)

print("Job completed successfully.")
dynamic_frame.show()
job.commit()