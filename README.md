# ScotiaHack Wildlife Trafficking Detection

## Overview
This project was developed for the ScotiaBank hackathon, focusing on identifying and combating wildlife trafficking through financial transaction analysis. By leveraging transaction data and customer demographics, we aim to pinpoint fraudulent activities and networks that may be involved in illegal wildlife trade.

## Dataset Overview
The dataset comprises various transaction data types and customer demographic information categorized as follows:

- **EMT Transactions**: Electronic money transfers within and outside the country.
- **Cash Transactions**: Direct cash flows within the financial system, tracked internally and cross-border.
- **Wire Transactions**: Large-scale, verified wire transfers, both domestic and international.
- **KYC (Know Your Customer)**: Contains consumer demographics with a unique `Customer ID` and a foreign key `Consumer ID` used in the transaction dataset.

## Tasks

### Task 1: Fraud Detection
- **Objective**: Identify potentially fraudulent customers using the flag indicators in the KYC dataset.
- **Methodology**: Due to the highly imbalanced dataset, ensemble methods and neural networks were applied. Evaluation metrics included the F1 Score and the AUC-ROC curve.

### Task 2: Wildlife Community Detection
- **Objective**: Detect networks possibly involved in money laundering related to wildlife trafficking.
- **Approach**: Identify anomalous transactions and score these using network analysis metrics (PageRank, Betweenness, Closeness, and Eigenvector centrality). The Node2Vec algorithm was then used to find similarities and cluster entities based on these similarities. Clusters were ranked by the presence of highly anomalous consumers.

### Task 3: Wildlife Trafficker Detection
- **Objective**: Surf the web to verify if individuals from the KYC data are involved in wildlife trafficking.
- **Tools Used**: A combination of Scrapy and Selenium for web scraping. Google News was the primary source for initial screening, followed by sentiment analysis and Named Entity Recognition (NER) using spaCy and Zero-shot learning techniques to pinpoint traffickers.

## Technologies
- Python for data analysis and machine learning
- Scrapy and Selenium for data scraping
- spaCy for NER tasks
- Neural networks for classification and anomaly detection

## How to Run the Project
Instructions on setting up the environment, installing dependencies, and running each task are detailed in subsequent sections.

## Contributors
List of team members and contributors to the project.

## License
Specify the license under which this project is released (if applicable).
