# Linux Server Vulnerability Data Project

## Overview

This project involves the generation and analysis of realistic dummy data for Linux servers' vulnerabilities. The process includes creating three essential tables in CSV format using the `generate_data.py` script:

1. **linux_server_table.csv:** Contains details about Linux servers, including distribution, kernel version, vulnerabilities, and more.
2. **owner_table.csv:** Represents information about the owners of the servers, such as their IDs, locations, first names, and last names.
3. **location_table.csv:** Contains data related to server locations, mapping location IDs to geographical locations.

## Necessary Packages

Make sure you have the following Python packages installed to run the `generate_data.py` script:

- [pandas](https://pandas.pydata.org/): Data manipulation and analysis library.
- [numpy](https://numpy.org/): Library for numerical operations in Python.
- [Faker](https://faker.readthedocs.io/): A Python library for generating fake data.
- [datetime](https://docs.python.org/3/library/datetime.html): A module to work with dates and times.

## Steps

### 1. Data Generation

The `generate_data.py` script begins by importing necessary Python packages, including pandas, numpy, datetime, and Faker, a library for creating fake data. The script is designed to generate synthetic data for Linux server vulnerabilities. Let's break down the key components of the script:

1. **Setting Seeds:**
   ```python
   np.random.seed(42)
   fake = Faker()
   Faker.seed(42)
   fake.add_provider(internet)
   ```
   Seeds are set to ensure reproducibility of the generated data. The Faker library is configured with an internet provider for creating fake IP addresses.

2. **Defining Variables:**
   ```python
   num_servers = 1000
   linux_distributions = ["Ubuntu", "CentOS", "Red Hat", "Debian", "SUSE"]
   kernel_versions = {...}
   locs = ["Australia", "US", "Europe"]
   ```
   Parameters such as the number of servers, Linux distributions, kernel versions, and server locations are defined.

3. **Functions for Data Generation:**
   - `get_vul(ker_ver: str) -> int`: Generates the number of vulnerabilities based on the kernel version.
   - `get_patched(ker_ver: str) -> float`: Determines the ratio of vulnerabilities that are patched.
   - `get_date(vul_pat: int, tot_vul: int) -> int`: Calculates the days since the last update based on the patched and total vulnerabilities.

4. **Generating Primary Keys:**
   ```python
   sys_id = [str(np.random.choice(system_prefix)) + str(fake.aba()) for _ in range(num_servers)]
   owner_id = [str(np.random.choice(owner_prefix)) + "_" + str(...) for _ in range(25)]
   ```
   Primary keys for systems and owners are created using a combination of random system prefixes, ABA (routing) numbers, and owner prefixes.

5. **Generating Dummy Tables:**
   ```python
   owner_table = pd.DataFrame({...})
   owner_table.to_csv("owner_table.csv", index=False)

   location_table = pd.DataFrame({...})
   location_table.to_csv("location_table.csv", index=False)
   ```
   Owner and location tables are generated using pandas DataFrames and saved as CSV files.

6. **Generating Linux Server Table:**
   ```python
   data = {...}
   df = pd.DataFrame(data)
   df.to_csv("linux_server_table.csv", index=False)
   ```
   The Linux server table is created by combining the generated data into a DataFrame and then saved as a CSV file.

7. **Completion Message:**
   ```python
   print("Dummy data for Linux servers has been generated and saved to 'linux_server_data.csv'")
   ```
   A message is printed to indicate the successful generation and saving of dummy data.

In summary, the `generate_data.py` script utilizes various functions and randomization techniques to create synthetic data for Linux servers, including details about vulnerabilities, owners, and locations. The generated data is saved in CSV format for further analysis and exploration.

### 2. Data Import and Exploration in MSSQL

Once the synthetic data is generated using the `generate_data.py` script, the next step involves importing the CSV files into Microsoft SQL Server (MSSQL) and conducting exploratory data analysis (EDA) using SQL queries. Here are the SQL queries that answer specific questions about the generated data:

#### Q1. Total Number of Vulnerabilities in All Servers
```sql
SELECT 
    SUM(total_vul) all_vulnerabilities
FROM
    linux_server_project..linux_server_table;
```

#### Q2. Percentage of Vulnerabilities that Have Been Patched
```sql
SELECT
    ROUND(SUM(vul_patched) * 1.0 / SUM(total_vul), 2) as percent_patched
FROM
    linux_server_project..linux_server_table;
```

#### Q3. Linux Distribution with the Most Vulnerabilities
```sql
SELECT TOP 1
    distribution
    ,SUM(total_vul) total_vulnerabilities
FROM
    linux_server_project..linux_server_table
GROUP BY
    distribution
ORDER BY 
    2 DESC;
```

#### Q4. Kernel Version with the Most Vulnerabilities
```sql
SELECT TOP 1
    kernel_ver
    ,SUM(total_vul) total_vulnerabilities
FROM
    linux_server_project..linux_server_table
GROUP BY
    kernel_ver
ORDER BY 
    2 DESC;
```

#### Q5. Owner with the Most Vulnerabilities
```sql
SELECT TOP 1
    owner_id
    ,SUM(total_vul) total_vulnerabilities
FROM
    linux_server_project..linux_server_table
GROUP BY
    owner_id
ORDER BY 
    2 DESC;
```

#### Q6. Minimum, Average, and Maximum Vulnerability for All Systems
```sql
SELECT
    MIN(total_vul) min_vul
    ,AVG(total_vul) avg_vul
    ,MAX(total_vul) max_vul
FROM 
    linux_server_project..linux_server_table;
```

#### Q7. Minimum, Average, and Maximum Patching Ratio
```sql
SELECT
    ROUND(MIN(vul_patched * 1.0 / total_vul), 2) min_patch
    ,ROUND(AVG(vul_patched * 1.0 / total_vul), 2) avg_patch
    ,ROUND(MAX(vul_patched * 1.0 / total_vul), 2) max_patch
FROM 
    linux_server_project..linux_server_table;
```

#### Q8. Linux Distribution Wise Breakdown of Server Count
```sql
SELECT
    distribution,
    COUNT(*) no_of_servers
FROM
    linux_server_project..linux_server_table
GROUP BY
    distribution
ORDER BY
    2 DESC;
```

#### Q9. Kernel Version Wise Breakdown of Server Count
```sql
SELECT
    kernel_ver
    ,COUNT(*) no_of_servers
FROM
    linux_server_project..linux_server_table
GROUP BY
    kernel_ver
ORDER BY
    2 DESC;
```

#### Q10. Average Duration Since Last Update
```sql
SELECT
    AVG(DATEDIFF(DAY, last_update_date, GETDATE())) avg_days_since_last_update
FROM
    linux_server_project..linux_server_table;
```

#### Q11. Top 10 Systems with Most Vulnerabilities and Owner Information
```sql
SELECT TOP 10
    li.sys_id
    ,li.distribution
    ,li.kernel_ver
    ,li.total_vul
    ,li.owner_id
    ,CONCAT(ow.first_name, ' ', ow.last_name) owner_name
    ,lo.[location]
FROM
    linux_server_project..linux_server_table li
    LEFT JOIN
    linux_server_project..owner_table ow 
    ON li.owner_id = ow.owner_id
    LEFT JOIN
    linux_server_project..location_table lo
    ON ow.location_id = lo.location_id
ORDER BY li.total_vul DESC;
```

The remaining queries (Q12 to Q26) follow a similar structure and focus on various aspects of the data, including server locations, user statistics, patching information, and cumulative vulnerability statistics over time. These queries provide valuable insights into the characteristics of the generated synthetic data, aiding in further exploration and analysis.

For instance, consider the creation of a view (Q14) where a comprehensive set of information from all tables is combined into a single view named `server_info_view`. This allows for streamlined querying and analysis across multiple tables.

Moreover, the use of subqueries is exemplified in Q19, where servers with more than 80% of vulnerabilities remaining unpatched are identified. This demonstrates the versatility of subqueries in filtering and comparison tasks.

The application of Common Table Expressions (CTEs) is illustrated in Q21, showcasing the use of named temporary result sets to simplify complex queries. Here, the query identifies users with the third-highest total vulnerabilities in each location.

Additionally, GROUP BY is employed in Q17 to calculate the average number of vulnerabilities for each combination of location and Linux distribution. This serves to aggregate data and derive meaningful statistics.

Finally, the usage of window functions is demonstrated in Q26, where servers are organized by the day they were patched. The query calculates running sums of both total vulnerabilities and patched vulnerabilities, providing a dynamic view of the data evolution over time.

#### View Creation (Example for Q14)
```sql
-- Create or alter view with necessary info from all tables
USE linux_server_project;
GO

CREATE OR ALTER VIEW server_info_view AS
(
    SELECT
        li.sys_id
        ,li.distribution
        ,li.kernel_ver
        ,li.total_vul
        ,li.vul_patched
        ,li.ip4_add
        ,li.last_update_date
        ,ow.owner_id
        ,CONCAT(ow.first_name, ' ', ow.last_name) owner_name
        ,lo.location
    FROM
        linux_server_project..linux_server_table li 
        LEFT JOIN
        linux_server_project..owner_table ow 
        ON li.owner_id = ow.owner_id
        LEFT JOIN
        linux_server_project..location_table lo 
        ON ow.location_id = lo.location_id
);
```

#### Subquery (Example for Q19)
```sql
-- Find all systems for which more than 80% of the vulnerabilities are not patched
SELECT
    *
FROM
    linux_server_project..server_info_view
WHERE
    vul_patched < (
        SELECT 
            AVG(vul_patched)
        FROM
            linux_server_project..server_info_view
    );
```

#### Common Table Expression (CTE) (Example for Q21)
```sql
-- Find the user with the third most total vulnerabilities in each location using CTE
WITH vul_cte AS (
    SELECT
        owner_id
        ,owner_name
        ,location
        ,SUM(total_vul) total_vulnerabilities
    FROM
        linux_server_project..server_info_view
    GROUP BY
        owner_id
        ,owner_name
        ,location
),
ranked_cte AS (
    SELECT
        owner_id
        ,owner_name
        ,location
        ,DENSE_RANK() OVER(PARTITION BY location ORDER BY total_vulnerabilities DESC) rank_by_vul
    FROM
        vul_cte
)
SELECT *
FROM ranked_cte
WHERE rank_by_vul = 3;
```

#### GROUP BY (Example for Q17)
```sql
-- Average number of vulnerabilities for location and Linux distribution
SELECT
    location
    ,distribution
    ,COUNT(*) num_of_servers
    ,AVG(total_vul) avg_vul
FROM 
    linux_server_project..server_info_view
GROUP BY
    location
    ,distribution
ORDER BY
    1;
```

#### Window Functions (Example for Q26)
```sql
-- Organize the servers by the day they were patched and calculate a running sum of total vulnerabilities and patched vulnerabilities
SELECT
    sys_id
    ,owner_id
    ,last_update_date
    ,SUM(total_vul) OVER(ORDER BY last_update_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) cumsum_total_vul
    ,SUM(vul_patched) OVER(ORDER BY last_update_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) cumsum_vul_patched
FROM
    linux_server_project..server_info_view;
```

These examples showcase the use of various SQL techniques like creating views, using subqueries, employing CTEs, utilizing GROUP BY for aggregations, and leveraging window functions for analytical tasks. Feel free to adapt these examples to other queries as needed.

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