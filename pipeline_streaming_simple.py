from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
from pyspark.sql.functions import col, to_timestamp, current_timestamp
import time

def write_bronze():
    # Initialisation de Spark avec les configurations Delta
    spark = SparkSession.builder \
        .appName("BronzeLayer") \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", "2") \
        .config("spark.sql.streaming.checkpointLocation", "/tmp/bronze_checkpoint") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("INFO")

    # Chemins ABSOLUS
    sensor_data_path = "/home/scott/Documents/Projets/smart_tech/SmartTech/sensor_data"
    sensor_data_bronze_path = "/home/scott/Documents/Projets/smart_tech/SmartTech/sensor_data_bronze"

    # Schéma des données
    schema = StructType([
        StructField("timestamp", StringType(), True),
        StructField("device_id", StringType(), True),
        StructField("building", StringType(), True),
        StructField("floor", IntegerType(), True),
        StructField("type", StringType(), True),
        StructField("value", DoubleType(), True),
        StructField("unit", StringType(), True)
    ])

    # Lecture du flux JSON
    df_stream = spark.readStream \
        .schema(schema) \
        .option("maxFilesPerTrigger", 1) \
        .json(sensor_data_path)

    # Nettoyage minimal (correction du format de timestamp)
    df_bronze = df_stream \
        .withColumn("timestamp", to_timestamp(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss'Z'")) \
        .withColumn("ingestion_time", current_timestamp())

    # Écriture dans Delta
    query = df_bronze.writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", "/tmp/bronze_checkpoint") \
        .partitionBy("building", "type") \
        .start(sensor_data_bronze_path)

    print(f"Pipeline démarré ! Ajoute des fichiers JSON dans {sensor_data_path} pour les traiter.")

    # Attendre que des données soient écrites
    while query.isActive and query.recentProgress == []:
        time.sleep(1)  # Attendre 1 seconde entre chaque vérification

    # Lire les données écrites (après le premier batch)
    print("\nLecture des données écrites dans la table Delta (Bronze) :")
    df_bronze_read = spark.read.format("delta").load(sensor_data_bronze_path)
    df_bronze_read.show(5, truncate=False)

    query.awaitTermination()

if __name__ == "__main__":
    write_bronze()
