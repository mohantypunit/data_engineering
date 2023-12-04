import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_unixtime, to_timestamp, year, month, dayofmonth, hour, dayofweek, lag, when, col
from pyspark.sql.window import Window
from pyspark.sql.utils import AnalysisException

# Initialize a SparkSession
print("Initializing SparkSession...")
spark = SparkSession.builder \
    .appName("Time-Series Data Processing") \
    .getOrCreate()

# Path to the JSON file
json_file_path = './data.json'  # Replace with your JSON file path

# Read JSON data into a DataFrame
print("Reading JSON data...")
df = spark.read.option("multiline", "true").json(json_file_path)

# Print the DataFrame schema
print("DataFrame Schema:")
df.printSchema()

# Convert timestamp from UNIX format to a readable timestamp format
print("Converting timestamp...")
df = df.withColumn("timestamp", to_timestamp(from_unixtime("timestamp")))

# Data Cleaning: Handling Missing Values and Removing Duplicates
print("Cleaning data...")
df = df.na.fill({'consumption_kwh': 0})  # Replace nulls in 'consumption_kwh' with 0
df = df.dropDuplicates()

# Replace negative values in 'consumption_kwh' with None
print("Handling negative values...")
df = df.withColumn('consumption_kwh', when(df['consumption_kwh'] >= 0, df['consumption_kwh']))

# Calculate the first and third quartiles
print("Calculating quartiles for outlier detection...")
Q1, Q3 = df.approxQuantile("consumption_kwh", [0.25, 0.75], 0.05)

# Calculate the interquartile range (IQR)
IQR = Q3 - Q1

# Define lower and upper bounds for outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filtering out the outliers
print("Filtering outliers...")
df = df.filter(
    (col('consumption_kwh') >= lower_bound) & 
    (col('consumption_kwh') <= upper_bound)
)

# Feature Engineering: Time-Based Features
print("Performing feature engineering...")
df = df.withColumn('year', year('timestamp'))
df = df.withColumn('month', month('timestamp'))
df = df.withColumn('day', dayofmonth('timestamp'))
df = df.withColumn('hour', hour('timestamp'))
df = df.withColumn('weekday', dayofweek('timestamp'))

# # Aggregation: Time-Based Aggregation
# print("Aggregating data...")
# df_grouped = df.groupBy('sensor_id', 'year', 'month', 'day', 'hour').avg('consumption_kwh')

# df_grouped.printSchema()

# Data Windowing for Time-Series
print("Creating time-series window...")
windowSpec = Window.partitionBy('hour').orderBy('timestamp')
df = df.withColumn('prev_consumption', lag('consumption_kwh').over(windowSpec))

# Print the DataFrame schema
print("Transformed DataFrame Schema:")
df.printSchema()

output_folder = './processed_data'

# Writing data to output folder
try:
    print("Writing data to output folder...")
    df.write.mode("overwrite").partitionBy('year', 'month', 'day', 'hour').format('parquet').save(output_folder)
    print("Data successfully written to output folder.")
    
except AnalysisException as e:
    print("Error writing to the folder: ", e)
except Exception as e:
    print("An unexpected error occurred: ", e)

# Stop the SparkSession
print("Stopping SparkSession...")
spark.stop()
print("Script completed.")
