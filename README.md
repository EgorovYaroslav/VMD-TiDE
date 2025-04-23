## Overview
The project contains Python project for VMD-TiDE model.
This repository requires setting up a new environment with Python 3.10 and installing dependencies from `requirements.txt`. Follow the instructions below to set up and run the project.

---

## Prerequisites

Before you begin, ensure that you have the following installed on your system:
- **Git** (for cloning the repository)
- **Python 3.10** (required for this project)

---

## Installation Steps

### Step 0: Install PostgreSQL
Install PostgreSQL and create a database for the project:
```bash
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

Switch to the `postgres` user and create a database:
```bash
sudo -i -u postgres
createdb forecast_project
createuser --pwprompt forecast_user
```

Grant privileges to the user:
```sql
psql
GRANT ALL PRIVILEGES ON DATABASE forecast_project TO forecast_user;
\q
psql -U postgres -d forecast_project
CREATE SCHEMA f107;
\q
exit
```

---

### Step 1: Clone the Repository
To get started, clone the project repository using the following command:

```bash
mkdir -m 755 projects
cd projects

```bash
git clone https://git.iszf.irk.ru/diegon/f107.git
cd f107
```

## Step 6: Configure the Environment
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

Update the `.env` file with your environment-specific settings

### Step 2: Install Dependencies
Install the required dependencies listed in the `requirements.txt` file using `pip`:

```bash
sudo apt install python3-pip
sudo apt install python3-venv
```

```bash
python3 -m venv forecast
source forecast/bin/activate
```

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install all the necessary packages and libraries for the project.

---

## Step 8: Run Migrations
Run the database migrations:
```bash
python3 migrate.py
```

## Running the Project

How to train and predict with model you can find in `example.ipynb` Jupyter Notebook




## License
This project is licensed under GPL-3.0. See the `LICENSE` file for more details.

---

## Contact
For any questions or issues, please contact Yaroslav Egorov at egorov@iszf.irk.ru.
```

---
