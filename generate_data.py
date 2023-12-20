import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
from faker.providers import internet

# Define the directory path
directory = "./data"

# Create the "data" directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

# Seed for reproducibility
np.random.seed(42)
fake = Faker()
Faker.seed(42)
fake.add_provider(internet)


# Number of servers
num_servers = 1000

# Linux distributions and their typical kernel versions
linux_distributions = ["Ubuntu", "CentOS", "Red Hat", "Debian", "SUSE"]
kernel_versions = {
    "Ubuntu": ["4.15.0", "5.4.0", "5.10.0"],
    "CentOS": ["3.10.0", "4.18.0", "5.6.0"],
    "Red Hat": ["3.10.0", "4.18.0", "5.6.0"],
    "Debian": ["4.19.0", "5.10.0", "5.15.0"],
    "SUSE": ["4.12.0", "4.19.0", "5.10.0"],
}

locs = ["Australia", "US", "Europe"]


def get_vul(ker_ver: str) -> int:
    """Get vulnerability for kernel version

    Args:
        ker_ver (str): Kernel version

    Returns:
        int: Number of vulnerabilites
    """
    if ker_ver == "3":
        return int(np.random.normal(400, 20))
    elif ker_ver == "4":
        return int(np.random.normal(300, 20))
    else:
        return int(np.random.normal(200, 20))


def get_patched(ker_ver: str) -> float:
    """Get the ratio of patched vulnerability

    Args:
        ker_ver (str): Kernel version

    Returns:
        float: ratio of vulnerabilities patched
    """
    if ker_ver == "3":
        return 0.3 + np.round(np.random.uniform(-0.15, 0.15), 2)
    elif ker_ver == "4":
        return 0.5 + np.round(np.random.uniform(-0.15, 0.15), 2)
    else:
        return 0.7 + np.round(np.random.uniform(-0.15, 0.15), 2)


def get_date(vul_pat: int, tot_vul: int) -> int:
    days = 90 * (1 - vul_pat / tot_vul) + np.random.uniform(-10, 10)
    return int(days)


system_prefix = ["SYS", "APP", "WEB"]
# primary keys
sys_id = [
    str(np.random.choice(system_prefix)) + str(fake.aba()) for _ in range(num_servers)
]
owner_prefix = ["au", "eu", "us"]
owner_id = [
    str(np.random.choice(owner_prefix))
    + "_"
    + str(np.random.randint(10000, 99999) + int(np.random.uniform(-20, 40)))
    for _ in range(25)
]
owner_location_map = {"au": 1, "eu": 2, "us": 3}
location_id = [1, 2, 3]

# Generate dummy tables

# owner table
owner_table = pd.DataFrame(
    {
        "owner_id": owner_id,
        "location_id": [owner_location_map[owner[:2]] for owner in owner_id],
        "first_name": [fake.first_name() for _ in owner_id],
        "last_name": [fake.last_name() for _ in owner_id],
    }
)

owner_table.to_csv("./data/owner_table.csv", index=False)

# location table
location_table = pd.DataFrame(
    {
        "location_id": location_id,
        "location": ["Australia", "European Union", "United States"],
    }
)
location_table.to_csv("./data/location_table.csv", index=False)

# linux server table

data = {}

data["sys_id"] = sys_id

data["distribution"] = [
    np.random.choice(linux_distributions) for _ in range(num_servers)
]

data["kernel_ver"] = [
    np.random.choice(kernel_versions[distribution])
    for distribution in data["distribution"]
]

data["total_vul"] = [get_vul(ker_ver[0]) for ker_ver in data["kernel_ver"]]

data["vul_patched"] = [
    int(vul * get_patched(ker[0]))
    for ker, vul in zip(data["kernel_ver"], data["total_vul"])
]

data["ip4_add"] = [fake.ipv4_private() for _ in range(num_servers)]

data["owner_id"] = [np.random.choice(owner_id) for _ in range(num_servers)]

data["last_update_date"] = [
    datetime.now() - timedelta(get_date(vul_pat, tot_vul))
    for vul_pat, tot_vul in zip(data["vul_patched"], data["total_vul"])
]
# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv("./data/linux_server_table.csv", index=False)

print(
    "Dummy data for Linux servers has been generated and saved to 'linux_server_data.csv'"
)
