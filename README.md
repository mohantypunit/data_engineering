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
2. Technologieüberlegungen
3. Annahmen abhängig von Anforderungen
4. Eine einfache Architektur mit Azure Cloud
5. Python-Skript für die Umwandlung von JSON in  Time-Series  geeignete Datenstrukturen 
6. Jupyter-Notebook für eine einfache Datenanalyse eines Datensatzes von 50000 Sekunden Messung
7. Eine Präsentation und GitHub Repo über die oben genannten Einreichungen

---

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
\
---

### 4. Vorgeschlagene Architektur:

![Architecture](https://github.com/mohantypunit/data_engineering/blob/main/img/architecture.png?raw=true)

- Aufnahme: Azure Functions zur Aufnahme von Daten vom Sensor.
- Verarbeitung: Azure Functions für die anfängliche Verarbeitung und Transformation.
- Speicherung: Data Lake zur Speicherung der verarbeiteten Daten.
- Integration mit ML-Modell: Einsatz von Azure Machine Learning Service für Modelltraining und Inferenz.
- Datenanalyse: Azure Databricks oder Azure Synapse Analytics für tiefere Datenanalyse und Visualisierung.
- Überwachung: Azure Monitor für die Überwachung der Datenverarbeitung und der Infrastruktur.
- CI/CD: Azure DevOps für die Bereitstellung der Architektur.
- Geheimnisspeicherung: Azure Keyvault für die Speicherung von Geheimnissen wie API-Schlüssel.
- Kostenmanagement und Billing: Azure Cost Management und Billing für die Überwachung und Kontrolle der Ausgaben in Azure.
- Identitäts- und Zugriffsmanagement: Azure Active Directory (Azure AD) für sicheres Identitäts- und Zugriffsmanagement.
- Compliance und Governance: Azure Policy für das Definieren und Durchsetzen von Richtlinien zur Sicherstellung der Compliance und der Best Practices.

_**Annahmen**_

In dieser Architektur sind die wichtigsten Annahmen:
   - Die Daten werden in einem JSON-Format gesendet.
   - Die Daten werden durch eine API verfügbar gemacht.
   - Als Datenquelle wird ein einzelner Sensor verwendet und die Daten werden mit einer Frequenz von 1 Messung pro Sekunde gesendet d.h. werden die Daten durch einfacher Architektur prozessiert.
   - Realtimeverarbeitung ist nicht intensiv rechenintensiv, was Azure Functions zu einer praktikablen Option macht.
   - Das bestehende ML-Modell kann mit dem Azure Machine Learning Service integriert werden.

Einige Unsicherheiten, die auftreten können, sind:

   - Datenqualität und -konsistenz: Die Qualität und das Format der eingehenden Daten könnten variieren.
   - Skalierungsbedarf: Wenn das Datenvolumen oder die Geschwindigkeit unerwartet zunehmen, muss die Architektur möglicherweise neu bewertet werden.
   - Integrationskomplexität: Die Integration des bestehenden ML-Modells mit Azure-Diensten könnte unvorhergesehene Herausforderungen darstellen.

---

## Python-Skripte
   To run the following scripts:
   1. Docker installieren.
   2. Klonen Sie das Repository.
   3. Wechseln Sie in das Verzeichnis des Repositories.
   4. Führen Sie den folgenden Befehl aus:
   5. docker-compose up
   6. Wenn Sie den folgenden Link im Terminal sehen, klicken Sie darauf, um das Jupyter-Notebook zu öffnen:
        ```http://127.0.0.1:8888/lab?token=<long token>```
   7. Öffnen Sie ein neues Terminal im Jupyter Lab und führen Sie den folgenden Befehl aus, um die Python-Skripte auszuführen:
        ```python transform.py```
   8. Die transformierten Daten werden im Ordner 'processed_data' im Parquet-Format gespeichert, aufgeteilt in Partitionen basierend auf dem Jahr, Monat, Tag und Stunde des Zeitstempels.
   9. Die transformierten Daten können mit dem folgenden Befehl gelesen werden:
            ```spark.read.parquet("processed_data")```
   10. Öffnen Sie das Notebook 'data_analysis.ipynb', um eine einfache Datenanalyse der Daten zu sehen.

---

### 5. Python-Skript für die Umwandlung von JSON in Time-Series geeignete Datenstrukturen
    
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

### 6. Jupyter-Notebook für eine einfache Datenanalyse eines Datensatzes von 50000 Sekunden Messung

Dieses Jupyter-Notebook verwendet PySpark, um eine einfache Datenanalyse eines Datensatzes von 50000 Sekunden Messung durchzuführen. Das Notebook durchläuft mehrere Schritte, um die Daten zu bereinigen, verstehen und schließlich zu visualisieren.

Plots:
1. **Boxplot**: Ein Boxplot der 'consumption_kwh'-Werte, um die Verteilung der Daten zu visualisieren.
  ![BoxPlot](https://github.com/mohantypunit/data_engineering/blob/main/img/boxplot.png?raw=true)

  Das obige Boxplot zeigt, dass es Ausreißer in den Daten gibt. Einen Ausreißer am rechten Extrem und zwei weitere links. Dies sind die gleichen Ausreißer, die wir im letzten Diagramm gesehen haben.


2. **Histogramm**: Ein Histogramm der 'consumption_kwh'-Werte, um die Verteilung der Daten zu visualisieren.
  ![histogram](https://github.com/mohantypunit/data_engineering/blob/main/img/histogram.png?raw=true)

  Wir können zwei Anomalien in den Daten erkennen. Die erste ist ein negativer Wert für 'consumption_kwh' und die zweite ein Wert von 0,0. Wir werden diese beiden Werte aus dem Datensatz entfernen.

3. **Zeitreihenplot**: Ein Zeitreihenplot der 'consumption_kwh'-Werte über die Zeit.
  ![timeseriesplot](https://github.com/mohantypunit/data_engineering/blob/main/img/timeseriesplot_kwh.png?raw=true)

  Dieses Diagramm zeigt, dass keine Ausreißer in den Daten vorhanden sind und die Daten zwischen 0 und 5 kWh variieren.

4. **Rolling_mean**: Ein Plot der 'consumption_kwh'-Werte mit einem gleitenden Durchschnitt von 60 Sekunden, um die Trends in den Daten zu visualisieren.
  ![rolling_mean](https://github.com/mohantypunit/data_engineering/blob/main/img/rollin-avg-hour.png?raw=true)

  Dieses Diagramm zeigt den stündlichen gleitenden Durchschnitt des Energieverbrauchs. Alle Analysen zeigen, dass die Daten ein einfaches Wachstumsmuster vom 31. Dezember 2022 abends um 23:00 Uhr bis zum 1. Januar 2023 um 12:00 Uhr aufweisen. Also ist mitten in der Nacht der Stromverbrauch am niedrigsten und mitten am Tag am höchsten.

  Von 9:00 bis 13:00 Uhr am 1. Januar 2023 liegt der Energieverbrauch nahe dem maximalen Wert des gesamten Datensatzes. Dies könnte darauf hindeuten, dass die Maschine zu dieser Zeit am aktivsten ist. 


