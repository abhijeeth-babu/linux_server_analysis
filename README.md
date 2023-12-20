# Linux Server Vulnerability Data Project

## Overview

This project involves the generation and analysis of realistic dummy data for Linux servers' vulnerabilities. The process includes creating three essential tables in CSV format using the `generate_data.py` script:

1. **linux_server_table.csv:** Contains details about Linux servers, including distribution, kernel version, vulnerabilities, and more.
2. **owner_table.csv:** Represents information about the owners of the servers, such as their IDs, locations, first names, and last names.
3. **location_table.csv:** Contains data related to server locations, mapping location IDs to geographical locations.

## Steps

### 1. Data Generation

- Utilized the `generate_data.py` script to create synthetic data reflecting vulnerabilities in Linux servers.
- Three CSV tables were generated, each serving a distinct purpose in the subsequent steps.

### 2. Data Import and Exploration in MSSQL

- Imported the CSV files into MSSQL as flat files.
- Performed data type adjustments as necessary during the import process.
- Executed an Exploratory Data Analysis (EDA) using SQL queries to gain insights into the generated data.

### 3. Server Vulnerability Dashboard in Power BI

- Leveraged the CSV files to create a "Server Vulnerability Dashboard" in Power BI.
- Visualized and analyzed the Linux server vulnerabilities, providing a comprehensive view of the data.

## Project Components

- **generate_data.py:** Python script for generating synthetic data.
- **linux_server_table.csv:** Table containing Linux server details.
- **owner_table.csv:** Table with information about server owners.
- **location_table.csv:** Table mapping location IDs to geographical locations.

## Usage

1. Run `generate_data.py` to recreate the dummy data.
2. Import the generated CSV files into MSSQL for further analysis.
3. Explore the data using SQL queries for insights.
4. Use the CSV files to create a "Server Vulnerability Dashboard" in Power BI.

Feel free to adapt and expand upon this project for your specific data analysis needs. Happy exploring!