# Data Engineering Challenge
## Beschreibung
Der Usecase:

- Daten = Sensordaten

- Sensoren = 1

- Maschinen = 1

- Datenquellentyp: API-Endpoint

- Datentyp: JSON

- Frequenz: 1 Messung pro Sekunde

- Verwendung: Vorhersagen mit bestehendem ML-Modell

 

Einreichungen:

1. Fragen zur Anforderungserhebung

2. Annahmen abhängig von Anforderungen

3. Eine einfache Architektur mit Azure Cloud

4. Python-Skript für die Umwandlung von JSON in  Time-Series  geeignete Datenstrukturen 

5. Jupyter-Notebook für eine einfache Datenanalyse eines Datensatzes von 50000 Sekunden Messung

6. Eine Präsentation und GitHub Repo über die oben genannten Einreichungen




### 1. Fragen zur Anforderungserhebung

      - Welche Art von Vorverarbeitung ist erforderlich, bevor die Daten in das ML-Modell eingespeist werden?
      - Wie ist das bestehende ML-Modell integriert und welche Anforderungen hat es an die Eingabedaten?
      - Ist eine Realtime verarbeitung notwendig, oder können die Daten in Batches verarbeitet werden?
      - Wie lange müssen wir die Daten speichern und gibt es spezifische Speicheranforderungen?
      - Gibt es Sicherheits- oder Compliance-Anforderungen für die Daten?

### 2. Technologieüberlegungen

      - **Azure IoT Hub**: Für die Datenaufnahme, besonders wenn die Sensordaten kontinuierlich gesendet werden.
      - **Azure Functions**: Für die Verarbeitung der Daten in Realtime oder nahezu Realtime, besonders wenn eine leichte Verarbeitung erforderlich ist.
      - **Azure Stream Analytics**: Wenn eine komplexe Ereignisverarbeitung notwendig ist oder große Datenströme effizient gehandhabt werden müssen.
      - **Azure Blob Storage oder Azure Data Lake**: Für die Speicherung großer Datenmengen.
      - **Azure Machine Learning Service**: Für die Integration mit dem bestehenden ML-Modell, besonders wenn zusätzliche ML-Fähigkeiten benötigt werden.
      - **Azure Keyvault**: Für die Speicherung von Geheimnissen wie API-Schlüssel.
      - **Azure DevOps**: Für die CI/CD-Pipeline, besonders wenn die Bereitstellung automatisiert werden soll.
      - **Azure Monitor**: Für die Überwachung der Datenverarbeitung und der Infrastruktur.
### 3. Annahmen und Anpassungsfähigkeit
      - **Annahme zur Häufigkeit und zum Volumen**: Wenn Daten weniger häufig oder in kleineren Volumina gesendet werden, könnten einfachere Datenverarbeitungsmethoden ausreichend sein.
      - **Komplexitätsannahme**: Wenn die Daten eine umfangreiche Vorverarbeitung erfordern, könnten robustere Azure-Dienste wie Databricks notwendig sein.
      - **Annahme zur Realtimeverarbeitung**: Der Bedarf an Realtimeverarbeitung beeinflusst, ob Sie Azure Functions (für leichte, Realtimeverarbeitung) oder Azure Stream Analytics (für intensivere Streamverarbeitung) wählen.

### 4. Vorgeschlagene Architektur:

Aufnahme: Azure IoT Hub zur Aufnahme von Daten vom Sensor.
Verarbeitung: Azure Functions für die anfängliche Verarbeitung und Transformation.
Speicherung: Data Lake zur Speicherung der verarbeiteten Daten.
Integration mit ML-Modell: Einsatz von Azure Machine Learning Service für Modelltraining und Inferenz.
Datenanalyse: Azure Databricks oder Azure Synapse Analytics für tiefere Datenanalyse und Visualisierung.
Überwachung: Azure Monitor für die Überwachung der Datenverarbeitung und der Infrastruktur.
CI/CD: Azure DevOps für die Bereitstellung der Architektur.
Geheimnisspeicherung: Azure Keyvault für die Speicherung von Geheimnissen wie API-Schlüssel.


### 5. Annahmen
In dieser Architektur sind die wichtigsten Annahmen:

      - Die Sensordaten können effizient vom Azure IoT Hub verwaltet werden.
      - Realtimeverarbeitung ist nicht intensiv rechenintensiv, was Azure Functions zu einer praktikablen Option macht.
      - Das bestehende ML-Modell kann mit dem Azure Machine Learning Service integriert werden.

