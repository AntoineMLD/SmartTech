from pyspark.sql import SparkSession

# Initialisation de Spark AVEC LES CONFIGURATIONS DELTA OBLIGATOIRES
spark = SparkSession.builder \
    .appName("ReadDeltaTable") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Chemin ABSOLU vers ta table Delta
delta_table_path = "/home/scott/Documents/Projets/smart_tech/SmartTech/sensor_data_silver"

# Lecture de la table Delta
try:
    df = spark.read.format("delta").load(delta_table_path)
    print("\nContenu de la table Delta (Silver) :")
    df.show(truncate=False)

    print("\nSchéma de la table :")
    df.printSchema()

    print(f"\nombre de lignes : {df.count()}")
except Exception as e:
    print(f"Erreur lors de la lecture de la table Delta : {e}")

spark.stop()
