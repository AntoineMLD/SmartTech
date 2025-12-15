from pyspark.sql import SparkSession

# Initialisation de Spark AVEC LES CONFIGURATIONS DELTA OBLIGATOIRES
spark = SparkSession.builder \
    .appName("ReadDeltaTable") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Chemin ABSOLU vers ta table Delta
delta_table_path = "/home/scott/Documents/Projets/smart_tech/SmartTech/sensor_data_bronze"

# Lecture de la table Delta
try:
    df = spark.read.format("delta").load(delta_table_path)
    print("\n✅ Contenu de la table Delta (Bronze) :")
    df.show(truncate=False)

    print("\n📋 Schéma de la table :")
    df.printSchema()

    print(f"\n📊 Nombre de lignes : {df.count()}")
except Exception as e:
    print(f"❌ Erreur lors de la lecture de la table Delta : {e}")

spark.stop()