Einige Unsicherheiten, die auftreten können, sind:

      - Datenqualität und -konsistenz: Die Qualität und das Format der eingehenden Daten könnten variieren.
      - Skalierungsbedarf: Wenn das Datenvolumen oder die Geschwindigkeit unerwartet zunehmen, muss die Architektur möglicherweise neu bewertet werden.
      - Integrationskomplexität: Die Integration des bestehenden ML-Modells mit Azure-Diensten könnte unvorhergesehene Herausforderungen darstellen.


## Python-Skripte
    To run the following scripts:
    1. install docker
    2. clone the repository
    3. cd into the repository
    4. run the following command: 
        ```docker-compose up```
    5. when you see the following link in the terminal, click on it to open the jupyter notebook:
        ```http://http://127.0.0.1:8888/lab?token=<a long token>```
    6. open a new terminal in the jupyter lab and run the following command to run the python scripts:
        ```python transform.py```
    7. the transformed data will be saved in the processed_data folder in parquet format divided into partitions based on the year, month, day, and hour of the timestamp.
    8. the transformed data can be read using the following command:
        ```spark.read.parquet("processed_data")```
    9. open the data_analysis.ipynb notebook to see a simple data analysis of the data.

### 6. Python-Skript für die Umwandlung von JSON in Time-Series geeignete Datenstrukturen
    
    Dieses Python-Skript verwendet PySpark, um Time-Series-Daten aus einer JSON-Datei zu verarbeiten und in eine für Zeitreihenanalysen geeignete Datenstruktur umzuwandeln. Das Skript durchläuft mehrere Schritte, um die Daten zu bereinigen, zu transformieren und schließlich in einem optimierten Format zu speichern.

Skript-Erklärung:
- **Initialisierung einer SparkSession**: Eine SparkSession wird als Einstiegspunkt für die Verwendung von Spark-Funktionalitäten erstellt. Dies ermöglicht es, Daten zu verarbeiten und zu analysieren.
- **Einlesen der JSON-Daten**: Das Skript liest JSON-Daten aus einer Datei in einen Spark DataFrame. Die Option multiline ist auf true gesetzt, um mehrzeilige JSON-Dateien zu unterstützen.
- **Schema-Anzeige**: Das Schema des DataFrame wird angezeigt, um die Struktur der eingelesenen Daten zu überprüfen.
- **Konvertierung des Zeitstempels**: Der UNIX-Zeitstempel wird in ein lesbares Zeitstempelformat umgewandelt, um die Analyse zu erleichtern.
- **Datenbereinigung**:Umgang mit fehlenden Werten und Entfernen von Duplikaten, um die Datenqualität zu verbessern.
- **Behandlung negativer Werte**: Negative Werte im 'consumption_kwh'-Feld werden durch None ersetzt, um unrealistische Datenpunkte zu eliminieren.
- **Quartilsberechnung und Ausreißer-Filterung**: Berechnung der Quartile und des Interquartilbereichs (IQR) zur Identifizierung und Filterung von Ausreißern in den Daten.
- **Feature-Engineering (Zeitbasierte Merkmale)**: Ableitung zusätzlicher Merkmale aus dem Zeitstempel, wie Jahr, Monat, Tag, Stunde und Wochentag, um detailliertere Analysen zu ermöglichen.
- **Zeitreihenfenster-Erstellung**: Erstellung eines Zeitfensters für die Zeitreihenanalyse, indem ein lag-Feature hinzugefügt wird, das den vorherigen Wert von 'consumption_kwh' darstellt.
- **Daten in Ausgabeverzeichnis schreiben**: Die transformierten Daten werden im parquet-Format im Ausgabeverzeichnis processed_data gespeichert. Der Schreibmodus overwrite wird verwendet, um bestehende Daten zu überschreiben.
- **Beenden der SparkSession**: Die SparkSession wird am Ende des Skripts geschlossen, um Ressourcen freizugeben.

*Anwendungsbereich des Skripts*:
- Dieses Skript eignet sich hervorragend für die Verarbeitung und Analyse von Zeitreihendaten, insbesondere wenn große Datensätze vorliegen.
- Durch die Konvertierung in das parquet-Format und das Partitionieren der Daten wird eine effiziente Speicherung und spätere Analyse ermöglicht.
- Die hinzugefügten Zeitmerkmale und das Zeitfenster sind besonders nützlich für Vorhersagemodelle in der Zeitreihenanalyse.

### 7. Jupyter-Notebook für eine einfache Datenanalyse eines Datensatzes von 50000 Sekunden Messung








