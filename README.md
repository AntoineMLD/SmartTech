SmartTech – Pipeline IoT Temps Réel avec Spark, Kafka et Delta Lake

Contexte du Projet
SmartTech simule un système IoT pour bâtiments intelligents, avec :

Capteurs (température, humidité, énergie, CO2).
Traitement temps réel pour détecter des anomalies et alimenter des tableaux de bord.
Historisation des données pour analyses ultérieures.
Ce dépôt implémente deux pipelines pour répondre à un brief académique en deux parties :


# SmartTech – Pipeline IoT Temps Réel avec Spark, Kafka et Delta Lake

Bibliothèques Python :


pip install pyspark delta-spark kafka-python
Ajoute ces lignes à ton ~/.bashrc ou ~/.zshrc :

export JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64/"
export PATH="$JAVA_HOME/bin:$PATH"


source ~/.bashrc  # ou source ~/.zshrc


Utilisation
# SmartTech – Pipeline IoT Temps Réel avec Spark, Kafka et Delta Lake


## 🚀 Contexte du Projet

SmartTech simule un système IoT pour bâtiments intelligents :

- **Capteurs** (température, humidité, énergie, CO2)
- **Traitement temps réel** pour détecter des anomalies et alimenter des tableaux de bord
- **Historisation** des données pour analyses ultérieures

Ce dépôt implémente deux pipelines pour répondre à un brief académique :
1. **Veille** sur le streaming structuré avec Spark (concepts clés, architecture Médaillon)
2. **Mise en pratique** avec des pipelines Spark + Kafka

---

## 📁 Structure du Dépôt

| Fichier/Script                | Rôle                                                        |
|------------------------------|-------------------------------------------------------------|
| `pipeline_streaming_simple.py`| Pipeline Spark local (fichiers JSON → Delta Bronze)         |
| `kafka_producer.py`           | Simulateur de capteurs (envoie des données dans Kafka)      |
| `spark_kafka_consumer.py`     | Pipeline Spark Streaming (Kafka → Delta Silver)             |
| `read_delta.py`               | Lecture des tables Delta (Bronze/Silver)                    |
| `docker-compose.yml`          | Déploiement local de Kafka/Zookeeper                        |
| `sensor_data/`                | Dossier pour les fichiers JSON (mode local)                 |
| `sensor_data_bronze/`         | Table Delta Bronze (données brutes)                         |
| `sensor_data_silver/`         | Table Delta Silver (données nettoyées)                      |

---

## 🛠️ Prérequis

- Python 3.8+
- Java 11/17 (OpenJDK recommandé)
- Docker (pour Kafka/Zookeeper)
- Bibliothèques Python :

```bash
pip install pyspark delta-spark kafka-python
```

### Configuration Java

Ajoutez à votre `~/.bashrc` ou `~/.zshrc` :

```bash
export JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64/"
export PATH="$JAVA_HOME/bin:$PATH"
```

Puis rechargez votre shell :

```bash
source ~/.bashrc  # ou source ~/.zshrc
```

---

## ▶️ Utilisation

### Pipeline Local (Fichiers JSON → Delta Bronze)

1. Placez des fichiers JSON dans `sensor_data/` (exemple ci-dessous)
2. Lancez le pipeline :
      ```bash
      python3 pipeline_streaming_simple.py
      ```
      Les données sont écrites dans `sensor_data_bronze/` (format Delta)

#### Exemple de fichier JSON (`sensor_data/test.json`) :

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

### Pipeline Kafka (Temps Réel)

1. **Démarrer Kafka/Zookeeper**
      ```bash
      docker-compose up -d
      ```
2. **Lancer le producteur Kafka (simulateur de capteurs)**
      ```bash
      python3 kafka_producer.py
      ```
      Génère des données aléatoires (1 message/seconde) dans le topic `sensor_data`.
3. **Lancer le consommateur Spark**
      ```bash
      python3 spark_kafka_consumer.py
      ```
      Consomme les messages Kafka, les nettoie, et les écrit dans `sensor_data_silver/` (Delta Silver).
4. **Lire les données Delta**
      ```bash
      python3 read_delta.py
      ```
      Affiche les données stockées dans Delta.

---

## 🏛️ Architecture Médaillon

| Niveau   | Description                                         | Dossier/Table           |
|----------|-----------------------------------------------------|-------------------------|
| Bronze   | Données brutes (peu ou pas transformées)            | `sensor_data_bronze/`   |
| Silver   | Données nettoyées (timestamps corrigés, schémas validés) | `sensor_data_silver/`   |
| Gold     | (Optionnel) Agrégations (moyennes, anomalies)       | À implémenter           |

---

## 🧩 Concepts Clés

### Pourquoi Kafka ?

| Avantage         | Explication                                                        |
|------------------|--------------------------------------------------------------------|
| Découplage       | Producteurs et consommateurs sont indépendants                     |
| Scalabilité      | Gère des millions de messages/seconde                              |
| Persistance      | Les messages sont stockés durablement (contrairement à un dossier) |
| Ordre garanti    | Dans une partition, l'ordre des messages est préservé              |
| Reprise après panne | Grâce aux offsets (position dans la partition)                  |

### Termes Kafka

| Terme           | Rôle                                                               |
|-----------------|--------------------------------------------------------------------|
| Topic           | Canal de communication (ex: `sensor_data`)                         |
| Partition       | Sous-division d'un topic pour paralléliser la lecture/écriture     |
| Offset          | Position d'un message dans une partition (ex: offset=42)           |
| Consumer Group  | Groupe de consommateurs qui se partagent les partitions            |

---

## 📝 Notes Techniques

- **Arrêt des flux** : Les scripts tournent en continu. Utilisez `Ctrl+C` pour les arrêter.
- **Checkpointing** : Spark stocke les offsets Kafka dans `/tmp/kafka_checkpoint` pour la reprise après panne.
- **Partitionnement Delta** : Les tables sont partitionnées par `building` et `type` pour des requêtes optimisées.

---
