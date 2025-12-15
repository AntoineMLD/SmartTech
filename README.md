
# SmartTech – Pipeline de Streaming PySpark

## Description
Ce projet met en place un pipeline de streaming de données IoT avec PySpark et Delta Lake. Il permet de traiter en temps réel des fichiers JSON de capteurs déposés dans un dossier, de les nettoyer et de les stocker dans un format optimisé (Delta Lake) pour des analyses ultérieures.

## Fonctionnement du script
Le script `pipeline_streaming_simple.py` :
- Lit en continu les fichiers JSON déposés dans le dossier `sensor_data`.
- Applique un schéma strict aux données (timestamp, device_id, building, floor, type, value, unit).
- Corrige le format du timestamp et ajoute une colonne d'horodatage d'ingestion.
- Écrit les données dans un dossier Delta Lake (`sensor_data_bronze`), partitionnées par bâtiment et type de capteur.
- Affiche un aperçu des données ingérées.
- Fonctionne en mode streaming : tout nouveau fichier JSON ajouté à `sensor_data` est automatiquement traité.

## Prérequis
- Python 3.8+
- Java 11 ou 17 (OpenJDK recommandé)
- PySpark
- Delta Lake

### Installation des dépendances
Active ton environnement virtuel puis installe les paquets nécessaires :
```zsh
pip install pyspark delta-spark
```

### Configuration Java
Assure-toi que la variable d'environnement `JAVA_HOME` est bien définie :
```zsh
export JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64/"
export PATH="$JAVA_HOME/bin:$PATH"
```
Ajoute ces lignes à la fin de ton `~/.zshrc` si besoin.

## Utilisation
1. Place tes fichiers JSON de capteurs dans le dossier `sensor_data` (à créer si besoin).
2. Lance le pipeline :
```zsh
python3 pipeline_streaming_simple.py
```
3. Les données traitées seront stockées dans le dossier `sensor_data_bronze` au format Delta Lake.

## Exemple de fichier JSON attendu
```json
{
	"timestamp": "2025-12-15T10:00:00Z",
	"device_id": "sensor_001",
	"building": "A",
	"floor": 2,
	"type": "temperature",
	"value": 22.5,
	"unit": "C"
}
```

## Notes
- Le script fonctionne en local, mais peut être adapté pour un cluster Spark.
- Le format Delta Lake permet des requêtes efficaces et une gestion des versions des données.

## Auteur
AntoineMLD
