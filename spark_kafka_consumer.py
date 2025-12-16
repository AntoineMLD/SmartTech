from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, TimestampType
from pyspark.sql.functions import col, from_json, current_timestamp

def consume_from_kafka():
    spark = SparkSession.builder \
        .appName("KafkaToDelta") \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", "2") \
        .config("spark.sql.streaming.checkpointLocation", "/tmp/kafka_checkpoint") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,io.delta:delta-core_2.12:2.4.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("INFO")

    # Schéma des données Kafka 
    kafka_schema = StructType([
        StructField("timestamp", LongType(), True),
        StructField("device_id", StringType(), True),
        StructField("building", StringType(), True),
        StructField("floor", LongType(), True),
        StructField("type", StringType(), True),
        StructField("value", DoubleType(), True),
        StructField("unit", StringType(), True)
    ])

    # Lecture depuis Kafka
    df_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "sensor_data") \
        .option("startingOffsets", "earliest") \
        .load()

    # Parsing et nettoyage
    df_parsed = df_stream.select(
        from_json(col("value").cast("string"), kafka_schema).alias("data")
    ).select("data.*") \
     .withColumn("ingestion_time", current_timestamp()) \
     .withColumn("timestamp", (col("timestamp") / 1000).cast("timestamp"))

    # Écriture dans Delta (niveau Silver)
    query = df_parsed.writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", "/tmp/silver_checkpoint") \
        .partitionBy("building", "type") \
        .start("/home/scott/Documents/Projets/smart_tech/SmartTech/sensor_data_silver")

    query.awaitTermination()

if __name__ == "__main__":
    consume_from_kafka()
