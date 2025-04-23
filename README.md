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

## Step 3: Install PostgreSQL
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

### Step 3: Install Dependencies
Install the required dependencies listed in the `requirements.txt` file using `pip`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install all the necessary packages and libraries for the project.

---

## Running the Project

How to train and predict with model you can find in `example.ipynb` Jupyter Notebook



---

## Additional Notes
- If you encounter any issues during installation, ensure that Python 3.10 is correctly installed and accessible in your system's PATH.
- To deactivate the virtual environment, simply run:
  ```bash
  deactivate
  ```

---

## Contribution
If you wish to contribute to this project, please fork the repository and submit a pull request with your changes. Ensure that your code adheres to the project's coding standards.

---

## License
This project is licensed under [insert license here]. See the `LICENSE` file for more details.

---

## Contact
For any questions or issues, please contact Yaroslav Egorov at egorov@iszf.irk.ru.
```

---
